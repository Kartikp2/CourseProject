## Abstract:

Build a search engine that can support video segment search for Courseera lecture videos with transcripts. This would allow an user to type in a query
and see a ranked list of short video segments so that the user can precisely locate which segment to watch in a lecture in order to
know more about a concept. We intend to build the search engine based on the scrapping/indexing/ranking concepts learnt from this course.
The end solution will provide an User Interface for the user to type in the query and to view the results as links to the video
segments.

## What are the names and NetIDs of all your team members? Who is the captain? The captain will have more administrative duties than team members.

- Matthew Kryczka - kryczka3
- Selvaganapathy Thirugnanam - st26
- Diana Arita - dianama2
- Kartik Patel – kartikp2

- Captain – Kartik Patel


## What topic have you chosen?
Intelligent Learning Platform- Build a search engine that can support video segment search. This would allow you to type in a query and see a ranked list of short
video segments so that you can precisely locate which segment to watch in a lecture in order to know more about a concept. 

## Why this is a problem :
Apart from searching videos by titles, There is no easy way to search by video content. This makes harder for users who are
interested in finding precise locations of the videos where a concept or a term is mentioned.

## How does it relate to the theme and class ?
Assuming, Each Video segment as a document, we will try to address the "Pull" mode of the text retrival problem by ranking the
these documents based on the transcripts available for each video segment and return the segments that best matches the query.



## Briefly describe any datasets, algorithms or techniques you plan to use ?

We plan to use course lectures videos (i.e videos of CS 410: Text Information Systems) as the dataset. At a very high level, we tend
to perform the following :
1. Scrape the videos along with the transcripts
2. Extract documents out of scrapped videos and transcripts and build an association between them
3. Use Tokenizer(Stemming and other normalization techniques) to extract lexical units (words)
4. Use an Indexer (inverted Index) for faster response from the Search Engine.
5. Perform Ranking/Scoring based on Probabilistic retrieval functions (Eg: BM25)


So UI will be built for the user to submit the query. Once submitted, the query is further normalized and
sent to ranking function to score against the data available in the index. The top ranked results will then be displayed
in the UI. The results would provide links to the video segments.


## How will you demonstrate that your approach will work as expected?

Demo video for the demonstration. We will try to search for concept as keywords used in our lectures and the results should contain
video segments related to the concepts.

## Which programming language do you plan to use?

- scrapping, indexing, ranking  ---> Python
- UI                            ---> Javascript frameworks (either Angular or React)
- Backend                       ---> Python/Flask

## Time Allocation

- Scraping the video text	---> 10 hours
- Indexing	              ---> 20 hours
- Ranking                	---> 20 hours
- UI(Backend & Frontend)	---> 10 hours
- Mapping the video 	    ---> 20 hours

