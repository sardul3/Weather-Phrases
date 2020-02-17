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
        ## Add back a new statement for when there is no available data
    csv_hour = pull_hour_data(url)
    #print(csv_hour)
    hour_dict = parse_hour_data(csv_hour)
    ##print("************ Hour Dict ***********")
    ##print(hour_dict)
    ##print("####### Temp Data ########")
    temp_data = temp_hour(hour_dict)
    ##print(temp_data)
    hum_data = hum_hour(hour_dict)
    wind_data = wind_hour(hour_dict)
    precip_data = precip_hour(hour_dict)
    dict_builder(temp_data, hum_data, wind_data, precip_data)
    os.system("sudo cp phrases.json /var/www/html/weather/phrases.json")
    #precip = precip_day_count("Cheyenne")
    #except:
    #    print("error")
    #    exit()

#look into parallel processing

#isolate each category into an array to be sent back in a station dictionary
# ^^ reference wims rest service organization

#decide how to prioritize phrases       #figure out which measurements corelate with each phrase type
#make a comparison option for customize phrase category

#add phrase(s) in an array and add to dictionary

#add dictionary option to list just station and phrases     #print to command line

#Consider adding a timestamp tag with the weather phrases in output per station 

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



#   make a parse_day_data to work for precip comparisons and temp comparisons      #
#   make 5min data option for certain data types, if no 5min data then use hour data to sort    #

#hour data used for wind, humidity, cloudy, and current temp and precip data


#pulls data from url and returns the csv
#data contains the most recent hour for each station (precip, wind, temp, humidity)
#work on getting cloud coverage  
def pull_hour_data(url):
    now = datetime_now()
    hour = hour_ago(now)
    hour = hour[:10] + "0000"
    #print(hour)
    start = now.strftime('%Y%m%d%H%M%S')
    #EBW and BBW did not have data, but may stil need to be added later
    params = { "net": "KSRE" , "int": "hour", "t_start": str(hour), "t_end": str(hour), "vars":"PRECIP,TEMP2MAVG,WSPD2MAVG,RELHUM2MAVG"}
    #params = { "stn": "Manhattan" , "int": "hour", "t_start": str(hour), "t_end": str(hour), "vars":"PRECIP,TEMP2MAVG,WSPD2MAVG,RELHUM2MAVG"}
    r = None
    r = requests.get( url, params = params )
    print(r.text)
    return r.text



##find way to do a daily check for the month for precip data


### fix to day data and make new timestamps

#Not currently being used, pulls same data as pull_hour_data but for day
def pull_day_data(url):
    now = datetime_now()
    day = day_ago(now)
    day = day[:10] + "0000"
    #print(day)
    start = now.strftime('%Y%m%d%H%M%S')
    #swapped station for network, EBW and BBW may need to be added later
    #params = { "stn": "Manhattan", "int": "day", "t_start": str(day), "t_end": str(start), "vars":"PRECIP,TEMP2MAVG,WSPD2MAVG,RELHUM2MAVG"}
    params = { "net": "KSRE", "int": "day", "t_start": str(day), "t_end": str(start), "vars":"PRECIP,TEMP2MAVG,WSPD2MAVG,RELHUM2MAVG"}
    r = None
    r = requests.get( url, params = params )
    print(r.text)
    return r.text

#takes the csv and splits the headers
# adds data to arrays, puts all information in a dictionary to be returned
def parse_hour_data(csv_hour):

    csv_header = csv_hour.split("\n")[0]
    #print(csv_header)
    if "No data available" in str(csv_header):
        return "None"
    csv_lines = []
    x = csv_hour.split("\n")
    for line in x:
        csv_lines.append(line)
        #print("***")
        #header index
        headers = csv_header.split(",")
        ###     find way to deal with errors involving no data and header errors    ###
        stat_index = headers.index( "STATION" )
        time_index = headers.index("TIMESTAMP")
        temp_index = headers.index("TEMP2MAVG")
        hum_index = headers.index("RELHUM2MAVG")
        precip_index = headers.index("PRECIP")
        wind_index = headers.index("WSPD2MAVG")

        #print(stat_index)

        #separates headers from lines and groups each line into an array to be sorted
        stations = []
        time_hour = []
        temp_hour = []
        hum_hour = []
        precip_hour = []
        wind_hour = []
        for i in range(1,len(csv_lines)):
            stations.append(csv_lines[i].split(",")[stat_index])
            time_hour.append(csv_lines[i].split(",")[time_index])
            temp_hour.append(csv_lines[i].split(",")[temp_index])
            hum_hour.append(csv_lines[i].split(",")[hum_index])
            precip_hour.append(csv_lines[i].split(",")[precip_index])
            wind_hour.append(csv_lines[i].split(",")[wind_index])
            #print("hour array")
            #print(str(stations))
    hour_dict = {"station": stations, "time": time_hour, "temp": temp_hour, "humidity": hum_hour, "precip": precip_hour, "wind": wind_hour}
    #print(str(hour_dict))
    return hour_dict


