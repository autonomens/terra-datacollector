import settings
from helpers import overpass

AREA_ID = 3600000000 + 8654

QUERY = f'''
    [maxsize:1073741824];
    area({AREA_ID})->.searchArea;
    way["railway"="rail"](area.searchArea);
    out body;>;out skel qt;
'''

NAMESPACE = 'PACA:sud_foncier_eco'
FILENAME = 'osm_rails.xml'

if __name__ == '__main__':
    overpass.main(settings, QUERY, NAMESPACE, FILENAME)
