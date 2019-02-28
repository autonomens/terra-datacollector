import settings
from helpers import ckan3


CKAN_PORTAL = 'https://trouver.datasud.fr'
DATASET_ID = 'lignes-expresses-regionales-et-chemins-de-fer-de-provence-points-darrets-et-horaires-des-lignes'
RESSOURCE = 'TRANSPORT_RegionSUD_LER_CP.GTFS.zip'

NAMESPACE = 'FR:datasud'
FILENAME = RESSOURCE

if __name__ == '__main__':
    ckan3.main(settings, CKAN_PORTAL, DATASET_ID, RESSOURCE, NAMESPACE, FILENAME)
