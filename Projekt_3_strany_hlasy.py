# projekt 3
# tady scrapuju jmena stran a jejich vysledky ze zadaneho okrsku (viz obsah_stranky)

import os
import csv
import requests
import urllib
from bs4 import BeautifulSoup

# nacist obsah stranky
obsah_stranky = requests.get("https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=11&xobec=584428&xvyber=6204")
# prevod na bs format
rozdelene_html = BeautifulSoup(obsah_stranky.text, "html.parser")
print(len(rozdelene_html))

# HLEDANI NAZVU OBCE
# vyhlednani vsech tagů <h3>
vsechny_h3 = list(rozdelene_html.find_all("h3"))
# z tagu <h3> vybere ten, ktery obsahuje text "Obec:"
for obec in vsechny_h3:
    if "Obec:" in obec.get_text():
       vybrana_obec = obec.get_text()
# prevede objekt na list
vybrana_obec_list = vybrana_obec.split(" ")
# spoji vse od indexu 1; aby se osetrily nazvy obce o vice nez jednom slove
konecna_obec = " ".join(vybrana_obec_list[1:])
print(f"Vybraná obec: {konecna_obec}", end="")

# HLEDANI POCTU VOLICU
volicu = rozdelene_html.find("td", class_="cislo", headers="sa2").get_text()
# HLEDANI POCTU OBALEK
obalek = rozdelene_html.find("td", class_="cislo", headers="sa5").get_text()
# HLEDANI POCTU PLATNYCH
platnych = rozdelene_html.find("td", class_="cislo", headers="sa6").get_text()
print(f"Počet voličů: {volicu}\nPočet odevzdaných obálek: {obalek}\nPočet platných obálek: {platnych}")

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
quit()
print(len(strany_seznam) == len(hlasy_seznam))
print(hlasy_seznam)
print(len(hlasy_seznam))
    





    

quit()
tabulky = tabulky[1:].get_text()
print(tabulky)

tabulky = list(tabulky)
for tabulka in tabulky:
    print(tabulka[0])
    #print(type(tabulka.get_text()))
#print(tabulky)
      



quit()
url = "https://books.toscrape.com/index.html"
odpoved_serveru = requests.get(url)
odpoved_serveru.content
rozdelene_html = BeautifulSoup(odpoved_serveru.content)
type(rozdelene_html)
quit()
adresa_rozcesti = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"







