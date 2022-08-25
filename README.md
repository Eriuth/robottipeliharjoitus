# Pieni peli vastauksena ohjelmoinnin jatkokurssin haasteeseen

Tämä pieni python-peli on kirjoitettu 2020 vuoden lopussa. Se on toiminut vastauksena yhtenä ohjelmoinnin jatkokurssin viimeisimmistä tehtävistä ennen tenttiä. Tehtävänannon voisi luonnehtia jotakuinkin "niillä, mitä olet oppinut, tee oma peli". Muistelen, että suurin osa kanssaopiskelijoideni peleistä, joita näin, toimivat logiikalla "liikuta hiirtä tai käytä näppäimistöä ja ohjaa hahmoasi välttelemään hirviöitä sekä kerää kolikoita"-periaatteella.

Pelin tarkoitus on veikata, lähteekö robotti oikealle vai vasemmalle. Jos se osuu hirviöön, veikkaus menee väärin, ja tulee game over tai saa vähemmän kolikkoja kuin oikein veikkaamalla. Värit ovat aikamoiset. Tarkoituksella.

Tässä vaiheessa koodausta olen erityisesti miettinyt ja ihmetellyt rakenteita - miten kirjoittaa ja rakentaa koodia niin, että sitä voi itse myöhemmin jatkaa, se on selkeää luettavaa kaverille (opiskelijat arvioivat toistensa koodia), miettinyt hyvän koodaamisen tapaa ja hyvän koodin palikoita.

Kurssilta saatuja materiaaleja ovat png-tiedostot, jotka vakuutettiin olevan luvallisia jakaa.

Rekrytoijille, joilla suoritusotteeni ovat hyppysissä ja toinen kulmakarva koholla -> todistuksessani saattaa lukea myöhempi aika kurssille. Aika viittaa lähemmäs hetkeä, jolloin tukipalveluiden kanssa yhdistimme eri sähköposteille tekemiäni kursseja yhden käyttäjätilin alle. 

Kiitos Helsingin yliopisto sekä hauskoista avoimista kursseista että kaikesta tuesta, jota olen saanut - oli kyse sitten pisteen eroista sähköpostiosoitteessani ilmoittautuessa tai kokonaan uusien taitojen hankinnan motivoinnista. Isoin ja pienin tavoin avoimet kurssit ovat mahdollistaneet osaamisen hankintaa, motivaatioita ja saatava tuki on eri tavoin purkanut esteitä tieltäni.

# Mitä peliin voisi parantaa

 - Kysymyssivun ohjaava pelaamislogiikka. Nyt seikkailevalla hahmolla on lähdön oletussuunta ja kääntymissuunta eri muuttujissa. <br> Näin hahmo saattaa lähteä eri suuntaan, kuin pelaaja hahmotti.
 - Kysymyssivun tekniikka - valinnan tarkkuus on vain raapaistu kasaan. Sivulogiikan voi korjata tyylikkäämmäksi myös teknisesti.
 - Lisää kenttiä.
 - Kolikon poistuminen, kun se kerätään.
 - Jakaminen. Alunperin halusin nimenomaan lähettää pelin pikkusiskolleni ja isoveljelleni näytiksi & joululahjoiksi, mutta viruksientorjunta tuhosi exeksi muotoillut tiedostot yrityksistä (ja avuista) huolimatta. Demo taisi tapahtua muistaakseni etänä, joten pelikokemusta ei saanut välitettyä toivotussa aikaikkunassa.