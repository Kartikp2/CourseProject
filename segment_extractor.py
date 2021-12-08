import re
import os
import csv
import glob
import json
import cv2
from pathlib import Path

# convert time to seconds


def get_time_as_seconds(time):
    time = time.split(",")[0]  # ignoring the milliseconds
    hr, min, sec = map(int, time.split(':'))
    return hr * 60 * 60 + min * 60 + sec


# extract segment details from segment_raw_txt
def get_segment_details(course_metadata, course_id, week_nbr, lesson_nbr, video_id, segment_raw_txt):
    segment = {}

    segment_content = segment_raw_txt.split("\n")
    seg_id = int(segment_content[0])  # cue
    timeline = segment_content[1].split(" --> ")

    key = str(course_id) + "_" + str(week_nbr) + "_" + \
        str(lesson_nbr) + str(video_id) + "_" + str(seg_id)

    segment["key"] = key
    segment["course_id"] = course_id
    segment["week_nbr"] = week_nbr
    segment["video_id"] = video_id

    segment["timeline_start"] = timeline[0]
    segment["timeline_end"] = timeline[1]
    segment["segment_nbr"] = seg_id
    segment["segment_txt"] = segment_content[2]

    cm = course_metadata[course_id][str(week_nbr) + "." + str(lesson_nbr) + "." + str(video_id)]

    lesson_id = cm["item_id"]
    video_title = cm["title"]
    segment["tas"] = get_time_as_seconds(timeline[0])

    segment["segment_link"] = "https://www.coursera.org/learn/" + course_id + "/lecture/" + \
        lesson_id + "?t=" + str(segment["tas"])

    segment["video_title"] = video_title

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
    csv_columns = ["key", "course_id", "week_nbr", "video_id", "video_title", "timeline_start",
                   "timeline_end", "segment_nbr", "segment_link", "segment_txt", "pic_name"]
    try:
        with open("courseera_video_segments.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimeter = '~')
            writer.writeheader()
            for data in segments:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def normalize_text(string, stripNumbersPrefix = False):
    """ Text normalization from
    https://github.com/yoonkim/CNN_sentence/blob/23e0e1f735570/process_data.py
    as specified in Yao's paper.
    """
    string = re.sub(r"[^A-Za-z0-9,!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    string = string.strip().lower()

    if (stripNumbersPrefix == True):
        i = re.search(r"[a-zA-Z]", string).start()
    else:
        i = 0
    return string[i:]

# return segments per week


def get_segments(course_metadata, course_id, week_nbr, lesson_nbr, video_id, srt_file):
    with open(srt_file, 'r') as f:
        content = f.read()

        # get video file name. assuming it to be mp4. can be made dynamic later..
        video_file_name = os.path.dirname(
            srt_file) + "/" + srt_file.split("/")[-1].split(".")[0] + ".mp4"
        vidcap = cv2.VideoCapture(video_file_name)

    # split by segments
        segments = re.split("\n\n", content)
        seg_content_list = []

        for segment in segments:
            seg_content = get_segment_details(
                course_metadata, course_id, week_nbr, lesson_nbr, video_id, segment)
            m = int(seg_content["tas"]/60) * 60

            thumbnail_name = "pic_" + \
                str(course_id) + "_" + str(week_nbr) + \
                "_" + str(video_id) + "_" + str(m)
            seg_content["pic_name"] = thumbnail_name+".jpg"

            imgfileName = "video_thumbnails/" + \
                str(course_id) + "/" + thumbnail_name+".jpg"

            if (not os.path.exists(imgfileName)):
                vidcap.set(cv2.CAP_PROP_POS_MSEC, (m * 1000))
                success, image = vidcap.read()
                cv2.imwrite(imgfileName, image)

            del seg_content["tas"]
            seg_content_list.append(seg_content)

    return seg_content_list


def load_sylabus_metadata(course_metadata, course_id, sylabus_as_json):
    syb_meta_dict = {}
    week_module_map = {}
    video_nbr = 0
    lesson_id = 0
    prev_lesson_id = ""
    lesson_nbr = 0
    last_module_id = ""

    with open(sylabus_as_json, 'r') as f:
        content = f.read()
        course_json = json.loads(content)

        for i, module in enumerate(course_json["elements"][0]["moduleIds"]):
            week_module_map[module] = {}
            week_module_map[module]["week_nbr"] = i + 1
            week_module_map[module]["lesson_names"] = {}

        for cml in course_json["linked"]["onDemandCourseMaterialLessons.v1"]:
            mod_id = cml["moduleId"]
            lesson_name = cml["name"]
            week_module_map[mod_id]["lesson_names"][cml["id"]] = lesson_name

        for item in course_json["linked"]["onDemandCourseMaterialItems.v2"]:

            module_id = item["moduleId"]
            week_nbr = week_module_map[module_id]["week_nbr"]
            lesson_id = item["lessonId"]

            if last_module_id != module_id:
                video_nbr = 0
                lesson_nbr = 0

            if prev_lesson_id != lesson_id:
                lesson_nbr = lesson_nbr + 1

            last_module_id = module_id
            prev_lesson_id = lesson_id

            if (item["contentSummary"]["typeName"] == "lecture"):
                video_nbr = video_nbr + 1
                video_title = item["name"]

                k = str(week_nbr) + "." + str(lesson_nbr) + "." + str(video_nbr)

                syb_meta_dict[k] = {"week_nbr": week_nbr,
                                    "lesson_nbr": lesson_nbr,
                                    "video_nbr": video_nbr,
                                    "item_id": item["id"],
                                    "title": video_title,
                                    "lesson_name" : week_module_map[module_id]["lesson_names"][lesson_id]
                                    }

        course_metadata[course_id] = syb_meta_dict


def getDocForIndexing(course_id, week_nbr, video_id, file):

    doc = {}
    content = ""
    with open(file, 'r') as f:
        content = f.read()
        content = content.replace("\n", "")
        content = content.replace("\r", "")

    doc["course_id"] = course_id
    doc["week_nbr"] = week_nbr
    doc["video_id"] = video_id
    doc["content"] = content

    return doc

def main():

    seg_content_final_list = []
    courses = ["cs-410", "stat-420", "cs-416-dv"]
    course_metadata = {}
    docs = []

    for course_id in courses:
        scan_dir = "courseera-dl/" + course_id + "/"
        srt_files = glob.glob(scan_dir + '**/*.srt', recursive=True)
        meta_raw_json = "courseera-dl/" + course_id + "-syllabus-raw.json"

        load_sylabus_metadata(course_metadata, course_id, meta_raw_json)

        for srt in srt_files:

            filename            = os.path.basename(srt).split(".")[0].split("_")[1]
            normalized_filename = normalize_text(filename)

            week_info_path = os.path.dirname(os.path.dirname(srt)) + '/**week*information/'
            week_info = glob.glob(week_info_path, recursive=False)

            if len(week_info) == 0:
                # try to extract from the parent folder
                week_nbr = int(srt.split("/")[-3].split("_")[0])
            else:
                week_nbr = int(week_info[0].split("/")[-2].split("-")[1])

            # get the lesson name
            lesson_name = os.path.dirname(srt).split("/")[-1].split("_")[1]
            normalized_lesson_name = normalize_text(os.path.dirname(srt).split("/")[-1].split("_")[1])

            # get the video name

            res = list(filter(lambda x: week_nbr == x["week_nbr"]  and 
            (filename == x["title"] or normalized_filename == normalize_text(x["title"], False) or normalized_filename == normalize_text(x["title"], True)) and 
            (lesson_name == x["lesson_name"] or normalized_lesson_name == normalize_text(x["lesson_name"])), 
            list(course_metadata[course_id].values())))

            resCnt = len(res)

            if resCnt == 1:
                video_id = res[0]["video_nbr"]
                lesson_nbr = res[0]["lesson_nbr"]

            elif resCnt == 0:
                print("!!!! NO match found for :" + srt)
            else:
                print("~~~~ Multiple mathces found for srt :" + srt)

            seg_content_srt = get_segments(
                course_metadata, course_id, week_nbr, lesson_nbr, video_id, srt)

            seg_content_final_list.extend(seg_content_srt)

            p = Path(srt)
            txt_file_name = str(p.parents[0]) + "/" + p.stem + ".txt"
            docs.append(getDocForIndexing(
                course_id, week_nbr, video_id, txt_file_name))

    # write the final output to a csv
    seg_content_final_list.sort(key=lambda a: (
        a["course_id"], a["week_nbr"], a["video_id"], a["segment_nbr"]))
    write_segments_to_csv(seg_content_final_list)

    docs.sort(key=lambda a: (a["course_id"], a["week_nbr"], a["video_id"]))
    export_csv_for_indexing(docs)


if __name__ == "__main__":
    main()
