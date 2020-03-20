from bs4 import BeautifulSoup
import grequests
import json

urls=   [
    'https://www.mohfw.gov.in/'
]
requests = (grequests.get(u) for u in urls)
responses = grequests.map(requests)

labels=["Screened","Active","Discharged","Migrated","Deaths"]

overall_list=[]
statewide_list=[]

for i, response in enumerate(responses):
    soup = BeautifulSoup(response.text, 'html.parser')
    selectedtags = soup.select("tbody tr")
    
    for row in selectedtags:
        tds = row.select("td")
        if(tds[0].text.lower().find("India".lower()) != -1):
            statewide_list.append({"Name":"Total","Confirmed-Indian":tds[1].text,"Confirmed-Foreign":int(tds[2].text.strip('\r\n')),"Cured/Discharged/Migrated":int(tds[3].text.strip('\r\n')),"Death":int(tds[4].text.strip('\r\n'))})
        else:
            statewide_list.append({"Name":tds[1].text.strip('\r\n'),"Confirmed-Indian":int(tds[2].text),"Confirmed-Foreign":int(tds[3].text),"Cured/Discharged/Migrated":int(tds[4].text),"Death":int(tds[5].text)})
        
    selectedtags =  soup.select("ol strong")
    for singletag in selectedtags:        
        txt=singletag.getText().split(":")
        if(len(txt)>1):
            # print(txt[0])
            # print(int(txt[1].strip().replace(",","")))
            for label in labels:
                if(txt[0].lower().find(label.lower()) !=-1):
                    overall_list.append({"label":label,"Description":txt[0].strip("\t"),"value":int(txt[1].strip().replace(",",""))})
                        
import pprint
pprint.pprint(statewide_list)
with open('api/statewide.json', 'w') as file:
    file.write(json.dumps(statewide_list))
    print "Saved Statewide data"

pprint.pprint(overall_list)
with open('api/overall.json', 'w') as file:
    file.write(json.dumps(overall_list))
    print "Saved Overall data"
