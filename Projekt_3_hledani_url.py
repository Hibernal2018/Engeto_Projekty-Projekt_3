# projekt 3
# tady hledam zpusob jak ze zadaneho paramatru (asi cislo obce) nejit prislusnou URL

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# nejdriv najdeme vsechny odkazy na strance kraju
parametr = "6204"
vychozi_url_kraju = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
stranka_kraju = requests.get(vychozi_url_kraju).text
polivka_kraju = BeautifulSoup(stranka_kraju, "html.parser")
vsechny_url_kraju = polivka_kraju.find_all("a")
# ziskame vse, co je za =
ciselnik_kraje = []
pomocny_list_kraje = []
# extrahujeme obsah href, a pokud je obsazen v url a zaroven url obsahuje "ps311", vytvorime splitem pomocny_list_kraje
# nasledne z nej selektujeme 2. a 3. prvek, pokud ma prek listu delku == 4
for kraj in vsechny_url_kraju:
    href = kraj.get('href')
    if href and "ps311" in href:
        pomocny_list_kraje.append(href.split("="))
for prvek in pomocny_list_kraje:
    if len(prvek) == 4:
        ciselnik_kraje.append(prvek[2])
        ciselnik_kraje.append(prvek[3])
print(ciselnik_kraje)
quit()

# najdeme prvni odkaz obsahujici parametr; ziskame realtivni url ale s tagy
for url_obec in vsechny_url_kraju:
    url_obec = str(url_obec)
    if parametr in url_obec and "ps32?x" in url_obec:
        break
# ocistime relativni url pomoci bs a prevedeme na str, bo urljoin pracuje jen se stringy
polivka_okres = BeautifulSoup(url_obec, "html.parser")
relativni_url_okres = polivka_okres.a["href"]
relativni_url_okres = str(relativni_url_okres)
# ted vychozi a relativni url spojime
vychozi_url_okresu = urljoin(vychozi_url_kraju, relativni_url_okres)

# ciselnik obci v okrese
# ziskame vsechny odkazy v danem okrese a prevedeme na text; pak rozdelime do listu a z nej vyberem prvky, ktere jsou cisla; to hodi ciselnik obci
cisla_obci = []
vsechny_url_okresu = requests.get(vychozi_url_okresu).text
polivka_obci = BeautifulSoup(vsechny_url_okresu, "html.parser").get_text()
pomocny_list_obci = polivka_obci.split("\n")
for cast in pomocny_list_obci:
    if cast.isnumeric():
        cisla_obci.append(cast)
# vytvorime url adresu kazde obce 
# spolecny zaklad: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=
# nasleduje cislo kraje -> vytvorit ciselnik kraju
# pak: &xobec=CISLO OBCE Z CISELNIKU&xvyber=CISLO OKRESU(parametr)
vychozi_url_obce = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj="










