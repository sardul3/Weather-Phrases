#parse the previous day's rain for each station
#update their dictionaries for precip days and no rain days
#dict = {"station": station, "precip": # of days in a row, "dry": dry day streak"}
#if rain day, dry = 0, and vise versa
#make into an array of dictionaries in a json file to be read in by weather_phrase.py
#set this into a cron task to be ran every 24 hours to get newest updated rain data - run at 3 am? to get newest midnight updates for all stations?


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
    data = station_call()
    send_file(data)

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

#one day ago
def day_ago(now):
    #gets t_start by subtracting 24 hours from now
    #print(now)
    start = now - timedelta(hours=24)
    start = start.strftime('%Y%m%d%H%M%S')
    #print(start)
    return start

#one month ago
def month_ago(now):
    #gets t_start by subtracting 24 hours from now
    #print(now)
    start = now - timedelta(days=30)
    start = start.strftime('%Y%m%d%H%M%S')
    #print(start)
    return start


def station_call():

    stations = ['Ashland 8S', 'Ashland Bottoms', 'Belleville 2W', 'Butler', 'Cherokee', 'Cheyenne', 'Clay', 'Colby', 'Elmdale 1SE', 'Garden City', 'Grant', 'Gray', 'Gypsum', 'Hamilton', 'Harper', 'Haskell', 'Hays', 'Haysville', 'Hiawatha', 'Hill City', 'Hodgeman', 'Hutchinson 10SW', 'Jewell', 'La Crosse', 'Lake City', 'Lakin', 'Lane', 'Leoti', 'Lorraine', 'Manhattan', 'McPherson 1S', 'Meade', 'Miami', 'Mitchell', 'Moscow 10NW', 'Ness City', 'Olathe', 'Osborne', 'Ottawa 2SE', 'Overbrook', 'Parsons', 'Richfield', 'Rock Springs', 'Rocky Ford', 'Rossville 2SE', 'Roth Tech Farm', 'Satanta', 'Scandia', 'Sedan', 'Sheridan', 'Sherman', 'Silver Lake 4E', 'Spearville', 'St John 1NW', 'Stanton', 'Tribune', 'Tribune 6NE', 'Viola', 'Wallace', 'Washington', 'Willis Tech Farm', 'Woodson']
    i = 0
    dry = 0
    wet = 0
    data = []
    for i in range(0, len(stations)):
        station = stations[i]
        try:
            dry = dry_day_count(station)
            wet = precip_day_count(station)
        except:
            dry = "Missing"
            wet = "Missing"
            continue
        precip_dict = {"station": station, "Dry days": str(dry), "Precip days": str(wet)}
        print(precip_dict)
        data.append(precip_dict)
    return data

def dry_day_count(station):
    now = datetime_now()
    month = month_ago(now)
    month = month[:8] + "000000"
    #print(month)
    start = now.strftime('%Y%m%d%H%M%S')
    params = { "stn": station, "int": "day", "t_start": str(month), "t_end": str(start), "vars":"PRECIP"}
    r = None
    r = requests.get( url, params = params )
    #print(r.text)
    csv_day = r.text

    csv_header = csv_day.split("\n")[0]
    csv_lines = []
    x = csv_day.split("\n")
    for line in x:
        csv_lines.append(line)
        #### Add solar radiation stuff for cloudy coverage  ###

        #headers index
        headers = csv_header.split(",")
        stat_index = headers.index( "STATION" )
        time_index = headers.index("TIMESTAMP")
        precip_index = headers.index("PRECIP")
        #separates headers from lines and groups each line into an array to be sorted
        stations = []
        time_day = []
        precip_day = []
        for i in range(1,len(csv_lines)):
            stations.append(csv_lines[i].split(",")[stat_index])
            time_day.append(csv_lines[i].split(",")[time_index])
            precip_day.append(csv_lines[i].split(",")[precip_index])
    #print("day array")
    #print(str(stations))
    reverse = precip_day[::-1]
    stat_reverse = stations[::-1]
    time_reverse = time_day[::-1]
    day_dict = {"station": stat_reverse, "time": time_reverse, "precip": reverse}
    #print(str(day_dict))
    count = 0
    for num in range(0, len(reverse)):
        if float(reverse[num]) == float(0.0):
            count += 1
        else:
            #print(count)
            #with open("dry_days.txt", "w") as f_out:
            #find way to append and replace count
            #maybe append as a dict with each station name as a key and count as a value
            #find way to rework this function to get that working
            return count
    #print(count)
    return count



# checks data over last month to count consecutive rain days
# returns day count
def precip_day_count(station):
    now = datetime_now()
    month = month_ago(now)
    month = month[:8] + "000000"
    #print(hour)
    start = now.strftime('%Y%m%d%H%M%S')
    params = { "stn": station, "int": "day", "t_start": str(month), "t_end": str(start), "vars":"PRECIP"}
    r = None
    r = requests.get( url, params = params )
    #print(r.text)
    csv_day = r.text

    csv_header = csv_day.split("\n")[0]
    csv_lines = []
    x = csv_day.split("\n")
    for line in x:
        csv_lines.append(line)

        #### Add solar radiation stuff for cloudy coverage  ###

        #headers index
        headers = csv_header.split(",")
        stat_index = headers.index( "STATION" )
        time_index = headers.index("TIMESTAMP")
        precip_index = headers.index("PRECIP")
        #separates headers from lines and groups each line into an array to be sorted
        stations = []
        time_day = []
        precip_day = []
        for i in range(1,len(csv_lines)):
            stations.append(csv_lines[i].split(",")[stat_index])
            time_day.append(csv_lines[i].split(",")[time_index])
            precip_day.append(csv_lines[i].split(",")[precip_index])
    #print("day array")
    #print(str(stations))
    reverse = precip_day[::-1]
    stat_reverse = stations[::-1]
    time_reverse = time_day[::-1]
    day_dict = {"station": stat_reverse, "time": time_reverse, "precip": reverse}
    #print(str(day_dict))
    count = 0
    for num in range(0, len(reverse)):
        if float(reverse[num]) > float(0.0):
            count += 1
        else:
            #print(count)
            #with open("dry_days.txt", "w") as f_out:
            #find way to append and replace count
            #maybe append as a dict with each station name as a key and count as a value
            #find way to rework this function to get that working
            return count
    #print(count)
    return count

def send_file(precip_dict):
    print("********************* Final Phrase *********************")
    #f = open("phrases.json","w")
    #f.write(str(final_phrase))
    #f.close()
    with open("precip.json", "w") as f_out:
        json.dump(precip_dict, f_out)
    print(precip_dict)
    print("Success")





if __name__ == "__main__":
    main()


