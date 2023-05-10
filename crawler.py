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
        if(len(tds)<5):
            continue
        if(tds[0].text.lower().find("India".lower()) != -1):
            statewide_list.append({"Name":"Total","Confirmed-Indian":int(tds[1].text.strip('\r\n#*')),"Confirmed-Foreign":0,"Cured/Discharged/Migrated":int(tds[2].text.strip('\r\n#*')),"Death":int(tds[3].text.strip('\r\n#*'))})
        else:
            statewide_list.append({"Name":tds[1].text.strip('\r\n#*'),"Confirmed-Indian":int(tds[2].text.strip('\r\n#*')),"Confirmed-Foreign":0,"Cured/Discharged/Migrated":int(tds[3].text.strip('\r\n#*')),"Death":int(tds[4].text.strip('\r\n#*'))})
    

    selectedtags =  soup.select("span.icount")
    count=0
    for singletag in selectedtags:          
        txt=singletag.getText()
        if(count<len(labels)):
            overall_list.append({"label":labels[count],"value":int(txt.strip().replace(",","").replace("#",""))})
        count+=1

def get_out(list_info):

    list_info = list(map(lambda x:x.strip(), list_info))

    new_list = [a for a in list_info if (a!='')]

    names= new_list[0::2]
    numbers=new_list[1::2]
    numbers = list(map(lambda x:x.replace('#',''),numbers))
    numbers = list(map(lambda x:x.replace('*',''),numbers))

    old_dict = list(zip(names, numbers))

    new_dict = dict()

    c=0
    while c <len(old_dict):
        new_dict[old_dict[c][0]] = [(names[it], numbers[it]) for it in range(c+1, c+int(old_dict[c][1])+1)]
        c=c+int(old_dict[c][1])+1
    
    return new_dict

def district_level_json():      
    # creating a pdf file object 
    
    # urllib.request.urlretrieve(url, 'districts.pdf')
    import requests
    url = 'https://www.mohfw.gov.in/pdf/DistrictWiseList324.pdf'
    myfile = requests.get(url)
    open('districts.pdf', 'wb').write(myfile.content)

    pdfFileObj = open('districts.pdf', 'rb') 
    
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    
    # printing number of pages in pdf file 
    print(pdfReader.numPages) 
    
    # creating a page object 
    pageObj = pdfReader.getPage(0) 
    
    # extracting text from page 
    text=pageObj.extractText()

    
    # closing the pdf file object 
    pdfFileObj.close() 

    arr=text.split("\n")
    arr=arr[11:]

    with open('api/districts.json', 'w') as file:
        file.write(json.dumps(get_out(arr)))
        print "Saved Overall data two"




                        
import pprint
pprint.pprint(statewide_list)
with open('api/statewide.json', 'w') as file:
    file.write(json.dumps(statewide_list))
    print "Saved Statewide data"

pprint.pprint(overall_list)
with open('api/overall.json', 'w') as file:
    file.write(json.dumps(overall_list))
    print "Saved Overall data test"

# district_level_json()
