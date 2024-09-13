"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Milan Novák
email: novakmilan@email.cz
discord: milannovak_77018
"""
import csv
import os
import requests
from bs4 import BeautifulSoup
import sys

def zkontroluj_vstupni_argumenty(argumenty):
    """
    Zkontroluje vlastnosti vstupních argumentů

    """
    if len(argumenty) < 3:
            print("Zadali jste příliš málo argumentů. Zkuste to znovu.")
            sys.exit(1)
    if argumenty[1].endswith(".csv"):
            print("Zdá se, že jste přehodili pořadí argumentů. Zkuste to znovu.")
            sys.exit(1)
    if not argumenty[1].startswith("https://"):
            print("Adresa webové stránky musí začínat https://") 
            print("Zkuste to znovu.")  
            sys.exit(1) 
    if not argumenty[2].endswith(".csv"):
            print("Výstupní soubor nemá správnou příponu. Zkuste to znovu s .csv na konci.")
            sys.exit(1)

def nacti_vstupni_argumenty():          
    """
    Nacte vstupní argumenty

    Returns: 
        str: url_okres, str: vystup_csv
    """
    try:
        argument_1 = sys.argv[1]
        argument_2 = os.path.join(r"D:\Privat_doma\Python_Engeto\Moje_cviceni\Projekt_3", sys.argv[2])
    except Exception as e:
        print("Nastala neočekávaná chyba. Ukončuji program.")
        print(e)
        sys.exit(1)
    else:
        return argument_1, argument_2

def nacti_stranku_okresu(adresa_okresu):
    """
    Nacte obsah stranky vybraneho okresu a najde v nich vsechny odkazy ("a")
    
    Return:
        bs: vsechny_url_okresu 
    """
    try:    
        with requests.get(adresa_okresu) as odpoved:
            obsah_stranky_okres = odpoved.text
    except requests.exceptions.RequestException as e:
        print("Chyba při načítání stránky.")
        print(e)
        sys.exit(1)
    else:
        print("STAHUJI DATA Z VYBRANÉHO URL:", adresa_okresu)
        html_okresu = BeautifulSoup(obsah_stranky_okres, "html.parser")
        vsechny_url_okresu = html_okresu.find_all("a")
        return vsechny_url_okresu
 
def dopln_url_obci(vsechny_adresy_okresu):
    """
    Ze vsech odkazu na strance okresu ziska obsah href, a pokud je v nich obsazen text "ps311", prida je do listu doplnek_url_obci

    Return:
        list: doplnek_url_obci 
    """
    doplnek_url_obci = []
    for odkaz in vsechny_adresy_okresu:
        href = odkaz.get('href')
        if href and "ps311" in href:
            doplnek_url_obci.append(href)
    return doplnek_url_obci
    
def ziskej_url_obci(url_obce_1_cast, doplnek_url_obci):
    """
    Vytvari url s vysledky vsech obci a z nich ziskava kod obce

    Returns:
        list: url_vsech_obci, list(dict): vysledky
    """
    url_vsech_obci = []
    [url_vsech_obci.append(url_obce_1_cast + url_obce_2_cast) for url_obce_2_cast in doplnek_url_obci]
    return url_vsech_obci

def ziskej_kod_obce(adresa_obce):
    pomocny_kod_obce = adresa_obce.split("obec=")
    pomocny_kod_obce = pomocny_kod_obce[1].split("&")
    kod_obce = pomocny_kod_obce[0]
    return kod_obce

def nacti_obsah_stranky_obce(adresa_obce):
    """
    Nacte obsah stranky obsahujici vysledky obce

    Return:
        bs: html obce
    """
    with requests.get(adresa_obce) as odpoved:
        html_obce = BeautifulSoup(odpoved.text, "html.parser")
    return html_obce
  
def ziskej_nazev_obce(stranka_obce):
    """
    Najde vsechny tagy "h3" a vybere z nich ty obsahujíci slovo "obec".
    Prevede je na text, vybere a ocisti nazev obce a prida ho do listu vysledky

    Return:
        str: vybrana_obec
    """
    vsechny_h3 = list(stranka_obce.find_all("h3"))
    
    for obec in vsechny_h3:
        obec = obec.get_text()
        if "Obec:" in obec:
            vybrana_obec = (obec.split(": ")[1:])[0].strip()
    return vybrana_obec

def ziskej_souhrny_obce(stranka_obce):
    """
    V obsahu stranky obce najde podle zadanych kriterii pocet volicu, odevzdanych obalek a platnych hlasu a prida je do listu vysledky.

    Returns:
        str: pocet_volicu, pocet_obalek, pocet_platnych
    """
    pocet_volicu = stranka_obce.find("td", class_="cislo", headers="sa2").get_text().replace("\xa0", "")
    pocet_obalek = stranka_obce.find("td", class_="cislo", headers="sa5").get_text().replace("\xa0", "")
    pocet_platnych = stranka_obce.find("td", class_="cislo", headers="sa6").get_text().replace("\xa0", "")
    return pocet_volicu, pocet_obalek, pocet_platnych

def ziskej_hlasy_stran(stranky_obce):
    """
    Vytvori list hlasu ze vsech tabulek vysledku voleb v dane obci

    Return:
        list: hlasy_seznam
    """
    hlasy_obec = stranky_obce.find_all("td", class_="cislo", headers="t1sa2 t1sb3")
    if len(stranky_obce) > 3:
        hlasy_t2 = stranky_obce.find_all("td", class_="cislo", headers="t2sa2 t2sb3")
        hlasy_obec += hlasy_t2
    if len(stranky_obce) > 4:
        hlasy_t3 = stranky_obce.find_all("td", class_="cislo", headers="t3sa2 t3sb3")
        hlasy_obec += hlasy_t3
    return hlasy_obec

def export_do_csv(vystupni_soubor, hlavicka):
    """
    Exportuje ziskane vysledky do souboru csv
    """
    print("UKLÁDÁM DO SOUBORU:", vystupni_soubor)
    with open (vystupni_soubor, mode="w", encoding="utf-8", newline="") as vysledky_csv:
        vysledky_writer = csv.DictWriter(vysledky_csv, fieldnames=hlavicka, delimiter=",")
        vysledky_writer.writeheader()
        vysledky_writer.writerows(vysledky)

if __name__ == "__main__":
    
    adresy_vsech_obci = []
    vysledky = []
    vysledky_kod_obci = []
    vysledky_jmena_obci = []
    zahlavi = []

    zkontroluj_vstupni_argumenty(sys.argv)
    url_okres, vystup_csv = nacti_vstupni_argumenty()
    vsechny_url_okresu = nacti_stranku_okresu(url_okres)
    doplnek_adresy_obci = dopln_url_obci(vsechny_url_okresu)

    adresy_obci = ziskej_url_obci("https://volby.cz/pls/ps2017nss/", doplnek_adresy_obci)
    for adresa_obce in adresy_obci:
        if adresa_obce not in adresy_vsech_obci:
            adresy_vsech_obci.append(adresa_obce)
    
    i = -1
    for url_obce in adresy_vsech_obci:
        vysledky_obce = {}
        vysledky_strany = []
        vysledky_hlasy = []
        i += 1

        obsah_stranky_obce = nacti_obsah_stranky_obce(url_obce)
        
        cislo_obce = ziskej_kod_obce(adresy_vsech_obci[i])
        if cislo_obce not in vysledky_kod_obci:
            vysledky_kod_obci.append(cislo_obce)

        nazev_obce = ziskej_nazev_obce(obsah_stranky_obce)
        if  nazev_obce not in vysledky_jmena_obci:
            vysledky_jmena_obci.append(nazev_obce)

        volici, obalky, platne = ziskej_souhrny_obce(obsah_stranky_obce)
        
        strany = obsah_stranky_obce.find_all("td", class_="overflow_name")
        [vysledky_strany.append(strana.get_text()) for strana in strany]
            
        hlasy = ziskej_hlasy_stran(obsah_stranky_obce)
        [vysledky_hlasy.append(hlas.get_text().replace("\xa0", "")) for hlas in hlasy]
            
        souhrn = {
            "code": vysledky_kod_obci[i], 
            "location": vysledky_jmena_obci[i], 
            "registered": volici, 
            "envelopes": obalky, 
            "valid": platne
            }
        vysledky_obce.update(souhrn)
        
        [vysledky_obce.update({vysledky_strany[j]: vysledky_hlasy[j]}) for j in range (len(vysledky_strany))]
            
        vysledky.append(vysledky_obce)

    if vysledky:
        zahlavi = list(vysledky[0].keys())
    else:
        print("Nedošlo k načtení výsledků. Ověřte správnost zadané url adresy. Zkuste to znovu.")
        sys.exit(1)
    
    export_do_csv(vystup_csv, zahlavi)
    print("UKONČUJI:", sys.argv[0])       
