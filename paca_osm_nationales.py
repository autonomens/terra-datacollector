import settings as pyfile_settings
from helpers import overpass

AREA_ID = 3600000000 + 8654

QUERY = f'''
    [maxsize:1073741824];
    area({AREA_ID})->.searchArea;
    (
        way["highway"="trunk"](area.searchArea);
        way["highway"="primary"](area.searchArea);
    );
    out body;>;out skel qt;
'''

NAMESPACE = 'PACA:sud_foncier_eco'
FILENAME = 'osm_nationales.xml'

if __name__ == '__main__':
    overpass.main(pyfile_settings, QUERY, NAMESPACE, FILENAME)
