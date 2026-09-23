# Változásnapló

A formátum a Keep a Changelog elveit követi. A projekt jelenleg előzetes, konzultációs szakaszban van.

## [Nem kiadott]

- A 0.9.3-as esettanulmány előkészítése, klubadatok gyűjtése és a szakmai visszajelzések feldolgozása.

### 2026-09-23 – Kiegészítés: a Puskás Akadémia bevételi bontása nyilvános forrásból nem érhető el

- A [szeptember 23-i helyzetjelentés](KUTATASI_STATUSZ_2026-09-23.md) új 8. pontja: a társaság 2022–2024-es három beszámolócsomagjának teljes átnézése (65 oldal) után a bevételi jogcímbontás **nem feltárási hiány, hanem a nyilvános közzététel felső határa**.
- Az eredménykimutatás az árbevételt egyetlen belföldi sorban közli, az export sor mindhárom évben nulla; a kiegészítő melléklet szöveges, és nincs benne szponzori, reklám-, média-, jegy-, játékosértékesítési vagy TAO-bevételi tétel.
- Következmény az összehasonlíthatóságra: a vizsgált három társaságból egynél a saját bevételi arány, a bevételi diverzifikáció és a szponzori koncentráció **ebből a forráskörből nem számítható**.
- A társaságnak mindhárom évben nulla export árbevétele van, míg az FTC-nél van export szponzoráció és export tv-jogdíj.
- Az eredeti 7. pont sorrendje javítva: az FTC összevont bevételi sorainak szétválasztása lett a legfontosabb nyitott bevételi feladat.

A megállapítást **külön pontban** közöljük, nem az eredeti szöveg átírásával, mert a változás követhetősége maga is része az átláthatóságnak. A módszertani dokumentum, a mutatódefiníciók és a pénzügyi modell nem változott. A kiadás továbbra is 0.9.2-j1.

### 2026-09-23 – Forrásintegritás, MTK bevételi feltárás és forrásjegyzék

- Új [kutatási helyzetjelentés](KUTATASI_STATUSZ_2026-09-23.md): a 23 elsődleges forrás SHA-256 lenyomata újraellenőrizve (23/23 egyezik), és a 22 Internet Archive-mentés bájtra azonos a lenyomatokkal.
- Az MTK egyéb bevételének felosztása: 2023-ra és 2024-re a maradék nullára zárt; 2022-re 3 237 E Ft marad, mert a forrás maga nem bontja fel.
- A támogatási átvezetés pontosodott: a 2023-as 73 137 E Ft-os kapott–felhasznált különbözetet teljes egészében a TAO-jogcím viszi.
- Három forráseltérés rögzítve, kifejezetten nem számviteli szabálytalanságra vonatkozó megállapításként.
- Új [elsődleges forrásjegyzék](FORRASJEGYZEK.md): 23 dokumentum közzétételi hellyel, keltezéssel, letöltési dátummal és teljes SHA-256 lenyomattal, valamint az ellenőrzés reprodukálható menetével.
- Két módszertani rögzítés: az eszközeladás a mérési protokoll szerint nem része a teljes működési bevételnek (O); a pénzügyi értékek a renderelt PDF-oldalról visszaolvasva kerültek be, optikai karakterfelismerésből szám nem került átvételre.
- A [szeptember 22-i helyzetjelentés](KUTATASI_STATUSZ.md) változatlanul megmarad a stabil hivatkozás miatt, és előre-hivatkozást kapott az újabb lapra.
- Az [állítás–forrás mátrix](ALLITAS_FORRAS_MATRIX.md) hat új, forrásalapú sorral bővült (0.4).
- A [felhasználási és módszertani nyilatkozat](FELHASZNALASI_ES_MODSZERTANI_NYILATKOZAT.md) AI-szakasza pontosítva: az adatátvétel is AI-val támogatott, nem csak az előkészítés és szerkesztés.

A számtani felosztás lezárása **nem** önfenntarthatósági eredmény: a gyűjtősorok gazdasági tartalma, a finanszírozó eredete és az egységes működési bevételi nevező továbbra is nyitott. A nyers kutatási adatok emberi és független szakmai felülvizsgálata nem történt meg, és a részletes táblák a belső munkaváltozatban maradnak. A programkiadás továbbra is 0.9.2-j1.

### 2026-09-22 – Nyilvános kutatási helyzetjelentés

- Új [kutatási státusz](KUTATASI_STATUSZ.md) az FTC, a Puskás Akadémia és az MTK 2022–2024-es előzetes pénzügyi feldolgozásáról.
- Szervezeti, bevételi és időszaki összehasonlíthatósági korlátok, a négy pillér adatfedettsége és a következő lépések összefoglalva, nyilvános elsődleges forrásokkal.
- Az AI-val támogatott adatátvétel és a még hiányzó független szakmai felülvizsgálat egyértelműen jelölve.
- README-hivatkozás és a modellfeltételezések elkülönítése a kutatás állapotától.

