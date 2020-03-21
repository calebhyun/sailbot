#! /usr/bin/python
 
from gps import *
import time
    
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
print('latitude\tlongitude\ttime utc\t\t\taltitude\tepv\tept\tspeed\tclimb') # '\t' = TAB to try and output the data in columns.
   
try:
 
 
    while True:
        report = gpsd.next() #
        if report['class'] == 'TPV':
            print("TPV")
            print(getattr(report,'lat',0.0),"\t")
            print(getattr(report,'lon',0.0),"\t")
            print(time.time())
            #print(getattr(report,'time',''),"\t")
            #print(getattr(report,'alt','nan'),"\t\t")
            #print(getattr(report,'epv','nan'),"\t")
            #print(getattr(report,'ept','nan'),"\t")
            #print(getattr(report,'speed','nan'),"\t")
            #print(getattr(report,'climb','nan'),"\t")
        else:
            print("else")
            print(getattr(report,'lat',0.0),"\t")
            print(getattr(report,'lon',0.0),"\t")
            print(time.time())
            
        #time.sleep(.2) 
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print("Done.\nExiting.")
