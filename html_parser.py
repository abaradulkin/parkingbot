import io
from xml.etree import ElementTree as ET

with io.open("favbet.html", 'r', encoding='utf-8') as f:
    contents = f.read()
    tree = ET.fromstring(contents)
print len(tree.findall(".//li[@class='event--head-block']"))