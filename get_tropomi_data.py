#!/usr/bin/env python
import os, glob
from calendar import monthrange
import subprocess

###############
# code to download tropomi NO2 data from temis
# I run this on a linux environement
# Author: Christoph Riess, November 2020, WUR
###############

path = '/path/to/your/dir/' # parent dir for data

year = '2020' #year of data
month = '07' # month of data as 2-digit
data_path = path+'data/'+'tropomi/'+year+'/'+month+'/'

# # loop over all days in month
days = monthrange(int(year),int(month))[1]
for i in range(1,days+1):
    day = str(i).zfill(2) # day as 2-digit

    #get data as tar file from web
    print('Download data of day: '+day)
    get_data_str = 'wget -A .tar -P '+path+' --cut-dirs=2 -r -l1 -nH -N -a "logfile" http://d1qb6yzwaaq4he.cloudfront.net/tropomi/no2/'+year+'/'+month+'/tropomi_no2_'+year+month+day+'.tar'
    subprocess.call(get_data_str, shell=True)
    # un-tar file
    print('Un-tar data of day: '+day)
    untar_str = 'tar -xvf '+data_path+'tropomi_no2_'+year+month+day+'.tar -C '+data_path
    subprocess.call(untar_str, shell=True)
    #remove tar file
    print('Remove leftover files for day: '+day)
    subprocess.call('rm '+data_path+'tropomi_no2_'+year+month+day+'.tar',shell=True)
    #remove all files withdata outside region, defined by crossing time
    # for j in ['00','01','02','03','04','05','06','15','16','17','18','19','20','21','22','23']:
    #     files_to_delete = sorted(glob.glob(data_path+'*'+'_NO2____'+year+month+day+'T'+j+'*'))
    #     for file in files_to_delete:
    #         subprocess.call('rm '+file,shell=True)

#create filelist file
filelist = sorted(glob.glob(data_path+'S5P_'+'*'))
i=0
text = ''
while i<len(filelist) :
    text += filelist[i][len(data_path):] + '\n'
    i+=1
print(text)
file1 = open(data_path+"filelist","w")
file1.write(text)
file1.close()
