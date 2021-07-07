import xmltodict
import pprint
import json
import os
ROOT_DIR = r'D:\GitHub\Learning'
os.chdir(ROOT_DIR)

with open('./Data/highways.osm', encoding='utf-8') as fd:
    doc = xmltodict.parse(fd.read())

# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(json.dumps(doc))
with open('highways.json', 'w', encoding='utf-8') as f:
  json.dump(doc, f, ensure_ascii=False, indent=2)