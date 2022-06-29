#!/usr/bin/env python
""" s5phub_get_tropomi_data.py

This script takes:
- Date range
- coordinate data_range
- Product details

and downloads:
- corresponding TROPOMI data from s5phub
"""
##############################
### Christoph Riess ##########
### WUR, June 2022 ###########
### christoph.riess@wur.nl ###
##############################
import os, glob
from calendar import monthrange
import subprocess
import re

### USER INPUT ###

### give year and month
years = ['2021'] #year of data
months = ['06','07','08','09'] # month of data as 2-digits

### give corner coordinates of rectangle of interest
latl,lath = 50.,60.
lonl, lonh = 1.,10.

### give product detail
producttype = 'L2__NO2___'
processingmode = 'Offline'

path = './' # parent dir for saving data


### don't change below ###
polygon = "POLYGON(({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))".format(lonl,latl,lonh,lath) # this is rectangle, could be generalized to polygon
devnull = open(os.devnull, 'w')

### query loop
for year in years:
    for month in months:
        days = monthrange(int(year),int(month))[1]
        for i in range(1,days+1):
            day = str(i).zfill(2) # day as 2-digit

            ### get data as tar file from web
            print('Query data of day: '+day)
            query_str = """wget --no-check-certificate --user=s5pguest --password=s5pguest --output-document=./s5phubqueries/query_results_{0}_{1}_{2}.txt 'https://s5phub.copernicus.eu/dhus/search?q=generationdate:[{0}-{1}-{2}T00:00:00.000Z TO {0}-{1}-{2}T23:59:00.000Z] AND  producttype:{3} AND processingmode:{4} AND footprint:"Contains({5})"&rows=100&start=0&format=json'""".format(year,month,day,producttype,processingmode,polygon)
            subprocess.call(query_str, shell=True, stdout= devnull, stderr=devnull)
### download data loop
for year in years:
    for month in months:
        data_path = path+year+'/'+'mumm'+'/'

        days = monthrange(int(year),int(month))[1]
        for i in range(1,days+1):
            day = str(i).zfill(2) # day as 2-digit
            query_file = './s5phubqueries/query_results_{0}_{1}_{2}.txt'.format(year,month,day)

            ### find uuid in query output file
            with open(query_file) as f:
                contents = f.read()
                # print(contents)
                pattern = '"name":"uuid","content":"(.*?)"'
                finds = re.findall(str(pattern), contents, flags=0)

            for uuid in finds:
                ### get data from web
                print('Download data of day: '+day)
                download_data_str = """wget --no-check-certificate --content-disposition --continue --user=s5pguest --password=s5pguest "https://s5phub.copernicus.eu/dhus/odata/v1/Products('{0}')/\$value" -P {1}""".format(uuid,data_path)
                subprocess.call(download_data_str, shell=True, stdout= devnull, stderr=devnull)
