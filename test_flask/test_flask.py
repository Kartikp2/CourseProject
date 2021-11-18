from flask import Flask, request,  jsonify
import base64
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/search")
def search():
    print('search string :' + str(request.args.get("q")))
    f1 = os.path.dirname(__file__) + "/../video_thumbnails/cs-410/pic_cs-410_3_2_300.jpg"
    f2 = os.path.dirname(__file__) + "/../video_thumbnails/cs-410/pic_cs-410_3_6_240.jpg"
    with open(f1, "rb") as img:
        image1 = base64.b64encode(img.read())
    with open(f2, "rb") as img:
        image2 = base64.b64encode(img.read())
    dbResults = [
        {
        "course" : "cs-410 ",
        "week" : 2,
        "video_title" : "Implementation of TR Systems",
        "text_preview": "I hope you can reach the conclusion that",
        "segment_link" : "https://www.coursera.org/learn/cs-410/lecture/rLpwp?t=322",
        "img": image1.decode("utf-8")
        },
        {
            "course" : "cs-410 ",
            "week" : 4,
            "video_title" : "Statistical Language Model",
            "text_preview": "test example reach",
            "segment_link" : "https://www.coursera.org/learn/cs-410/lecture/rLpwp?t=899",
            "img": image2.decode("utf-8")
        }           
        ]
    return jsonify(dbResults)

if __name__ == '__main__':
   app.run()    