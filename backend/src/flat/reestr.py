import logging
from src.flat.models import MacroRegion, Region
from urllib.parse import urlencode, quote_plus

import requests


logger = logging.getLogger(__name__)

STREET_TYPES = {
    'улица': 'str1',
    'переулок': 'str2',
    'проспект': 'str3',
    'площадь': 'str4',
    'микрорайон': 'str5',
    'аллея': 'str6',
    'бульвар': 'str7',
    'аал': 'str8',
    'аул': 'str9',
    'въезд': 'str10',
    'выселки': 'str11',
    'городок': 'str12',
    'деревня': 'str13',
    'дорога': 'str14',
    'ж/д остановочный (обгонный) пункт': 'str15',
    'железнодорожная будка': 'str16',
    'железнодорожная казарма': 'str17',
    'железнодорожная платформа': 'str18',
    'железнодорожная станция': 'str19',
    'железнодорожный пост': 'str20',
    'железнодорожный разъезд': 'str21',
    'животноводческая точка': 'str22',
    'заезд': 'str23',
    'казарма': 'str24',
    'квартал': 'str25',
    'километр': 'str26',
    'кольцо': 'str27',
    'линия': 'str28',
    'местечко': 'str29',
    'набережная': 'str30',
    'населенный пункт': 'str31',
    'остров': 'str32',
    'парк': 'str33',
    'переезд': 'str34',
    'планировочный район': 'str35',
    'платформа': 'str36',
    'площадка': 'str37',
    'полустанок': 'str38',
    'поселок/станция': 'str39',
    'поселок сельского типа': 'str40',
    'починок': 'str41',
    'почтовое отделение': 'str42',
    'проезд': 'str43',
    'просек': 'str44',
    'проселок': 'str45',
    'проулок': 'str46',
    'разъезд': 'str47',
    'сад': 'str48',
    'село': 'str49',
    'сквер': 'str50',
    'слобода': 'str51',
    'станция': 'str52',
    'строение': 'str53',
    'территория': 'str54',
    'тракт': 'str55',
    'тупик': 'str56',
    'участок': 'str57',
    'хутор': 'str58',
    'шоссе': 'str59'
}


def _strip_cadastral_id(cadastral_id):
    stripped_cadastral_id = []
    cadastral_id = cadastral_id.split(':')
    for part in cadastral_id:
        if part:
            stripped_cadastral_id.append(part[:-1].lstrip('0') + part[-1])
    return ':'.join(stripped_cadastral_id)

class AddressWrapper:
    def __init__(self, macro_region_name, street, street_type, house, apartment, building=None, structure=None, region_name=None):
        self.street = street
        self.street_type = STREET_TYPES[street_type.lower()]
        self.house = house
        self.apartment = apartment
        self.building = building
        self.structure = structure
        macro_region = MacroRegion.objects.filter(name=macro_region_name).first()
        self.macro_region_id = macro_region.code if macro_region else None
        self.macro_region_name = macro_region_name
        if region_name:
            region = Region.objects.filter(name=region_name).first()
            self.region_id = region.code if region else None
            self.region_name = region_name


class RosreestrAPIClient:

    BASE_URL = 'http://rosreestr.ru/api/online'
    MACRO_REGIONS_URL = f'{BASE_URL}/macro_regions/'
    REGIONS_URL = f'{BASE_URL}/regions/' + '{}/'
    SEARCH_OBJECTS_BY_ADDRESS_URL = f'{BASE_URL}/address/fir_objects/'
    SEARCH_DETAILED_OBJECT_BY_ID = f'{BASE_URL}/fir_object/' + '{}/'

    REPUBLIC = 'республика'

    def _get_response_body(self, response: requests.Response):
        status_code = response.status_code
        if status_code >= 400:
            response.raise_for_status()
        elif status_code == 204:
            logger.info('There was an empty response body')
            return ''
        else:
            return response.json()

    def _get_macro_region_id(self, macro_region_name: str):
        macro_regions = requests.get(self.MACRO_REGIONS_URL).json()
        MacroRegion.objects.bulk_create(
            [
                MacroRegion(
                    name=mr['name'],
                    code=mr['id'],
                )
                for mr in macro_regions
            ],
            ignore_conflicts=True,
        )
        for macro_region in macro_regions:
            if macro_region['name'].lower() == macro_region_name.lower():
                return macro_region['id']
        raise ValueError(
            f'There was not found suitable macro region '
            f'for macro region name - `{macro_region_name}`')

    def _get_region_id(self, region_name: str, macro_region_id: int) -> int:
        regions = requests.get(self.REGIONS_URL.format(macro_region_id)).json()
        macro_region = MacroRegion.objects.get(code=macro_region_id)
        Region.objects.bulk_create(
            [
                Region(
                    name=r['name'],
                    code=r['id'],
                    macro_region=macro_region,
                )
                for r in regions
            ],
            ignore_conflicts=True,
        )
        for region in regions:
            if region['name'].lower() == region_name.lower():
                return region['id']
        raise ValueError(
            f'There was not found suitable region_id for '
            f'region name - `{region_name}` and macro region '
            f'name - `{macro_region_id}`')


    def _get_objects_by_address(self, address_wrapper: AddressWrapper):
        macro_region_id = address_wrapper.macro_region_id
        if not address_wrapper.macro_region_id:
            macro_region_id = self._get_macro_region_id(address_wrapper.macro_region_name.lower())

        region_id = None
        if hasattr(address_wrapper, 'region_id'):
            region_id = address_wrapper.region_id or self._get_region_id(
                address_wrapper.region_name, macro_region_id)

        search_query = {
            'macroRegionId': macro_region_id,
            'street': address_wrapper.street,
            'streetType': address_wrapper.street_type,
            'house': address_wrapper.house,
            'apartment': address_wrapper.apartment,
        }

        if region_id:
            search_query['regionId'] = region_id
        if address_wrapper.building:
            search_query['building'] = address_wrapper.building
        if address_wrapper.structure:
            search_query['structure'] = address_wrapper.structure
        

        print(f'search_objects_query: {search_query}')
        logger.info('Trying to download rosreestr objects')
        response = requests.get(self.SEARCH_OBJECTS_BY_ADDRESS_URL, params=search_query)

        objects = self._get_response_body(response)
        if objects:
            logger.info('Rosreestr objects were downloaded')
            logger.info(f'Number of rosreestr objects: {len(objects)}')
            return objects
        else:
            return []

    def _get_object(self, obj_id: str):
        obj_id = _strip_cadastral_id(obj_id)
        url = self.SEARCH_DETAILED_OBJECT_BY_ID.format(obj_id)
        logger.info(f'Trying to download detailed object, object_id: {obj_id}')
        response = requests.get(url)
        logger.info(f'Detailed object was downloaded, object_id: {obj_id}')
        data = self._get_response_body(response)
        if obj_id.find(':') == -1:
            premises_cn = data.get('premisesData', {}).get('premisesCn')
            print(premises_cn)
            if premises_cn:
                premises_cn = _strip_cadastral_id(premises_cn)
                try:
                    data['parcelData'] = requests.get(self.SEARCH_DETAILED_OBJECT_BY_ID.format(premises_cn)).json().get('parcelData')
                except Exception as e:
                    print(e)
        return data

    def get_flat_by_address(self, address_wrapper: AddressWrapper):
        flats = self._get_objects_by_address(address_wrapper)
        flat_id = flats[0]['objectId']
        if flat_id.find(':') != -1 and len(flats) > 1 and flats[1]['objectId'].find('_') != -1:
            flat_id = flats[1]['objectId']
        return self._get_object(flat_id)
