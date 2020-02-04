import sys
import operator
import time
import collections
import numpy as np
import matplotlib.pyplot as plt

# Dictionary variable declaration 
sent_count ={}
received_count = {}
sorted_sent_count = {}
sorted_received_count = {}
top_n_sender = {}

# Opening the data file, counting the number of emails sent and received by each person
with open(sys.argv[1], mode="r") as inputfile:
    for line in inputfile:
        items = line.split(",")
        if len(items) == 6:
            timeD,ID,sender,receiver,topic,mode = items
            list_of_receiver = receiver.split("|")
            if not sender in sent_count:
                sent_count[sender] = len(list_of_receiver)
            else:
                sent_count[sender] = sent_count[sender] + len(list_of_receiver)
            for i in list_of_receiver:
                if not i in received_count:
                    received_count[i] = 1
                else:
                    received_count[i] = received_count[i] + 1
                    
# Sorting in decending order of no. of emails sent/received
sorted_sent_count = sorted(sent_count.items(), key = lambda t: t[1], reverse=True)
sorted_received_count = sorted(received_count.items(), key = lambda t: t[1], reverse=True)

#Writing person, emails sent, emails received into the file named A.csv
outputFile = open("A.txt", "a")
outputFile.write("person");
outputFile.write(",");
outputFile.write("sent");
outputFile.write(",");
outputFile.write("received");
outputFile.write("\n");
for key,value in sorted_sent_count:    
    outputFile.write(key);
    outputFile.write(",");
    outputFile.write(str(value));
    outputFile.write(",");
    if key in received_count:
        outputFile.write(str(received_count.get(key)));
    else:
        outputFile.write("0");
    outputFile.write("\n");
for key, value in sorted_received_count:
    if not key in sent_count:
        outputFile.write(key);
        outputFile.write(",");
        outputFile.write("0");
        outputFile.write(",");
        outputFile.write(str(value));
        outputFile.write(",");
        outputFile.write("\n");

# Get the top N person based on no. of emails sent
top_n = 5
counter = 0
while (counter < top_n and counter < len(sorted_sent_count)):
    key = sorted_sent_count[counter][0]
    top_n_sender[key] = 1
    counter += 1

# Analyzing the email count over time for the top 5 person in terms of message sent
sender_count_over_time = {}
year_half = collections.OrderedDict()
year_half = {'f1998':0,'s1998':1,'f1999':2,'s1999':3,'f2000':4,'s2000':5,'f2001':6,'s2001':7,'f2002':8,'s2002':9}
with open('enron-event-history-all.csv', mode="r") as inputfile:
    for line in inputfile:
        items = line.split(",")
        if len(items) == 6:
            timeSend,ID,sender,receiver,topic,mode = items
            if sender in top_n_sender:
                list_of_receiver = receiver.split("|")
                count_over_time = {}
                format_time = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(float(timeSend)/1000.))
                month,day,yearandtime = format_time.split("/")
                year, exact_time = yearandtime.split(" ")
                if int(month) < 6:
                    half_year_count =  str("f") + str(year)
                else:
                    half_year_count =  str("s") + str(year)
                index = year_half.get(half_year_count)
                if sender not in sender_count_over_time:
                    templist = [0,0,0,0,0,0,0,0,0,0]
                    templist[index] = len(list_of_receiver)
                    sender_count_over_time[sender] = templist[:]
                else:   
                    templist[index] = sender_count_over_time[sender][index] + len(list_of_receiver)                    
                    sender_count_over_time[sender] = templist[:]

