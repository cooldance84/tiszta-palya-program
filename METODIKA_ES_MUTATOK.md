# Módszertan és mutatók

**Változat:** 0.9.2-j1, 2026. szeptember 22.  
**Státusz:** szakmai véleményezésre szánt mérési protokoll. A definíciók rögzítése nem jelenti a négy pillér hatásának igazolását.

## 1. Az összehasonlítás egysége

- Pénzügy: azonosított jogi személy vagy dokumentált, azonos tartalmú konszolidált kör és pontos beszámolási időszak. Az egyesület, az akadémia, a stadionüzemeltető és a profi csapat számai csak tételes egyeztetés és a belső ügyletek kiszűrése után összegezhetők.
- Sport: klub, versenysorozat, csapat és szezon. A 2022/23-as, 2023/24-es és 2024/25-ös szezon nem azonos a 2022-es, 2023-as vagy 2024-es naptári üzleti évvel. Szezonpénzügyet csak havi vagy tranzakciós adatokból képezünk; az éves adatot nem felezzük el automatikusan.
- Összevetési minta: FTC, Puskás Akadémia és MTK. Ez feltáró mintaválasztás, nem reprezentatív országos minta és nem kontrollcsoport önmagában.
- Pénzegység: forint, a nyilvános szemléltető táblában millió Ft. Tényadatnál rögzítendő a nominális év, nettó/bruttó ÁFA-kezelés, deviza és az átváltás dátuma/forrása. Reálérték csak külön megadott árindexszel számolható.
- A forrásban nem közölt érték hiányzó adat. A hiány, a nulla és a nem alkalmazható érték külön státusz. Nulla csak igazoló forrással rögzíthető. Nulla vagy negatív nevezőnél a bevételarányt nem számítjuk ki.

Minden megfigyeléshez szükséges: klub és jogi kör, időszak kezdete/vége, mutatóazonosító és definícióverzió, érték és egység, forráslink és oldal/táblázat, hozzáférési dátum, ellenőrző és ellenőrzési dátum, valamint összehasonlíthatósági megjegyzés. A belső adatbázis eredeti 0.1-es sémája ezekkel bővítendő az első ellenőrzött feltöltés előtt.

## 2. Bevétel, finanszírozás és közösségi kontroll

**O - teljes működési bevétel:** az azonos beszámolási körbe és időszakba tartozó, eredményként elszámolt működési tételek. Beletartozhat az adott időszak működési támogatása és szponzorációja. Nem része a játékosértékesítés ellenértéke vagy nyeresége, a hitelfelvétel, a tulajdonosi tőkeemelés és az eszközeladás. Támogatásokat külön jogcímen kell kimutatni. A saját bevételi mutató projektdefiníció, nem az UEFA korrigált működési bevételének helyettesítője.

**M - piaci és közösségi működési bevétel:** jegy, bérlet, klubnál maradó meccsnapi szolgáltatás, kereskedelmi, média-, digitális, magánszponzori és tagsági működési bevétel. A tagsági díjat egyszer számítjuk be. Tulajdonosi befizetés vagy állami cég szponzorációja nem kerülhet automatikusan ide; a forrás jellegét és a kapcsoltságot külön rögzítjük. Ismeretlen eredetű tételnél a besorolás és az arány is bizonytalan marad.

| Mutató / belső ID | Számítás és mértékegység | Időszak, forrás és adatgazda |
|---|---|---|
| Saját működési bevételi arány | 100 × M / O, %. A transzfer és a tőkefinanszírozás külön szerepel. | Üzleti év; negyedév csak azonos számviteli alapon. Klub pénzügy és ellenőrző. |
| P4_M01 Bevételi diverzifikáció | A kölcsönösen kizáró működési kategóriák összege O; kategória / O, %. A besorolatlan rész látható. | Üzleti év; beszámoló és analitika, klub pénzügy. |
| P4_M04 Szponzori koncentráció | Az egy gazdasági érdekkörhöz tartozó legnagyobb külső szponzor/támogató adott évi működési bevétele / O × 100, %. A top 3 ugyanezzel a csoportosítással külön közölhető. | Üzleti év; szerződések, beszámoló és kapcsoltsági nyilvántartás. Tőke és hitel külön finanszírozási tábla. |
| P1_M01 Tulajdon és szavazat | Tulajdoni és szavazati arány külön, testületenként. Védett ügy, jogosult, döntési küszöb és jogalap leírása. | Éves állapot és változások; cégadat, alapszabály. Jogi/irányítási felelős. |
| P1_M02 Szurkolói képviselet | A szabály létezése, a választás/mandátum és a tényleges részvétel külön adat. A határidőre érdemben megválaszolt, jogosult megkeresés / összes esedékes jogosult megkeresés × 100. | Félév; ügyrend, jegyzőkönyv, válasznapló. Klub és választott képviselet. Nulla ügy: nem alkalmazható. |
| P1_M03 Kapcsolt felek | Közzétett tulajdonosi lánc, kapcsolt partner és ügyletkategória leíró leltára; hiányzó adatok jelölése. | Év; beszámoló és cégadatok. Pénzügyi/jogi felelős. |

