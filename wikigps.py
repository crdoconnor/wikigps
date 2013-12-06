#!/usr/bin/python
# coding: utf-8
import sys
import requests
import json
import re
import pyexiv2
import fractions

search = sys.argv[1]
imagefiles = sys.argv[2:]
print "Searching for: '%s'" % search
print "Files to modify: %s" % imagefiles

wikipedia_search_url_prepend = "http://en.wikipedia.org/w/api.php?action=opensearch&search="
wikipedia_search_url_append = "&format=json&callback=spellcheck"
wikipedia_search_url = "%s%s%s" % (wikipedia_search_url_prepend, search, wikipedia_search_url_append)
json_text = requests.get(wikipedia_search_url).text.replace("spellcheck", "").lstrip("(").rstrip(")")
results_array = json.loads(json_text)[1]

i = 0
for item in results_array:
    i = i + 1
    print "%s) %s" % (i, item)

choice_number = int(raw_input("Which page? "))
choice_name = results_array[choice_number - 1]
choice_wikipedia_url = "https://en.wikipedia.org/wiki/%s" % choice_name

wikipedia_html_page = requests.get(choice_wikipedia_url).text
wikipedia_latitude = re.search("\<span class=\"latitude\"\>(.*?)\<\/span\>", wikipedia_html_page).group(1)
wikipedia_longitude = re.search("\<span class=\"longitude\"\>(.*?)\<\/span\>", wikipedia_html_page).group(1)
#regexp = re.compile("(\d+)°(\d+)′(\d+)″(N|E)")
regexp = re.compile("(\d+).(\d+).(\d+).(N|E)")
print wikipedia_latitude 
print wikipedia_longitude 
lat_hour = float(regexp.match(wikipedia_latitude).group(1))
lat_minute = float(regexp.match(wikipedia_latitude).group(2))
lat_second = float(regexp.match(wikipedia_latitude).group(3))

long_hour = float(regexp.match(wikipedia_longitude).group(1))
long_minute = float(regexp.match(wikipedia_longitude).group(2))
long_second = float(regexp.match(wikipedia_longitude).group(3))

for imagefile in imagefiles:
    print "Writing to %s" % imagefile
    metadata = pyexiv2.ImageMetadata(imagefile)
    metadata.read()
    print metadata
    metadata['Exif.GPSInfo.GPSLatitude'] = [fractions.Fraction.from_float(lat_hour).limit_denominator(99999), fractions.Fraction.from_float(lat_minute).limit_denominator(99999),fractions.Fraction.from_float(lat_second).limit_denominator(99999)]
    metadata['Exif.GPSInfo.GPSLatitudeRef'] = "N"
    metadata['Exif.GPSInfo.GPSLongitude'] = [fractions.Fraction.from_float(long_hour).limit_denominator(99999), fractions.Fraction.from_float(long_minute).limit_denominator(99999),fractions.Fraction.from_float(long_second).limit_denominator(99999)]
    metadata['Exif.GPSInfo.GPSLongitudeRef'] = "E"
    #metadata['Exif.GPSInfo.MapDatum']     = 'WGS-84'
    metadata.write()
