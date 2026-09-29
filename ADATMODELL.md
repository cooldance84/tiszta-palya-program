# A kutatás adatmodellje

**Közzétéve:** 2026. szeptember 29. A belső munkavázlat közlésre változatlanul átvett szövege.

## Miért nyilvános ez?

Ez a lap a kutatási adatbázis **szerkezetét és adatminőségi szabályait** írja le: milyen mezők tartoznak egy rekordhoz, milyen státuszai lehetnek egy megfigyelésnek, és mit teszünk akkor, ha egy adat hiányzik. Azért tesszük közzé, mert **a módszertan ellenőrizhetősége legalább annyira fontos, mint az eredmény** — és mert ebből látszik, milyen fegyelemmel készül az adat, amire a program állításai épülnek.

Néhány alapszabály, ami itt részletesen szerepel:

- a hiányzó adat, a nulla és a nem alkalmazható érték **három külön státusz**; nulla csak igazoló forrásból kerül be;
- a forrás kötőjele **nem** automatikus nulla;
- nyers forrássorból csak külön definíciós és beszámolásikör-egyeztetés után lesz mutató;
- a teljes pénzeszköz nem szabad pénz, a rövid lejáratú kötelezettség nem lejárt tartozás, a nettó árbevétel nem automatikus működési bevétel;
- az AI-forrásegyeztetés **nem** emberi vagy szakmai felülvizsgálat, és a rekordok státusza ezt tükrözi.

**Amit ez a lap hivatkozik, de nem tartalmaz.** A szövegben szereplő CSV-táblák (`penzugyi_alapadatok.csv`, `beveteli_egyeztetes.csv`, `forrasok.csv` és a többi), a megőrzött forrás-PDF-ek és a klubonkénti alaplapok a **belső munkarepóban** vannak, nem itt. A nyers kutatási adatok közzétételének kapuja az emberi és független szakmai felülvizsgálat, ami még nem történt meg; ezért itt a szerkezet szerepel, az adat nem.

A mutatódefiníciók gépi olvasható nyilvántartása viszont közzétéve: [mutatok.csv](mutatok.csv) és [pillerek.csv](pillerek.csv). A részletes mérési protokoll a [METODIKA_ES_MUTATOK.md](METODIKA_ES_MUTATOK.md).

---

## 0.4.1 – Az MTK egyéb bevétel bontása

A nyers tábla 336-ról **349 sorra** bővült (FTC 116, PAFC 99, MTK 134); a séma és a korábbi sorok változatlanok. A bevételi egyeztető 102-ről **115 sorra** (58 részlet, 27 maradék, 30 tájékoztató); a kontroll továbbra is 27 sor, mindegyik nulla eltéréssel.

Új `mutato_kod` értékek: `RAW_EGYEB_BEV_VISSZAIRT_ERTEKVESZTES`, `RAW_EGYEB_BEV_ESZKOZERTEKESITES`, `RAW_EGYEB_BEV_KAROK`, `RAW_EGYEB_BEV_KI_NEM_EMELT`, `RAW_AKADEMIA_TAM_FELHASZNALT`, `RAW_AKADEMIA_PLUSZ_TAM_FELHASZNALT`, `RAW_MLSZ_TAM_FELHASZNALT`, `RAW_TAO_RENDELKEZESRE_ALLO`.

Új `forras_oszlop` érték: `targyev; Rendelkezésre álló összeg` — a támogatási táblázat harmadik oszlopa. A kapott, a felhasznált és a rendelkezésre álló oszlop három külön adat; **nem összegezhetők**, és a rendelkezésre álló összeg nem az adott időszak bevétele.

**Új O/M besorolási érték: `kizart_eszkozertekesites`.** A [mérési protokoll](METODIKA_ES_MUTATOK.md) 2. része szerint az eszközeladás nem része a teljes működési bevételnek (O), ezért az eszközértékesítési sor O és M szempontból is kizárt — a `kizart_jatekosertekesites` mintájára. Új `kategoria` értékek: `ERTEKVESZTES_VISSZAIRAS`, `ESZKOZERTEKESITES`, `KAROK_RENDEZESE`, `EGYEB_KI_NEM_EMELT`, `KIEGESZITO_AKADEMIA_TAM_FELHASZNALT`, `KIEGESZITO_AKADEMIA_PLUSZ_TAM_FELHASZNALT`, `KIEGESZITO_MLSZ_TAM_FELHASZNALT`, `KIEGESZITO_TAO_RENDELKEZESRE_ALLO`.

Az `ellenorzo` mező új értéke `Claude Opus 5 (AI)`; a korábbi sorok `Codex (AI)` jelölése változatlan. Mindkettő AI-forrásegyeztetést jelent, nem emberi auditot: az `emberi_felulvizsgalo` mind a 349 sornál üres.

