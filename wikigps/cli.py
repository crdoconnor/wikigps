"""Command line interface to saddle."""
# coding: utf-8
import os
import sys
import requests
import json
import re
import fractions
from clip import App, ClipExit, arg, opt, echo

app = App()

def get_coordinates(page):
    """Request a wikipedia page from its name and parse and get back the coordinates in a tuple."""
    choice_wikipedia_url = u"https://en.wikipedia.org/wiki/{0}".format(page)
    wikipedia_html_page = requests.get(choice_wikipedia_url).text

    # Not a page with coordinates
    if re.search(u"""\<span class=\"latitude\"\>(.*?)\<\/span\>""", wikipedia_html_page) is None:
        return None

    try:
        lat_str = re.search(u"\<span class=\"latitude\"\>(.*?)\<\/span\>", wikipedia_html_page).group(1)
        long_str = re.search(u"\<span class=\"longitude\"\>(.*?)\<\/span\>", wikipedia_html_page).group(1)
        regexp = re.compile(u"(\d+).(\d+).(\d+).(N|E|S|W)")

        if regexp.match(lat_str) is not None and regexp.match(long_str):
            lat_tuple = (float(regexp.match(lat_str).group(1)),
                         float(regexp.match(lat_str).group(2)),
                         float(regexp.match(lat_str).group(3)),)
            long_tuple = (float(regexp.match(long_str).group(1)),
                          float(regexp.match(long_str).group(2)),
                          float(regexp.match(long_str).group(3)),)

        regexp = re.compile(u"(\d+).(\d+).(N|E|S|W)")

        if regexp.match(lat_str) is not None  and regexp.match(long_str):
            lat_tuple = (float(regexp.match(lat_str).group(1)),
                         float(regexp.match(lat_str).group(2)),
                         30.0,)
            long_tuple = (float(regexp.match(long_str).group(1)),
                          float(regexp.match(long_str).group(2)),
                          30.0,)

    except ValueError, AttributeError:
        sys.stderr.write(u"Problem parsing page {0}. Please report to colm.oconnor.github@gmail.com!".format(page))
        sys.exit(1)

    return (lat_tuple, long_tuple)

def search_wikipedia(keyword):
    """Do a spell checked search on wikipedia and get back coordinates of the only page that matched that had coordinates (or None)."""
    sys.stdout.write(u"SEARCHING: '{0}'...\n".format(keyword))
    search_url = "http://en.wikipedia.org/w/api.php?action=opensearch&search={0}&format=json&callback=spellcheck".format(keyword)
    json_text = requests.get(search_url).text.replace("/**/spellcheck(", "").rstrip(")")
    matching_pages = json.loads(json_text)[1]

    matching_page_count = 0
    matching_coordinates = None

    for page in matching_pages:
        coordinates = get_coordinates(page)
        sys.stdout.write(u"\nFOUND: {0} ".format(page))
        if coordinates is not None:
            matching_coordinates = coordinates
            matching_page_count = matching_page_count + 1
            sys.stdout.write(u"at {0}".format(coordinates))
    return coordinates if matching_page_count == 1 else None

@app.main(description='Wikipedia EXIF data tagger.')
@arg('keyword', required=True, help='Enter key word (with underscores instead of spaces) to match page - e.g. inle_lake.')
@opt('-f', '--files', nargs=-1, default=None, name='imagefiles', help='Files to apply the GPS coordinates to the EXIF tag.')
def wikigps(keyword, filenames):
    """CLI interface."""
    try:
        import pyexiv2
    except ImportError:
        sys.stderr.write("ERROR: Could not import pyexiv2. Try running sudo apt-get install python-pyexiv2 or equivalent.\n")

    coordinates = search_wikipedia(keyword)

    if coordinates is None and len(imagefiles) > 0:
        sys.stderr.write("\nERROR: Too many matching pages with coordinates. Refine your search until there is just one page with matching coordinates.\n")
        sys.exit(1)

    for imagefile in imagefiles:
        sys.stdout.write("\nWRITING: {0}".format(imagefile)
        import pyexiv2
        metadata = pyexiv2.ImageMetadata(imagefile)
        metadata.read()
        sys.stdout.write("\nMETADATA: {0}".format(metadata))

        gps_lat = [fractions.Fraction.from_float(coordinates[0][0]).limit_denominator(99999),
                   fractions.Fraction.from_float(coordinates[0][1]).limit_denominator(99999),
                   fractions.Fraction.from_float(coordinates[0][2]).limit_denominator(99999),]

        gps_long = [fractions.Fraction.from_float(coordinates[1][0]).limit_denominator(99999),
                   fractions.Fraction.from_float(coordinates[1][1]).limit_denominator(99999),
                   fractions.Fraction.from_float(coordinates[1][2]).limit_denominator(99999),]

        metadata['Exif.GPSInfo.GPSLatitude'] = gps_lat
        metadata['Exif.GPSInfo.GPSLatitudeRef'] = "N"
        metadata['Exif.GPSInfo.GPSLongitude'] = gps_long
        metadata['Exif.GPSInfo.GPSLongitudeRef'] = "E"
        metadata.write()

def run():
    try:
        app.run()
    except ClipExit:
        pass

if __name__ == "__main__":
    run()
