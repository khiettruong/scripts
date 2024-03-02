# Date: Mar 2024
# Author: Khiet Truong
# Converts a csv file to TextGrid, will also fill in non-consecutive timestamps
# Expects csv file with ";" as separator
# starttime;endtime;text
# Usage: python3 bin/csv2tg.py in.csv out.TextGrid

from natsort import natsorted # pip install natsort
import os
import sys
import csv

csvFile = str(sys.argv[1])
TgFile = str(sys.argv[2])

#filename1 = os.path.splitext(csvFile)[0]

csvIn = open(csvFile, encoding='utf-8', mode='r')
TgOut = open(TgFile, encoding='utf-8', mode='w')


reader = csv.reader(csvIn,delimiter=";") # read data from csv file
data = list(reader) # read into python list format
label_count = len(data) # total numer of rows in csv file
end_time = data[-1][1]

filled_data=data
j=0

if data[0][0] != 0:
    filled_data.append(['0',data[0][0],'0'])


while j<(label_count-1):
    if (data[j+1][0] != data[j][1]):
        filled_data.append([data[j][1],data[j+1][0],'0'])
    j=j+1


label_count2=len(filled_data)
filled_data_sorted=natsorted(filled_data)
for k in range(label_count2):
    print(filled_data_sorted[k])

TgOut.write('File type = "ooTextFile"\n')
TgOut.write('Object class = "TextGrid"\n')
TgOut.write('xmin = 0\n')
TgOut.write('xmax = '+str(end_time)+'\n')
TgOut.write('tiers? <exists>\n')
TgOut.write('size = 1\n')
TgOut.write('item []:\n') 
TgOut.write('\titem [1]:\n')
TgOut.write('\t\tclass = "IntervalTier"\n') 
TgOut.write('\t\tname = "Labels"\n')
TgOut.write('\t\txmin = 0\n') 
TgOut.write('\t\txmax = '+str(end_time)+'\n') 
TgOut.write('\t\tintervals: size = '+str(label_count2)+'\n');

for j in range(label_count2):
    TgOut.write('\t\tintervals ['+str(j)+']:\n')
    TgOut.write('\t\t\txmin = '+str(filled_data_sorted[j][0])+'\n') 
    TgOut.write('\t\t\txmax = '+str(filled_data_sorted[j][1])+'\n') 
    TgOut.write('\t\t\ttext = "'+str(filled_data_sorted[j][2])+'"\n')


csvIn.close()
TgOut.close()

