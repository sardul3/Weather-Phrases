import os
import sys
import requests
import random
import json
import pytz
import os.path
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

#http://mesonet.k-state.edu/rest/stationdata?stn=Ashland%20Bottoms&int=5min&t_start=20191114000000&t_end=20191114000000&vars=PRECIP,TEMP2MAVG,WSPD2MAVG,RELHUM2MAVG
#pull data from rest service url
url = "http://mesonet.k-state.edu/rest/stationdata"
#start with daily, and move toward weekly for comparisons

#start with one station and slowly add

#calls all functions and send each ones data to the final dict
def main():
    #try:
    data = same_temp()
    send_file(data)
    #except:
    #    exit()

#current time
def datetime_now():
    #sets current time
    tz = pytz.timezone("America/Chicago")
    now = datetime.now()
    now = tz.localize(now)
    return now

#one hour ago
def hour_ago(now):
    #gets t_start by subtracting 1 hour from now
    #print(now)
    start = now - timedelta(hours=1)
    start = start.strftime('%Y%m%d%H%M%S')
    #print(start)
    return start



#maybe do a test first before other hourly tests to see if weather is gonna be the same/ close to previous day
#tests how similar the temperature is to previous day at the same hour
#if day is within close range it returns a matching phrase, else returns none statement
def same_temp():
    url = "http://mesonet.k-state.edu/rest/stationdata"
    now = datetime_now()
    hour = hour_ago(now)
    hour = hour[:10] + "0000"
    print(hour)
    start = now.strftime('%Y%m%d%H%M%S')
    params = { "net": "KSRE", "int": "hour", "t_start": str(hour), "t_end": str(hour), "vars":"TEMP2MAVG"}
    r = None
    r = requests.get( url, params = params )
    #print("***")
    print(r.text)
    #csv_day = r.text
    if "No data available" in str(csv_day):
        #phrase = "Missing"
        exit()
       # maybe try turning this into a try/except statement because of header errors
    else:
        csv_header = csv_day.split("\n")[0]
        csv_lines = []
        x = csv_day.split("\n")
        for line in x:
            csv_lines.append(line)
            #headers index
            headers = csv_header.split(",")
            stat_index = headers.index( "STATION" )
            time_index = headers.index("TIMESTAMP")
            temp_index = headers.index("TEMP2MAVG")
            stations = []
            #time_day = []
            temp_day = []
            #print("b4")
            data = []
        for i in range(1,len(csv_lines)):
            #print("for")
            stations.append(csv_lines[i].split(",")[stat_index])
            temp_day.append(csv_lines[i].split(",")[temp_index])
            #print(temp_day)        
        for j in range(0, len(temp_day)):
            info = {"station": stations[j], "old temp": temp_day[j]}
            data.append(info)
        print(data)
        return data


def send_file(data):
    print("********************* Final Phrase *********************")
    #f = open("phrases.json","w")
    #f.write(str(final_phrase))
    #f.close()
    with open("same_temp.json", "w") as f_out:
        json.dump(data, f_out)
    print(data)
    print("Success")



if __name__ == "__main__":
    main()


