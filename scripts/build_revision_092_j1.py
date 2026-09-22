#!/usr/bin/env python3
"""A 0.9.2-j1 kiadás előállítása a megőrzött 0.9 PDF-ből és a modellből.

Futtatás a repó gyökerében: python scripts/build_revision_092_j1.py
Függőségek: PyMuPDF, reportlab. DejaVu Sans fontok szükségesek;
eltérő telepítésnél a TPP_FONT_DIR környezeti változó adható meg.
A régi fájlokat nem írja felül. A nem javított tartalmi oldalakat megőrzi.
Ez a rögzített kiadás előállítója, nem általános előrejelző. A modell megváltoztatása
új verziót és a számokat értelmező szövegek felülvizsgálatát igényli.
"""
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape
import hashlib
import json
import os
import re

import fitz
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.9.2-j1'
SUFFIX = '0_9_2_j1'
MODEL_SHA256 = 'e52ede4b45224f453ff50daaea60864707ccacddbabbcee04f00d76d85a4839c'
BASE = ROOT / 'dokumentumok/Tiszta_Palya_Program_konzultacios_valtozat_0_9.pdf'
FONT_DIR = Path(os.environ.get('TPP_FONT_DIR', '/usr/share/fonts/truetype/dejavu'))
FONT = FONT_DIR / 'DejaVuSans.ttf'
NAVY = colors.HexColor('#17324F')
TEAL = colors.HexColor('#007D7B')
TEXT = colors.HexColor('#24384D')
WIDTH = A4[0] - 112
UEFA = 'https://documents.uefa.com/r/UEFA-Club-Licensing-and-Financial-Sustainability-Regulations-2026/'


def calculate(m):
    out = []
    cash = m['opening_unrestricted_cash']
    unfunded_cash = cash
    total_finance = 0
    player_assets = m['initial_player_book_value']
    for i, year in enumerate(m['years']):
        public = m['public_related_operating_income'][i]
        market = m['market_operating_income'][i]
        gain = m['disposal_profit'][i]
        cost = m['operating_expenses_including_amortisation'][i]
        amort = m['player_amortisation'][i]
        nbv = m['disposed_registrations_book_value'][i]
        fees = m['direct_disposal_fees'][i]
        purchase = m['player_acquisition_payments'][i]
        capex = m['other_capex_payments'][i]
        proceeds = gain + nbv + fees
        coverage = public + market + gain
        result = coverage - cost
        transfer_cash = proceeds - fees - purchase
        cash_expense = cost - amort
        flow = public + market - cash_expense + transfer_cash - capex
        bridge = result + amort + nbv - purchase - capex
        assert flow == bridge, (year, flow, bridge)
        unfunded_cash += flow
        gap = max(0, m['minimum_cash_buffer'] - cash - flow)
        total_finance += gap
        cash += flow + gap
        player_assets += purchase - amort - nbv
        assert player_assets >= 0
        out.append(dict(year=year, public=public, market=market, gain=gain,
                        coverage=coverage, cost=cost, result=result, amort=amort,
                        nbv=nbv, proceeds=proceeds, fees=fees, purchase=purchase,
                        capex=capex, transfer_cash=transfer_cash,
                        cash_expense=cash_expense, cash_flow=flow,
                        unfunded_cash=unfunded_cash, gap=gap,
                        cumulative_finance=total_finance, funded_cash=cash,
                        player_assets=player_assets))
    return out


def value(n):
    return f'{n:,.0f}'.replace(',', ' ')


def md_table(headers, rows):
    return '\n'.join(['| ' + ' | '.join(headers) + ' |',
                       '|' + '|'.join(['---'] * len(headers)) + '|'] +
                      ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows])


def financial_tables(rows):
    head = ['Mutató, M Ft'] + [f"{r['year']}. év" for r in rows]
    def lines(items):
        return [[label] + [value(r[key]) for r in rows] for label, key in items]
    accrual = lines([
        ('Köz-/államközeli működési bevétel', 'public'),
        ('Piaci működési bevétel', 'market'),
        ('Játékoseladási eredmény', 'gain'),
        ('Összes eredményfedezet', 'coverage'),
        ('Működési költség amortizációval', 'cost'),
        ('Egyszerűsített időszaki eredmény', 'result'),
    ])
    cash = lines([
        ('Eladási ellenérték befolyása', 'proceeds'),
        ('Közvetlen eladási díjfizetés', 'fees'),
        ('Játékosbeszerzés kifizetése', 'purchase'),
        ('Nettó transzfer-pénzáramlás', 'transfer_cash'),
        ('Készpénzes működési kiadás', 'cash_expense'),
        ('Egyéb beruházási kifizetés', 'capex'),
        ('Pénzváltozás új finanszírozás előtt', 'cash_flow'),
        ('Elméleti záró pénz pótlás nélkül', 'unfunded_cash'),
        ('Éves pótlólagos igény 200-as pufferhez', 'gap'),
        ('Halmozott finanszírozási igény', 'cumulative_finance'),
    ])
    return head, accrual, cash


