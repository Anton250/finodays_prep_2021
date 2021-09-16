import pandas as pd
import requests
from bs4 import BeautifulSoup


def fill_db():
    from src.car.models import Brand, Generation, Model, Modification
    df = pd.read_csv('cars_to_load.csv')

    marks = df['brand'].unique()

    data = {}

    for mark in marks:
        data[mark] = {
            'mark': Brand.objects.create(name=mark),
            'models': {}
        }

    models = df[['brand', 'model', 'body_type', 'doors_count']].drop_duplicates()

    for _, r in models.iterrows():
        data[r.brand]['models'][r.model + r.body_type] = {
            'model': Model.objects.create(
                name=r.model,
                brand=data[r.brand]['mark'],
                body_type=r.body_type,
                doors_count=r.doors_count,
            ),
            'gens': {}
        }

    gens = df[['brand', 'model', 'body_type', 'doors_count', 'generation_to_show']].drop_duplicates()

    for _, r in gens.iterrows():
        data[r.brand]['models'][r.model + r.body_type]['gens'][r.generation_to_show] = Generation.objects.create(
            name=r.generation_to_show,
            model=data[r.brand]['models'][r.model + r.body_type]['model'],
        )
    TRANSMISSIONS = {'автоматическая': 'AT', 'механическая': 'MT', 'вариатор': 'CVT', 'роботизированная': 'DCT'}
    DRIVES = {'передний': 'FWD', 'задний': 'RWD', 'полный': 'AWD'}
    Modification.objects.bulk_create(
        [
            Modification(
                name=f'{r.engine_volume}{TRANSMISSIONS[r.transmission]} ({int(r.engine_power)} л.с.) {r.fuel_type} {DRIVES[r.drive]}',
                generation=data[r.brand]['models'][r.model + r.body_type]['gens'][r.generation_to_show],
                engine_power=r.engine_power,
                engine_volume=r.engine_volume,
                fuel_type=r.fuel_type,
                transmission=r.transmission,
                drive=r.drive,
                cylinders_count=r.cylinders_count,
                wheel=r.wheel,
                height=r.height,
                length=r.length,
                width=r.width,
                wheel_base=r.wheel_base,
                catalog_link=r.catalog_link,
            )
            for _, r in df.iterrows()
        ]
    )

def get_eco_class(url: str):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'
    }
    if not url.endswith('/'):
        url = url + '/'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    result = ""
    for spec in soup.find_all('dd'):
        if isinstance(spec.contents[0], str) and spec.contents[0][:5] == "Euro ":
            result = spec.contents[0]

    return result
