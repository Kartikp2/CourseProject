from http.server import BaseHTTPRequestHandler, HTTPServer
from search_engine import SearchEngine
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
from json import dumps
import os
import base64

class MyServer(BaseHTTPRequestHandler):
    searchEngine = SearchEngine('/Users/Diana/OneDrive/Desktop/Github/CourseProject/courseera_video_lessons.csv', 'config.toml')

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def send_dict_response(self, d):
        """ Sends a dictionary (JSON) back to the client """
        self.wfile.write(bytes(dumps(d), "utf8"))

    def get_video_details(self,rankerResult,query):
        with open ('/Users/Diana/OneDrive/Desktop/Github/CourseProject/courseera_video_segments_copy.csv', 'rt', encoding="utf-8") as file:
            relevantLines = []
            for line in file:
                if (rankerResult in line):
                    relevantLines.append(line)

            # Look for the first line that has the query
            # if not found then use the first line
            temp = relevantLines[0].split("~")
            for line in relevantLines:
                elements = line.split("~")
                if (query in elements[9]):
                    temp = line.split("~")
                    break

            # if time_start has a 0 minute then look for the first line that has a 01 minute and use that image
            timeStartMinute = temp[5][4]
            imgPath = ""
            if (timeStartMinute == '0'):
                for line in relevantLines:
                    elements = line.split("~")
                    if (elements[5][4] == '1'):
                        imgPath = elements[10]
                        break
            else:
                imgPath = temp[10]

            # setting image path and then encoding
            f2 = os.path.dirname(__file__) + "\\video_thumbnails\\" + temp[1] + "\\" + imgPath
            f2 = f2[:-1]
            with open(f2, "rb") as img:
                image2 = base64.b64encode(img.read())
            
            result = {
                "course" : temp[1],
                "week" : temp[2],
                "video_title" : temp[4],
                "text_preview": temp[9],
                "segment_link" : temp[8],
                "img": image2.decode("utf-8")
            }
            return result
    
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        q = query_components["q"] 
        
        rankerResult = self.searchEngine.query_result(q[0])
        print(rankerResult)

        result = []
        for element in rankerResult:
            element = '~'.join(map(str,element))
            result.append(self.get_video_details(element, q[0]))

        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

        self.send_dict_response(result)

if __name__ == "__main__":
    httpd = HTTPServer(("127.0.0.1", 5000), MyServer)
    httpd.serve_forever()