def write_model_note(m, rows):
    head, accrual, cash = financial_tables(rows)
    scenarios = []
    for s in m['year5_scenarios']:
        coverage = s['market_operating_income'] + s['disposal_profit']
        result = coverage - rows[-1]['cost']
        flow = result + rows[-1]['amort'] + rows[-1]['nbv'] - rows[-1]['purchase'] - rows[-1]['capex']
        scenarios.append([s['name'], value(s['market_operating_income']), value(s['disposal_profit']), value(coverage), value(result), value(flow)])
    txt = '# Ellenőrizhető pénzügyi példa\n\n'
    txt += f'**Verzió:** {VERSION}. **Dátum:** 2026. szeptember 22.\n\n'
    txt += '**Minden bemeneti összeg saját modellfeltételezés. Nem magyar klubadat, nem NB I-átlag és nem előrejelzés.** Az éves pálya a számtani összefüggéseket és a lehetséges finanszírozási hiányt teszi ellenőrizhetővé.\n\n'
    txt += '## Kiindulás és mértékegység\n\nA 0. év 3 400 M Ft eredményfedezete: 2 400 M Ft köz-/államközeli működési bevétel + 500 M Ft piaci működési bevétel + 500 M Ft játékoseladási eredmény. Az eladási eredmény nem teljes transzferbevétel és nem szabad pénz. A modellezett működési forráscsökkentés 2 400 M Ft.\n\n'
    txt += 'Egység: millió forint, 2026-os változatlan árszint, nettó ÁFA nélküli bemenetek. A 0. év is szemléltető bázis.\n\n'
    txt += '## Eredményszemléletű pálya\n\n' + md_table(head, accrual) + '\n\n'
    txt += 'Eredményfedezet = köz-/államközeli működési bevétel + piaci működési bevétel + eladási eredmény. Időszaki eredmény = eredményfedezet - működési költség. Ez egyszerűsített modell, nem teljes számviteli eredménykimutatás.\n\n'
    txt += '## Pénzforgalmi pálya és hiány\n\n' + md_table(head, cash) + '\n\n'
    txt += 'Nyitó szabad pénz: 200 M Ft. Elvárt záró puffer: 200 M Ft, szintén feltételezés. A negatív elméleti záró pénz kielégítetlen finanszírozási igény, nem tényleges negatív készpénzállomány. A puffer fenntartásához 650 M Ft pótlólagos forrás kellene; puffer nélkül, a nem negatív éves pénzállományhoz 450 M Ft. Egyik forrás rendelkezésre állása sincs igazolva.\n\n'
    txt += 'A cash-flow híd: időszaki eredmény + 200 M Ft amortizáció + 300 M Ft kivezetett könyv szerinti érték - játékosbeszerzés - egyéb beruházás. Az eladási díj már az eladási eredményben szerepel, nem vonjuk le másodszor. Az eladási ellenérték = eladási eredmény + könyv szerinti érték + eladási díj. A közvetlen pénzáramlás és a híd minden évben egyezik.\n\n'
    txt += 'A regisztrációk könyv szerinti értékének ellenőrző hídja: 1 000 M Ft induló állomány + aktivált beszerzés - amortizáció - kivezetett érték. Az évenkénti záró értékek: ' + ', '.join(value(r['player_assets']) for r in rows) + ' M Ft. Az összesített amortizáció szerződésenkénti kalibrációja még szükséges.\n\n'
    txt += '## Három lehetséges 5. évi végpont\n\n'
    txt += md_table(['Eset', 'Piaci bevétel', 'Eladási eredmény', 'Eredményfedezet', 'Időszaki eredmény', 'Pénzváltozás'], scenarios) + '\n\n'
    txt += 'Egység: M Ft. Közös költség 2 500, amortizáció 200, kivezetett érték 300, játékosbeszerzés 650, egyéb beruházás 50; működési köz-/államközeli bevétel nulla. A konzervatív és optimista eset végponti érzékenység, nem külön kidolgozott ötéves pálya.\n\n'
    txt += '## Stressz és következtetés\n\nHa az 5. évben nincs játékoseladás, és az egyéb bemenetek nem változnak, 1 100 M Ft nettó eladási pénz marad el. A modell éves pénzváltozása így -1 100 M Ft. Eladás nélkül könyv szerinti kivezetést és eladási díjat sem számolunk. Ez szemléltető stressz, nem becsült valószínűség.\n\n'
    txt += 'A támogatási láb nullára futtatása ebben a modellben sem bizonyítja az önálló gazdálkodás megvalósíthatóságát. A központi eset pozitív 5. évi eredménye mellett az átmenetben pótlólagos forrás kell, és az 5. év szabad pénzáramlása nulla. Valós döntéshez havi pénzforgalom, stresszteszt, igazolt forrás és költségalkalmazkodás szükséges.\n\n'
    txt += '## Feltételezések és nyitott tételek\n\n' + '\n'.join('- ' + s for s in m['simplifications']) + '\n\n'
    txt += '## Újraszámítás\n\nBemenet: [modellparaméterek](modellek/penzugyi_pelda_0_9_2_j1.json). Előállító: [build_revision_092_j1.py](scripts/build_revision_092_j1.py). A `calculate` függvény és a PDF/Markdown táblák ugyanabból a bemenetből készülnek. A tényszámok későbbi betöltése külön verzió és dokumentált forrás nélkül nem végezhető el.\n\nSzámviteli fogalmak és források: [Módszertan és mutatók](METODIKA_ES_MUTATOK.md).\n'
    (ROOT / 'PENZUGYI_MODELL.md').write_text(txt, encoding='utf-8')


def setup_fonts():
    pdfmetrics.registerFont(TTFont('DVS', str(FONT)))
    pdfmetrics.registerFont(TTFont('DVS-Bold', str(FONT_DIR / 'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFontFamily('DVS', normal='DVS', bold='DVS-Bold', italic='DVS', boldItalic='DVS-Bold')


def styles():
    body = ParagraphStyle('body', fontName='DVS', fontSize=9.7, leading=13.5, textColor=TEXT, spaceAfter=9)
    return {
        'body': body,
        'title': ParagraphStyle('title', parent=body, fontName='DVS-Bold', fontSize=20, leading=25, textColor=NAVY, spaceAfter=17),
        'heading': ParagraphStyle('heading', parent=body, fontName='DVS-Bold', fontSize=12, leading=16, textColor=TEAL, spaceBefore=7, spaceAfter=7),
        'small': ParagraphStyle('small', parent=body, fontSize=8.6, leading=11.6),
        'cell': ParagraphStyle('cell', parent=body, fontSize=8.1, leading=10.4, spaceAfter=0),
        'head': ParagraphStyle('head', parent=body, fontName='DVS-Bold', fontSize=8.1, leading=10.4, spaceAfter=0),
    }


def table_block(headers, data, widths=None):
    s = styles()
    cells = [[Paragraph(str(c), s['head']) for c in headers]] + [[Paragraph(str(c), s['cell']) for c in row] for row in data]
    t = Table(cells, colWidths=widths or [WIDTH / len(headers)] * len(headers), repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E9F2F4')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F7F8')]),
        ('LINEBELOW', (0,0), (-1,0), .6, TEAL),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 5), ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    return t


