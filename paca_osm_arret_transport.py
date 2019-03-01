import settings as pyfile_settings
from helpers import overpass

AREA_ID = 3600000000 + 8654

QUERY = f'''
    [out:csv(::id,::lat,::lon,name,highway,amenity,railway)];
    area({AREA_ID})->.searchArea;
    (
        nwr[highway=bus_stop](area.searchArea);
        nwr[amenity=bus_station](area.searchArea);
        nwr[amenity=ferry_terminal](area.searchArea);
        nwr[amenity=taxi](area.searchArea);
        nwr[railway=halt](area.searchArea);
        nwr[railway=station][station=subway](area.searchArea);
        nwr[railway=station][subway=yes](area.searchArea);
        nwr[railway=tram_stop](area.searchArea);
    );
    out center;
'''

NAMESPACE = 'PACA:sud_foncier_eco'
FILENAME = 'osm_arret_transport.csv'

if __name__ == '__main__':
    overpass.main(pyfile_settings, QUERY, NAMESPACE, FILENAME)
