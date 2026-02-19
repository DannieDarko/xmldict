import json
from xmldict import XmlDict

with open('xml.json', 'r') as f:
    xml_json=XmlDict.from_dict(json.load(f))
with open('xml.xml', 'r') as f:
    xml_xml=XmlDict.from_xml(f.read().encode('utf-8'))
json_dict=json.dumps(xml_json.to_dict(), sort_keys=True)
xml_dict=json.dumps(xml_xml.to_dict(), sort_keys=True)
print(f'Success: {json_dict==xml_dict}')
print(json.dumps({'from_json': xml_json.to_dict(), 'from_xml': xml_xml.to_dict()}, indent=2))
