###TOO LONG DIDN'T READ###

Svrha ovog projektnog rada jeste upoznavanje sa IoT sistemima uz pomoć senzora, u ovom slučaju DH11 (senzor za temperaturu i vlažnost vazduha) i MQ135 (senzor za detekciju gasova), mikrokontrolera Arduino Uno, i Raspberry Pi.
U ovom projektu se korišćenjem MQTT protokola šalju podaci prikupljeni sa senzora na open-source platformu koja se zove Grafana, na kojoj se vrši vizuelizacija podataka.
Takođe, uz pomoć Flask framework-a smo omogućili da korisnik putem HTTP zahteva traži trenutno stanje vrednosti temperature i vlažnosti vazduha, ili raspoloživosti CO2 u vazduhu. u ppm (parts per million)

#########################

Ovaj projektni rad fokusira se na implementaciju pametnog sistema za monitoring kvaliteta vazduha i temperature u okviru pčelarstva. Korišćenjem senzora kao što su DHT11 i MQ135,
koji su dostupni i relativno jednostavni za upotrebu, može se ostvariti efikasan način praćenja prisustva štetnih gasova i temperature u košnicama.
DHT11 senzor meri temperaturu i vlažnost, dok MQ135 senzor detektuje prisustvo gasova kao što su CO2, amonijak i dim.
Ovaj pristup omogućava pčelarima da prate nivoe zagađenja vazduha, temperaturne uslove, identifikuju potencijalne pretnje po zdravlje pčela i preduzmu potrebne korake za očuvanje svojih kolonija.

Za projektovanje ovog IoT sistema potrebna je sledeća oprema: 
  Raspberry Pi mikroračunar	
  Arduino Uno
  DHT11 senzor za temperaturu i vlažnost vazduha	 
  MQ-135 senzor za detekciju štetnih gasova	 
  Kablovi	 
  USB kabl	 
  USB-C Punjač	

skripta.py:
  Ova skripta je zadužena za komunikaciju sa Arduino pločom putem serijske konekcije. Ključne funkcije uključuju:
  podaci(): Očitava podatke sa svih senzora i vraća ih kao rečnik.
  celzijus(): Očitava i vraća samo vrednost temperature.
  vlaznost(): Očitava i vraća samo vrednost vlažnosti.
  co2_ppm(): Očitava i vraća vrednost koncentracije CO2.
  
app.py:
  Ova skripta koristi Flask framework za kreiranje veb servera koji omogućava pregled podataka sa senzora putem veb stranice. Ključne funkcije uključuju:
  home(): Definiše početnu stranicu koja sadrži linkove ka različitim endpoint-ovima za pregled podataka.
  podaci(): Endpoint koji vraća JSON objekat sa svim podacima.
  celzijus(), vlaznost(), co2_ppm(): Endpoint-ovi koji vraćaju pojedinačne vrednosti u JSON formatu.

Svaki Python projekat, pogotovu onaj koji zahteva uključivanje dodatnih biblioteka, treba da ima svoje virtuelno okruženje. Stoga, to će biti prvi korak u kreiranju Raspberry Pi aplikacije. 
Potrebno je kreirati novo razvojno okruženje:
  python -m venv --system-site-packages env .
Koristi se - -system-site-packages kako bi se uključile i sve sistemske biblioteke.
Komandom cd env ulazi se u kreirano okruženje i komandom source bin/activate pokreće virtuelno okruženje.
Sada kada je podešeno virtuelno okruženje može se početi sa izradom projekta.

Potrebno je instalirati Mosquitto kroz sledeća tri koraka:
  Update i upgrade RPi-a
    sudo apt update
    sudo apt upgrade
  Potrebno je instalirati Mosquitto i klijentski softver. Klijenstski softver služi za testiranje da li MQTT broker radi na našem RPi-ju. 
    sudo apt install mosquitto mosquitto-clients
    Automatski je podešeno da se Mosquitto server pokreće pri samom pokretanju RPi-ja.
  Nakon instalacije, broker je pokrenut. Radi provere da li je broker stvarno pokrenut, potrebno je pokrenuti sledeću komandu.
    sudo systemctl status mosquitto
    
  Ako je servis uredno pokrenut, potrebno je da se ispisuje active (running)
 

Sada je potrebno kreirati sopstvenog publisher-a i subscriber-a: 
  Prvo je potrebno instalirati paho-mqtt biblioteku pomoću komande 
    pip install paho-mqtt
  
  Zatim treba kreirati sledeće Python skripte:
    publisher.py:
      Uvezene su potrebne biblioteke, a zatim definisane poruke koje će biti poslate. Svaka poruka ima topic (temu) i payload (sadržaj poruke). Zatim sledi konfiguracija MQTT parametara (host I mqtt_tppic).
      U beskonačnoj while petlji koristi se funkcija publish.multiple() za slanje veće količine poruka. Sadržaj poruke se dobija pomoću funkcija celzijus(),vlaznost(),co2_ppm() koje su importovane iz skripta.py skripte.
    subscriber.py:
      Importovane su potrebne biblioteke, a zatim definisana funkcija on_message() za obradu poruka. U ovoj funkciji, payload se dekodira iz binarnog oblika u string a zatim se ispisuje u konzoli. 
      Nakon toga, sledi konfiguracija MQTT parametara. Kreira se instanca mqtt.Client() koja predstavlja MQTT klijenta. Zatim se postavlja on_message funkcija kao funkcija za obradu primljenih poruka. Sledi povezivanje sa MQTT brokerom koristeći client.connect() metodu specificirajući adresu brokera i port. Takođe, potrebno je pretplatiti se na temu “bees” koristeći client.subscribe() metodu.
      U while petlji koristi se client.loop_forever() da bi se započela petlja za prijem poruka. Svaki put kada se petlja izvrši, povećava se promenljiva counter za 1.
  Program se pokreće tako što se prvo pokrene publisher komandom: python publisher.py, a zatim se pokreće subscribee komandom: python subscriber.py

Grafana predstavlja open-source platformu za vizuelizaciju i analizu podataka.

Link ka uputsvu za instalaciju grafane:
https://grafana.com/tutorials/install-grafana-on-raspberry-pi/

Nakon instalacije i podešavanja Grafane potrebno je iskucati komandu:
  GF_HTTP_ADDR=”172.20.222.234” 
Ovom komandom postavlja se IP adresa na kojoj Grafana sluša dolazne http zahteve.
  U ovom slučaju IP adresa je 172.20.222.234.
Sada je ostalo samo da se pokrene server komandom:
  sudo service grafana-server start
Sada je moguće pristupiti Grafana GUI na portu 5000. Potrebno je ukucati adresu na kojoj je povezan RaspberryPi  „172.20.222.250“:5000
Potrebno je koristiti MQTT Data Source plugin da bi se kao tip izvora podataka koristio MQTT. 
Potrebno je kliknuti na "Configuration" (Konfiguracija) u gornjem meniju, a zatim izabrati "Data Sources" (Izvori podataka), Kliknuti na "Add data source" (Dodaj izvor podataka) i izabrati "MQTT" iz padajućeg menija(MQTT plugin for Grafana | Grafana Labs).  
Nakon toga, treba kreirati novi dashboard.