**Adatátvételi eljárás ezeknél a soroknál:** a PDF-oldalakat a Windows beépített renderelőjével (`Windows.Data.Pdf`) képpé alakítottuk, és az értékeket a képi oldalról olvastuk vissza. A gépi szövegkinyerés nem használható, mert a mellékletek egyedi kódolású (subset) betűtípusokat tartalmaznak; a rendelkezésre álló `en-US` OCR csak az oldalak megtalálására szolgált. **Számot OCR-ből nem vettünk át.**

## 0.4 – Külön bevételi egyeztetési nézet

A `beveteli_egyeztetes.csv` és `beveteli_egyeztetes_kontroll.csv` a meglévő nyers tábla feldolgozott nézete. A 336 nyers rekord és a korábbi CSV-sémák változatlanok. Új rekordtípus: 50 bevételi részlet, 27 számított maradék, 25 nem összegezhető tájékoztató sor; a kontroll 27 eredménykimutatási bevételi főösszeget követ.

A részletsor `alap_adat_id` mezője a nyers rekordra mutat. A maradék alapja a `fo_sor_adat_id` szerinti főösszeg, amelyből a `kivont_adat_idk` mezőben `|` jellel elválasztott rekordokat vonjuk le. A `szamitas` olvasható leírás, nem futó Excel-képlet. A tájékoztató sorok kapcsolt keresztmetszetek, támogatási nézetek vagy állományok; nem növelik a bevételt.

A kategória, elszámolási nézet, O/M-kezelés, finanszírozói eredet, kapcsoltság és visszatérő jelleg külön mező. Definícióverzió: `BEV_EGY_0.1`; státusz: `AI_besorolas_felulvizsgalando`. Az emberi felülvizsgáló üres. A nyers adat AI-forrásegyeztetése nem jelenti az új gazdasági besorolás jóváhagyását.

A kontroll részletösszege és maradéka együtt adja a forrásfőösszeget. A nulla eltérés önmagában nem jelzi az O/M besorolás teljességét. A részletes mezőértelmezés, hiánylista és frissítési rend a belső bevételi jegyzetben található; az belső ellenőrző program a forráskapcsolatokat és számításokat vizsgálja.

## A korábbi nyers adatmodell megőrzött szabályai

**Frissítés:** 2026-09-22. A 0.1-es törzs- és szezonos táblák megmaradnak. A 0.2 külön pénzügyi forrástáblát vezetett be; a 0.3 ezt PAFC- és MTK-adatokkal bővíti, az oszlopok módosítása nélkül. Az üzleti évet nem nevezzük át szezonná.

## Nyers pénzügyi alapadatok – 0.2

A `penzugyi_alapadatok.csv` egy sora egy jogi személy, egy üzleti időszak és egy forrássor pontosan azonosított adata. A törzsadatokhoz a `klub_id`, a forráskatalógushoz a `forras_id` kapcsolja. A jogi entitások: `FTC_ZRT` (FTC), `PAFC_KFT` (Puskás Akadémia), `MTK_ZRT` (MTK). A `RAW_` kódok forrástételek, nem a `mutatok.csv` projekt-KPI-azonosítói. Az alapítványi körforrás nem jelent betöltött alapítványi pénzügyi sort.

| Mezőcsoport | Mezők és értelmezés |
|---|---|
| Azonosítás | `adat_id` egyedi; `klub_id`; `jogi_entitas_id`; `jogi_entitas_nev`; `cegjegyzekszam`; `beszamolasi_kor`. |
| Idő | `idoszak_tipus`: `uzleti_evi_forgalom` vagy `ev_vegi_allomany`; `idoszak_kezdet`, `idoszak_vege`. Állománynál az érték a zárónapra szól, a kezdőnap a hozzá tartozó beszámolási év kezdete. |
| Adat | `mutato_kod`; `forras_sor_megnevezes`; `ertek`; `mertekegyseg`; `afa_kezeles`. A jelen értékek nominális egész számok ezer HUF-ban; M Ft = ezer HUF / 1000. |
| Forráshely | `forras_id`; `forras_oldal` az 1-től számított PDF-oldal; `forras_oszlop`: tárgyév vagy az előző év összehasonlító oszlopa. Az URL és a fájllenyomat a forráskatalógusban. |
| Definíció | `definicio_verzio`: `FTC_RAW_0.1`, `PAFC_RAW_0.1` vagy `MTK_RAW_0.1`; eredeti beszámolói sor, nem egységesített klubközi KPI. Az alsorok és a főösszegek nem összegezhetők újra. |
| Ellenőrzés | `hozzaferes_datum`; `adatminoseg`; `statusz`; `atvetel_statusz`; `ellenorzo`; `ellenorzes_datum`; `emberi_felulvizsgalo`; `emberi_felulvizsgalat_datum`; `megjegyzes`. |

