import requests
import argparse
from typing import Optional, List


class Brewery:
    def __init__(
            self,
            id: str,
            name: str,
            brewery_type: str,
            city: str,
            state_province: Optional[str],
            postal_code: str,
            country: str,
            website_url: Optional[str],
            phone: Optional[str]
    ):
        self.id = id
        self.name = name
        self.brewery_type = brewery_type
        self.city = city
        self.state_province = state_province
        self.postal_code = postal_code
        self.country = country
        self.website_url = website_url
        self.phone = phone

    def __str__(self) -> str:
        state = self.state_province if self.state_province else "Brak danych"
        return (f" Browar: {self.name} ({self.city}, {state}) - Typ: "
                f"{self.brewery_type}")


def pobierz_browary(city: Optional[str] = None):
    url = "https://api.openbrewerydb.org/v1/breweries"
    params = {"per_page": 20}

    if city:
        params["by_city"] = city.replace(" ", "_")

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            dane_json = response.json()
            lista_browarow: List[Brewery] = []

            for item in dane_json:
                nowy_browar = Brewery(
                    id=item.get('id'),
                    name=item.get('name'),
                    brewery_type=item.get('brewery_type'),
                    city=item.get('city'),
                    state_province=item.get('state_province'),
                    postal_code=item.get('postal_code'),
                    country=item.get('country'),
                    website_url=item.get('website_url'),
                    phone=item.get('phone')
                )
                lista_browarow.append(nowy_browar)

            return lista_browarow
        else:
            print(f"Błąd połączenia: {response.status_code}")
            return []

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pobieranie informacji o "
                                                 "browarach.")
    parser.add_argument("--city", type=str,
                        help="Miasto, z którego chcesz pobrać browary",
                        required=False)
    args = parser.parse_args()

    browary = pobierz_browary(city=args.city)

    if args.city:
        print(f"\n Szukam browarów w mieście: {args.city}")

    print(f" Pobrano {len(browary)} browarów. Oto one:\n")

    if not browary:
        print("Nie znaleziono browarów dla podanych kryteriów.")
    else:
        for browar in browary:
            print(browar)
