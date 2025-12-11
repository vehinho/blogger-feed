import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BLOG_JSON = "https://vele5.blogspot.com/feeds/posts/default?alt=json&max-results=20"
RSS_FILE = "rss.xml"

resp = requests.get(BLOG_JSON)
data = resp.json()

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = data["feed"]["title"]["$t"]
ET.SubElement(channel, "link").text = "https://vele5.blogspot.com/"
ET.SubElement(channel, "description").text = "Custom RSS feed with tags"

for entry in data["feed"]["entry"]:
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = entry["title"]["$t"]
    ET.SubElement(item, "link").text = entry["link"][0]["href"]
    ET.SubElement(item, "pubDate").text = datetime.strptime(entry["published"]["$t"][:19], "%Y-%m-%dT%H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    description = ""
    if "content" in entry:
        description = entry["content"]["$t"]
    elif "summary" in entry:
        description = entry["summary"]["$t"]
    ET.SubElement(item, "description").text = description
    
    # Tags
    if "category" in entry:
        for tag in entry["category"]:
            ET.SubElement(item, "category").text = tag["term"]

tree = ET.ElementTree(rss)
tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)
print(f"RSS feed saved as {RSS_FILE}")
