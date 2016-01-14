Dump1090 FAA Registration Information

This script will output useful FAA registration information given raw (csv) data from dump1090 (https://github.com/antirez/dump1090).

This script takes the ICAO number from the raw dump1090 output and looks up registration information from a local copy of the FAA Registration database.

Before use you will need to download and import the FAA aircraft registration data from  http://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download/. Unzip the file and point the --import option at the directory.

Then use the --follow option and pipe raw dump1090 data into stdin.

Sample output:
`Manufacturer                   Model                Owner                                    ICAO       N Number   Serial
CESSNA                         560                  M AIRE LLC                               A68***     5****      5****
BOEING                         737-3H4              SOUTHWEST AIRLINES CO                    A3E***     3****      2****
BOMBARDIER INC                 CL-600-2C10          EXPRESSJET AIRLINES INC                  AA0***     7****      1****
BOEING                         737-8H4              SOUTHWEST AIRLINES CO                    AB5***     8****      3****
BOEING                         767-316F             CHIRIHUE LEASING TRUST                   A90***     6****      3****
`

Usage:
dump1090-faareg.py
 --import <FAA data dir>
      provide path to unzipped FAA registry data
      dir will contain MASTER.txt and ACFTREG.txt files
      zip can be found here: http://www.faa.gov/licenses_certificates/aircraft_certification/aircraft_registry/releasable_aircraft_download/
 --follow
      pipe in raw (csv) data from dump1090 raw
