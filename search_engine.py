import math
import metapy
import pytoml
import pandas as pd
import os
import shutil
from pathlib import Path


class SearchEngine:
    def __init__(self):
        self.path = str(Path('coursera_video_lessons.csv').absolute())
        self.df = self.build_corpus()
        self.config = 'config.toml'
        self.idx = self.build_idx()
        self.query = metapy.index.Document()
        self.ranker = self.ranker(self.config)

    # Build inverted index for faster access to data    
    def build_idx(self):
        if os.path.isdir(self.path[0:self.path.rfind('/') + 1] + 'idx'):
            path = self.path[0:self.path.rfind('/') + 1] + 'idx'
            shutil.rmtree(path)
        idx = metapy.index.make_inverted_index(self.config)
        return idx
    
    # Generate corpus ( currently each line is a lesson)    
    def build_corpus(self):
        
        try:
            df = pd.read_csv(self.path)
        except FileNotFoundError:
            print(self.path)
            print("Could not open/read file")
            
        textcolumn = ['content'] # ignore the other columns
        new_df_text = pd.DataFrame(df, columns=textcolumn)
        
        file = self.path[0:self.path.rfind('/') + 1] + 'course/'
        new_data_file = file + 'course.dat'
        with open(new_data_file, 'w') as f:
            for index, row in df.iterrows():
                text = row['content']
                f.write(text)
                f.write('\n')
                
        return df

    # OkapiBM25 used to ranke user entered query    
    def ranker(self, config):
         return metapy.index.OkapiBM25(k1=1.75, b=0.45, k3=2.6)
    
    # Score query and return top 5 video segments ( can be changed later!)
    def ranker_score(self, number_results=5):
        ranker = self.ranker
        top_docs = ranker.score(self.idx, self.query, num_results=number_results)
        return top_docs

    # Return results for the backend to make use of (course, week, lesson)
    def query_result(self,text, num_results=5):
        self.query.content(text) 
        top_docs = self.ranker_score(num_results)
        top_links = []
        for num, (d_id, _) in enumerate(top_docs):
            course = self.df.iloc[d_id-1].course_id
            week = self.df.iloc[d_id-1].week_nbr 
            lesson = self.df.iloc[d_id-1].video_id
            top_links.append((course,week,lesson)) # (course, week, lesson)
        return top_links