def page_pdf(title, blocks):
    s = styles()
    content = [Paragraph(title, s['title'])]
    for b in blocks:
        if isinstance(b, str):
            content.append(Paragraph(b, s['body']))
        elif 'h' in b:
            content.append(Paragraph(b['h'], s['heading']))
        elif 'small' in b:
            content.append(Paragraph(b['small'], s['small']))
        elif 'table' in b:
            head, data, widths = b['table']
            content.extend([table_block(head, data, widths), Spacer(1, 12)])
    stream = BytesIO()
    SimpleDocTemplate(stream, pagesize=A4, leftMargin=56, rightMargin=56, topMargin=74, bottomMargin=66).build(content)
    result = fitz.open(stream=stream.getvalue(), filetype='pdf')
    if len(result) != 1:
        raise ValueError(f'Egy oldalra tervezett rész túlcsordult: {title} ({len(result)} oldal)')
    return result


def revised_pages(m, r):
    head, accrual, cash = financial_tables(r)
    numeric_widths = [181] + [(WIDTH - 181) / 6] * 6
    pages = {}
    pages[1] = [('A dokumentum státusza', [
        'Ez az anyag szakmai konzultációra szánt koncepciótanulmány. Nem jogi szakvélemény, nem hivatalos szakpolitikai program, és nem állítja, hogy a javaslatok jelenlegi formájukban bevezethetők.',
        'A cél ellenőrizhető kutatási és pilotprogram felépítése. A tényeket, a modellfeltételezéseket és a kutatási hipotéziseket külön kezeljük. Külső szakmai validáció még szükséges.',
        {'h':'A 0.9.2-j1 javítás tárgya'},
        'Egységes pénzügyi bázis és éves költségpálya; eredmény és pénzáramlás külön táblában; a transzferek kettős költséglevonásának javítása; mérési definíciók; a rövid pilot és a hosszú utánkövetés elválasztása; egységes verzió és oldalszámozás.',
        {'table': (['Verzió','Dátum','Státusz / tartalom'],[
            ['0.1','2026.09.','Eredeti rövid koncepció'],
            ['0.9 / 0.9.2','2026.09.19.','Konzultációs anyag; utánpótlási bővítés'],
            [VERSION,'2026.09.22.','Javított konzultációs kiadás'],
            ['0.9.3','Előkészítés','Külön esettanulmány-fejlesztési lépés'],
            ['1.0','Tervezett','Adatokkal és szakértői visszajelzésekkel megalapozott változat'],
        ],[80,83,WIDTH-163])},
        {'h':'Miben kérünk szakmai segítséget?'},
        'A klubadatok és a mutatók összehasonlíthatóságában, a hazai jogi alkalmazhatóságban, a pénzügyi feltételezések kalibrálásában és az önkéntes pilot kutatási tervében.',
        'A Tiszta Pálya Program megjelölés a név- és védjegykutatás lezárásáig munkacím. A javított számítás nem bizonyítja a modell eredményességét.',
    ])]
    pages[2] = [('1. Vezetői összefoglaló', [
        'A professzionális klubfutball fenntarthatósága a finanszírozási koncentráció, a politikai kitettség és a működési ösztönzők mérhető javítását igényli. A közösségi utánpótlási feladat és a profi csapat üzleti kockázata külön kezelendő.',
        {'h':'A modell négy pillére'},
        '<b>Közösségi kontroll:</b> tagi/szurkolói képviselet és védett döntési jogok, a választott jogi formához igazítva.',
        '<b>Bevételarányos költségfegyelem:</b> az UEFA 70%-os keretköltség-szabálya viszonyítási pont. A hazai licencmutató önálló kalibrációt és jogi vizsgálatot igényel.',
        '<b>Utánpótlás és játékosút:</b> képzési minőség, tényleges játékperc, első csapatos átmenet, hosszú távú pálya és elkülönített gazdasági eredmény.',
        '<b>Piaci és közösségi bevételek:</b> meccsnapi, kereskedelmi, digitális és tagsági bevétel fejlesztése a klub saját bázisához mérten.',
        {'h':'Mit mutat a javított számpélda?'},
        'A 0. évi 3 400 M Ft eredményfedezet 2 400 M Ft köz-/államközeli működési bevételből, 500 M Ft piaci működési bevételből és 500 M Ft eladási eredményből áll. Egyik szám sem igazolt magyar klubátlag.',
        'A központi esetben az 5. évi eredményfedezet 2 700 M Ft, a költség 2 500 M Ft, az eredmény +200 M Ft. A pénzáramlás ugyanakkor nulla, és a 200 M Ft-os pénzpuffer fenntartásához az átmenetben összesen 650 M Ft pótlólagos forrás kellene. Ennek rendelkezésre állása nincs igazolva.',
        'A példa nem támaszt alá automatikus támogatáskivezetést. Javasolt következő lépés: szakmai és jogi felülvizsgálat, ellenőrzött klubadatok, majd önkéntes megvalósíthatósági pilot. A rövid pilot nem bizonyít 3-5 éves utánpótlási hatást.',
    ])]
    pages[4] = [('3. Fogalmi keret és vizsgálati kérdések', [
        'A vizsgálat tárgya a magyar férfi professzionális klubfutball. A tömegsport, az olimpiai sportok és a közösségi utánpótlás társadalmi céljai nem vezethetők le ebből automatikusan.',
        {'h':'A forrás eredete és számviteli szerepe két külön dimenzió'},
        '<b>Közvetlen közpénz:</b> költségvetési, önkormányzati vagy pályázati támogatás. <b>Adóösztönző:</b> jogszabályi kedvezményhez kötött támogatási csatorna, külön jogcímmel és felhasználási céllal.',
        '<b>Államközeli kereskedelmi bevétel:</b> állami/önkormányzati cégtől származó szponzoráció. A piaci érték és a kapcsoltság külön vizsgálat tárgya.',
        '<b>Piaci és közösségi működési bevétel:</b> jegy, bérlet, a klubnál maradó szolgáltatás, kereskedelmi, média-, digitális, magánszponzori és tagsági bevétel. Csak azonosított jogi körrel és időszakkal számítható arány.',
        '<b>Transzfer:</b> az eladási eredmény, az időszaki transzfereredmény és a tényleges pénzáramlás külön mutató. <b>Finanszírozás:</b> a tulajdonosi tőke és a hitel pénzforrást adhat, de nem működési bevétel.',
        {'h':'Kutatási kérdések'},
        'Mekkora a forráskoncentráció és a 12-24 havi sokktűrés? Mely közösségi jogok javítják az elszámoltathatóságot? Mely költségszabály mérsékli a túlköltést arányos sport- és munkapiaci hatással? Milyen játékosút és bevételi láb tartható fenn különböző klubtípusoknál?',
        {'h':'Összehasonlíthatósági feltétel'},
        'A klub, az akadémia és a stadionüzemeltető adatait nem adjuk össze automatikusan. Az üzleti évet nem azonosítjuk a labdarúgó-szezonnal. Ismeretlen adat nem nulla. Minden arányhoz rögzített számláló, nevező, időszak, forrás és ellenőrző szükséges.',
        'A részletes projektdefiníciók a nyilvános Módszertan és mutatók dokumentumban találhatók (METODIKA_ES_MUTATOK.md).',
    ])]
    pages[10] = [('9. Pénzügyi fenntarthatóság és költségkontroll', [
        'A klubok eltérő bevétele és költségszerkezete miatt a fix forintösszegű bérplafon helyett bevételarányos költségmutatót vizsgálunk. A hazai alkalmazás továbbra is konzultációs javaslat.',
        {'h':'UEFA-referencia és hazai mutató'},
        'A 2026-os UEFA-szabályzat 93. cikke és K melléklete rögzíti a teljes keretköltség-rátát, annak korrekcióit és eltérő elszámolási időszakait. A 94. cikk szerinti határ 70%. A teljes személyi ráfordítás / működési bevétel mutató nem ennek helyettesítője. [13-14]',
        'Hiányzó transzfer-, amortizációs, kölcsönügyleti vagy közvetítői adatokból nem közlünk UEFA-megfelelőséget. Korábbi szezonok jogi minősítéséhez az akkori szabályzat alkalmazandó.',
        {'h':'Kiegészítő projektmutatók'},
        '<b>Lejárt kötelezettség:</b> esedékesség, összeg, jogcím, vitatottság és átütemezés külön. A beszámolóban nem említett tartozás nem tekinthető nullának.',
        '<b>Likviditás:</b> szabad pénz / a következő három hónap átlagos havi fix készpénzkiadása. A hitelkeret és a garancia külön adat. Havi értékelés és 13 hetes esedékességi cash-flow szükséges.',
        '<b>Tulajdonosi forrás:</b> tőke, kölcsön, támogatás és kapcsolt szponzori ügylet elkülönítése; a tranzakció és piaci értéke dokumentálandó.',
        {'table': (['Időpont','Korábbi hazai célpélda','Státusz'],[
            ['0. év','adatfelvétel és próbaszámítás','nincs új szankció'],
            ['1. év','90%','nem kalibrált modellfeltételezés'],
            ['2. év','80%','nem kalibrált modellfeltételezés'],
            ['3. évtől','70-75%','hazai opció; nem UEFA-felmentés'],
        ],[72,159,WIDTH-231])},
        {'small':'A fenti sáv nem jogszabály és nem bevezetési menetrend. Az UEFA hatálya alá tartozó klub saját kötelezettségeit nem módosítja. Részletes mutatók: METODIKA_ES_MUTATOK.md, 2-4. rész.'},
    ])]
    pages[12] = [('10.2. Az akadémiai eredményesség mérése', [
        'Az akadémia eredménye az első csapatos beépítés, a más klubnál folytatott pálya, a fejlődés, a gazdasági kimenet és a kettős életpálya együttes vizsgálatából értelmezhető.',
        {'table': (['Terület','Konzultációs mutató','Értelmezési feltétel'],[
            ['Első csapat','bemutatkozók; 900/1500 bajnoki percet elérők','nyers perc; a küszöb nem validált optimum'],
            ['Pályán maradás','3 és 5 év múlva is profi szinten játszók','teljes induló kohorsz és hiányzók követése'],
            ['Továbblépés','dokumentált sportszintváltás','előre rögzített szintbesorolás'],
            ['Gazdasági kimenet','eladási eredmény és pénzáramlás külön','képzési/szolidaritási tétel egyszer számít'],
            ['Edzői munka','egyéni célok és fejlődési trend','önmagában nem bizonyít oksági hozzáadott értéket'],
            ['Kettős életpálya','tanulás, végzettség, lemorzsolódás','jogszerű, aggregált utánkövetés'],
        ],[82,206,WIDTH-288])},
        'A klubnál képzett játékosok aránya az összes játékosperchez viszonyít. A képzési előéletet regisztrációval kell igazolni. Versenyszint-súlyok hiányában nyers perceket közlünk sorozatonként; összevont „minőségi percet” még nem számolunk.',
        {'h':'Nemzetközi példák és korlátaik'},
        {'small':'Spanyolország: a Real Madrid több szintű akadémiai útja klubszintű példa, nem minden spanyol klub modelljének bizonyítéka. [11] Horvátország: a HNS akadémiai és oktatási struktúrája látható; a klubfinanszírozás külön vizsgálandó. [10] Szerbia: a teljesen piaci működés állítása még nem igazolt. A CIES a tényleges tapasztalat méréséhez ad módszertani példát, nem kész magyar súlyokat. [12]'},
        {'h':'Szurkolói tapasztalatból kutatási hipotézis'},
        {'small':'A Vidi saját nevelésű játékosainak tartós beépítésére vonatkozó észrevétel ellenőrzéséhez 15-20 szezon keret-, játékperc- és pályaadatait kell vizsgálni. A más klubnál hasznosult játékost is követni kell. A 6-8 játékos rövid pilotja ezt nem helyettesíti.'},
    ])]
    pages[14] = [('12. Ötéves átmenet - döntési kapukkal', [
        {'table': (['Időszak','Feladat','Továbblépés feltétele'],[
            ['0-6 hónap','adatfelvétel, jogi előszűrés, klubtipológia','megbízható bázis és önkéntes partner'],
            ['6-18 hónap','1-2 megvalósíthatósági pilot','mérhető adatminőség, kezelhető teher és finanszírozás'],
            ['2. év','licenc-próbaszámítás, független értékelés','feltárt sport- és munkapiaci kockázatok'],
            ['3. év','esetleges szabályozási javaslat','a konkrét beavatkozáshoz elegendő bizonyíték'],
            ['4-5. év','feltételes kiterjesztés és utánkövetés','pénzügyi, sport- és közösségi feltételek teljesülése'],
        ],[74,190,WIDTH-264])},
        'Ez munkaterv, nem automatikus szabálybevezetés. A 3-5 éves akadémiai kimenetek megfigyelése tovább tarthat, mint az első rövid pilot. Hiányzó eredményt nem pótol a tervezett naptári ütem.',
        {'h':'Védőkorlátok'},
        'Az utánpótlás és a közösségi szolgáltatás támogatása külön feladat. A profi csapat reformjával együtt nem vágható vissza automatikusan.',
        'A támogatási láb csökkentése csak igazolt pénzügyi teljesítőképességgel és 13 hetes cash-flow tervvel vizsgálható. A szerződött jövőbeli bevétel önmagában nem rendelkezésre álló pénz.',
        'Súlyos adat-, integritási, fizetőképességi vagy gyermekvédelmi hiba esetén felfüggesztési döntés szükséges. A küszöböket, döntési jogokat és helyreállítási tervet indulás előtt rögzíteni kell.',
        'Független értékelő dokumentálja a változásokat és a bizonytalanságokat. A cél ellenőrzött, diverzifikált és sokkálló finanszírozás; a közforrás nullázása nem önálló sikerkritérium.',
    ])]
    pages[15] = [
      ('13. Pénzügyi példa - 0-5. évi eredménypálya', [
        'Minden összeg saját modellfeltételezés, nem klubadat és nem NB I-átlag. Egység: millió Ft, 2026-os változatlan árszint, nettó ÁFA nélküli bemenetek.',
        'A 0. évi 3 400 M Ft eredményfedezet: 2 400 M Ft köz-/államközeli működési bevétel + 500 M Ft piaci működési bevétel + 500 M Ft játékoseladási eredmény. A modellezett működési forráskiesés így 2 400 M Ft, nem 3 000 M Ft.',
        {'table':(head,accrual,numeric_widths)},
        '<b>Eredményfedezet</b> = működési bevételek + játékoseladási eredmény. Ez nem árbevétel és nem pénzállomány. <b>Időszaki eredmény</b> = eredményfedezet - működési költség.',
        'A költség minden évben 200 M Ft játékosamortizációt tartalmaz. A kivezetett könyv szerinti érték és az eladási díj már az eladási eredményben szerepel; a működési költség nem vonja le újra.',
        'A korábbi 2 500 M Ft „biztonsági küszöb” helyett itt az 5. év kifejezett költségfeltételezése áll. A külön pénzpuffer 200 M Ft. Mindkettő klubadatokkal kalibrálandó.',
        'A szerepeltetett egyenletes forráscsökkentés szemléltető stresszpálya, nem javasolt automatikus kivezetés. A következő oldal kimutatja az átmenet pénzigényét.',
      ]),
      ('13.2. Pénzforgalom és finanszírozási hiány', [
        'Egység: M Ft. Nyitó szabad pénz és elvárt záró puffer: 200 M Ft. A példában az elszámolás és a pénzügyi rendezés éven belül egybeesik; a valós részletfizetések külön tervet igényelnek.',
        {'table':(head,cash,numeric_widths)},
        '<b>Éves pénzváltozás</b> = időszaki eredmény + amortizáció + kivezetett könyv szerinti érték - játékosbeszerzés - egyéb beruházás.',
        'A negatív elméleti pénzállomány kielégítetlen hiányt jelez. A puffer megtartásához összesen <b>650 M Ft</b> új forrás kellene; puffer nélkül a nem negatív éves állományhoz 450 M Ft. Forrása és formája nincs igazolva. Hitel esetén a kamat és törlesztés további igény.',
        {'small':'Az adó, kamat, régi adósság törlesztése, forgótőke- és nettó ÁFA-pénzmozgás, egyéb nem pénzbeli korrekció és a beruházási amortizáció itt nulla feltételezés. A teljes feltételezéslista, a keretérték hídja és újraszámítás: PENZUGYI_MODELL.md. Az éves tábla nem helyettesíti a havi/13 hetes likviditási tervet.'},
      ]),
    ]
    scenarios=[]
    for s in m['year5_scenarios']:
        total=s['market_operating_income']+s['disposal_profit']
        result=total-r[-1]['cost']
        flow=result+r[-1]['amort']+r[-1]['nbv']-r[-1]['purchase']-r[-1]['capex']
        scenarios.append([s['name'],value(s['market_operating_income']),value(s['disposal_profit']),value(total),value(result),value(flow)])
    pages[16] = [('14. Három végpont és stresszpontok', [
        'Az 5. évi végpontok M Ft-ban, azonos költség- és kifizetési feltételekkel. A konzervatív és optimista eset végponti érzékenység; csak a központi esethez tartozik teljes 0-5. évi pálya.',
        {'table': (['Eset','Piaci bevétel','Eladási eredmény','Eredmény-<br/>fedezet','Időszaki eredmény','Pénz-<br/>változás'],scenarios,[86,79,83,84,79,WIDTH-411])},
        'Közös feltétel: 2 500 M Ft költség, benne 200 M Ft amortizáció; 300 M Ft eladott könyv szerinti érték; 650 M Ft játékosbeszerzés és 50 M Ft egyéb beruházás; a vizsgált köz-/államközeli működési bevétel nulla.',
        'A központi eset 2 700 M Ft fedezete nem teljesíti a korábbi 3 000 M Ft célt. A +200 M Ft eredmény itt nulla szabad éves pénzáramlással jár. Az átmeneti finanszírozási igényt a 13.2. fejezet mutatja.',
        {'h':'Eladás nélküli stressz'},
        'Ha az 5. évben nincs játékoseladás, az 1 100 M Ft nettó eladási pénzbevétel kiesik. Változatlan működési és beszerzési feltételekkel a pénzváltozás -1 100 M Ft. Ilyenkor eladási díjat és könyv szerinti kivezetést sem számolunk.',
        {'h':'További, külön kalibrálandó stresszek'},
        'Két átigazolási ablak eladás nélkül; 20%-os meccsnapi bevételkiesés; főszponzor elvesztése; kiesés vagy elmaradó kupabevétel; 10-15%-os bér- és szolgáltatási költségemelkedés. A hatásokat nem szabad automatikusan összeadni, az együttjárást és a reakciókat is modellezni kell.',
        'A négy pillér és a finanszírozási átállás működőképessége e szemléltető számokból még nem igazolható.',
    ])]
    pages[18] = [('16. A 6-12 hónapos megvalósíthatósági pilot', [
        'Az első pilot az adatgyűjtés és az együttműködés működőképességét vizsgálja. Nem tartalmaz kötelező bérplafont vagy nemzetiségi kvótát. Rövid megfigyelésből országos vagy többéves oksági hatás nem állapítható meg.',
        {'h':'Pilotmodulok'},
        '<b>Adat és transzparencia:</b> egységes riport, kapcsolt ügyletek, adatlefedettség, ellenőrzési nyom és adminisztrációs idő.',
        '<b>Közösség:</b> mandátummal rendelkező képviselet, dokumentált konzultáció, válaszidő és a védett ügyek tényleges gyakorlása.',
        '<b>Kereskedelem:</b> nettó elszámolt bevétel, befolyt pénz és szerződésállomány külön; fizető kihasználtság és 90 napos visszatérés.',
        '<b>Tehetségút:</b> 6-8 előre meghatározott módon kiválasztott játékos fejlesztési és adatrögzítési folyamatpróbája. A teljes jogosult csoport mérete és a kiválasztás torzítása közlendő.',
        '<b>Pénzügy:</b> keretköltség-próbaszámítás, 13 hetes cash-flow, stressz- és helyreállítási terv.',
        {'h':'Előre rögzítendő értékelési keret'},
        'Bázisérték, adatgazda, azonos időszak és definíció, adatlefedettségi küszöb, összevetési terv, költség és leállítási szabály. A lehetséges +10-20% piaci bevételi cél ténylegesen elszámolt bevételre vonatkozik; jövőbeli szerződés nem helyettesítheti.',
        'A +10%-os fizetőkihasználtság-cél relatív változás, nem +10 százalékpont. Árat, kapacitást és sportsikert is rögzíteni kell. A javulás előtte/utána megfigyelése nem önmagában oksági bizonyíték.',
        '<b>3-5 éves utánkövetés:</b> teljes akadémiai kohorsz pályán maradása, szintváltása és kettős életpályája. A még le nem telt időhorizont nem minősíthető sikernek vagy kudarcnak.',
        'A pilotot független szakmai partner értékeli. A heti egyszeri, 12 hetes forrásfeltárás külön előkészítő munkaciklus; nem klubpilot és nem a modell validálása.',
    ])]
    pages[19] = [
      ('17. KPI- és adatkeret', [
        'Egységes projektdefiníciók, azonos szervezeti kör és időszak szükséges. A mutatókat adatgazdával, forrással, ellenőrzési nyommal és a hiányok megjelölésével közöljük.',
        {'table': (['Mutató','Számítás / feltétel','Ritmus / adatgazda'],[
            ['Saját bevételi arány','piaci és közösségi működési bevétel / teljes működési bevétel','év; pénzügy + auditor'],
            ['Koncentráció','azonos érdekkörű top 3 külső működési forrás / teljes működési bevétel','év; pénzügy'],
            ['UEFA keretköltség-ráta','a 93. cikk és K melléklet teljes definíciója; hiányzó adatnál nincs ráta','év; klub + licencadat'],
            ['Likviditási hónap','szabad pénz / következő 3 hó átlagos havi fix készpénzkiadása','hó; pénzügy'],
            ['Saját nevelésű játékperc','igazolt klubképzési feltételű játékospercek / összes bajnoki játékosperc','szezon; akadémia + liga'],
            ['Súlyozott perc','nyers perc × előre rögzített súly; validált súly nélkül nem számoljuk','sorozatonként nyers adat'],
            ['Fizető kihasználtság','fizetett belépéssel jelen lévők / adott meccs értékesíthető kapacitása','mérkőzés; jegyrendszer'],
            ['Visszatérés','új vevői kohorsz visszatérő tagja / teljes követési idejű kohorsz','90/180 nap; CRM'],
            ['Közösségi befolyás','jogalap, mandátum, részvétel, határidős válasz és dokumentált döntés','félév; klub + képviselet'],
        ],[105,255,WIDTH-360])},
        {'small':'A transzfermutatók a következő oldalon szerepelnek. A bevételi, játékperc- és közönségarányok százalékban, a likviditás hónapban közlendő. Nulla/negatív nevező esetén nincs értelmezhető bevételarány. A hiány nem nulla; összpontszám és klubrangsor még nincs.'},
        {'small':'Részletes definíciók, képzési korhatár, kohorsz, forrás és adatminőség: METODIKA_ES_MUTATOK.md. Nyilvánosan csak megfelelően aggregált adat közölhető.'},
      ]),
      ('17.2. Transzfereredmény és pénzáramlás', [
        'A korábbi képlet a teljes bekerülési értéket és az amortizációt is levonta. Ezt javítjuk: az eladáskor fennálló könyv szerinti értékből indulunk, így a korábbi költség nem vonódik le még egyszer. [15]',
        {'h':'1. Eladási nyereség vagy veszteség'},
        'Elszámolt eladási ellenérték - közvetlen eladási díjak - kivezetéskori könyv szerinti érték. A nettó ellenértékből már levont díjat nem vonjuk le újra.',
        {'h':'2. Időszaki transzfereredmény'},
        'Az eladási eredményekhez hozzáadjuk az egyéb transzferbevételeket, levonjuk az időszaki amortizációt, értékvesztést és a még el nem számolt kapcsolódó ráfordításokat. Minden tétel egyszer szerepel. Ez külön projektkimutatás, nem automatikusan az UEFA-ráta nevezője.',
        {'h':'3. Transzfer-pénzáramlás'},
        'Tényleges befolyó transzferpénz - az időszakban kifizetett beszerzések és közvetlen díjak. Nincs amortizációs levonás. A részletfizetés és a bónusz teljesítésének időpontját külön követjük.',
        {'h':'Egyszerű példa, M Ft'},
        '100 bekerülés - 40 halmozott amortizáció = 60 könyv szerinti érték. 150 eladási ellenérték - 10 díj - 60 könyv szerinti érték = <b>80 eladási nyereség</b>.',
        'Ha az adott évben 90 folyik be, 10 díjat és 50 új beszerzést fizetünk, a <b>transzfer-pénzáramlás 30</b>. Az eredmény és a pénzáramlás eltérését a mérleg és a fizetési ütemezés vezeti át.',
        {'small':'A példa aktivált regisztrációs jogokra vonatkozik. A beszerzést azonnal költségként elszámoló klubnál más átvezetés kell. Időszak, számviteli politika és nettósítás dokumentálandó. Forrás: UEFA 2026 G.3.3, G.3.4(5), G.3.6; adatgazda: pénzügy + auditor. A 13. fejezet eladási eredményt használ, az amortizációt a működési költségben számolja.'},
      ]),
    ]
    pages[20] = [('18. Kérdések a szakmai felülvizsgálathoz', [
        'A szakmai konzultáció célja a modell gyenge pontjainak, az adatfeltételeknek és a következő kutatási lépésnek az azonosítása. Az egyeztetés nem jelent támogatói vagy validációs nyilatkozatot.',
        {'h':'Sportmenedzsment és sportgazdaság'},
        '1. Koherens-e a négy pillér kapcsolata, és mely elemhez hiányzik lényeges bizonyíték?',
        '2. Mely pénzügyi és játékosút-mutató módosítandó? Milyen képzési kohorsz és összevetési csoport szükséges?',
        '3. Milyen feltételekkel hasonlítható össze az FTC, a Puskás Akadémia és az MTK három szezonja az eltérő jogi és beszámolási körök mellett?',
        '4. Mely elsődleges adatforrás és kispiaci európai klubmodell használható? Melyik intézményi elem ültethető át?',
        '5. Milyen adatminőségi és lezárási feltétele legyen a 12 hetes, heti egyszeri forrásfeltárásnak? Hogyan ellenőrizzük az automatizált adatjelölteket?',
        '6. Mit vizsgálhat egy 6-12 hónapos megvalósíthatósági pilot, és mihez kell többéves utánkövetés?',
        {'h':'Szellemi tulajdon és intézményi együttműködés'},
        'Mely dokumentumelemek védhetők, és mit bizonyít az önkéntes műnyilvántartás? Melyik aktuális változat benyújtása indokolt? Milyen névkutatás és szolgáltatási osztály szükséges?',
        'Hogyan rögzíthető a meglévő anyag, a későbbi közös fejlesztés, a szerzői és felhasználási jog, az adatkezelés és az esetleges licenc? Milyen intézményi eljárás és AI-közreműködési dokumentáció megfelelő?',
        'A jogi és szakmai válaszokat külön kell dokumentálni. A nyilvános állítás csak a ténylegesen megkapott és közlésre alkalmas visszajelzésre épülhet.',
    ])]
    return pages


