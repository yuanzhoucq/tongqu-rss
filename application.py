from flask import Flask, Response
import urllib
import ssl
import json
import traceback
import xml.etree.cElementTree as ET

app = Flask(__name__)

blacklist = ["西服", "驾校", "学车"]


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/rss')
def tongqu_rss():
    try:
        url = "https://tongqu.me/api/act/type?type=0&status=0&order=act.create_time&number=20"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        context = ssl._create_unverified_context()
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req, context=context).read()
        response = json.loads(response)
        acts = response["result"]["acts"]

        rss = ET.Element("rss", version="2.0")
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = "Tongqu rss"
        ET.SubElement(channel, "url").text = "Tongqu rss"
        ET.SubElement(channel, "description").text = "Tongqu rss"

        for idx, act in enumerate(acts):
            should_remove = False
            for word in blacklist:
                if act["name"].find(word) > -1:
                    should_remove = True
                    break
            if should_remove:
                continue
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = act["name"]
            ET.SubElement(item, "link").text = "https://tongqu.me/act/" + act["actid"]
            ET.SubElement(item, "description").text = "开始时间：{0}\n地点：{1}".format(act["start_time"], act["location"])
    # Pring error logs for Azure App Service
    except Exception:
        with open("D:\home\site\wwwroot\\error.txt", "w") as f:
            f.write(traceback.format_exc())
            return "Something wrong."
    return Response(ET.tostring(rss, encoding="utf8", method="xml"), mimetype='application/xml')