A fórumok száma vagy a testületi hely önmagában nem bizonyít érdemi közösségi befolyást. A formális jogot és annak dokumentált gyakorlását együtt, összpontszám nélkül mutatjuk be.

## 3. Költségfegyelem és likviditás

**P2_M01 - bér- és személyi ráfordítási arány:** az adott jogi kör beszámoló szerinti teljes személyi jellegű ráfordítása / O × 100. Éves összehasonlító mutató, nem UEFA squad cost ratio. Csak a játékosokra/edzőkre szűkített változat esetén külön megnevezés és azonos személyi kör szükséges. Forrás: beszámoló, béranalitika; adatgazda: pénzügy.

**P2_M02 - UEFA-referencia:** a 2026-os szabályzat 93. cikkének számlálója a releváns személyek juttatása, regisztrációs amortizáció, kölcsönügyletek és külön még el nem számolt közvetítői költség. Nevezője a korrigált működési bevétel, az eladási eredmény, az értékvesztés és az egyéb transzferbevételek/ráfordítások szabály szerinti összege. A működési és költségtételek 12 hónaposak, a transzferoldal meghatározott tételei 36 hónapból évesítettek; a részletszabályokat és előjeleket a K melléklet adja. A 94. cikk szerinti határ 70%. Ez csak teljes adatokkal nevezhető UEFA-mutatónak. A hazai alternatíva külön, előzetes projektmutató lenne.

A 2026-os referenciát nem használjuk korábbi szezonok jogszerűségének utólagos minősítésére. Történeti megfeleléshez az adott időszakban alkalmazandó szabályzat kell. Hiányzó amortizáció, kölcsönügylet, ügynöki adat, kapcsolt korrekció vagy időszak esetén az eredmény nem számítható ki megbízhatóan. Forrás/adatgazda: klubanalitika, licencadat, auditor; hivatalos éves számítás, a belső negyedéves becslés külön megjelöléssel.

**P2_M03 - lejárt kötelezettség:** referencia-napon esedékes, ki nem fizetett tartozás Ft-ban és típusonként, az átütemezés és vitatott státusz külön jelölésével. A nyilvános beszámoló hallgatása nem nulla. Havi követés, pénzügyi/jogi ellenőrzés; licencminősítés az alkalmazandó szabály szerint.

**P2_M04 - likviditási hónap:** szabadon felhasználható pénz / a következő három hónap tervezett havi fix készpénzkiadásának átlaga. A korlátozott pénz kizárt, a le nem hívott hitel/garancia külön adat. Nulla nevezőnél nem alkalmazható. Havi mérés, bank és cash-flow terv; adatgazda: pénzügy. Emellett 13 hetes, esedékességi alapú pénzforgalmi terv és 12 havi stresszterv szükséges. Az illusztratív éves pálya nem helyettesíti ezeket.

## 4. Három külön transzfermutató

Aktivált játékos-regisztráció esetén:

1. **Eladási eredmény:** elszámolt eladási ellenérték - egyszer levont közvetlen eladási díjak - a kivezetéskori könyv szerinti érték. A könyv szerinti érték már tartalmazza a korábbi amortizáció és értékvesztés hatását; a teljes bekerülési értéket és az amortizációt nem vonjuk le újra.
2. **Időszaki transzfereredmény (projektkimutatás):** eladási eredmények + külön kimutatott egyéb transzferbevételek - időszaki regisztrációs amortizáció és értékvesztés - a korábban még el nem számolt kapcsolódó ráfordítások. Kölcsönügyletek, képzési és szolidaritási tételek külön soron, egyszer szerepelnek. Ez nem az UEFA-ráta nevezőjének automatikus megfelelője.
3. **Transzfer-pénzáramlás:** az időszak tényleges transzferpénz-bevétele - tényleges beszerzési és kapcsolódó díjfizetése. Nem vonunk le amortizációt. Részleteket és bónuszokat pénzügyi rendezésük szerint követünk.