Jelenlegi állapot: `adatminoseg=hivatalos_elsodleges`, `statusz=ellenorzendo`, `atvetel_statusz=forraskeppel_egyeztetett_AI`. Az ellenőrző **Codex (AI)**, nem emberi auditor. Az emberi mezők üresek, amíg nincs tényleges felülvizsgálat. A számtani egyezés önmagában nem teszi a sort szakmailag validálttá.

Adatátvételkor OCR segítheti a keresést, de számot a PDF képi oldalával egyeztetünk. Ellenőrzendő a személyi részösszeg, az eredménylevezetés, a mérlegegyezőség és az időszak. Forráseltérést az alaplapon dokumentálunk; az eredeti számot nem javítjuk becsléssel.

Hiányt nem töltünk nullával. A forrás kötőjele nem automatikus nulla; nulla csak kifejezett forrásértékből kerül be. Nyers forrássorból KPI csak külön definíciós és beszámolásikör-egyeztetés, valamint az ellenőrzési státusz felülvizsgálata után készülhet. A teljes pénzeszköz nem szabad pénz; a rövid kötelezettség nem lejárt tartozás; a nettó árbevétel nem automatikus működési bevétel.

### Forrásállítások kiegészített státusza

A `bizonyitekok.csv` új `bizonyitottsag=forras_egyeztetett_AI` értéke azt jelenti, hogy az állítás a konkrét forráshelyhez visszaolvasással kapcsolható. Emberi és szakmai ellenőrzése még függőben van; nem bizonyított modellhatás. Az `FTC_A001`–`FTC_A008` a mostani alaplap helyi állításazonosítói, az állítás szövege ugyanebben a táblában található. A `mutato_id` az érintett kutatási témát jelöli, nem egy elkészült mutatóértéket.

A `forrasok.csv` régi, általános keresőoldal-bejegyzései megmaradnak. Az új dokumentumbejegyzések `datum` mezője a dokumentum keltezése, a `letoltes_datum` a tényleges hozzáférés napja, a `forras_hash` a letöltött PDF SHA-256 lenyomata. A hash az adott fájl ellenőrzésére szolgál, önmagában nem hiteles időbélyeg.

### Forrásmegőrzés – 2026-09-23

Három új oszlop; a korábbi 9 mező és minden értékük változatlan.

| Mező | Tartalom |
|---|---|
| `helyi_fajl` | A megőrzött példány útvonala: `forrasok/pdf/<forras_id>.pdf`. Üres az általános katalógussoroknál, amelyekhez nem tartozik letöltött dokumentum. |
| `helyi_hash_ellenorizve` | Az a nap, amikor a helyi fájl SHA-256 lenyomatát a `forras_hash` ellen ellenőriztük. Üres érték azt jelenti, hogy nem történt ellenőrzés — nem azt, hogy megbukott. |
| `archiv_url` | Független webarchívum-pillanatkép URL-je, ha van. Üres érték nem jelent hiányzó forrást; a helyi megőrzés és a `forras_hash` attól még érvényes. |

A `helyi_fajl` a hash által igazolt konkrét példány. A `forras_hash` addig csak egy állítás volt egy sehol nem tárolt fájlról; a megőrzött példánnyal válik ellenőrizhetővé. Az ellenőrzés bármikor megismételhető: `sha256sum forrasok/pdf/<forras_id>.pdf` a `forras_hash` `sha256:` előtag nélküli értékével kell egyezzen.

Ha egy forrás URL-je később más tartalmat ad vissza, az **nem** a helyi példány hibája: az eltérést rögzíteni kell, a helyi példányt megőrizni, és az érintett rekordok összehasonlíthatósági státuszát felülvizsgálni. A helyi fájlt nem írjuk felül az új letöltéssel.

### A 0.3-as betöltés szabályai

