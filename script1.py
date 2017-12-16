#! python
from ciscoconfparse import CiscoConfParse
import re
import os
import json

path = "configs"

devices = {}
for file in os.listdir(path):
    config = CiscoConfParse(path + "\\" + file)
    hostname = re.search('hostname\s(.+?)$', config.find_objects(r"^hostname")[0].text).group(1)
    line_vtys = config.find_objects(r"^line vty")
    vtys_list = []
    vty_acl = {}
    for line in line_vtys:
        vty_number = re.search('line vty (\d\s\d)', line.text).group(1)
        for child in line.children:
            if "access-class" in child.text:
                acl = re.search('access\-class\s(.+?)\sin', child.text).group(1)
                vty_acl[vty_number] = acl
    vtys_list.append(vty_acl)
    devices[hostname] = vtys_list

print (json.dumps(devices, indent=1))

with open('result.json', 'w') as fp:
    json.dump(devices, fp)

for device_name, vty_acl in devices.items():
    print("! " + device_name)
    for item in vty_acl:
        print(item)