def build_main(m, rows):
    original = fitz.open(BASE)
    assert len(original) == 24, 'A kiinduló dokumentum váratlanul megváltozott.'
    raw = BASE.read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == 'a393b33c18661c1502b8939d629bf592b5337d70', 'A forrás PDF nem a felülvizsgált változat.'
    updates = revised_pages(m, rows)
    result = fitz.open()
    for i in range(len(original)):
        if i in updates:
            for title, blocks in updates[i]:
                sub = page_pdf(title, blocks)
                result.insert_pdf(sub)
        else:
            result.insert_pdf(original, from_page=i, to_page=i)
    refs = [
        {'h':'13. UEFA 2026 - 93. cikk és K melléklet'},
        {'small': '<link href="' + UEFA + 'Article-93-Calculation-of-squad-cost-ratio-Online">A keretköltség-ráta hivatalos számítási szabálya (kattintható)</link>'},
        'A mutató teljes definíciója és az időszakok. A hazai egyszerűsített ráta külön megnevezést igényel.',
        {'h':'14. UEFA 2026 - 94. cikk'},
        {'small': '<link href="' + UEFA + 'Article-94-Squad-cost-rule-Online?contentId=ECUHs41EOPHcoQeGRa3OSA">A 70%-os keretköltség-szabály (kattintható)</link>'},
        {'h':'15. UEFA 2026 - G.3 melléklet'},
        {'small': '<link href="' + UEFA + 'G.3-Accounting-requirements-for-the-permanent-transfer-of-a-player-s-registration-Online?contentId=mbp0thahzVgyytKVZPxyiQ">Az átigazolások számviteli kezelése (kattintható)</link>'},
        'Aktiválás vagy közvetlen költségelszámolás, eladási eredmény és közvetlen díjak. A jogszabály/standard szerinti alkalmazás klubonként ellenőrzendő.',
        {'h':'A kiadás ellenőrizhető kiegészítői'},
        '<link href="https://github.com/cooldance84/tiszta-palya-program/blob/main/METODIKA_ES_MUTATOK.md">Módszertan és mutatók</link>: szervezeti kör, időszak, képlet, adatgazda, hiánykezelés és pilot.',
        '<link href="https://github.com/cooldance84/tiszta-palya-program/blob/main/PENZUGYI_MODELL.md">Pénzügyi modell</link>: bemenetek, éves eredmény és cash-flow, finanszírozási hiány, végponti stressz és újraszámítás.',
        'Ellenőrzés dátuma: 2026. szeptember 22. A 2026-os UEFA-szabályok hivatkozási alapot adnak; a korábbi szezonok megfelelőségét az akkori szabályok alapján kell megítélni.',
    ]
    result.insert_pdf(page_pdf('20.2. A javítás elsődleges forrásai', refs))
    # Az eredeti borító arculatát megtartjuk, kizárólag a verziómezőt cseréljük.
    cover = result[0]
    boxes = cover.search_for('KONZULTÁCIÓS TERVEZET 0.9')
    assert boxes, 'A borítón nem található a régi verziómező.'
    rect = boxes[0]
    cover.add_redact_annot(rect + (-2,-2,20,4), fill=(23/255,50/255,79/255))
    cover.apply_redactions()
    cover.insert_font(fontname='TPP', fontfile=str(FONT))
    cover.insert_text((rect.x0, rect.y1-2), 'KONZULTÁCIÓS TERVEZET ' + VERSION, fontname='TPP', fontsize=13, color=(1,1,1))
    for i in range(1, len(result)):
        page = result[i]
        page.add_redact_annot(fitz.Rect(0,0,page.rect.width,43), fill=(244/255,246/255,247/255))
        page.add_redact_annot(fitz.Rect(0,page.rect.height-51,page.rect.width,page.rect.height), fill=(1,1,1))
        page.apply_redactions()
        page.insert_font(fontname='TPP', fontfile=str(FONT))
        page.insert_text((56,28), 'TISZTA PÁLYA PROGRAM ' + VERSION + ' | KONZULTÁCIÓS TERVEZET', fontname='TPP', fontsize=7.7, color=(23/255,50/255,79/255))
        page.draw_line((56,page.rect.height-34),(page.rect.width-56,page.rect.height-34), color=(.84,.88,.9), width=.6)
        page.insert_text((page.rect.width-111,page.rect.height-19), f'{i+1}. oldal', fontname='TPP', fontsize=8, color=(.4,.46,.53))
    result.set_metadata({'title':'Tiszta Pálya Program - konzultációs változat '+VERSION,'author':'Kiss Tiborcz','subject':'Javított pénzügyi és módszertani konzultációs kiadás, 2026-09-22'})
    result.subset_fonts()
    dest=ROOT/'dokumentumok'/f'Tiszta_Palya_Program_konzultacios_valtozat_{SUFFIX}.pdf'
    result.save(dest, garbage=4, deflate=True)
    check=fitz.open(dest)
    txt='\n\f\n'.join(p.get_text(sort=True) for p in check)
    dest.with_suffix('.txt').write_text(txt,encoding='utf-8')
    assert len(check)==27
    assert 'bekerülés, amortizáció' not in txt
    print('MAIN',dest.name,'pages',len(check),'bytes',dest.stat().st_size)