#Separate data out into different arrays


def parse_day_data(csv_day):

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
        temp_index = headers.index("TEMP2MAVG")
        hum_index = headers.index("RELHUM2MAVG")
        precip_index = headers.index("PRECIP")
        wind_index = headers.index("WSPD2MAVG")

        #separates headers from lines and groups each line into an array to be sorted
        stations = []
        time_day = []
        temp_day = []
        hum_day = []
        precip_day = []
        wind_day = []
        for i in range(1,len(csv_lines)):
            stations.append(csv_lines[i].split(",")[stat_index])
            time_day.append(csv_lines[i].split(",")[time_index])
            temp_day.append(csv_lines[i].split(",")[temp_index])
            hum_day.append(csv_lines[i].split(",")[hum_index])
            precip_day.append(csv_lines[i].split(",")[precip_index])
            wind_day.append(csv_lines[i].split(",")[wind_index])
        #print("day array")
        #print(str(stations))
        if "No data available" in str(csv_header):
            day_dict = {"station": stations, "time": time_day, "temp": "None", "humidity": "None", "precip": "None", "wind": "None"}
        else:
            day_dict = {"station": stations, "time": time_day, "temp": temp_day, "humidity": hum_day, "precip": precip_day, "wind": wind_day}
        #print(str(day_dict))
        return day_dict


#temp in celcius - if wanting fahrenheit: (Celcius * (9/5)) + 32

## Phrase arrays, when temp is matched on the 1-3 scale, a phrase is randomly chosen from the array and sent to a 'temp' section in an output dictionary. 


###         Tmperature Options         ### 


#extremely hot temp
very_hot = ["it's Africa hot", "Who turned the thermostat to 'Hell'", "Let's boil some eggs on the sidewalk"]

#hot temp
warm_hot = ["Put the bikini on", "Time to hit the pool", "Turn the AC on!", "Pull out the short sleeves", "It's a warm day"]

#dictionary of array types, number is randomly generated between 0 and value's array length, then called and placed in a 'temp section in output dict #


#decide whether to keep mid_cool on list or whether to combine it into cold. figure out how to order cool and cold data

#cooler, but not coat weather
cool_temp = ["Sweater weather", "Temperature's falling like a rock", "May want a sweatshirt today", "Jacket recommended", "Grab your coat...it's chilly", "Crank the heat"]

#snow cold -- show probably check precip before using these
#starting from "put your mittens on.." in frozen_temp

#Freezing temp, ice, below zero
frozen_temp = ["Antarctica called...they want their weather back", "Does shivering count as excerise?", "Being this cold should be illegal", "it's so cold, polar bears aren't even going outside", "Put your mittens on, it's freezing", "Better wear your snow boots", "Don't burn your hand doing the boiling water trick", "Time to shovel the driveway", "tired of winter, next season please..", "Defrosting...Ain't nobody got time for that"]


#getting into late/mid fall and winter


#dictionary of all temp categories which are split into arrays of varying degrees of key temp type #

temperature = {"very hot": very_hot, "hot": warm_hot, "cold": cool_temp, "very cold": frozen_temp}

