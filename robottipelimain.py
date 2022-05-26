#memo, 0 robo, 1 hirviö, 2 kolikko, 3 ovi, 5 seinä, 6 lattia, 7 VOIIITTOOOOOOOOOOOOOOOOO
#kentät luotu excelillä, eli hups -> varmaan voisi myös suoraan py, jotenkin XD, nyt vain muutettu tekstit pythonissa listoiksi teksteistä (copypaste on ystävä)
#roboa liikutetaan arvaamalla oikea tai vasen, ei nuolinäppäimillä, jää arvioijan arvioitavaksi, osuuko vaatimuksiin, vertaispainoksi loin useamman kentän ja valintaikkuna oli must
#eroavaisuuksia esimerkkiin¨
# esimerkiksi "etsi robo" -funktioiden sijaan päädyin automatiikan vuoksi tallettamaan muuttujan robon sijainnista 

#made by Tuire Ahola ja rankasti otettu mallia: pygame, omat ohjeet, ks. myös laitetut linkit sekä luonnollisesti Ohjelmoinnin perusteet ja jatkokurssi, syksy 2020, Hki avoin Yo eli https://python-s20.mooc.fi/
#huomioithan, että peli on osa kurssipalautusta, kurssilla ei ilmoitettu, kuka omistaa kuvat, mutta oletan, että ne on ok luvitettu.... niitä piti ainakin käyttää

#kehitettävää, voisi poistaa kolikot tai löydä ruudun päälle, jos on kerätty... Mietin myös vaihtoehtoista kuvaa eli ns. perinteistä väritmenettänyttä tai käänteistä...
#päätin olla huomauttelematta, jos onnistuu keräämään 0-pistettä kentästä, tästä voi olla eri mieltä

from sys import exit
import sys
import os
import pygame
import math

