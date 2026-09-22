# Ellenőrizhető pénzügyi példa

**Verzió:** 0.9.2-j1. **Dátum:** 2026. szeptember 22.

**Minden bemeneti összeg saját modellfeltételezés. Nem magyar klubadat, nem NB I-átlag és nem előrejelzés.** Az éves pálya a számtani összefüggéseket és a lehetséges finanszírozási hiányt teszi ellenőrizhetővé.

## Kiindulás és mértékegység

A 0. év 3 400 M Ft eredményfedezete: 2 400 M Ft köz-/államközeli működési bevétel + 500 M Ft piaci működési bevétel + 500 M Ft játékoseladási eredmény. Az eladási eredmény nem teljes transzferbevétel és nem szabad pénz. A modellezett működési forráscsökkentés 2 400 M Ft.

Egység: millió forint, 2026-os változatlan árszint, nettó ÁFA nélküli bemenetek. A 0. év is szemléltető bázis.

## Eredményszemléletű pálya

| Mutató, M Ft | 0. év | 1. év | 2. év | 3. év | 4. év | 5. év |
|---|---|---|---|---|---|---|
| Köz-/államközeli működési bevétel | 2 400 | 1 920 | 1 440 | 960 | 480 | 0 |
| Piaci működési bevétel | 500 | 700 | 950 | 1 250 | 1 600 | 1 900 |
| Játékoseladási eredmény | 500 | 500 | 550 | 600 | 700 | 800 |
| Összes eredményfedezet | 3 400 | 3 120 | 2 940 | 2 810 | 2 780 | 2 700 |
| Működési költség amortizációval | 3 400 | 3 200 | 3 000 | 2 800 | 2 600 | 2 500 |
| Egyszerűsített időszaki eredmény | 0 | -80 | -60 | 10 | 180 | 200 |

Eredményfedezet = köz-/államközeli működési bevétel + piaci működési bevétel + eladási eredmény. Időszaki eredmény = eredményfedezet - működési költség. Ez egyszerűsített modell, nem teljes számviteli eredménykimutatás.

## Pénzforgalmi pálya és hiány

| Mutató, M Ft | 0. év | 1. év | 2. év | 3. év | 4. év | 5. év |
|---|---|---|---|---|---|---|
| Eladási ellenérték befolyása | 850 | 850 | 900 | 950 | 1 050 | 1 150 |
| Közvetlen eladási díjfizetés | 50 | 50 | 50 | 50 | 50 | 50 |
| Játékosbeszerzés kifizetése | 500 | 600 | 600 | 650 | 650 | 650 |
| Nettó transzfer-pénzáramlás | 300 | 200 | 250 | 250 | 350 | 450 |
| Készpénzes működési kiadás | 3 200 | 3 000 | 2 800 | 2 600 | 2 400 | 2 300 |
| Egyéb beruházási kifizetés | 0 | 50 | 50 | 50 | 50 | 50 |
| Pénzváltozás új finanszírozás előtt | 0 | -230 | -210 | -190 | -20 | 0 |
| Elméleti záró pénz pótlás nélkül | 200 | -30 | -240 | -430 | -450 | -450 |
| Éves pótlólagos igény 200-as pufferhez | 0 | 230 | 210 | 190 | 20 | 0 |
| Halmozott finanszírozási igény | 0 | 230 | 440 | 630 | 650 | 650 |

Nyitó szabad pénz: 200 M Ft. Elvárt záró puffer: 200 M Ft, szintén feltételezés. A negatív elméleti záró pénz kielégítetlen finanszírozási igény, nem tényleges negatív készpénzállomány. A puffer fenntartásához 650 M Ft pótlólagos forrás kellene; puffer nélkül, a nem negatív éves pénzállományhoz 450 M Ft. Egyik forrás rendelkezésre állása sincs igazolva.

A cash-flow híd: időszaki eredmény + 200 M Ft amortizáció + 300 M Ft kivezetett könyv szerinti érték - játékosbeszerzés - egyéb beruházás. Az eladási díj már az eladási eredményben szerepel, nem vonjuk le másodszor. Az eladási ellenérték = eladási eredmény + könyv szerinti érték + eladási díj. A közvetlen pénzáramlás és a híd minden évben egyezik.