#take the temperature for each station and figures out the best phrase to match with a priority level
# puts the phrase, priority level, data, and station name into a dictionary to be added into the array returned
def temp_hour(hour_dict):
    data = []
    station = []
    temp_array = []
    #print("test hour_dict")
    #print(hour_dict['temp'])
    #print(hour_dict['station'])
    station = hour_dict['station']
    data = hour_dict['temp']
    #print(str(data))
    for x in range(0, len(data)):
        # compare same temp data with same time from previous day #
        #if phrase comes back as 'none', then new phrase is chosen based on temp
        #else comparison phrase from data of the previous day at same time is used
        #print("temp_hour test " + station[x])
        #tests how similar the temperature is to previous day at the same hour
        #try:
        phrase = same_temp(station[x], data[x])
        #except:
        #    phrase = "none"
        #    continue
        #print("*************************  Phrase  ************************")
        #print(phrase)
        #print("***********************************************************")
        if "none" in str(phrase):
            if float(data[x]) < float(0):
                #print("brr " + str(data[x]))
                phrase = temperature['very cold'][random.randrange(0,len(frozen_temp))]
                #print(phrase)
                t_d = {"phrase": phrase, "priority": "1", "data": data[x], "station": station[x]}
                print(t_d)
            else:
                if float(data[x]) >= float(26):
                    if float(data[x]) > float(95):
                        #print("super hot " + str(data[x]))
                        phrase = str(temperature['very hot'][random.randrange(0, len(very_hot))])
                        #print(phrase)
                        t_d = {"phrase": phrase, "priority": "1", "data": data[x], "station": station[x]}
                        print(t_d)
                    else:
                        #print("hot " + str(data[x]))
                        phrase = str(temperature['hot'][random.randrange(0, len(warm_hot))])
                        #print(phrase)
                        t_d = {"phrase": phrase, "priority": "2", "data": data[x], "station": station[x]}
                        print(t_d)
                else:
                    if (float(data[x]) > float(18)) and (float(data[x]) < float(26)):
                        #print("warm " + str(data[x]))
                        phrase = str(temperature['hot'][random.randrange(0, len(warm_hot))])
                        #print(phrase)
                        t_d = {"phrase": phrase, "priority": "3", "data": data[x], "station": station[x]}
                        print(t_d)
                    else:
                        if (float(data[x]) > float(0)) and (float(data[x]) < float(16)):
                            if (float(data[x]) < float(10)):
                                #print("chilly " + str(data[x]))
                                phrase = str(temperature['cold'][random.randrange(0, len(cool_temp))])
                                #print(phrase)
                                t_d = {"phrase": phrase, "priority": "2", "data": data[x], "station": station[x]}
                                print(t_d)
                            else:
                                #print("cool " + str(data[x]))
                                phrase = str(temperature['cold'][random.randrange(0, len(cool_temp))])
                                #print(phrase)
                                t_d = {"phrase": phrase, "priority": "3", "data": data[x], "station": station[x]}
                                print(t_d)
                        else:
                            #print("eh -use day comparison " + str(data[x]))
                            t_d = {"phrase": phrase, "priority": "4", "data": data[x], "station": station[x]}
        else:
            if "Missing" in str(phrase):
                t_d = {"phrase": phrase, "priority": "5", "data": data[x], "station": station[x]}
            else:
                t_d = {"phrase": phrase, "priority": "4", "data": data[x], "station": station[x]}
            print("******************")
            print(t_d)
        temp_array.append(t_d)
    print(temp_array)
    return temp_array



#maybe do a test first before other hourly tests to see if weather is gonna be the same/ close to previous day
#tests how similar the temperature is to previous day at the same hour
#if day is within close range it returns a matching phrase, else returns none statement
def same_temp(station, data):
    with open('same_temp.json') as f:
        info = json.load(f)
    #print(info)
    line = 0
    old = 100.0
    for line in range(0, len(info)):
        #print(info[line])
        #text = json.loads(data[line])
        stat = info[line]['station']
        #print(" from JSON File : " + str(stat))
        if str(stat) == station:
            old = info[line]['old temp']
            print(old)
   
    print(old)
    # if data is missing, it returns missing
    if 'M' in str(data):
        phrase = "Missing"
        return phrase
    if 'M' in str(old):
        phrase = "Missing"
        return phrase
    difference = float(data) - float(old)
    #print(difference)
    if (float(difference) < float(2)) and (float(difference) > float(-2)):
        phrase = "Pretty much the same as yesterday"
        return phrase
    else:
        if (difference > float(2)) and (difference < float(5)):
            phrase = "It's warmer than yesterday"
            return phrase
        if (difference < float(-2)) and (difference > float(-5)):
            phrase = "It's colder than yesterday"
            return phrase
        else:
            phrase = "none"
            return phrase





