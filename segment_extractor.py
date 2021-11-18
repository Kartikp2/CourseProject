import re
import os
import csv
import glob
import json
import cv2
from pathlib import Path

# convert time to seconds
def get_time_as_seconds(time):
    time = time.split(",")[0] # ignoring the milliseconds
    hr, min, sec = map(int, time.split(':'))
    return hr * 60 * 60 + min * 60 + sec
    

# extract segment details from segment_raw_txt
def get_segment_details(course_metadata, course_id, week_nbr, video_id, segment_raw_txt):
    segment = {}

    segment_content = segment_raw_txt.split("\n")
    seg_id = int(segment_content[0]) #cue
    timeline = segment_content[1].split(" --> ")

    key    = str(course_id) + "_" + str(week_nbr) + "_" + str(video_id) + "_" + str(seg_id)
    segment["key"] = key
    segment["course_id"] = course_id
    segment["week_nbr"] = week_nbr
    segment["video_id"] = video_id

    segment["timeline_start"] = timeline[0]
    segment["timeline_end"]   = timeline[1]
    segment["segment_nbr"]    = seg_id
    segment["segment_txt"]    = segment_content[2]
    cm = course_metadata[course_id][str(week_nbr) + "." + str(video_id)]
    
    lesson_id = cm["id"]
    video_title = cm["title"]
    segment["tas"] = get_time_as_seconds(timeline[0])

    segment["segment_link"]   = "https://www.coursera.org/learn/cs-410/lecture/" + lesson_id + "?t=" + str(segment["tas"])

    segment["video_title"]    = video_title
    
    return segment

def export_csv_for_indexing(docs):
    csv_columns = ["course_id", "week_nbr", "video_id", "content"]
    try:
        with open("courseera_video_lessons.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in docs:
                writer.writerow(data)
    except IOError:
        print("I/O error")


# persist the segment content to a csv file
def write_segments_to_csv(segments):
    csv_columns = ["key", "course_id", "week_nbr", "video_id", "video_title", "timeline_start", "timeline_end", "segment_nbr", "segment_link", "segment_txt", "pic_name"]
    try:
        with open("courseera_video_segments.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in segments:
                writer.writerow(data)
    except IOError:
        print("I/O error")

# return segments per week
def get_segments(course_metadata, course_id, video_id, week_nbr, srt_file):
    with open(srt_file, 'r') as f:
        content = f.read()

        #get video file name. assuming it to be mp4. can be made dynamic later..
        video_file_name = os.path.dirname(srt_file) + "/" + srt_file.split("/")[-1].split(".")[0] + ".mp4"
        vidcap = cv2.VideoCapture(video_file_name)

    # split by segments
        segments = re.split("\n\n", content)
        seg_content_list = []

        for segment in segments :
            seg_content = get_segment_details(course_metadata, course_id, week_nbr, video_id, segment)
            m = int(seg_content["tas"]/60)  * 60

            thumbnail_name = "pic_" +  str(course_id) + "_" + str(week_nbr) + "_" + str(video_id) + "_" + str(m)
            seg_content["pic_name"] = thumbnail_name+".jpg"

            imgfileName = "video_thumbnails/" + str(course_id) + "/" + thumbnail_name+".jpg"

            if (not os.path.exists(imgfileName)):
                vidcap.set(cv2.CAP_PROP_POS_MSEC,(m* 1000))
                success,image = vidcap.read()
                cv2.imwrite(imgfileName, image)
        
            del seg_content["tas"]
            seg_content_list.append(seg_content)

    return seg_content_list


def load_sylabus_metadata(course_id, sylabus_as_json):
    course_metadata = {}
    syb_meta_dict = {}

    with open(sylabus_as_json, 'r') as f:
        content = f.read()
        course_json = json.loads(content)

        for item in course_json["linked"]["onDemandCourseMaterialItems.v2"]:
            if (item["contentSummary"]["typeName"] == "lecture"):
                if item["name"].startswith("Lesson"):
                    s = item["name"].replace("Lesson ", "")
                    week_video   = s.split(":")[0]
                    video_title   = s.split(":")[1]

                    syb_meta_dict[week_video] = {"id" : item["id"], "title" : video_title}
                else:
                    name = item["name"]
                    week_video   = name.split(" ")[0]
                    video_title  = name.split(" ")[1]

                    if "." in week_video:
                        syb_meta_dict[week_video] = {"id" : item["id"], "title" : video_title}

        course_metadata[course_id] = syb_meta_dict

    return course_metadata


def getDocForIndexing(course_id, week_nbr, video_id, file):

    doc = {}    
    content = ""
    with open(file, 'r') as f:
        content =  f.read()
        content = content.replace("\n","")
        content = content.replace("\r","")

    doc["course_id"] = course_id
    doc["week_nbr"]  = week_nbr
    doc["video_id"]  = video_id
    doc["content"]   = content

    return doc

def main():
    
    seg_content_final_list = []
    course_id = "cs-410"
    scan_dir = "courseera-dl/cs-410/"
    srt_files = glob.glob(scan_dir + '**/*.srt', recursive=True)
    txt_files = glob.glob(scan_dir + '**/*.txt', recursive=True)

    docs = []
    
    course_metadata = load_sylabus_metadata(course_id, "courseera-dl/cs-410-syllabus-raw.json")

    for srt in srt_files:
        video_id = int(os.path.basename(srt).split("_")[0])
        week_nbr = int(os.path.dirname(srt).split("/")[-2].split("_")[0])

        seg_content_srt = get_segments(course_metadata, course_id, video_id, week_nbr, srt)
        seg_content_final_list.extend(seg_content_srt)

        p = Path(srt)
        txt_file_name = str(p.parents[0]) + "/" + p.stem + ".txt"
        docs.append(getDocForIndexing(course_id, week_nbr, video_id, txt_file_name))
            
            # print(os.path.basename(srt) + " --> " +  str(len(seg_content_final_list)))
            # print(os.path.dirname(srt).split("/")[3] + "==> " + str(video_id) + " -- > " + str(video_id.isdigit()))
    

    # write the final output to a csv
    seg_content_final_list.sort(key=lambda a : (a["course_id"], a["week_nbr"], a["video_id"], a["segment_nbr"]))
    write_segments_to_csv(seg_content_final_list)

    docs.sort(key=lambda a : (a["course_id"], a["week_nbr"], a["video_id"]))
    export_csv_for_indexing(docs)


if __name__ == "__main__":
    main()