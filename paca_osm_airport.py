import settings
from helpers import overpass

AREA_ID = 3600000000 + 8654

QUERY = f'''
    [out:csv(::id,::lat,::lon,name)];
    area({AREA_ID})->.searchArea;
    nwr["aeroway"="aerodrome"]["iata"](area.searchArea);
    out center;
'''

NAMESPACE = 'FR:PACA'
FILENAME = 'osm_airport.csv'

if __name__ == '__main__':
    overpass.main(settings, QUERY, NAMESPACE, FILENAME)
