import settings as pyfile_settings
from helpers import overpass

AREA_ID = 3600000000 + 8654

QUERY = f'''
    [out:csv(::id,::lat,::lon)];
    area({AREA_ID})->.searchArea;
    nwr[amenity=bank](area.searchArea);
    out center;
'''

NAMESPACE = 'PACA:sud_foncier_eco'
FILENAME = 'osm_bank.csv'

if __name__ == '__main__':
    overpass.main(pyfile_settings, QUERY, NAMESPACE, FILENAME)