**Számpélda, M Ft:** 100 bekerülés - 40 halmozott amortizáció = 60 könyv szerinti érték. A 150 eladási ellenérték és 10 eladási díj mellett az eladási nyereség 80. Ha az adott évben csak 90 folyik be, 10 díjat és 50 új játékosbeszerzést fizetünk, a transzfer-pénzáramlás 30. A korábbi 40-et az eladási eredményből nem vonjuk le még egyszer.

Forrás: UEFA 2026 G.3.3, G.3.4(5), G.3.6. A fenti aktiválási példa nem alkalmazható átvezetés nélkül a beszerzést közvetlenül költségként elszámoló klubra. Az éves és hároméves összesítés időszaka, a számviteli politika és a nettósítás dokumentálandó. Adatgazda: klub pénzügy és auditor. A 13-14. fejezet pénzügyi példája külön jelöli, melyik mutatót használja.

## 5. Utánpótlás és játékosút

**P3_M01 - saját nevelésű játékperc aránya:** az előre rögzített klubképzési feltételt teljesítő játékosok első csapatos bajnoki perce / az első csapat összes játékosának ugyanazon bajnoki játékperce × 100. A nevező játékospercek összege, nem csapatmeccsek × 90. Kupák, nemzetközi és kölcsönben játszott percek külön sorozatban szerepelnek. A mérkőzésadat-szolgáltató percszámítását következetesen alkalmazzuk.

Konzultációs klubképzési feltétel: legalább három teljes szezon vagy 36 igazolt hónap a vizsgált klubnál a 15. és a 21. születésnap között, nemzetiségtől függetlenül. Ezt regisztrációs adatokkal kell igazolni; ez a kutatás előzetes definíciója, nem automatikus jogi jogosultság. Ismeretlen képzési előélet esetén a lefedettséget külön közöljük, a teljes arányt nem tekintjük ellenőrzöttnek. Adatgazda: akadémia, liga/adatpartner; frissítés mérkőzésenként, összesítés szezononként.

**Súlyozott perc:** Σ(játékperc × előre rögzített versenyszint-súly). A súlyok még nincsenek szakmailag validálva, ezért jelenleg nem számolunk összevont „minőségi percet”. Nyers perceket és versenysorozatot közlünk. A 900/1500 perces küszöb csak saját bajnoki, súlyozatlan percre vonatkozó vizsgálati határ, nem igazolt optimum és nem kötelező cél.

**P3_M02 - akadémia/felnőtt átmenet:** az adott szezonban először hivatalos első csapatos bajnokin pályára lépő, a klubképzési feltételt teljesítő játékosok száma. A 900 és 1500 percet elérők külön darabszám. Arányhoz előre kijelölt teljes akadémiai kilépő kohorsz kell, a kieső/eltűnő tagokat is megtartva a nevezőben.

**P3_M03 - játékosút követhetősége:** a megadott követési időpontban igazolt státuszú kohorsztag / teljes induló kohorsz × 100, az ismeretlenek arányával együtt. A 3 és 5 év utáni profi pályán maradás külön hosszú távú kimenet. A klub-, sportszint- és képzési hatás nem állapítható meg néhány kiválasztott játékos alapján.

**P3_M04 - kettős életpálya:** program megléte, jogosultak, résztvevők és utánkövetési lefedettség külön; iskolai előrehaladás csak megfelelő jogalappal és aggregáltan. A program létezése nem eredményességi mutató. Adatgazda: akadémia/képzési felelős; szezonos követés.

## 6. Meccsnapi bevétel és közönség

**P4_M02 - meccsnapi bevétel:** nettó jegy- és bérletbevétel, valamint a klubnál maradó meccsnapi szolgáltatási bevétel, kettős elszámolás nélkül. Az időszaki bérletbevételt a számviteli elszámolás szerint követjük. A büfé üzemeltetőjének teljes forgalma nem automatikusan klubbevétel. Mérkőzés/szezon/üzleti év csak dokumentált egyeztetéssel összekapcsolható; adatgazda: pénzügy és jegyrendszer.

