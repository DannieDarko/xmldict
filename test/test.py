import json
from xmldict import XmlDict

with open('xml.json', 'r') as f:
    xml_dict=XmlDict.from_dict(json.load(f))
with open('xml.xml', 'r') as f:
    xml=XmlDict.from_xml(f.read().decode('utf-8'))
print(json.dumps({'from_dict': xml_dict.to_dict(), 'from_xml': xml.to_dict()}, indent=2))
