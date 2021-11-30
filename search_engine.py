import pandas as pd
import os
import shutil
import metapy
import math
import pytoml

class SearchEngine:
    def __init__(self, path, config):
        self.path = path
        self.df = self.build_corpus()
        self.config = config
        self.idx = self.build_idx(config)
        self.query = metapy.index.Document()
        self.ranker = self.ranker(self.config)

        
    def build_idx(self, config):
        if os.path.isdir(self.path[0:self.path.rfind('/') + 1] + 'idx'):
            path = self.path[0:self.path.rfind('/') + 1] + 'idx'
            shutil.rmtree(path)
        idx = metapy.index.make_inverted_index(config)
        return idx
        
    def build_corpus(self):
        
        try:
            df = pd.read_csv(self.path)
        except FileNotFoundError:
            print(self.path)
            print("Could not open/read file")
            
        textcolumn = ['content'] # ignore the other columns
        new_df_text = pd.DataFrame(df, columns=textcolumn)
        
        file = self.path[0:self.path.rfind('/') + 1]
        new_data_file = file + 'course.dat'
        with open(new_data_file, 'w', encoding="utf-8") as f:
            for index, row in df.iterrows():
                text = row['content']
                f.write(text)
                f.write('\n')
                
        src = new_data_file
        dst = self.path[0:self.path.rfind('/') + 1] + 'course'

        shutil.copy2(src,dst)
        return df

    def ranker(self, config):
         return metapy.index.OkapiBM25(k1=1.65, b=0.75, k3=2.6)
        
    def ranker_score(self):
        ranker = self.ranker
        top_docs = ranker.score(self.idx, self.query, num_results=5)
        return top_docs

    def query_result(self,text):
        self.query.content(text) 
        top_docs = self.ranker_score()
        top_links = []
        for num, (d_id, _) in enumerate(top_docs):
            course = self.df.iloc[d_id-1].course_id
            week = int(self.df.iloc[d_id-1].week_nbr )
            lesson = int(self.df.iloc[d_id-1].video_id)
            top_links.append((course,week,lesson)) # (course, week, lesson)
        return top_links