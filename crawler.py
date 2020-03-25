from bs4 import BeautifulSoup
import grequests
import json

urls=   [
    'https://www.mohfw.gov.in/'
]
requests = (grequests.get(u) for u in urls)
responses = grequests.map(requests)

labels=["Screened","Active","Discharged","Deaths","Migrated"]

overall_list=[]
statewide_list=[]

for i, response in enumerate(responses):
    soup = BeautifulSoup(response.text, 'html.parser')
    selectedtags = soup.select("#cases tbody tr")
    
    for row in selectedtags:
        tds = row.select("td")
        print(tds)
        if(tds[0].text.lower().find("India".lower()) != -1):
            statewide_list.append({"Name":"Total","Confirmed-Indian":tds[1].text,"Confirmed-Foreign":int(tds[2].text.strip('\r\n#*')),"Cured/Discharged/Migrated":int(tds[3].text.strip('\r\n#*')),"Death":int(tds[4].text.strip('\r\n#*'))})
        else:
            statewide_list.append({"Name":tds[1].text.strip('\r\n#*'),"Confirmed-Indian":int(tds[2].text.strip('\r\n#*')),"Confirmed-Foreign":int(tds[3].text.strip('\r\n#*')),"Cured/Discharged/Migrated":int(tds[4].text.strip('\r\n#*')),"Death":int(tds[5].text.strip('\r\n#*'))})
    

    selectedtags =  soup.select("span.icount")
    count=0
    for singletag in selectedtags:          
        txt=singletag.getText()
        if(count<len(labels)):
            overall_list.append({"label":labels[count],"value":int(txt.strip().replace(",","").replace("#",""))})
        count+=1
        
                        
import pprint
pprint.pprint(statewide_list)
# with open('api/statewide.json', 'w') as file:
#     file.write(json.dumps(statewide_list))
#     print "Saved Statewide data"

pprint.pprint(overall_list)
with open('api/overall.json', 'w') as file:
    file.write(json.dumps(overall_list))
    print "Saved Overall data"
