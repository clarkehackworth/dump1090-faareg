#!/usr/bin/python

import sqlite3 as lite
import sys
import getopt
import os

options, remainder = getopt.getopt(sys.argv[1:], 'h:i:f',[ 'help', 
                                                         'import=',
                                                         'follow',
                                                         ])

faa_data_dir = ''
follow=False

for opt, arg in options:
    if opt in ('-i', '--import'):
        faa_data_dir = arg
    elif opt in ('-f', '--follow'):
        follow = True
    elif opt in ('-h', '--help'):
       print """ --import <FAA data dir>
      provide path to unzipped FAA registry data
      dir will contain MASTER.txt and ACFTREG.txt files
      zip can be found here: http://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download/
 --follow 
      pipe in raw (csv) data from dump1090 raw"""
       exit(0)

def main():
   if faa_data_dir != '':
      importfromfile(faa_data_dir)
      exit(0)
   if follow:
      follow()

def follow():
   try:
      con = lite.connect('aircraft.db')
      with con:
         icaoList = []
         line = ''

         print '{:30s} {:20s} {:40s} {:10s} {:10s} {:10s}'.format('Manufacturer','Model','Owner','ICAO','N Number','Serial')
         while line != "q":
            line = sys.stdin.readline()
            linearray = line.split(',')            
            if len(linearray) >= 3:
               icao = linearray[4]

               try:
                  icaoIndex = icaoList.index(icao)
               except ValueError:
                  icaoIndex = -1
               if icaoIndex < 0:
                  cur = con.cursor()
         
                  cur.execute("select * from master where modeSCodeHex='"+icao+"'")
                  masterData = cur.fetchone()
                  
                  if masterData is not None:
                     cur.execute("select * from acftref where code='"+masterData[2]+"'")
                     planeData = cur.fetchone()

                     if planeData is None:
                        #print "Could not find plane with code "+masterData[2]

                        planeData = ['Unknown','Unknown','']
  
                  else: 
                     masterData = ['','','','','','','Unknown']
                     planeData = ['Unknown','Unknown','']


                  print '{:30s} {:20s} {:40s} {:10s} {:10s} {:10s}'.format(planeData[1],planeData[2],masterData[6],icao,masterData[0],masterData[1])

                  if len(icaoList) > 25:
                     icaoList.pop()
               else:
                  if icaoIndex != 0:
                     icaoList.pop(icaoIndex)
               if icaoIndex != 0:
                  icaoList.insert(0,icao) 
               
   except lite.Error, e:
      print "Error %s:" % e.args[0]
      print "Have you used --import to import the FAA database?"
      sys.exit(1)
   finally:
         if con:
            con.close()

def importfromfile(faa_dir):
   if faa_dir != '':


      con = lite.connect('aircraft.db')
      try:
         with con:
    
            with open(faa_dir+os.sep+"MASTER.txt") as f:
               content = f.readlines()
            cur = con.cursor()    


            cur.execute("DROP TABLE IF EXISTS master;" )
            cur.execute("CREATE TABLE master(nNumber TEXT ,serial TEXT, modelCode TEXT , engModel TEXT, yearMade TEXT, regType TEXT, name TEXT,street1 TEXT,street2 TEXT,city TEXT,state TEXT,zip TEXT,region TEXT,county TEXT,country TEXT, lastActionDate TEXT,certIssueDate TEXT,cert TEXT,aircraftType TEXT,engineType TEXT,statusCode TEXT,modeSCode TEXT,owner TEXT,airWorthDate TEXT,otherNames1 TEXT,otherNames2 TEXT,otherNames3 TEXT,otherNames4 TEXT,otherNames5 TEXT,expDate TEXT,ID INT,kitMfr TEXT, kitModelMfr TEXT,modeSCodeHex TEXT)" )

            count = 0
            for line in content:
               data = line.split(',')
               if count>0:
                  sys.stdout.write('.')
                  cur.execute("INSERT INTO master VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (data[0].strip(),data[1].strip(),data[2].strip(),data[3].strip(),data[4].strip(),data[5].strip(),data[6].strip(),data[7].strip(),data[8].strip(),data[9].strip(),data[10].strip(),data[11].strip(),data[12].strip(),data[13].strip(),data[14].strip(),data[15].strip(),data[16].strip(),data[17].strip(),data[18].strip(),data[19].strip(),data[20].strip(),data[21].strip(),data[22].strip(),data[23].strip(),data[24].strip(),data[25].strip(),data[26].strip(),data[27].strip(),data[28].strip(),data[29].strip(),int(data[30]),data[31].strip(),data[32].strip(),data[33].strip()))
               count=count+1


            with open(faa_dir+os.sep+"ACFTREF.txt") as f:
               content = f.readlines() 
            

            cur.execute("DROP TABLE IF EXISTS acftref;" )
            cur.execute("CREATE TABLE acftref(code TEXT, mfr TEXT , model TEXT,  type TEXT, typeEng TEXT , accat TEXT , buildCert TEXT, engNo TEXT , numSeats TEXT, weight TEXT , speed TEXT)")
            
            count = 0
            for line in content:
               data = line.split(',')
               if count>0:
                  sys.stdout.write('.')
                  cur.execute("INSERT INTO acftref VALUES(?,?,?,?,?,?,?,?,?,?,?)", (data[0].strip(),data[1].strip(),data[2].strip(),data[3].strip(),data[4].strip(),data[5].strip(),data[6].strip(),data[7].strip(),data[8].strip(),data[9].strip(),data[10].strip()))
               count=count+1
      except lite.Error, e:
         print "Error %s:" % e.args[0]
         sys.exit(1)
      finally:
         if con:
            con.close() 


main()

