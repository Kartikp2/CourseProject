# Smart Video Search Enigne

Team: Diana Arita, Kartik Patel, Matthew Kryczka, Selvaganapathy Thirugnanam

Presentation: https://mediaspace.illinois.edu/media/t/1_tpvrr7g7

Documentation: https://github.com/Kartikp2/CourseProject/blob/main/Documents/CS-410%20Course%20Project%20Documentation.pdf

# Problem Statement

There is no easy way to search by video content. This makes it hard for users who are interested in finding precise locations of the videos where a concept or a term is mentioned.

# Abstract

Build a search engine that can support video segment search for Coursera lecture videos with transcripts. This would allow a user to type in a query and see a ranked list of short video segments so that the user can precisely locate which segment to watch in a lecture in order to know more about a concept. We intend to build the search engine based on the scrapping/indexing/ranking concepts learnt from this course. The end solution will provide a User Interface for the user to type in the query and to view the results as links to the video segments.

# Project Overview

- Scrape the videos along with the transcripts (Coursera dl)
- Extract documents out of scrapped videos and transcripts and build an
association between them
- Use Tokenizer(Stemming and other normalization techniques) to extract
lexical units (words)
- Use an Indexer (inverted Index) for faster response from the Search
Engine.
- Perform Ranking/Scoring based on Probabilistic retrieval functions (Eg:
BM25)

# Software Used

- Coursera-dl package: https://github.com/coursera-dl/coursera-dl
- Metapy library: https://github.com/meta-toolkit/metapy

# Running UI
Download code from github: https://github.com/Kartikp2/CourseProject.git
- Run backend
  - Be in the directory! ( same as server.py)
  - To install the dependencies - npm install
  - Run server.py
- Run Frontend
  - Be in the directory (search-ui -> smart-video-search)
  - To install the dependencies - npm install
  - To run app - npm start
  - Go to browser and hit url https://localhost:3000

# Files

**Not all of the coursera-dl files were uploaded as they take up a lot of space ( the project is already close to 1GB!)**

- Documents 
  - Contains proposal, progress report, powerpoint, and final documentation
- Course
  - Contains course data for ranking and line.toml file
- idx/inv
  - Inverted index for faster access to data
- initial_analysis
  - Snippet of what dat looks like coming out of coursera-dl package, segment_extractor.py that converts the srt data and links multiple data into a csv
- search-ui
  - Code base for the frontend
- test_flask
  - Sample flask that returns the results that the frontend expects
- video_thumbnails
  - File that conatins images of video thumbails (obtained from the segment_extractor.py)
- coursera_video_lessons
  - Used by the search engine to build the data and used for ranking
  - Each line is a lecture
- coursera_video_segments
  - Used by backend to further narrow query results
  - Each line is a transcript segment
- search_engine.py
  - Using Metapy library to build the search ranker. Build corpus, inverted index, and use OkapiBM25 to rank queries
- server.py
  - Backend file that fetches the query from UI and runs it on the search engine. Finally returns the most relevant video segment