##################  work on winter humidity details and snow chances for high winter humidity       ################
### Consider no humidity statements for winter unless super dry or super high humidity with chance of snow ###


###         Humidity Options            ###

very_humid = ["Rainforest humid", "Second shirt required", "Better tie up the hair", "It's the humidity, not the heat"]

##      Or should I leave it blank and make a combination statement for "lots of heat.."        ##
##      if blank, it may help with prioritizing, comsider the same for rain unless dry streak      ##

comfort_hum = ["A comfortable humidity"]
#["Lots of heat, little humidity", "a little humid"]
low_hum = ["Like a desert out there", "It's a dry heat", "Dry lips are the worst"]

#winter humidity - add more
humid = ["Chance of snow"] #if 90 to 100% for consecutive hours

dry_hum = ["Dry lips are the worst", "Grab some chapstick, its a dry day"]

humidity = {"humid": very_humid, "comfortable": comfort_hum, "dry": low_hum}
humidity_winter = {"humid": humid, "comfortable": comfort_hum, "dry": dry_hum}

#takes humidity data for each station and matches it to proper phrase with a priority ranking
#puts phrase, priority level, data, and station in a dictionary to be added to the returned array
def hum_hour(hour_dict):
    data = []
    temp = []
    station = []
    hum_array = []
    #print("test hour_dict")
    #print(hour_dict['humidity'])
    temp = hour_dict['temp']
    data = hour_dict['humidity']
    station = hour_dict['station']
    print(str(data))
    for x in range(0, len(data)):
        if 'M' in str(data[x]):
            phrase = "Missing"
            h_d = {"phrase": phrase, "priority": "5", "data": data[x], "station": station[x]}
            print(h_d)
        else:
            if 'M' in str(temp[x]):
                phrase = "Missing"
                h_d = {"phrase": phrase, "priority": "5", "data": data[x], "station": station[x]}
                print(h_d)
            else:

                if float(data[x]) < float(31):
                    if (float(temp[x]) <= float(4.0)):
                        #print("dry cold " + str(data[x]))
                        phrase = str(humidity_winter['dry'][random.randrange(0,len(dry_hum))])
                        h_d = {"phrase": phrase, "priority": "2", "data": data[x], "station": station[x]}
                        print(h_d)
                    else:
                        #print("dry heat " + str(data[x]))
                        phrase = str(humidity['dry'][random.randrange(0,len(low_hum))])
                        h_d = {"phrase": phrase, "priority": "2", "data": data[x], "station": station[x]}
                        print(h_d)
                else:
                    if float(data[x]) >= float(46):
                        #print("very humid " + str(data[x]))
                        if(float(temp[x]) > float(26.8)):
                            phrase = str(humidity['humid'][random.randrange(0,len(very_humid))])
                            h_d = {"phrase": phrase, "priority": "1", "data": data[x], "station": station[x]}
                            print(h_d)
                        else:
                            #print none - dont want to risk inaccurate chance of snow - else print humid
                            phrase = "none"
                            h_d = {"phrase": phrase, "priority": "4", "data": data[x], "station": station[x]}
                            print(h_d)
                    else:
                        #print("comfortable humidity " + str(data[x]))
                        phrase = str(humidity['comfortable'][random.randrange(0, len(comfort_hum))])
                        h_d = {"phrase": phrase, "priority": "3", "data": data[x], "station": station[x]}
                        print(h_d)
        hum_array.append(h_d)
    print(hum_array)
    return hum_array





###         Wind Options        ###

#set 5mph at windy, if below then calm
#if more than 10 -very windy
#check within an hour interval to detemine wind

very_windy = ["Tie down the trampoline", "Windy as $#@&", "Yes! Leaves are moving to the neighbors", "Gone with the wind", "Bad day to wear a skirt", "Bad hair day"]

low_wind = ["Yes! Leaves are moving to the neighbors", "Lost in the wind...", "Bad hair day", "Hold onto your hat", "Watch your skirt alert"]

no_wind = ["Stagnant", "Great spray day", "Good hair day", "Still as Christmas Eve"]


wind = {"very windy": very_windy, "some wind": low_wind, "no wind": no_wind}

