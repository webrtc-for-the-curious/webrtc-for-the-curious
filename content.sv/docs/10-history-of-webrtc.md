---
title: Historia
type: docs
weight: 11
---


# Historia
Detta kapitel skrivs fortfarande och vi har inte alla fakta än. Vi genomför intervjuer för att bygga en mer samlad historia av digital kommunikation.

### RTP
RTP och RTCP är protokollet som hanterar all mediatransport för WebRTC. Det definierades i [RFC 1889](https://tools.ietf.org/html/rfc1889) i januari 1996.
Vi är väldigt lyckliga att få en av författarna [Ron Frederick](https://github.com/ronf) prata om det själv. Ron laddade nyligen upp
[Network Video tool](https://github.com/ronf/nv) på GitHub, ett projekt som la grunden till RTP.

**I hans egna ord:** ([Originaltext på engelska](../../10-history-of-webrtc/#rtp))

I oktober 1992 började jag experimentera med Sun VideoPix frame grabber
med tanken att skriva ett nätverksvideokonferensverktyg baserat på IP
multicast. Det modellerades efter "vat" - ett telefonkonferensverktyg utvecklat
på LBL, eftersom det använde ett liknande enkelt protokoll där användare som vill
gå med i konferenser helt enkelt bara skickade data till en viss
multicast-grupp och samtidigt lyssnade på den gruppen för ta emot video från andra
medlemmar.

För att programmet verkligen skulle lyckas behövde det komprimera
videodata innan den skickas till nätverket. Mitt mål var att göra en tillräkligt
bra videoström som skulle rymmas i cirka 128 kbps, eller en den normala
bandbredden tillgänglig på en vanlig ISDN-modem linje. Jag hoppades också att göra
något som fortfarande såg ok ut men bara använde halva denna bandbredd. Detta
betydde att jag behövde ungefär en faktor 20 i kompression för den specifika
bildstorlek och bildhastighet jag arbetade med. Jag kunde uppnå denna 
komprimering och ansökte om patent på de tekniker som jag använde, senare beviljat
i patent [US5485212A][1]: Videokomprimering av programvara för telekonferenser.

[1]: https://patents.google.com/patent/US5485212A

I början av november 1992 släppte jag videokonferensverktyget "nv" (själva 
programmet) gratis på nätet. Efter några initiala tester användes programmet
för att sända delar av November Internet Engineering Task Force till hela
världen. Cirka 200 subnät i 15 länder kunde ta emot denna sändning,
och cirka 50-100 personer fick video med "nv" någon gång under veckan.

Under de kommande månaderna sändes tre andra workshops och några mindre
möten via "nv" till internet, inklusive Australiska NetWorkshop, 
MCNC Packet Audio and Video workshoppen och MultiG-workshoppen om
distribuerad virtuell verklighet från Sverige.

En release av källkoden för "nv" följde i februari 1993 och i mars släppte
jag en version av verktyget där jag introducerade ett nytt wavelet-baserat
komprimeringsschema. I maj 1993 lade jag till stöd för färgvideo.

Nätverksprotokollet som används för "nv" och andra internetkonferensverktyg
blev grunden för Realtime Transport Protocol (RTP). Det standardiserades
genom Internet Engineering Task Force (IETF), först publicerat i
RFC [1889][2] - [1890][3] och senare reviderad i RFC [3550][4] - [3551][5]
tillsammans med olika andra RFC:er som täcker profiler för att skicka specifika
format av ljud och video.

[2]: https://tools.ietf.org/html/rfc1889
[3]: https://tools.ietf.org/html/rfc1890
[4]: https://tools.ietf.org/html/rfc3550
[5]: https://tools.ietf.org/html/rfc3551

Under de följande åren fortsatte arbetet med "nv" och verktyget portades
till ytterligare ett antal hårdvaruplattformar och videoinspelare.
Det fortsatte att användas som ett av de främsta verktygen för sändning
konferenser på internet vid den tiden, inklusive av NASA för
att sända live-video av uppskjutningar av rymdskytteln på nätet.

1994 lade jag till stöd i "nv" för videokomprimeringsalgoritmer
utvecklat av andra, inklusive vissa hårdvarukomprimeringsscheman som
CellB-format som stöds av SunVideo-videoinspelningskortet. Det gjorde det
möjligt för "nv" att skicka video i CUSeeMe-format, för att skicka video 
till användare som körde CUSeeMe på Mac och PC.

Den senast släppta versionen av "nv" var version 3.3beta, släppt
i juli 1994. Jag arbetade med en "4.0alpha"-release som var avsedd
att migrera "nv" till version 2 av RTP-protokollet, men detta arbete blev
aldrig slutfört på grund av att jag gick vidare till andra projekt. En 
kopia av 4.0alfa ingår i [Network Video tool](https://github.com/ronf/nv)
arkivet, men det är oavslutat och det finns kända problem med det, 
särskilt i det ofullständiga RTPv2-stödet.

Ramverket i "nv" blev senare grunden för video
konferenser i projektet "Jupiter multimedia MOO" på Xerox PARC, som
så småningom blev grunden för ett avknoppningsföretag "PlaceWare", senare
förvärvades av Microsoft. Det användes också som grund för ett antal
hårdvarukonferensprojekt som tillät sändning av fullständig NTSC
video över Ethernet och ATM-nätverk med hög bandbredd.
Jag använde också senare en del av den här koden som grund för "Mediastore", 
som var en nätverksbaserad videoinspelnings- och uppspelningstjänst.

**Kommer du ihåg de andra personernas motiv/idéer i utkastet?**

Vi var alla forskare som arbetade med IP-multicast och hjälpte till att skapa
internet-multicast-systemet (även kallad MBONE). MBONE skapades av
Steve Deering (som först utvecklade IP-multicast), Van Jacobson och Steve
Casner. Steve Deering och jag hade samma rådgivare på Stanford och Steve
slutade arbeta på Xerox PARC när han lämnade Stanford. Jag tillbringade en
sommar på Xerox PARC som praktikant för att arbeta med IP multicast-relaterade 
projekt och fortsatte att arbeta för dem på deltid, och senare på full tid 
medan jag var på Stanford. Van Jacobson och Steve Casner var två av de fyra 
författarna på de första RTP-RFC:erna, tillsammans med Henning Schulzrinne 
och jag själv. Vi alla hade MBONE-verktyg som vi arbetade med som möjliggjorde 
olika former av online-samarbete och försöker komma på ett gemensamt basprotokoll
alla dessa verktyg som kunde användas var det som ledde till RTP.

**Multicast är superfascinerande. WebRTC är enkelsändning, kan du utveckla det lite mer?**

Innan jag kom till Stanford och lärde mig om IP-multicast hade jag en lång 
historia av att arbeta med olika sätt för människor att använda datorer som ett 
sätt kommunicera med varandra. Detta började i början av 80-talet för mig
när jag körde en digital anslagstavla (BBS) där människor kunde logga in
och lämna meddelanden till varandra, båda privata (typ av motsvarande
e-post) och offentliga (diskussionsgrupper). Ungefär under samma tid lärde jag 
mig också om onlinetjänstleverantören CompuServe. En av de coola funktionerna
på CompuServe var något som kallades "CB Simulator" där människor
kunde prata med varandra i realtid. Det var helt textbaserat, men det
hade en koncept med "kanaler" som en riktig CB-radio och flera personer
kunde se vad andra skrev, så länge de var i samma kanal.
Jag byggde min egen version av CB som kördes på ett timesharing-system jag hade
åtkomst som lät användare på systemet skicka meddelanden till varandra
i realtid, och under de närmaste åren arbetade jag med några vänner med att
utveckla mer sofistikerade versioner av kommunikationsverktyg i realtid
på flera olika datorsystem och nätverk. I själva verket en av dessa
system är fortfarande i drift, och jag använder det varje dag för att prata med 
folk jag gick till college med för 30+ år sedan!

Alla dessa verktyg var textbaserade, eftersom datorer på den tiden oftast
saknade ljud- och videofunktioner, men när jag kom till Stanford och
lärde mig om IP-multicast blev jag fascinerad av tanken att använda multicast 
för att bygga något mer som en riktig “radio”, där du kan skicka en signal
ut på nätverket som inte riktades till en enskild användare, men istället kan
alla som ställde in den "kanalen" ta emot den. Av en händelse så var den
dator jag portade IP-multicast-koden till av den första generationen
SPARC-station från Sun, och den hade faktiskt inbyggt ljud av telefonkvalitet
i hårdvaran! Du kan digitalisera ljud från en mikrofon och spela upp det igen
på inbyggda högtalare (eller via ett headset). Så min första tanke var att
ta reda på hur man skickar ljud över nätverket i realtid med IP-multicast,
och se om jag kunde bygga en motsvarande "CB-radio", men med riktigt
ljud istället för text.

Det fanns några knepiga problem att lösa, som det faktum att datorn
kunde bara spela en ljudström åt gången, så om flera personer pratade
du behövde man matematiskt "blanda" flera ljudströmmar till en enda så att 
du kunde spela upp det, men det kunde göras i mjukvara när man förstått
hur ljud-samplingen fungerade. Den ljudapplikationen ledde mig till att 
arbeta med MBONE och så småningom gå från ljud till video med “nv”.

**Har något som utelämnats från protokollet som du önskar att du hade lagt till?
Är det något i protokollet du ångrar?**

Jag skulle inte säga att jag ångrar det, men ett vanligt klagomål som människor 
har om RTP är komplexiteten i att implementera RTCP, kontrollprotokollet
som körs parallellt med RTP-datatrafiken. Jag tror att komplexiteten
var en stor del av varför RTP inte antogs i större utsträckning, särskilt i
enkelsändningsfallet där det inte fanns lika stort behov av RTCPs funktioner.
När nätverksbandbredden blev mindre begränsad och trängseln inte var ett lika 
stort problem, började många människor helt enkelt streama ljud och video över 
vanlig TCP (och senare HTTP), och i allmänhet fungerade det "tillräckligt bra",
så det var inte värt att använda RTP.

Tyvärr innebär användning av TCP eller HTTP att ljud och video från flera 
applikationer måste skicka samma data över nätverket flera gånger, till var 
och en av alla klienter som vill ta emot det, vilket gör det mycket mindre
effektivt ur ett bandbreddsperspektiv. Jag önskar ibland att vi hade drivit
på hårdare att få IP-multicast accepterat utanför forskarkretsarna.
Jag tror att vi kunde ha sett övergången från kabel och analog TV till
internetbaserad ljud och video mycket tidigare om vi hade gjort det.

**Vilka saker trodde du skulle byggas med RTP? Har något coolt RTP
projekt eller idé som aldrig blev av?**

En rolig sak jag byggde var en version av det klassiska ”Spacewar”-spelet
som använde IP-multicast. Utan att ha någon form av central server kunde
flera klienter var och en köra spacewar programmet och börja sända sina
skepps plats, hastighet, riktning, och liknande information för eventuella 
”kulor” som den avfyrat, och alla andra instanser av programmet plockade
upp den informationen och använde den lokalt, så att användarna kan alla
se varandras skepp och kulor, med skepp som "exploderar" om de kraschar
in i varandra eller om kulorna träffar dem. Jag gjorde till och med ”skräp” 
från explosioner till levande föremål som kan ta ut andra skepp, ibland 
ledande till roliga kedjereaktioner!

I andan i det ursprungliga spelet byggde jag det med simulerad vektor
grafik, så du kan göra saker som att zooma in och ut och se all grafik
skala upp och ner. Fartygen själva var en massa linjesegment i vektorform 
som jag fick några av mina kollegor på PARC att hjälpte mig att designa, 
så alla spelares skepp hade ett unikt utseende.

I grund och botten kan alla program som kan dra nytta av en realtidsdataström 
som inte kräver perfekt leverans av paket i ordning dra nytta av RTP. Så förutom
ljud och video kunde vi bygga saker som en delad whiteboard. Till och med 
fil-överföringar kan dra nytta av RTP, särskilt i samband med IP-multicast.

Tänk dig något som BitTorrent, men där du inte behöver skicka all daata
från punkt till punkt mellan klienterna. Den ursprungliga källan kunde skicka 
en multicast-ström till alla nerladdare på en gång och eventuella paketförluster 
på vägen kunde snabbt rensas upp genom en återöverföring från andra klienter som
redan fått den datan. Du kan till och med begränsa din återutsändningsförfrågan 
så att någon peer i närheten skickar kopian av datan, och även den sändningen
kan vara multicast för andra i den regionen, eftersom en paketförlust i
mitt i nätverket ofta betyder at en massa klienter nedströms från den punkten 
alla saknar samma data.

**Varför var du tvungen att bygga din egen videokomprimering. Fanns det inget annat
tillgängligt då?**

När jag började bygga "nv" använde de enda systemen jag kände till för
videokonferenser mycket dyr och specialiserad hårdvara. Till exempel,
Steve Casner hade tillgång till ett system från BBN som kallades "DVC" (och
senare kommersialiserad som "PictureWindow"). Komprimering krävde
specialiserad hårdvara, men dekompressionen kunde göras i programvara.
Det som gjorde "nv" unikt var att både kompression och dekompression
gjordes i programvara, och det enda hårdvarukravet var att ha
något för att digitalisera en inkommande analog videosignal.

Många av de grundläggande begreppen om hur man komprimerar video fanns redan 
då, till exempel dök MPEG-1-standarden upp precis vid samma tid som "nv",
men kodning i realtid med MPEG-1 var definitivt INTE möjligt på den tiden.
De förändringar jag gjorde handlade om att ta dessa grundläggande koncept 
men använda mig av mycket effektivare algoritmer där jag undvek saker som
cosinus transformerar och flyttalsberäkningar, och till och med undvvek
heltalsmultiplikationer eftersom de var mycket långsamma på SPARC-stations. 
Jag försökte göra så mycket som möjligt med bara addition, subtraktion,
bitmasker, och bitskiftning, och det blev tillräckligt snabbt för att 
fortfarande kännas som en video.

Inom ett år eller två från släppet av "nv" fanns det många olika ljud
och videoverktyg att välja mellan, inte bara på MBONE utan på andra platser
som CU-SeeMe-verktyget byggt på Mac. Så det var helt klart en idé vars tid
hade kommit. Jag gjorde faktiskt "nv" kompatibelt med många av dessa verktyg,
och i ett fåtal fall plockade andra verktyg upp min "nv"-codec, så att de 
kunde kommunicera via min komprimeringsalgoritm.

# SDP
# ICE
# SRTP
# SCTP
# DTLS
