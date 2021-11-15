# 1) Which tasks have been completed?  
 
- Successfully linked transcript to video segments for Coursera course CS 410 
- Successfully completed indexing and ranking. We still need to do some finetuning.
 
 
 
# 2) Which tasks are pending?  
 
- Linking the ranked queries back to the text segments
 
- UI (50 % complete). UI is built on top of (React + Bootstrap ) framework and allows the following:
•	     Ability to search the videos based on a query term
•	     Display the appropriate video sub-segments  as "links" under the "Search results" section.
 
- Backend (started) :  A REST endpoint is created to perform the search. Further work needs to be done to integrate the ranker component and then tie back the results
to the video subsegments.
 
 
 
# 3) Are you facing any challenges? 
 
- Facing challenges with linking queries and text segments  
- Issues with extracting the proper Coursera links along with text  
- Missing some data, most likely due to different srt format
