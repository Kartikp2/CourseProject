from http.server import BaseHTTPRequestHandler, HTTPServer
from search_engine import SearchEngine
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
from json import dumps

class MyServer(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def send_dict_response(self, d):
        """ Sends a dictionary (JSON) back to the client """
        self.wfile.write(bytes(dumps(d), "utf8"))

    def get_video_details(self,rankerResult):
        with open ('/Users/Diana/OneDrive/Desktop/Github/CourseProject/courseera_video_segments.csv', 'rt', encoding="utf-8") as file:
            for line in file:
                if (rankerResult in line):
                    temp = line.split(",")
                    result = {
                        "course" : temp[1],
                        "week" : temp[2],
                        "video_title" : temp[4],
                        "text_preview": temp[9],
                        "segment_link" : temp[8],
                        "img": temp[10]
                    }
                    return result
    
    def do_GET(self):
        #print('search string :' + str(request.args.get("q")))
        query_components = parse_qs(urlparse(self.path).query)
        q = query_components["q"] 
        
        searchEngine = SearchEngine('/Users/Diana/OneDrive/Desktop/Github/CourseProject/courseera_video_lessons.csv', 'config.toml')

        rankerResult = searchEngine.query_result(q[0])
        print(rankerResult)

        result = []
        for element in rankerResult:
            element = ','.join(map(str,element))
            result.append(self.get_video_details(element))

        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

        self.send_dict_response(result)

if __name__ == "__main__":        
    httpd = HTTPServer(("127.0.0.1", 5000), MyServer)
    httpd.serve_forever()
    #print("Server started http://%s:%s" % (hostName, serverPort))