def inline_md(text):
    text=escape(text)
    text=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda z: '<link href="'+ (z.group(2) if z.group(2).startswith('http') else 'https://github.com/cooldance84/tiszta-palya-program/blob/main/'+z.group(2))+'">'+z.group(1)+'</link>',text)
    return text


def build_summary():
    md=(ROOT/'VEZETOI_OSSZEFOGLALO.md').read_text(encoding='utf-8')
    md=re.sub(r'<p align="center">.*?</p>','',md,flags=re.S)
    s=styles()
    for name in ['body','small']:
        s[name].fontSize=9.1
        s[name].leading=12
        s[name].spaceAfter=6
    s['title'].fontSize=19
    s['title'].leading=23
    s['title'].spaceAfter=7
    s['heading'].fontSize=11
    s['heading'].leading=14
    s['heading'].spaceBefore=5
    s['heading'].spaceAfter=5
    story=[]
    lines=md.splitlines()
    i=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:
            i+=1;continue
        if line.startswith('|'):
            data=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch('[-: ]+',x) for x in cells):
                    data.append([inline_md(x) for x in cells])
                i+=1
            story.extend([table_block(data[0],data[1:],[139,WIDTH-139]),Spacer(1,7)])
            continue
        kind='title' if line.startswith('# ') else 'heading' if line.startswith('## ') else 'body'
        text=line[2:] if line.startswith('# ') else line[3:] if line.startswith('## ') else line[2:] if line.startswith('> ') else line
        story.append(Paragraph(inline_md(text),s[kind]))
        i+=1
    out=ROOT/'dokumentumok'/f'Tiszta_Palya_Program_vezetoi_osszefoglalo_{SUFFIX}.pdf'
    SimpleDocTemplate(str(out),pagesize=A4,leftMargin=56,rightMargin=56,topMargin=36,bottomMargin=36,title='Tiszta Pálya Program - vezetői összefoglaló '+VERSION,author='Kiss Tiborcz').build(story)
    p=fitz.open(out)
    assert len(p)==1, f'A vezetői összefoglaló {len(p)} oldalra törik.'
    print('SUMMARY',out.name,'pages',len(p),'bytes',out.stat().st_size)


def main():
    model=json.loads((ROOT/'modellek'/f'penzugyi_pelda_{SUFFIX}.json').read_text(encoding='utf-8'))
    model_bytes=json.dumps(model,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    if hashlib.sha256(model_bytes).hexdigest() != MODEL_SHA256:
        raise ValueError('Megváltoztak a rögzített kiadás bemenetei. Új kiadás előtt a szöveges következtetéseket, az összefoglalót és a verziót is felül kell vizsgálni; önmagában a táblák frissítése nem elegendő.')
    rows=calculate(model)
    write_model_note(model,rows)
    setup_fonts()
    build_main(model,rows)
    build_summary()


if __name__=='__main__':
    main()