**Fizető kihasználtság:** fizetett jeggyel/bérlettel ténylegesen beléptetett néző / az adott mérkőzés értékesíthető kapacitása × 100. Az ingyenes belépő, eladott de fel nem használt jegy és lezárt szektor külön adat. Éves aggregátum: belépések összege / meccsenkénti kapacitások összege; nem a százalékok egyszerű átlaga.

**90/180 napos visszatérés:** azonosítható új vásárlói kohorszból a határidőn belül újra fizetőként megjelenő személyek / a teljes megfigyelési időt elért jogosult kohorsz × 100, %. Csoportjegy-vásárló és látogató nem azonos egység. Hiányzó azonosító és még le nem telt követés külön közlendő. Adatgazda: klub CRM; havi kohorszok, jogszerű adatkezeléssel.

**P4_M03 - közösségi programok:** előre rögzített programkategóriánként eseményszám és elérés. Az eseményrészvételek összege és az egyedi résztvevő külön mutató. Forrás: klub/alapítvány eseménynapló; éves összesítés. A részvételszám nem társadalmi hatásbizonyíték.

## 7. A pilot és a forrásfeltárás külön feladata

**12 hetes, heti egyszeri forrásfeltárás:** munkaszervezési ciklus a három klub három lezárt szezonjának adatjelöltjeihez. Lezáráskor mutatónként és időszakonként forráslefedettség, hiánylista, ellenőrzési státusz és összehasonlíthatósági döntés készül. Az idő letelte nem adatminőségi kritérium. Automatizált találat nem kerülhet ellenőrzött megfigyelésként az adatbázisba.

**6-12 hónapos megvalósíthatósági pilot:** az adatgyűjtés működését, terhét, a pénzügyi riportolást, a közösségi részvételi folyamatot és rövid távú kereskedelmi változásokat vizsgálja. A 6-8 játékosból álló célzott csoport folyamatpróba, nem reprezentatív hatásvizsgálat. A beválasztás szabályait és a teljes jogosult kohorsz méretét közölni kell.

A már elszámolt piaci bevétel változása, a befolyt pénz és az új szerződésállomány három külön mutató. Jövőbeli szerződés nem számítható be elért bevételként. A 10-20%-os bevételi és 10%-os relatív fizetőkihasználtság-változás csak lehetséges célteszt; bázis, ár, kapacitás és sportsiker kontrollálása szükséges. A célértékeket a pilot indulása előtt kell rögzíteni.

**3-5 éves utánkövetés:** teljes kohorszok pályán maradása, szintváltása, tanulmányi és gazdasági kimenete. A még le nem telt időhorizont eredménye hiányzó/függő adat. A pilot rövid távú sikere nem bizonyítja az akadémia oksági hatását vagy az országos önfenntartást.

Értékelés: előre rögzített bázis és összevetési terv, dokumentált kimaradások, klubtól és szerzőtől független értékelő. A kis mintás előtte/utána mérésből legfeljebb feltáró következtetés vonható le. Bővítés csak megfelelő adatminőség, jogi keret és finanszírozás mellett indokolt.

## 8. Elsődleges szabályforrások

- [UEFA 2026, 93. cikk és K melléklet](https://documents.uefa.com/r/UEFA-Club-Licensing-and-Financial-Sustainability-Regulations-2026/Article-93-Calculation-of-squad-cost-ratio-Online): keretköltség-ráta, tételek és időszakok.
- [UEFA 2026, 94. cikk](https://documents.uefa.com/r/UEFA-Club-Licensing-and-Financial-Sustainability-Regulations-2026/Article-94-Squad-cost-rule-Online?contentId=ECUHs41EOPHcoQeGRa3OSA): 70%-os szabály.
- [UEFA 2026, G.3 melléklet](https://documents.uefa.com/r/UEFA-Club-Licensing-and-Financial-Sustainability-Regulations-2026/G.3-Accounting-requirements-for-the-permanent-transfer-of-a-player-s-registration-Online?contentId=mbp0thahzVgyytKVZPxyiQ): transzferek számviteli kezelése.

Ellenőrzés: 2026. szeptember 22. Az egyéb projektmutatók saját, konzultációra szánt meghatározások. A súlyok, küszöbök, oksági értelmezés és hazai jogi alkalmazás további szakmai felülvizsgálatot igényel.