# Analyzing the received unique email/person name count over time for the 5 person
tracking_unique = {}
unique_received_count_over_time = {}
with open('enron-event-history-all.csv', mode="r") as inputfile:
    for line in inputfile:
        items = line.split(",")
        if len(items) == 6:
            timeSend,ID,sender,receiver,topic,mode = items            
            format_time = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(float(timeSend)/1000.))
            month,day,yearandtime = format_time.split("/")
            year, exact_time = yearandtime.split(" ")
            receiver_count = 0
            list_of_receiver = receiver.split("|")
            if int(month) < 6:
                half_year_count =  str("f") + str(year)
            else:
                half_year_count =  str("s") + str(year)
            index = year_half.get(half_year_count)
            while receiver_count < len(list_of_receiver):
                receiver_name = list_of_receiver[receiver_count]
                if receiver_name in top_n_sender:
                    time_and_sender = str(receiver_name) + str(sender) + str(half_year_count)
                    if time_and_sender not in tracking_unique:
                        tracking_unique[time_and_sender] = 1                     
                        if receiver_name not in unique_received_count_over_time:
                            tempor = [0,0,0,0,0,0,0,0,0,0]
                            tempor[index] = 1
                            unique_received_count_over_time[receiver_name] = tempor
                        else:
                            unique_received_count_over_time[receiver_name][index] += 1
                    else:
                        tracking_unique[time_and_sender] = 1
                receiver_count += 1


# Visualization of second and third requirements which shows the email sent and received over time in separate chart for the top 5 people (max no. of emails sent or received)
# Xaxis - shows the duration half yearly(six months)
x_axis_name = ['May,1998','Dec,1998','May,1999','Dec,1999','May,2000','Dec,2000','May,2001','Dec,2001','May,2002','Dec,2002']

# Get the person name, duration and email count
top_n_person_send = list(sender_count_over_time.keys())
top_n_person_send_count = list(sender_count_over_time.values())
top_n_person_received = list(unique_received_count_over_time.keys())
top_n_person_received_count = list(unique_received_count_over_time.values())

# Plotting the figures
receiving_figure = plt.figure("Unique Email Receiving Count in Six Months interval")
plt.figure(1, figsize = (8.5,11))
receiving_figure.set_size_inches(18.5, 10.5)
axes = plt.gca()
axes.set_xlim([0,11])
axes.set_ylim([0,300])

yticks = np.arange(0, 300, 10)
plt.xticks(range(10), x_axis_name)
plt.yticks(yticks)

plt.plot(range(10), top_n_person_received_count[0], 'b-', label = top_n_person_received[0])
plt.plot(range(10), top_n_person_received_count[1], 'r-', label = top_n_person_received[1])
plt.plot(range(10), top_n_person_received_count[2], 'g-', label = top_n_person_received[2])
plt.plot(range(10), top_n_person_received_count[3], 'y-', label = top_n_person_received[3])
plt.plot(range(10), top_n_person_received_count[4], 'm-', label = top_n_person_received[4])
plt.legend()
plt.xlabel('Duration(Six Months)')
# beautify the x-labels
plt.gcf().autofmt_xdate()
plt.ylabel('Receiving Count')

sending_figure = plt.figure("Sending Email Count For Each Six Months")
sending_figure.set_size_inches(18.5, 10.5)
axes = plt.gca()
axes.set_xlim([0,11])
axes.set_ylim([0,8000])

yticks = np.arange(0, 8000, 1000)
plt.xticks(range(10), x_axis_name)
plt.yticks(yticks)

plt.plot(range(10), top_n_person_send_count[0], 'b-', label = top_n_person_send[0])
plt.plot(range(10), top_n_person_send_count[1], 'r-', label = top_n_person_send[1])
plt.plot(range(10), top_n_person_send_count[2], 'g-', label = top_n_person_send[2])
plt.plot(range(10), top_n_person_send_count[3], 'y-', label = top_n_person_send[3])
plt.plot(range(10), top_n_person_send_count[4], 'm-', label = top_n_person_send[4])
plt.legend()
plt.xlabel('Duration(Six Months)')
plt.gcf().autofmt_xdate()
plt.ylabel('Sending Count')

# Saving the file
receiving_figure.savefig("Unique Email Receiving Count For Each Six Months", dpi=100)
sending_figure.savefig("Sending Email Count For Each Six Months", dpi=100)