# takes wind data for each station and pairs it with proper phrase and priority level
# puts phrase, priority level, station, and data into dictionary to be added in returned array
def wind_hour(hour_dict):
    data = []
    station = []
    wind_array = []
    #print("test hour_dict")
    #print(hour_dict['wind'])
    data = hour_dict['wind']
    station = hour_dict['station']
    print(str(data))
    for x in range(0, len(data)):
        if 'M' in str(data[x]):
            phrase = "Missing"
            w_d = {"phrase": phrase, "priority": "5", "data": data[x], "station": station[x]}
            print(w_d)
        else:
            if float(data[x]) <= float(5):
                #print("no wind " + str(data[x]))
                phrase = str(wind['no wind'][random.randrange(0,len(no_wind))])
                w_d = {"phrase": phrase, "priority": "3", "data": data[x], "station": station[x]}
                print(w_d)
            else:
                if float(data[x]) >= float(12):
                    #print("very windy " + str(data[x]))
                    phrase = str(wind['very windy'][random.randrange(0,len(very_windy))])
                    w_d = {"phrase": phrase, "priority": "1", "data": data[x], "station": station[x]}
                    print(w_d)
                else:
                    #print("some wind " + str(data[x]))
                    phrase = str(wind['some wind'][random.randrange(0, len(low_wind))])
                    w_d = {"phrase": phrase, "priority": "2", "data": data[x], "station": station[x]}
                    print(w_d)
        wind_array.append(w_d)
    print(wind_array)
    return wind_array



########################################################
### work on windchill and frostbite data ###


#Not active
# Goal: to use for wind chill information
def wind_temp(hour_dict):
    temp = hour_dict["temp"]
    wind = hour_dict["wind"]
    phrase = "none"
    for x in range(0, len(wind)):
        if float(temp[x]) < float(-25):
            phrase = "increased risk of frostbite"
            return phrase
    return phrase



###      Precipitation Options      ###

#heavy_rain = ["Raining cats and dogs out there"]

mid_rain = ["umbrella necessary", "Liquid sunshine"]

#rain = {"heavy rain": heavy_rain, "mid rain": mid_rain}

none = ["No rain"]
### [Too cold for rain! (measuring rainfall with temperatures less than 40F)]
### [Rain, rain, go away... (multiple days of rain)] [Turn off the spicket! (several days with rain)] [Rainy Day Streak: x days]
### [Where do we put in the order for rain? (period of dry weather in summer)] [Needed: Rain. (x days without rainfall)] [Badly needed: Rain. (10x days without rainfall)] [Please, please, please bring us some rain. (20x days without rain)] [Too. Dry. (30x days without rain)]

#make an if statement to go along with dry days to match length
dry_days = []


## Need to determine comparison data for counting days with or days with out rain ##
## Work on making comparison information for days in monthly data
### use 5min or houly data to see if precip is current between last interval
#use day comparison to see for precip day streaks or dry day streaks

#decide what to do for 'none'
precip = {"rain": mid_rain, "none": none}


#********************************************************************

