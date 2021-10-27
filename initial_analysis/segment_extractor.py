import re
import os
import csv
import glob

# convert time to seconds
def get_time_as_seconds(time):
    time = time.split(",")[0] # ignoring the milliseconds
    hr, min, sec = map(int, time.split(':'))
    return hr * 60 * 60 + min * 60 + sec
    

# extract segment details from segment_raw_txt
def get_segment_details(course_id, week_nbr, video_id, segment_raw_txt):
    segment = {}

    segment_content = segment_raw_txt.split("\n")
    seg_id = segment_content[0] #cue
    timeline = segment_content[1].split(" --> ")

    key    = str(course_id) + "_" + str(week_nbr) + "_" + str(video_id) + "_" + str(seg_id)
    segment["key"] = key

    segment["timeline_start"] = timeline[0]
    segment["timeline_end"]   = timeline[1]
    segment["segment_txt"]    = segment_content[2]
    segment["segment_link"]   = "https://www.coursera.org/learn/cs-410/lecture/rLpwp?t=" + str(get_time_as_seconds(timeline[0]))

    return segment


# persist the segment content to a csv file
def write_segments_to_csv(segments):
    csv_columns = ["key", "timeline_start", "timeline_end",  "segment_link", "segment_txt"]
    try:
        with open("courseera_video_segments.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in segments:
                writer.writerow(data)
    except IOError:
        print("I/O error")


# return segments per week
def get_segments(course_id, video_id, week_nbr, srt_file):
    with open(srt_file, 'r') as f:
        content = f.read()

    # split by segments
        segments = re.split("\n\n", content)
        seg_content_list = []
    
        for segment in segments :
            seg_content = get_segment_details(course_id, week_nbr, video_id, segment)
            seg_content_list.append(seg_content)

    return seg_content_list

    

def main():
    
    seg_content_final_list = []
    course_id = "cs-410"
    scan_dir = "courseera-dl/cs-410/"
    srt_files = glob.glob(scan_dir + '**/*.srt', recursive=True)

    for srt in srt_files:
        week_nbr = int(os.path.basename(srt).split("_")[0])
        video_id = os.path.dirname(srt).split("/")[3].split("_")[1].split("-")[1]

        if (video_id.isdigit()):
            seg_content_srt = get_segments(course_id, video_id, week_nbr, srt)
            seg_content_final_list.extend(seg_content_srt)
            
            # print(os.path.basename(srt) + " --> " +  str(len(seg_content_final_list)))
            # print(os.path.dirname(srt).split("/")[3] + "==> " + str(video_id) + " -- > " + str(video_id.isdigit()))
    

    # write the final output to a csv
    write_segments_to_csv(seg_content_final_list)


if __name__ == "__main__":
    main()