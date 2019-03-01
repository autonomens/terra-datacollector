import settings as pyfile_settings
from helpers import overpass

AREA_ID = 3600000000 + 8654

QUERY = f'''
    area({AREA_ID})->.searchArea;
    relation["type"="route"]["route"="bus"](area.searchArea);
    (._;>>;);
    out;
'''

NAMESPACE = 'PACA:sud_foncier_eco'
FILENAME = 'osm_routes_bus.xml'

if __name__ == '__main__':
    overpass.main(pyfile_settings, QUERY, NAMESPACE, FILENAME)
