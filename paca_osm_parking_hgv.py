import settings
from helpers import overpass

AREA_ID = 3600000000 + 8654

QUERY = f'''
    [out:csv(::id,::lat,::lon)];
    area({AREA_ID})->.searchArea;
    nwr[amenity=parking][hgv=yes](area.searchArea);
    out center;
'''

NAMESPACE = 'PACA:sud_foncier_eco'
FILENAME = 'osm_parking_hgv.csv'

if __name__ == '__main__':
    overpass.main(settings, QUERY, NAMESPACE, FILENAME)
