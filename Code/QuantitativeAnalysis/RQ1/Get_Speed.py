#get the response time
import pandas as pd
import re
import textstat
#from textblob import TextBlob   #import error
import datetime 
import numpy as np
import os
import unicodedata

def get_date(mes, community_name):
    #community_name is the original dile name
    mes = mes[mes.find(' <') + 2 : ].strip()             #add name to match the messgae -- get date
    raw_file = open(community_name, "r",encoding= "utf-8")
    for per_line in raw_file.readlines():
        if mes in per_line:
            weekday = per_line[1 : per_line.find("] ")]
            break
    #print(weekday)
    weekday = weekday[weekday.find(" ") + 1 : ]
    #print(weekday)
    weeknum = datetime.datetime.strptime(weekday, "%H:%M:%S")
    return weeknum

#get csv of data
root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../.."))  # get ccurrent dir
data_df = pd.DataFrame({"DialogNum":[], "dialog_speed":[]})   
data_dir = root + "/Data/DataRQ/RQ1/Response/"              # input：location dialogs with/without reponse
res_dir = root + "/Data/DataRQ/RQ1/Speed/"

if not os.path.exists(res_dir):    
    os.makedirs(res_dir) 

community_dirs = os.listdir(data_dir)
for per_community in community_dirs:
    if ("unrespond" in per_community):
        continue                             #only deal dilogs with responses
    if ("android" not in per_community):
        continue
    print(per_community)
    community_txt_dir = data_dir + per_community
    community_name = per_community.split(".")[0]
    community_dir = root + "/Data/DataAscii/" + community_name + ".txt"   #Problem: Add process or not

    dialog_count = 1
    data_df = pd.DataFrame({"DialogNum":[], "dialog_speed":[]})   
    with open (community_txt_dir, "r", encoding= "utf-8") as f:
        first_utterance_flag = 1           #Tag the start of a dialog
        cal_dialog_time = 0                #Tag whether the response time of a dialog has been calculated
        lines = f.readlines()
        for index, line in enumerate(lines):
            #print(line)
            if (first_utterance_flag == 1):
                print(dialog_count)
                first_name = line[line.find(' <') + 2 : line.find('> ')]
                first_time = get_date(line, community_dir)
                #print(first_time)
                res = []
                res.append(dialog_count)
                first_utterance_flag = 0
                dialog_count += 1
                continue
            if (line == "--------------------------------------------------------------------------------\n"):
                first_utterance_flag = 1 #Tag the next utterance start a new dialog
                cal_dialog_time = 0
            #data_df.to_csv("D://zju//1-paper//1_newdataset//1-Discord_dataset//Rq1Analysis//rq1_res.csv")
            #break
            else:
                # the utterance in a dialog but is not the initial one
                if (cal_dialog_time == 0):
                    next_name = line[line.find(' <') + 2 : line.find('> ')]
                    if (next_name != first_name):
                        next_time = get_date(line, community_dir)
                        #print(next_time)
                        cal_dialog_time = 1    #The response time of this dialog has been calculated
                        dialog_speed = next_time - first_time
                        res.append(dialog_speed.total_seconds())
                        #print(res)
                        data_df.loc[len(data_df.index)] = res
                       # res = []

        print("done")
        data_df.to_csv(res_dir + community_name + ".speed.csv")

    #break