# takes precip data for all stations and matches with appropriate phrase and priority level
#puts data, phrase, priority level, and station into dictionary to be added to returned array
def precip_hour(hour_dict):
    data = []
    station = []
    precip_array = []
    #print("test hour_dict")
    #print(hour_dict['precip'])
    data = hour_dict['precip']
    station = hour_dict['station']
    #print(str(data))
    #figure out what is considered heavy rain
    for x in range(0, len(data)):
        if 'M' in str(data[x]):
            phrase = "Missing"
            p_d = {"phrase": phrase, "priority": "5", "data": data[x], "station": station[x]}
            #print(p_d)
        else:
            if float(data[x]) > float(0.00):
                #print("rain " + str(data[x]))
	        # test consecutive days of rain
                days = precip_day_count(station[x])
                phrase = str(precip['rain'][random.randrange(0, len(mid_rain))])
                if int(days) < int(3):
                    phrase = str(precip['rain'][random.randrange(0, len(mid_rain))])
                    p_d = {"phrase": phrase, "priority": "1", "data": data[x], "station": station[x]}
                    #print(p_d)
                else:
                    if (int(days) > int(2)) and (int(days) <= int(4)):
                        phrase = "Turn off the spicket! (" + str(days) + " consecutive rain days)"
                    if (int(days) > int(4)) and (int(days) <= int(7)):
                        phrase = "Rain, Rain, Go away... (" + str(days) + " consecutive rain days)"
                    if int(days) > int(7):
                        phrase = "Rainy Day Streak: " + str(days) + " days"
                    p_d = {"phrase": phrase, "priority": "1", "data": data[x], "station": station[x]}
                    #print(p_d)
            else:
                #print("no rain " + str(data[x]))
	 # checks for consecutive dry days
                try:
                    days = dry_day_count(station[x])
                except:
                    days = 0
                if int(days) < int(8):
                    phrase = str(precip['none'])
                    p_d = {"phrase": phrase, "priority": "4", "data": data[x], "station": station[x]}
                    #print(p_d)
                else:
                    phrase = str(precip['none'])
                    if int(days) >= int(8):
                        phrase = "Needed: Rain (" + str(days) + " days without rainfall)"
                    if (int(days) >= int(10)) and (int(days) <= int(20)):
                        phrase = "Badly needed: Rain (" + str(days) + " days without rainfall)"
                    if (int(days) >= int(20)) and (int(days) <= int(30)):
                        phrase = "Please, Please, Please bring us some rain (" + str(days) + " days without rainfall)"
                    if (int(days) >= 30):
                        phrase = "Too. Dry. (" + str(days) + " days without rainfall)"
                    p_d = {"phrase": phrase, "priority": "2", "data": data[x], "station": station[x]}
                    #print(p_d)
        precip_array.append(p_d)
    print(precip_array)

    # make function to check up on number of rainy or dry consecutive days 
    return precip_array

# compares data for the last month to find number of days since last rainfall 
# returns day count since last rain
def dry_day_count(station):
    with open('precip.json') as f:
        data = json.load(f)
    #print(data)
    line = 0
    for line in range(0, len(data)):
        #print(data[line])
        #text = json.loads(data[line])
        stat = data[line]['station']
        if str(stat) == station:
            days = data[line]['Dry days']
            print(days)
            return days
    print("Missing")
    return 0


# checks data over last month to count consecutive rain days
# returns day count
def precip_day_count(station):
    with open('precip.json') as f:
        data = json.load(f)
    #print(data)
    line = 0
    for line in range(0, len(data)):
        #print(data[line])
        #text = json.loads(data[line])
        stat = data[line]['station']
        if str(stat) == station:
            days = data[line]['Precip days']
            print(days)
            return days
    print("Missing")
    return 0
    #maybe set json stuff to not include current date, then add 1 to the count before returning so it is not a stored item?


###     Cloudy options      ###

very_cloudy = ["Overcast"]

partly_cloudy = ["I think the sun is trying to come out", "partly cloudy", "A little ray of sunshine"]

few_clouds = ["Mostly clear"]

clear = ["Mr. Blue Sky", "Not a cloud in sight"]

cloudy = {"clouds" : very_cloudy, "partly": partly_cloudy, "few clouds": few_clouds, "clear": clear}

#Not Active, but would like to get it working
#def cloudy_hour(hour_dict):
#    data = []
#    print("test hour_dict")
#    print(hour_dict['cloudy'])
#    data = hour_dict['cloudy']
#    print(str(data))
#    #for x in range(0, len(data)):
#    #    if float(data[x]) <= float(5):
#    #        print("no wind " + str(data[x]))
#    #        print(wind['no wind'][random.randrange(0,len(no_wind))])
#    #    else:
#    #        if float(data[x]) >= float(12):
#    #            print("very windy " + str(data[x]))
#    #            print(wind['very windy'][random.randrange(0,len(very_windy))])
#    #        else:
#    #            print("some wind" + str(data[x]))
#    #            print(wind['some wind'][random.randrange(0, len(low_wind))])
#    return data




###     Custom Options      ###

#if hot and dry in summer : ["Better water the garden", "Prevent Sparks!]

#if hot and humid : ["All we need is a beach!", "Heat index is somewhere between OMG and WTF"]


#   Seasonal - figure out how to tell time of year     #

#if late fall warmth : ["Indian summer!"]

#if early cold in fall : ["Too early for this cold..."]

#if large temp drop in late fall : ["Winter is coming..."]

#if late cold in spring : ["Too late for this cold..."]

#if snow/very cold temp in spring : ["What a lovely winter we are having this spring"]