A regisztrációk könyv szerinti értékének ellenőrző hídja: 1 000 M Ft induló állomány + aktivált beszerzés - amortizáció - kivezetett érték. Az évenkénti záró értékek: 1 000, 1 100, 1 200, 1 350, 1 500, 1 650 M Ft. Az összesített amortizáció szerződésenkénti kalibrációja még szükséges.

## Három lehetséges 5. évi végpont

| Eset | Piaci bevétel | Eladási eredmény | Eredményfedezet | Időszaki eredmény | Pénzváltozás |
|---|---|---|---|---|---|
| Konzervatív | 1 600 | 600 | 2 200 | -300 | -500 |
| Központi | 1 900 | 800 | 2 700 | 200 | 0 |
| Optimista | 2 400 | 1 100 | 3 500 | 1 000 | 800 |

Egység: M Ft. Közös költség 2 500, amortizáció 200, kivezetett érték 300, játékosbeszerzés 650, egyéb beruházás 50; működési köz-/államközeli bevétel nulla. A konzervatív és optimista eset végponti érzékenység, nem külön kidolgozott ötéves pálya.

## Stressz és következtetés

Ha az 5. évben nincs játékoseladás, és az egyéb bemenetek nem változnak, 1 100 M Ft nettó eladási pénz marad el. A modell éves pénzváltozása így -1 100 M Ft. Eladás nélkül könyv szerinti kivezetést és eladási díjat sem számolunk. Ez szemléltető stressz, nem becsült valószínűség.

A támogatási láb nullára futtatása ebben a modellben sem bizonyítja az önálló gazdálkodás megvalósíthatóságát. A központi eset pozitív 5. évi eredménye mellett az átmenetben pótlólagos forrás kell, és az 5. év szabad pénzáramlása nulla. Valós döntéshez havi pénzforgalom, stresszteszt, igazolt forrás és költségalkalmazkodás szükséges.

## Feltételezések és nyitott tételek

- A működési bevételek és a készpénzes működési költségek az adott évben befolynak, illetve kifizetésre kerülnek.
- A transzferellenérték és a közvetlen díjak elszámolása és pénzügyi rendezése ugyanabban az évben történik. Nincs részletfizetés, feltételes bónusz vagy követelésváltozás.
- Az eredményfedezet a működési bevétel és az eladási eredmény összege; nem számviteli árbevétel és nem pénzállomány.
- A működési költség tartalmazza az időszaki 200 M Ft játékosamortizációt, de nem tartalmazza a transzfereredményben már levont könyv szerinti értéket és eladási díjakat.
- A játékosbeszerzéseket aktiváljuk. A keret könyv szerinti értékének mozgását külön ellenőrizzük, az éves amortizáció még nem szerződésenként számított adat.
- A beruházások vizsgálati horizonton belüli amortizációja, az egyéb nem pénzbeli korrekció, a forgótőkeváltozás, a nettó ÁFA-pénzmozgás, az adó, a kamat és a régi hitel törlesztése nulla feltételezés. Valós klubnál külön felvenni szükséges.
- A szükséges pótlólagos finanszírozás formája és forrása még nincs megadva. Hitel esetén a kamatot és törlesztést újra kell modellezni; a hiány kimutatása nem finanszírozási ígéret.
- A 200 M Ft minimum pénzpuffer és minden bevételi, költség- és beruházási pálya belső feltételezés. A korábbi 2,5 Mrd Ft küszöb itt kizárólag az 5. év költségfeltételezése.
- A támogatáscsökkentés egy stresszelt szemléltető pálya, nem javasolt automatikus kivezetési ütem. Csak az itt modellezett profi működési lábat érinti.

## Újraszámítás

Bemenet: [modellparaméterek](modellek/penzugyi_pelda_0_9_2_j1.json). Előállító: [build_revision_092_j1.py](scripts/build_revision_092_j1.py). A `calculate` függvény és a PDF/Markdown táblák ugyanabból a bemenetből készülnek. A tényszámok későbbi betöltése külön verzió és dokumentált forrás nélkül nem végezhető el.

Számviteli fogalmak és források: [Módszertan és mutatók](METODIKA_ES_MUTATOK.md).
