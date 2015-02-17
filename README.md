Wikigps
=======

Applies the GPS coordinates of any wikipedia page to a JPEG image's EXIF data.

Install:

First install the dependencies. On Ubuntu, this is:

$ sudo apt-get install python-pyexiv2 python-pip

Then install via pip:

    : pip install wikigps

Use:

$ wikigps check beijing_airport

Wikipedia page with coordinates found: Beijing International Airport, coordinates

$ wikigps apply beijing_airport -a *.jpg

Applying to IMG_0001.jpg...
Applying to IMG_0002.jpg...