A részletes nyers adatok és az egyeztetendő számszaki eltérések a belső munkaváltozatban maradnak. Nincs új klubrangsor, politikai függőségi minősítés vagy igazolt önfenntartási következtetés. A programkiadás továbbra is 0.9.2-j1.

## [0.9.2-j1] - 2026-09-22

### Javítva

- a 3 400 M Ft-os bázis összetétele és a 2 400 M Ft-os működési forráscsökkentés egységesítve;
- 0-5. évi eredmény- és költségpálya, külön cash-flow híd, pótlólagos finanszírozási igény és végponti érzékenység;
- a transzfereredmény korábbi kettős költséglevonása megszüntetve; eladási eredmény, időszaki eredmény és pénzáramlás külön definiálva;
- saját bevétel, UEFA-ráta, nyers/súlyozott perc, kohorsz, közösségi befolyás és hiánykezelés pontosítva;
- a 6-12 hónapos megvalósíthatósági pilot elválasztva a 3-5 éves utánkövetéstől; realizált bevétel és jövőbeli szerződés külön;
- egységes 0.9.2-j1 borító, fejléc, metaadat és oldalszám; 27 oldalas fő PDF, TXT és egyoldalas összefoglaló.

### Hozzáadva

- `METODIKA_ES_MUTATOK.md`, `PENZUGYI_MODELL.md`, ellenőrizhető JSON-bemenet és reprodukálható kiadási script;
- UEFA 2026 elsődleges szabályhivatkozások a költségrátához és a transzferek elszámolásához;
- a korábbi PDF-ek történeti státuszának egyértelmű jelölése a README-ben.

A javítás nem új klubadat-betöltés, nem külső szakmai validáció és nem a 0.9.3-as esettanulmány lezárása.

## Korábbi munkabejegyzések (0.9.2 után)

Az alábbi bejegyzések a korábbi munkafázist őrzik. Az aktuális javításokat a 0.9.2-j1 szakasz rögzíti; a régi verzió- és oldalszámok történeti adatok.

### Hozzáadva

- 0.1-es nyilvános állítás–forrás mátrix 34 ellenőrzési ponttal és bizonyítottsági jelöléssel
- első prioritású adat-, forrás- és jogi felülvizsgálati hiánylista
- a 0.9.2-es konzultációs változat egyoldalas vezetői összefoglalója Markdown- és PDF-formátumban

### Módosítva

- a Vidi-utánpótlási felvetés semleges, ellenőrizhető kutatási kérdésként szerepel
- az edzőkre vonatkozó általános minősítés helyett mérhető edzőkiválasztási, továbbképzési és teljesítményértékelési kérdés került a mátrixba
- a README rögzíti az SZTNH-megkeresés megtörténtét és hivatkozik az állítás–forrás mátrixra

## [0.9.2] – 2026-09-19

### Hozzáadva

- az edzői minőséget rendszerszintű utánpótlási tényezőként kezelő alfejezet
- kompetenciaalapú edzőkiválasztási, továbbképzési és értékelési minimumrendszer
- az akadémiai eredményesség hatdimenziós KPI-táblája
- a Vidi-szurkolói tapasztalat ellenőrizhető kutatási hipotézissé alakítása
- FIFA-, HNS-, Real Madrid- és CIES-források az utánpótlási fejezethez

### Módosítva

- a dokumentum 22 oldalról 24 oldalra bővült
- a horvát, szerb és spanyol példák állításai bizonyíthatósági korlátot kaptak
- az „új edzők kellenek” felvetést átlátható szakmai minőségi kapuvá fogalmaztuk át

## [0.9.1] – 2026-09-19

### Javítva

- a szerző neve minden dokumentumban egységesen **Kiss Tiborcz**

## [0.9] – 2026-09-19

### Hozzáadva

- 22 oldalas konzultációs dokumentum
- a konzultációs PDF kereshető szöveges változata
- nyilvános projektstruktúra, verziózási szabály és döntési napló
- felhasználási és módszertani nyilatkozat

### Módosítva

- a kategorikus állítások vizsgálandó hipotézisekké alakítása
- a fix összegű bérplafon helyett bevételarányos keretszabály vizsgálata
- a nemzetiségi kvóta helyett hazai neveléshez és játékperchez kötött ösztönzők vizsgálata
- a pénzügyi modell elkülönítése tényadatokra és forgatókönyv-feltételezésekre