class Harjoituspeli:
    def __init__(self):
        pygame.init()

        self.laskuri_kentat = 1 # tervetuloatekstit 0, 1 kenttä1, myöh. laajennokset, jos ehtii
        self.laskuri_pisteet = 0 #täydet - jotain?

        self.kentta_suoritettu = False
        self.peli_suoritettu = False

        # self.testauksen_apulaskuri = 0

        self.lataa_kuvat()
        self.aloita_kentta()

        # varit # https://coolors.co/c0c0c0-040404-ffff00-ffff99-800202-6b6b00, luotu kuvien avulla
        self.robon_harmaa = (192, 192, 192)
        self.moron_musta = (4,4,4)
        self.kolikon_keltainen = (255,255,0)
        self.vaalea_lattia = (255,255,173) #shadea muuntamalla, vaalennettu kolikko
        self.robon_punasilma = (128,2,2)
        self.pinkihko = (253,134,134) #silmistä söpömmiksi
        self.generoitu_vihrea = (107,107,0) #bistre lienee vihreä, oliivi tai jotain?
        self.pronssi = (102,102,0) #generoitu ja shadea muutettu, vastin pinkihkölle, sopii seinäksi

        #leveys pelille on ruudukon leveys eli määrä * valittu mitta
        #kuvien lisäksi elementit eli ns. ruudut apuna
        self.laatan_leveys = self.kuvat[0].get_width() #robo mittatikkuna
        self.laatan_korkeus = self.kuvat[0].get_height() # robo mittatikkuna
        self.kartan_leveys = len(self.kartta[0])
        self.kartan_korkeus = len(self.kartta)
        
        nayton_leveys = self.laatan_leveys*self.kartan_leveys #huom, määritä kartta ja sen korkeus!
        nayton_korkeus = self.laatan_korkeus*self.kartan_korkeus #huom, määritä kartta ja sen korkeus!
        self.naytto = pygame.display.set_mode((nayton_leveys,nayton_korkeus))

        #otsikko & ikitarpeellinen kello, jotta animaatiot pyörivät
        pygame.display.set_caption("Robo labyrintissä. Arvaa ja voita pisteitä.")
        self.kello = pygame.time.Clock()

        #roboa varten, myös funktio muuta kulma sekä animointi lopussa, kartassa itsessään aloituskohta (x,y) sekä aloituskulma
        # self.aloitus_kartalla_x = self.kartta[19][9] # siirretty karttakohtaiseksi
        # self.aloitus_kartalla_y = len(self.kartta)-1 # ei toiminut vaan antoi listan, tulee olla int -> self.kartta[19] # siirretty karttakohtaiseksi
        self.aloituskohta_x = self.aloitus_kartalla_x*self.laatan_leveys
        self.aloituskohta_y = self.aloitus_kartalla_y*self.laatan_korkeus
        # self.kulma = math.radians(180) # siirretty karttakohtaiseksi
        # self.suunta_y = math.sin(self.kulma) #kiertona sin(180) eli 0jos aina oikea -> +90 -> -1, +90 > 0, +90 > +1 # siirretty karttakohtaiseksi
        # self.suunta_x = math.cos(self.kulma) #kiertona cos(180) eli alkaa -1, -90 kierrolla eli aina oikealla -> alku -1, 0, +1, 0, -1 # siirretty karttakohtaiseksi

        #pelaamisen kutsu
        self.silmukka()

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["robo","hirvio", "kolikko", "ovi"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))
        self.kuvat[0] = pygame.transform.scale(self.kuvat[0], (30,40))
        self.kuvat[2] = pygame.transform.scale(self.kuvat[2], (30,30)) #kolikko oli liian iso ruutuun, höh, piti pienentää
        self.kuvat[3] = pygame.transform.scale(self.kuvat[3], (30,40)) #tehdään hyvän kokoinen, vrt robo

    def aloita_kentta(self):
        self.kysytty_logiikkaa = False
        self.aina_vasen = False
        self.aina_oikea = False
        self.kentta_suoritettu = False

        if self.laskuri_kentat == 1 or self.laskuri_kentat == 0:
            #t-mallinen kartta, ei kolikoita tai paljon, voittopiste
            self.kartta = [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 2, 6, 2, 6, 6, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 5, 5, 5],
                [5, 6, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5],
                [5, 6, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5],
                [5, 2, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5],
                [5, 6, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 2, 5, 5, 5],
                [5, 6, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5],
                [5, 6, 2, 6, 2, 6, 2, 6, 6, 6, 6, 2, 6, 6, 2, 6, 6, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]

            self.aloitus_kartalla_x = self.kartta[19].index(6) #robon aloitus x
            self.aloitus_kartalla_y = len(self.kartta)-1 # robon aloitus y 
            self.kulma = math.radians(270) # aloitussuunnaksi robolle, ylös


        if self.laskuri_kentat == 2:
            #kiehkura, vasemmalle alkaen
            self.kartta = [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 6, 6, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5],
                [5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 6, 6, 6, 2, 6, 6, 6, 5, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 6, 5, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 5, 6, 6, 2, 6, 5, 6, 5, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 5, 6, 5, 5, 6, 5, 6, 5, 6, 5, 6, 5, 5, 5],
                [5, 2, 5, 2, 5, 2, 5, 2, 5, 7, 2, 5, 2, 5, 2, 5, 2, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 5, 6, 5, 5, 5, 5, 6, 5, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 5, 6, 6, 2, 6, 6, 6, 5, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5],
                [5, 6, 5, 6, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5],
                [5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 6, 6, 6, 6, 6, 6, 2, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]

            self.aloitus_kartalla_x = self.kartta[19][9] #robon aloitus x
            self.aloitus_kartalla_y = len(self.kartta)-1 # robon aloitus y 
            self.kulma = math.radians(180) # aloitussuunnaksi robolle, vasen

            self.aloituskohta_x = self.aloitus_kartalla_x*self.laatan_leveys
            self.aloituskohta_y = self.aloitus_kartalla_y*self.laatan_korkeus

           
        elif self.laskuri_kentat == 3:
            #sekamelska
            self.kartta = [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 6, 2, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 5, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 2, 5, 6, 5, 2, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 5, 2, 5, 6, 5, 5, 6, 5, 5, 5, 6, 6, 2, 5, 5, 5, 5, 5],
                [5, 6, 5, 6, 5, 6, 5, 5, 6, 5, 5, 5, 6, 5, 6, 5, 5, 5, 5, 5],
                [5, 2, 5, 6, 6, 6, 2, 6, 6, 7, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5],
                [5, 6, 5, 5, 5, 6, 5, 5, 6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 5, 5, 5, 6, 5, 5, 6, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 5, 5, 5, 2, 5, 5, 6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5],
                [5, 6, 2, 6, 6, 6, 6, 6, 6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 6, 2, 6, 6, 6, 6, 2, 6, 6, 6, 2, 6, 6, 2, 6, 6, 6, 5],
                [5, 5, 2, 5, 5, 6, 5, 5, 5, 5, 2, 5, 6, 5, 5, 5, 5, 5, 6, 5],
                [5, 5, 6, 5, 5, 6, 5, 5, 5, 5, 6, 5, 6, 5, 5, 5, 5, 5, 6, 5],
                [5, 5, 6, 5, 5, 6, 5, 5, 5, 5, 2, 5, 6, 5, 5, 5, 5, 5, 6, 5],
                [5, 5, 6, 2, 6, 6, 5, 5, 5, 5, 6, 5, 6, 6, 2, 6, 6, 6, 6, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5]]

            self.aloitus_kartalla_x = self.kartta[19].index(6) #robon aloitus x, ensimmäinen numero 6 eli vapaa käytävälaattaa
            self.aloitus_kartalla_y = len(self.kartta)-1 # robon aloitus y 
            self.kulma = math.radians(270) # aloitussuunnaksi robolle, ylös

            self.aloituskohta_x = self.aloitus_kartalla_x*self.laatan_leveys
            self.aloituskohta_y = self.aloitus_kartalla_y*self.laatan_korkeus

        #sitten pitäisi ottaa oikea
        elif self.laskuri_kentat == 4:
            self.kartta = [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                [5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 6, 6, 6, 5],
                [5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 5, 6, 6, 6, 2, 6, 6, 6, 6, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 6, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 5, 6, 5, 6, 2, 6, 6, 5, 6, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 5, 6, 5, 6, 5, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                [5, 5, 5, 2, 5, 2, 5, 2, 5, 2, 7, 5, 2, 5, 2, 5, 2, 5, 2, 5],
                [5, 5, 5, 6, 5, 6, 5, 6, 5, 5, 5, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 5, 6, 6, 6, 2, 6, 6, 5, 6, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5, 6, 5],
                [5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 2, 6, 6, 6, 6, 6, 6, 5, 6, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 5],
                [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 2, 6, 6, 6, 6, 6, 6, 6, 5]]

            self.aloitus_kartalla_x = self.kartta[19].index(6) #robon aloitus x, ensimmäinen numero 6 eli vapaa käytävälaattaa
            self.aloitus_kartalla_y = len(self.kartta)-1 # robon aloitus y 
            self.kulma = math.radians(360) # aloitussuunnaksi robolle, oikea

            self.aloituskohta_x = self.aloitus_kartalla_x*self.laatan_leveys
            self.aloituskohta_y = self.aloitus_kartalla_y*self.laatan_korkeus


    def silmukka(self):
        while True:
            self.tarkista_tapahtuneet()
            self.piirra_naytto()

    def tarkista_tapahtuneet(self):
        for tapahtuma in pygame.event.get():
            # if self.peli_suoritettu == True:
                # print("Onneksi olkoon")     
            if self.kentta_suoritettu == True:
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    if tapahtuma.pos[1] >= self.laatan_korkeus*6 and tapahtuma.pos[1] <= self.laatan_korkeus*7:
                        # print("korkeus ok")
                        if tapahtuma.pos[0] >= self.laatan_leveys and tapahtuma.pos[0] <= self.laatan_leveys*6:
                            # print("vasen x")
                            # self.seuraavan_kentan_alustus() #harkinnassa teenkö funktiona vai tässä, päädyin tähän
                            self.laskuri_kentat += 1
                            if self.laskuri_kentat == 5:
                                self.peli_suoritettu = True
                                self.kiitossivu() 
                                print(self.peli_suoritettu) 
                            self.aloita_kentta()

            if self.kysytty_logiikkaa == False:
                self.aina_vasen = False
                self.aina_oikea = False

                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    # print("Painoit jotain")
                    if tapahtuma.pos[1] >= self.laatan_korkeus*8 and tapahtuma.pos[1] <= self.laatan_korkeus*9:
                        # print("korkeus ok")
                        if tapahtuma.pos[0] >= self.laatan_leveys and tapahtuma.pos[0] <= self.laatan_leveys*6:
                            # print("vasen x")
                            self.aina_vasen = True
                            self.kysytty_logiikkaa = True
                        if tapahtuma.pos[0] > self.laatan_leveys*8 and tapahtuma.pos[0] <= self.laatan_leveys*14:
                            # print("oikea x")
                            self.aina_oikea = True
                            self.kysytty_logiikkaa = True

            if tapahtuma.type == pygame.QUIT:
                exit()

    def muuta_kulma(self): #robon etenemissuunnan funktio, aloituskulma kartan lisätietona
        if self.aina_vasen == True:
            self.kulma -= math.radians(90)
        elif self.aina_oikea == True:
            self.kulma += math.radians(90)
        else:
            raise ValueError("Huomaa, jokin virhe kulman muutosfunktiossa. Onko vasen tai oikea määritetty?") #testausta varten

    def kysymys_sivu(self):
        fontti_leipateksti = pygame.font.SysFont("cambria", 24)
        teksti = ["Päästäkseen labyrintistä,","robon kannattaa kääntyä aina", "vasemmalle", "tai", "oikealle.", "Arvaa nopein ja kerää pisteitä."]
        x = self.laatan_leveys
        y = self.laatan_korkeus
        for kirjoitus in teksti:
            rivi = fontti_leipateksti.render(kirjoitus, True, (self.moron_musta))
            self.naytto.blit(rivi, (x,y))
            y += self.laatan_korkeus
        y += self.laatan_korkeus
        pygame.draw.rect(self.naytto, (self.vaalea_lattia), (x, y, self.laatan_leveys*6, self.laatan_korkeus) )
        self.naytto.blit(fontti_leipateksti.render("Vasen", True,(self.moron_musta)), (x + self.laatan_leveys*2,y+5))
        pygame.draw.rect(self.naytto, (self.vaalea_lattia), (x + self.laatan_leveys*7, y, self.laatan_leveys*6, self.laatan_korkeus) )
        self.naytto.blit(fontti_leipateksti.render("Oikea", True,(self.moron_musta)), (x + self.laatan_leveys*9,y+5))
        

    def pistesivu(self):
        fontti_leipateksti = pygame.font.SysFont("cambria", 24)
        #tee tekstit, jos voitto ja häviö -> logiikkavoitto aina voittaa, eli ei tehty epäonnistuit, tipuit kartalta ja game over.
        teksti = ["Onneksi olkoon", "sinulla on yhteensä", str(self.laskuri_pisteet), "pistettä"] # teksti = ["Voi harmi", "ei tullut täysiä pinnoja," "Sait pisteitä:", self.laskuri_pisteet]
        x = self.laatan_leveys
        y = self.laatan_korkeus
        for kirjoitus in teksti:
            rivi = fontti_leipateksti.render(kirjoitus, True, (self.moron_musta))
            self.naytto.blit(rivi, (x,y))
            y += self.laatan_korkeus
        y += self.laatan_korkeus
        pygame.draw.rect(self.naytto, (self.vaalea_lattia), (x, y, self.laatan_leveys*6, self.laatan_korkeus) )
        self.naytto.blit(fontti_leipateksti.render("jatketaan", True,(self.moron_musta)), (x + self.laatan_leveys,y+5))

    def kiitossivu(self):
        #kun peli on suoritettu, self.peli_suoritettu == True, True annetaan tapahtumatarkistuksessa, alustetaan mainrungossa
        fontti_leipateksti = pygame.font.SysFont("cambria", 24)
        #vain voittoa ;)
        teksti = ["Onneksi olkoon!", "Läpäisit pelin!", "Keräsit", str(self.laskuri_pisteet), "pistettä.", "", "Kiitos pelaamisesta!"] # teksti = ["Voi harmi", "ei tullut täysiä pinnoja," "Sait pisteitä:", self.laskuri_pisteet]
        x = self.laatan_leveys
        y = self.laatan_korkeus
        for kirjoitus in teksti:
            rivi = fontti_leipateksti.render(kirjoitus, True, (self.moron_musta))
            self.naytto.blit(rivi, (x,y))
            y += self.laatan_korkeus


    # def etsi_robotti(self): #päätetty ettei tehdä
    # #     #käyttäen robon sijaintia, ks. missä se on kartalla
    # #     print("kysyit robon sijaintia")
    # #     print("tätä funktiota ei olla vielä tehty")
    #     pass

    # def sijoita_kolikot(self): # ei käytetä, kun palataan ja tehdään karttaaan, päätetty tehdä kartat uudestaan ja merkitä niihin tarvittavat, testit helpompia ja kenttien lopetus
    #     # self.lista_kolikoista = []
    #     for y in range(len(self.kartta)): #lista listoista 0-19
    #         if y == 9: #vain 9 rivi jatkuu
    #             for x in range(len(self.kartta[y])): #kohta listasta 0-19
    #                 if self.kartta[y][x] == 6:
    #                     self.naytto.blit(self.kuvat[2], (x*self.laatan_leveys, y*self.laatan_korkeus))
    #                     # self.kolikoista_kolikoista.append((x,y)
    #         else:
    #             for x in range(len(self.kartta[y])):
    #                 if x == 9 and self.kartta[y][x] == 6:
    #                     self.naytto.blit(self.kuvat[2], (x*self.laatan_leveys, y*self.laatan_korkeus))
    #                     # self.lista_kolikoista.append((x,y)

    def piirra_naytto(self):
        # self.naytto.fill(self.vaalea_lattia)
        # self.naytto.fill(self.generoitu_vihrea)
        self.naytto.fill(self.pinkihko)

        if self.peli_suoritettu == True:
            self.kiitossivu()

        if self.kentta_suoritettu == True and self.peli_suoritettu == False:
            self.pistesivu()

        if self.kysytty_logiikkaa == False and self.peli_suoritettu == False:
            self.kysymys_sivu()

        #print(pygame.font.get_fonts()) # testi, mitä fontteja olikaan. Hitsi, niitä oli paljon

        if self.kysytty_logiikkaa == True and self.kentta_suoritettu == False: # self.laskuri_kentat == 2 or self.laskuri_kentat == 4:
            for y_kohta in range(self.kartan_korkeus):
                for x_kohta in range(self.kartan_leveys):
                    ruutu = self.kartta[y_kohta][x_kohta]
                    # def piirra_lattiaruutu(self, x:int, y:int):
                    #     #rect(surface, color, rect) -> rect-kohdasta: http://www.pygame.org/docs/ref/draw.html#pygame.draw.rect & http://www.pygame.org/docs/ref/draw.html#pygame.draw.rect
                    if ruutu == 6 or ruutu == 2 or ruutu == 7:
                        pygame.draw.rect(self.naytto, (self.vaalea_lattia), (x_kohta*self.laatan_leveys, y_kohta*self.laatan_korkeus, self.laatan_leveys, self.laatan_korkeus) )
                    if ruutu == 7: #aseta ovi
                        self.naytto.blit(self.kuvat[3], (x_kohta*self.laatan_leveys, y_kohta*self.laatan_korkeus, self.laatan_leveys, self.laatan_korkeus))
                    if ruutu == 2:# or ruutu == 7: #aseta kolikko
                        self.naytto.blit(self.kuvat[2], (x_kohta*self.laatan_leveys, y_kohta*self.laatan_korkeus, self.laatan_leveys, self.laatan_korkeus))
                    if ruutu == 5: #seinä
                        pygame.draw.rect(self.naytto, (self.generoitu_vihrea), (x_kohta*self.laatan_leveys, y_kohta*self.laatan_korkeus, self.laatan_leveys, self.laatan_korkeus) )
        
            #robon animointia varten, ylhäällä self.kello sekä aloituskohtien määritelmä, muista nollata aina uuden kentän ladatessa                    
            self.naytto.blit(self.kuvat[0], (self.aloituskohta_x, self.aloituskohta_y )) # robo

            # pistelaskuri, tehtävä ja aiempien sijaan myös katsottu https://pygame.readthedocs.io/en/latest/4_text/text.html
            fontti_pisteteksti = pygame.font.SysFont("cambria", 14)
            pisteesi = fontti_pisteteksti.render("Pisteesi: "+ str(self.laskuri_pisteet), True, (self.moron_musta))
            self.naytto.blit(pisteesi, (17*self.laatan_leveys, 19*self.laatan_korkeus)) 
            
            
        pygame.display.flip()

        #animointia roboa varten
        if self.kysytty_logiikkaa == True and self.kentta_suoritettu == False:
            self.suunta_y = int(math.sin(self.kulma)) #kiertona sin(180) eli 0jos aina oikea -> +90 -> -1, +90 > 0, +90 > +1
            self.suunta_x = int(math.cos(self.kulma)) #kiertona cos(180) eli alkaa -1, -90 kierrolla eli aina oikealla -> alku -1, 0, +1, 0, -1
            #jos out of range of kartta, niin

            try:        
                #jos paikka kartalla, vs yksi ylös on tyhjää, eli verrataan seuraavaan potentiaaliseen, 2, 6, 7
                if self.kartta[int(self.aloitus_kartalla_y +self.suunta_y)][int(self.aloitus_kartalla_x +self.suunta_x)] == 6 or self.kartta[int(self.aloitus_kartalla_y +self.suunta_y)][int(self.aloitus_kartalla_x +self.suunta_x)] == 2 or self.kartta[int(self.aloitus_kartalla_y +self.suunta_y)][int(self.aloitus_kartalla_x +self.suunta_x)] == 7: 
                    self.aloitus_kartalla_y += self.suunta_y #aloituksen 180 vasemmalla on 0, sitten alas +1 , oikealla vasen, sitten ylös eli sin-1
                    self.aloituskohta_y += self.suunta_y*self.laatan_korkeus #aloituksen 180
                    self.aloitus_kartalla_x += self.suunta_x #nolla tässä
                    self.aloituskohta_x += self.suunta_x*self.laatan_leveys # nolla tässä
                    if self.kartta[self.aloitus_kartalla_y][self.aloitus_kartalla_x] == 2 or self.kartta[self.aloitus_kartalla_y][self.aloitus_kartalla_x] == 7:
                        self.laskuri_pisteet += 10
                    if self.kartta[self.aloitus_kartalla_y][self.aloitus_kartalla_x] == 7:
                        self.kentta_suoritettu = True
                        # self.seuraavan_kentan_alustus()
                        # print(self.kentta_suoritettu)
                if self.kartta[int(self.aloitus_kartalla_y +self.suunta_y)][int(self.aloitus_kartalla_x+ self.suunta_x)] == 5:
                    self.muuta_kulma() 
            except:
                self.kentta_suoritettu = True

        # print(self.laskuri_pisteet)
        self.kello.tick(6)#mietin kyllä esimerkin mukaan 60, 180 jne smoothimpaa, mutta päätin, että tähän sopii 10 pikselin heitto suuntaan ja töks-animointi

if __name__ == "__main__":
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    Harjoituspeli()