import requests
import datetime
import json

with open("./url.csv") as file:
    salles = file.read().split("\n")
    
def to_date(char):
    year = int(char[0:4])
    month = int(char[4:6])
    day = int(char[6:8])
    hour = int(char[9:11])
    minute = int(char[11:13])
    sec = int(char[13:15])
    date = datetime.datetime(year, month, day, hour, minute, sec)
    return int(date.timestamp())

salles_liste = {}

for item in salles :
    if item == "" : break

    batiment,salle,url = item.split(",")
    salle_code = batiment.replace(" ","_") + "_" + salle.replace(" ","_")

    salles_liste[salle_code] = {"batiment":batiment,"salle":salle}

    req = requests.get(url)
    if req.status_code != 200 : raise Exception("Api Univ Pété") 

    liste = []

    DTSTART=""
    DTEND=""
    SUMMARY=""
    
    text = req.text
    text = text.replace("\r","\n")
    text = text.replace("\n ","")
    text = text.split("\n")

    for item in text:
        line = item.split(":")
        code = line[0]
        value = ":".join(line[1:])

        if code == "DTSTART":
            DTSTART=to_date(value)
        elif code == "DTEND":
            DTEND=to_date(value)
        elif code == "SUMMARY":
            SUMMARY=value
        elif code == "END" and value == "VEVENT":
            liste.append([DTSTART , DTEND , SUMMARY])
    print(liste[0],salle_code)

    liste.sort()
    with open("./out/"+salle_code+".json","w+") as file:
        print(liste[0],salle_code)

        file.write(json.dumps(liste))

with open("./out/salles.json","w+") as file:
    file.write(json.dumps(salles_liste))
