import sys
import requests
import csv
from bs4 import BeautifulSoup

def nacti_url(url: str):
    odpoved = requests.get(url)

    if odpoved.ok:
        return BeautifulSoup(odpoved.text, features="html.parser")
    else:
        return None


def ziskej_seznam_obci(soup: BeautifulSoup) -> list[dict]:
    """Vyhledá na stránce všechny obce a vrátí jejich kódy, názvy a odkazy."""
    seznam_obci = []

    vsechny_kody = soup.find_all("td", class_="cislo")

    for bunka_kod in vsechny_kody:
        kod = bunka_kod.text
        odkaz_tag = bunka_kod.find("a")
        relativni_url = odkaz_tag["href"]
        plna_url = f"https://volby.gov.cz/pls/ps2017nss/{relativni_url}"
        bunka_nazev = bunka_kod.find_next_sibling("td", class_="overflow_name")
        nazev = bunka_nazev.text

        # Uložíme data o obci do slovníku a přidáme do seznamu
        obec_data = {
            "kod": kod,
            "nazev": nazev,
            "url_ob": plna_url
        }
        seznam_obci.append(obec_data)

    return seznam_obci


def zpracuj_detail_obce(soup_detail: BeautifulSoup) -> dict:
    """Vytáhne z detailu obce počty voličů, obálek, hlasů a výsledky stran."""
    volici = soup_detail.find("td", headers="sa2").text
    obalky = soup_detail.find("td", headers="sa3").text
    hlasy = soup_detail.find("td", headers="sa6").text

    # Vyčištění textu od skrytých znaků
    data_obce = {
        "volici": volici.replace("\xa0", "").strip(),
        "obalky": obalky.replace("\xa0", "").strip(),
        "hlasy": hlasy.replace("\xa0", "").strip()
    }

    vsechny_strany = soup_detail.find_all("td", class_="overflow_name")

    for strana_bunka in vsechny_strany:
        nazev_strany = strana_bunka.text

        # Hlasy jsou v buňce hned vedle (vpravo), použijeme find_next_sibling
        hlasy_bunka = strana_bunka.find_next_sibling("td", class_="cislo")
        if hlasy_bunka:
            pocet_hlasu = hlasy_bunka.text.replace("\xa0", "").strip()
            data_obce[nazev_strany] = pocet_hlasu

    return data_obce


def vytvor_csv(jmeno_csv: str, data: list[dict]) -> None:
    """Zapíše stažená data o obcích do CSV souboru."""
    if not data:
        return

    zahlavi = data[0].keys()

    with open(jmeno_csv, mode="w", newline="") as soubor:
        zapisovac = csv.DictWriter(soubor, fieldnames=zahlavi, delimiter=";")
        zapisovac.writeheader()
        zapisovac.writerows(data)


def main() -> None:
    if len(sys.argv) < 3:
        print("CHYBI URL NEBO JMENO CSV SOUBORU")
        # KONTROLA: pokud chybí jeden z argumentů, program skončí
        sys.exit(1)
    else:
        url = sys.argv[1]
        jmeno_csv = sys.argv[2]
        print(f"STAHUJI DATA Z VYBRANEHO URL: {url}")
        soup = nacti_url(url)

        # KONTROLA: Pokud stránka nejde načíst, program skončí
        if not soup:
            print("CHYBA: Stranku se nepodarilo nacist.")
            sys.exit(1)

        obce = ziskej_seznam_obci(soup)

        # KONTROLA: pokud uživatel zadal jinou stránku, program skončí
        if not obce:
            print("CHYBA: Odkaz neobsahuje volebni obce.")
            sys.exit(1)

        finalni_data = []

        print("STAHUJI DATA PRO JEDNOTLIVE OBCE, PROSIM CEKEJTE...")
        for obec in obce:
            soup_detail = nacti_url(obec["url_ob"])

            if soup_detail:
                detail_data = zpracuj_detail_obce(soup_detail)
                kompletni_obec = obec | detail_data

                # Z výsledného slovníku smažeme klíč "url", protože ho v CSV nepotřebujeme
                kompletni_obec.pop("url_ob", None)

                finalni_data.append(kompletni_obec)

        print("DATA BYLA USPESNE STAZENA.")
        vytvor_csv(jmeno_csv, finalni_data)
        print(f"SOUBOR {jmeno_csv} BYL USPESNE VYTVOREN!")

        print("UKONCUJI PROGRAM")
        sys.exit(0)

if __name__ == "__main__":
    main()
