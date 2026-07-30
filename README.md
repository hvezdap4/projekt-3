# Elections Scraper

Třetí projekt z kurzu Python Akademie od Engeta.

## Popis projektu

Slouží jako nástroj pro stahování (scrapování) a ukládání výsledků parlamentních voleb z roku 2017. Data jsou čerpána z oficiálního webu [volby.gov.cz](https://volby.gov.cz/pls/ps2017nss/ps3?xjazyk=CZ).

Program automaticky projde zvolený územní celek (okres), pro každou obec stáhne detailní volební výsledky a uloží je do strukturovaného CSV souboru.

## Instalace knihoven

Knihovny, které jsou použity v kódu, jsou uložené v souboru `requirements.txt`. V projektu jsou využity knihovny `requests` pro odesílání HTTP požadavků na volební server a `beautifulsoup4` pro následné parsování a analýzu staženého HTML obsahu. 

Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:


```bash
$ pip3 --version                    # Ověření verze manažeru balíčků
$ pip3 install -r requirements.txt  # Instalace všech potřebných knihoven
```

## Spuštění projektu
Spuštění souboru `main.py` v rámci přík. řádku požaduje dva povinné argumenty.

```bash
python main.py <odkaz-uzemniho-celku> <jmeno-souboru-csv>
```
Následně se vám stáhnou výsledky jako soubor s příponou `.csv`.

## Struktura výstupního CSV souboru

Výsledný soubor používá jako oddělovač středník (`;`) pro snadné otevírání v českém Excelu. Každý řádek obsahuje data pro jednu konkrétní obec:
* `kod` – Kód obce
* `nazev` – Název obce
* `volici` – Počet voličů zapsaných v seznamu
* `obalky` – Počet vydaných obálek
* `hlasy` – Počet platných hlasů
* `[Názvy stran]` – Samostatné sloupce pro každou kandidující stranu s počtem získaných hlasů

## Příklad spuštění (okres Benešov):

1. argument: `https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101`
2. argument: `vysledky_benesov.csv`

#### Spuštění programu:
```bash
python main.py "https://volby.cz](https://volby.gov.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"
```
Pokud nebudou zadány oba argumenty, program uživatele upozorní `CHYBI URL NEBO JMENO CSV SOUBORU` a bezpečně se ukončí.  
Pokud se nepodaří spojit se serverem, program uživatele upozorní `CHYBA: Stranku se nepodarilo nacist.` a bezpečně se ukončí.  
Pokud uživatel zadá jinou, než povolenou url adresu, program uživatele upozorní `CHYBA: Odkaz neobsahuje volebni obce.` a bezpečně se ukončí.

#### Průběh stahování:
```bash
STAHUJI DATA PRO JEDNOTLIVE OBCE, PROSIM CEKEJTE...
DATA BYLA USPESNE STAZENA.
SOUBOR vysledky_benesov.csv BYL USPESNE VYTVOREN!
UKONCUJI PROGRAM
```
#### Částečný výstup:
```bash
kod;nazev;volici;obalky;hlasy;Občanská demokratická strana;Řád národa...
529303;Benešov;13104;8485;8437;1052;10;2;624;3;802;597;109;35;112;6;11;948;3;6;414;2577;3;21;314;5;58;17;16;682;10
532568;Bernartice;191;148;148;4;0;0;17;0;6;7;1;4;0;0;0;7;0;0;3;39;0;0;37;0;3;0;0;20;0
530743;Bílkovice;170;121;118;7;0;0;15;0;8;18;0;2;0;0;0;3;0;0;2;47;1;0;6;0;0;0;0;9;0
```
