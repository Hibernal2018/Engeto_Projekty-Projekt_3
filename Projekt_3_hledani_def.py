# projekt 3


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# zaciname na url konkretniho uzemi!!!
# takze pro ten ukazkovy Prostejov je to parametr:
# https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
# 1. jde o to vytvorit url adresy obci    
# 1.1 vytvorit ciselnik obci v ramci uzemniho celku (Prostejov)
# 1.2 zjistit odlisnosti v url obci oproti uzemnimu celku
#    https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
#    https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=589268&xvyber=7103
#    rozdíl je ps32? vs 311?x a pridani 506761&xvyber
# 2. vytvorit na zaklade rozdilu a ciselniku obci url kazde obce
# 3. v rámci iterace pres vsechny obce je vsechny vyscrapovat
# 4. zapsat kod do funkci a pridat kontroly(pripojeni, vstupu apod.)
# 5. upravit vysledky pro export do csv (asi listy)
# 6. export do csv
# 7. vytvorit vsechny nalezitosti: hlavicka v kodu, readme, requirements.txt atd.
url_okres = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"
def nacti_url_okres(par_1):
    obsah_stranky_okres = requests.get(par_1).text
    polivka_okresu = BeautifulSoup(obsah_stranky_okres, "html.parser")
    vsechny_url_okresu = polivka_okresu.find_all("a")
    return vsechny_url_okresu

# ziskame vse, co je za =


# extrahujeme obsah href, a pokud je obsazen v url a zaroven url obsahuje "ps311", vytvorime splitem pomocny_list_kraje
# nasledne z nej selektujeme 2. a 3. prvek, pokud ma prek listu delku == 4
def dopln_url_pro_obce():
    doplnek_url_obci = []
    for odkaz in nacti_url_okres(url_okres):
        href = odkaz.get('href')
        if href and "ps311" in href:
            pomocny_list = href.split("=")
            url_nahradit = pomocny_list[2] + "=" + pomocny_list[3] + "=" + pomocny_list[4]
            doplnek_url_obci.append(url_nahradit)
    return doplnek_url_obci

# vytvari cyklus, ktery iteruje pres vsechny polozky listu doplnek url obci
# v kazde iteraci vytvari url jedne obce z ciselniku a pridava do listu url obce
def vytvor_url_vsech_obci():
    url_vsech_obci = []
    url_obce_1_cast = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj="
    for url_obce_2_cast in dopln_url_pro_obce():
        url_vsech_obci.append(url_obce_1_cast + url_obce_2_cast)
    return url_vsech_obci

# ted budeme scrapovat kazdou adresu z listu url obce

# nacist obsah stranky
###############################################################################
def najdi_h3():
    obsah_stranky_obce = requests.get(url_obce)
    # prevod na bs format
    rozdelene_html = BeautifulSoup(obsah_stranky_obce.text, "html.parser")

    # HLEDANI NAZVU OBCE
    # vyhlednani vsech tagů <h3>
    vsechny_h3 = list(rozdelene_html.find_all("h3"))
    return rozdelene_html, vsechny_h3

def vyber_h3_obec():
    # z tagu <h3> vybere ten, ktery obsahuje text "Obec:"
    for obec in najdi_h3():
        if "Obec:" in obec.get_text():
            vybrana_obec = obec.get_text()
    # prevede objekt na list
    vybrana_obec_list = vybrana_obec.split(" ")
    # spoji vse od indexu 1; aby se osetrily nazvy obce o vice nez jednom slove
    konecna_obec = " ".join(vybrana_obec_list[1:])
    print(f"Vybraná obec: {konecna_obec}", end="")
    return konecna_obec

def souhrn_obce():
    rozdelene_html, _ = najdi_h3()
     # HLEDANI POCTU VOLICU
    volicu = rozdelene_html.find("td", class_="cislo", headers="sa2").get_text()
    # HLEDANI POCTU OBALEK
    obalek = rozdelene_html.find("td", class_="cislo", headers="sa5").get_text()
    # HLEDANI POCTU PLATNYCH
    platnych = rozdelene_html.find("td", class_="cislo", headers="sa6").get_text()
    print(f"Počet voličů: {volicu}\nPočet odevzdaných obálek: {obalek}\nPočet platných obálek: {platnych}")
    return volicu, obalek, platnych

for url_obce in vytvor_url_vsech_obci():
    najdi_h3()
    vyber_h3_obec()
    souhrn_obce()
    
    
    


    ################################################################################
   

    #TABULKA VYSLEDKU
    # strany maji stejný tag pro vyhledavani i ve vice tabulkach
    # najdou se listy; iteruje se po prvcich a texty se pridavaji do noveho listu
    strany_seznam = []
    strany = rozdelene_html.find_all("td", class_="overflow_name")
    for strana in strany:
        strany_seznam.append(strana.get_text())


    # u hlasu je ruzny tag pro vice tabulek; kdyz rozdelene html obsahuje 4 nebo 5 prvku = dve nebo tri tabulky s vysledky, musi se napsat zvlast kod pro prvni a zvlast pro druhou a treti tabulku
    hlasy_seznam = []  
    hlasy_t1 = rozdelene_html.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
    for hlas_t1 in hlasy_t1:
        hlasy_seznam.append(hlas_t1.get_text())
    if len(rozdelene_html) == 4:
        hlasy_t2 = rozdelene_html.find_all("td", class_="cislo", headers="t2sa2 t2sb3")
        for hlas_t2 in hlasy_t2:
            hlasy_seznam.append(hlas_t2.get_text())
    if len(rozdelene_html) == 5:
        hlasy_t3 = rozdelene_html.find_all("td", class_="cislo", headers="t3sa2 t3sb3")
        for hlas_t3 in hlasy_t3:
            hlasy_seznam.append(hlas_t3.get_text())
    for i in range(len(strany_seznam)):
        print(f"{strany_seznam[i]}: {hlasy_seznam[i]} hlasů", sep="\n")