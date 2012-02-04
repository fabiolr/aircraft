# -*- coding: utf-8 -*-

from aircraft.flight.models import Airport
import urllib2, csv

#resp = urllib2.urlopen('http://www.ourairports.com/data/airports.csv')
resp = open('/tmp/airports.csv')

titles = resp.readline()

i = 0
for row in csv.reader(resp):
    remote_id = int(row[0])
    icao = row[1]
    atype = row[2]
    #name = row[3]
    latitude = float(row[4])
    longitude = float(row[5])
    elevation = int(row[6]) if len(row[6]) else None

    """
    try:
        unicode(name)
    except UnicodeDecodeError:
        continue
    """

    try:
        airport = Airport.objects.get(icao=icao)
        airport.atype = atype
        #airport.name = name
        airport.latitude = latitude
        airport.longitude = longitude
        airport.elevation = elevation
        airport.save()
    except Airport.DoesNotExist:
        Airport.objects.create(remote_id=remote_id,
                               icao=icao,
                               atype=atype,
                               #name=name,
                               latitude=latitude,
                               longitude=longitude,
                               elevation=elevation,
                               )