# Takes the phrases and sorts them based on priority level to narrow list to 1 or 2 phrases per station
# Adds chosen phrases to a final dictionary to be added to the array which is sent to phrases.txt
def dict_builder(temp_data, hum_data, wind_data, precip_data):
    #priorities: temp(1-4), hum(1-4), wind(1-3)
    print("test phrase")
    
    final_phrase = []
    #final_phrase = ""

    #print(temp_data)
    print(len(temp_data))
    print("####")
    #print(hum_data)
    print(len(hum_data))
    print("####")
    #print(wind_data)
    print(len(wind_data))
    print("####")
    #print(precip_data)
    print(len(precip_data))
    print("####")
    for x in range(0, len(temp_data)):
        #print("test")
        #print(temp_data)
        #print(temp_data['priority'][x])
        #print(str(temp_data[x]['priority']))

        if int(precip_data[x]['priority']) < 3:
            #final_dict = {"station": str(temp_data[x]['station']), "precip": str(precip_data[x]['phrase'])}
            final_dict = {"station": str(temp_data[x]['station']), "phrase": str(precip_data[x]['phrase'])}
        else:
            if int(wind_data[x]['priority']) == 1:
                #final_dict = {"station": str(temp_data[x]['station']), "wind": str(wind_data[x]['phrase'])}
                final_dict = {"station": str(temp_data[x]['station']), "phrase": str(wind_data[x]['phrase'])}
            else:
                if int(temp_data[x]['priority']) < 3:
                    #final_dict = {"station": str(temp_data[x]['station']), "temp": str(temp_data[x]['phrase'])}
                    final_dict = {"station": str(temp_data[x]['station']), "phrase": str(temp_data[x]['phrase'])}
                    if  int(hum_data[x]['priority']) == 1:
                        if int(temp_data[x]['priority']) == 5:
                            #final_dict = {"station": str(temp_data[x]['station']), "humidity": str(hum_data[x]['phrase'])}
                            final_dict = {"station": str(temp_data[x]['station']), "phrase": str(hum_data[x]['phrase'])}
                        else:
                            #final_dict = {"station": str(temp_data[x]['station']), "temp": str(temp_data[x]['phrase']), "humidity": str(hum_data[x]['phrase'])}
                            final_dict = {"station": str(temp_data[x]['station']), "phrase": str(temp_data[x]['phrase']) + ", " + str(hum_data[x]['phrase'])}
                    if  int(hum_data[x]['priority']) == 2:
                        if int(temp_data[x]['priority']) == 5:
                            #final_dict = {"station": str(temp_data[x]['station']), "humidity": str(hum_data[x]['phrase'])}
                            final_dict = {"station": str(temp_data[x]['station']), "phrase": str(hum_data[x]['phrase'])}
                        else:
                            #final_dict = {"station": str(temp_data[x]['station']), "temp": str(temp_data[x]['phrase']), "humidity": str(hum_data[x]['phrase'])}
                            final_dict = {"station": str(temp_data[x]['station']), "phrase": str(temp_data[x]['phrase']) + ", " + str(hum_data[x]['phrase'])}
                else:
                    #final_dict = {"station": str(temp_data[x]['station']), "temp": str(temp_data[x]['phrase'])}
                    final_dict = {"station": str(temp_data[x]['station']), "phrase": str(temp_data[x]['phrase'])}


        # deal with 'Missing' temp phrase statements when closer to webpage uploading

        print("final dict")
        print(final_dict)
        #final_phrase = str(final_phrase) + final_dict
        final_phrase.append(final_dict)
    print("********************* Final Phrase *********************")
    #f = open("phrases.json","w")
    #f.write(str(final_phrase))
    #f.close()
    with open("phrases.json", "w") as f_out:
        json.dump(final_phrase, f_out)
    print(final_phrase)
    print("Success")



#    #add all chosen phrases to the parameters
# add cloud stuff later
# figure out the best way to do the dict info with multiple stations - all in arrays and then how to output info
# for loop and figure out way to group data 
#may need to send info to another function to prioritize phrasing
# final result should only output station name, timestamp, and top 1 or 2 phrases
#   dict = {"station": station, "temp": temp_phrase, "precip": precip_phrase, "wind": wind_phrase}


if __name__ == "__main__":
    main()