- 336 pénzügyi sor: FTC 116, PAFC 99, MTK 121. A korábbi FTC-adatok és azonosítók változatlanok.
- 31 forráskatalógus-sor: 23 konkrét PDF és 8 általános forrásbejegyzés. A két új klubarchívum-bejegyzés nem jelent új pénzügyi rekordot. Ha egy csomaghoz nem rögzítettünk egységes keltezést, a `datum` üres, ennek oka a megjegyzésben szerepel; a hozzáférési dátum és a hash ettől még kötelező a konkrét PDF-eknél.
- Új helyi állításazonosítók: `PAFC_A001`–`PAFC_A006`, `MTK_A001`–`MTK_A008`; összesen 22 állítás–forrás kapcsolat. Az ellenőrzési státusz mindegyiknél AI-forrásegyeztetés, nem modellhatás-igazolás.
- Az MTK üres céltartalék-, hosszú lejáratú és hátrasorolt kötelezettségsora nem kerül be nullaként. A PAFC kifejezetten közölt nullái átvehetők.
- `RAW_JOG_NEM_AKTIVALT` és `RAW_JATEKOS_ERTEKESITES` eltérő eredeti bevételi címkék; nem egyetlen nettó transzfereredmény-mutató. A `RAW_UEFA` általános címke nem automatikusan kupaszereplési díj.
- A támogatási `KAPOTT` és `FELHASZNALT` kódok a melléklet külön oszlopai. A `forras_oszlop` ilyenkor például `targyev; Kapott támogatás`. A `RAW_MUKODESI_TAM` az eredményben elszámolt másik nézet; ezek nem összegezhetők. A halasztott bevétel és részei állományadatok.
- Egy forrássor nevét csak helyesírási/rövidítési szinten írjuk át olvasható formára; gazdasági jelentését nem bővítjük. Számtani vagy besorolási eltérés esetén az éves ER/mérleg főösszege a nyers bázis, az eltérő mellékletérték az alaplap DQ-jegyzékében marad.
- A `klubok.csv` liga mezője leíró törzsadat, nem szezonos versenyadat. MTK: `NB I / NB II`; a 2022/23-as NB II-es szezon külön elsődleges forrással igazolt.

A belső háromklubos jegyzet rögzíti a használható leíró összevetéseket és a még hiányzó egységesítést. A szezonos KPI-tábla üres marad; nincs rangsor vagy súlyozás.

## Törzsadatok

### `klubok.csv`

- `klub_id`: stabil belső azonosító
- `klub_nev`: hivatalos klubnév
- `orszag`, `liga`
- `klubtipus`: egyesület, gazdasági társaság, vegyes vagy ismeretlen
- `megjegyzes`

### `szezonok.csv`

- `szezon_id`: például `2024_25`
- `szezon_megnevezes`
- `kezdet`, `vege`

### `pillerek.csv`

A négy vizsgálati pillér:

1. közösségi kontroll és klubirányítás;
2. bevételarányos költségfegyelem;
3. utánpótlás és játékosút;
4. piaci és közösségi bevételek.

### `mutatok.csv`

Minden mutatóhoz kötelező:

- egyértelmű definíció;
- mértékegység;
- számítási szabály;
- adatforrás-típus;
- adatvédelmi és összehasonlíthatósági megjegyzés.

## Megfigyelések

A `megfigyelesek.csv` egy sora egy klub–szezon–mutató megfigyelés. A `statusz` értéke lehet:

- `tervezet`
- `forrasra_var`
- `ellenorzendo`
- `ellenorzott`
- `nem_osszehasonlithato`
- `nem_elerheto`

Az `adatminoseg` értékei:

- `hivatalos_elsodleges`
- `hivatalos_masodlagos`
- `megbizhato_masodlagos`
- `becsles`
- `hipotezis`
- `hianyzo`

## Forrás és bizonyíték

Egy állítás nem tekinthető ellenőrzöttnek pusztán azért, mert szerepel egy forrásjegyzékben. A `bizonyitekok.csv` kapcsolja össze az állítást, a forrást, az érintett mutatót és az ellenőrzés státuszát.

## Pontozás

Ebben a verzióban nincs összpontszám és nincs klubrangsor. A súlyozást csak a definíciók, az adatminőség és a TF szakmai véleménye után szabad kialakítani.


## Előzmény: 2026-09-22 - A mérési definíciók pontosítása

A [0.9.2-j1 módszertani protokoll](METODIKA_ES_MUTATOK.md) rögzíti a mutatóazonosítók részletes értelmezését, időszakát, nevezőjét, adatgazdáját és hiánykezelését. A `mutatok.csv` törzsdefiníciói ehhez igazodnak; státuszuk továbbra is tervezet, a TF szakmai visszajelzése még szükséges. Új ellenőrzött megfigyelés vagy bizonyítéksor ebben a javításban nem keletkezett.

A 0.2-es pénzügyi tábla már tartalmazza a jogi/beszámolási kört, időszakkezdést és -véget, definícióverziót, hozzáférési dátumot, oldalszintű forráshelyet, ellenőrzőt és ellenőrzési dátumot. A szezonos `megfigyelesek.csv` sémáját annak első tényleges adatbetöltése előtt ugyanígy bővíteni kell. A labdarúgó-szezon és az üzleti év nem feleltethető meg egymásnak automatikusan.
