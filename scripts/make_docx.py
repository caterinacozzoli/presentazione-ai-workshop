#!/usr/bin/env python3
"""
make_docx.py — Genera il documento Word del workshop
Crea: SCRIPT_WORKSHOP_AI_S1.docx (Script + Bibliografia)
Poi aprilo su Google Docs via File > Apri > Carica
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

OUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SCRIPT_WORKSHOP_AI_S1.docx')

BLUE  = RGBColor(0x06, 0x00, 0x6b)
RED   = RGBColor(0xf0, 0x0a, 0x0a)
GREY  = RGBColor(0x55, 0x55, 0x55)
BLACK = RGBColor(0x00, 0x00, 0x00)

def h1(doc, text):
    p = doc.add_heading(text, level=1)
    p.runs[0].font.color.rgb = BLUE
    p.runs[0].font.size = Pt(20)
    return p

def h2(doc, text):
    p = doc.add_heading(text, level=2)
    p.runs[0].font.color.rgb = BLUE
    p.runs[0].font.size = Pt(15)
    return p

def h3(doc, text):
    p = doc.add_heading(text, level=3)
    p.runs[0].font.color.rgb = RED
    p.runs[0].font.size = Pt(12)
    return p

def body(doc, text, color=None, bold=False, italic=False, size=11):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color or BLACK
    return p

def stage(doc, text):
    """Note di regia — grigio corsivo"""
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.color.rgb = GREY
    return p

def voice(doc, speaker, text, color_map):
    """Linea di dialogo con nome oratore in colore"""
    p = doc.add_paragraph()
    r_name = p.add_run(f"{speaker}: ")
    r_name.font.bold = True
    r_name.font.size = Pt(11)
    r_name.font.color.rgb = color_map.get(speaker, BLACK)
    r_text = p.add_run(text)
    r_text.font.size = Pt(11)
    return p

def placeholder(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(f"[ {text} ]")
    r.font.size = Pt(10)
    r.font.italic = True
    r.font.color.rgb = RGBColor(0xff, 0x99, 0x00)
    return p

def divider(doc):
    p = doc.add_paragraph("─" * 70)
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.color.rgb = GREY

def schermo(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    r = p.add_run(f"[schermo] {text}")
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(0x00, 0x55, 0xaa)
    return p

def build_doc():
    doc = Document()

    # Imposta margini
    for section in doc.sections:
        section.top_margin    = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin   = Inches(1.2)
        section.right_margin  = Inches(1.2)

    # Colori per oratore
    VOICES = {
        'SARA':     RGBColor(0x06, 0x00, 0x6b),   # blu
        'ALBERTO':  RGBColor(0xf0, 0x0a, 0x0a),   # rosso
        'GAIA':     RGBColor(0x00, 0x88, 0x44),   # verde
        'CATERINA': RGBColor(0x88, 0x00, 0x88),   # viola
        'TUTTI':    BLACK,
    }

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PAGINA 1: SCRIPT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    h1(doc, "SCRIPT — Workshop AI: Sessione 1")
    body(doc, '"Manuale di sopravvivenza all\'AI"', bold=True, size=13)
    body(doc, "Durata: ~50 min  |  Oratori: Sara · Alberto · Gaia · Caterina", color=GREY, size=11)
    body(doc, "Formato: 30' teoria dialogica + 10' mani in pasta + 10' confronto aperto  |  24 slide", color=GREY, size=11)
    doc.add_paragraph()

    # LEGENDA
    h3(doc, "LEGENDA")
    body(doc, "[slide →] = cambio slide     [schermo] = cosa appare sullo schermo", color=GREY, size=10)
    body(doc, "(nota corsiva) = indicazioni di regia / movimento", color=GREY, size=10, italic=True)
    body(doc, "[PLACEHOLDER] = contenuto da completare con i PDF", color=RGBColor(0xff,0x99,0x00), size=10)
    doc.add_paragraph()

    # PARTE 1
    divider(doc)
    h2(doc, "PARTE 1 — TEORIA DIALOGICA (30 min)")
    divider(doc)
    doc.add_paragraph()

    # SLIDE 1
    h3(doc, "SLIDE 1 — COVER")
    schermo(doc, '"Manuale di sopravvivenza all\'AI" | "Ecosistema · Prompt Engineering · Sfide Etiche" | Workshop AI Interno — Sessione 1')
    doc.add_paragraph()
    voice(doc, 'CATERINA', "Benvenuti. Siamo Sara, Alberto, Gaia e Caterina. Oggi vi parliamo di AI per condividere quanto abbiamo appreso usandola quotidianamente nei nostri processi. Non siamo qui per fare una lezione cattedratica, ma per esplorare insieme come questi strumenti stiano cambiando il nostro modo di lavorare.", VOICES)
    voice(doc, 'SARA', "L'obiettivo è proprio quello di fare chiarezza e darvi la sicurezza necessaria per sperimentare.", VOICES)
    voice(doc, 'ALBERTO', "Abbiamo pensato a questa sessione come a un momento di condivisione pratica tra colleghi. Un confronto aperto sui pro, i contro e le sfide di questa tecnologia.", VOICES)
    voice(doc, 'GAIA', "Parleremo anche di un aspetto spesso sottovalutato, ma per noi molto importante: l'impatto etico e ambientale dell'AI.", VOICES)
    doc.add_paragraph()

    # SLIDE 2
    h3(doc, "SLIDE 2 — SCALETTA")
    schermo(doc, "4 punti: 01 Ecosistema AI & Consumi | 02 Gestione dei File | 03 Prompt Optimization | 04 Generazioni Inclusive & Etica")
    doc.add_paragraph()
    voice(doc, 'CATERINA', "La nostra agenda di oggi. In circa 50 minuti copriremo quattro aree: partiremo dall'ecosistema generale e dai consumi, per poi entrare nel vivo della gestione dei file e di come ottimizzare i prompt. Chiuderemo con un aspetto fondamentale: etica e inclusività.", VOICES)
    voice(doc, 'ALBERTO', "Ovviamente, sentitevi liberi di intervenire con domande o riflessioni in qualsiasi momento.", VOICES)
    doc.add_paragraph()

    # SLIDE 3
    h3(doc, "SLIDE 3 — ROMPIGHIACCIO")
    schermo(doc, '"Prima di partire — Alzate la mano: chi ha già usato un tool di AI al lavoro?" (ChatGPT · Copilot · Gemini · Midjourney)')
    doc.add_paragraph()
    voice(doc, 'CATERINA', "Prima di entrare nel vivo, ci piacerebbe capire da dove partiamo. Quanti di voi usano già strumenti come ChatGPT, Copilot, Gemini o simili nel lavoro quotidiano?", VOICES)
    stage(doc, "(aspetta le mani, osserva la sala)")
    voice(doc, 'SARA', "Ottimo. E per chi non ha ancora avuto modo di esplorarli, l'obiettivo di oggi è proprio fornirvi le basi per iniziare in modo efficace.", VOICES)
    voice(doc, 'ALBERTO', "Iniziamo ad allineare il nostro vocabolario.", VOICES)
    doc.add_paragraph()

    # SLIDE 4
    h3(doc, "SLIDE 4 — SEZIONE 01: ECOSISTEMA AI & CONSUMI")
    stage(doc, "(cambio di sezione)")
    doc.add_paragraph()

    # SLIDE 5
    h3(doc, "SLIDE 5 — ECOSISTEMA: I PLAYER")
    schermo(doc, "AI Generativa: ChatGPT/OpenAI, Claude/Anthropic, Gemini/Google, Copilot/Microsoft, Midjourney/DALL·E")
    schermo(doc, "AI Classica: filtro spam, Netflix, Face ID, traduzione automatica")
    doc.add_paragraph()
    voice(doc, 'SARA', "Quando parliamo di \"AI\", spesso facciamo confusione tra due famiglie distinte.", VOICES)
    voice(doc, 'ALBERTO', "L'AI generativa — quella che crea testi, immagini e codice in modo dinamico — è il focus di oggi. Parliamo dei modelli di OpenAI (ChatGPT), Anthropic (Claude), Google (Gemini) e Microsoft (Copilot).", VOICES)
    voice(doc, 'SARA', "Poi c'è l'AI \"analitica\" o classica, che usiamo già da anni: il riconoscimento facciale degli smartphone, i filtri antispam, i suggerimenti di Netflix. L'AI generativa rappresenta uno step successivo: non classifica solo i dati, ma produce contenuti nuovi.", VOICES)
    doc.add_paragraph()

    # SLIDE 6
    h3(doc, "SLIDE 6 — COME FUNZIONA? IN PAROLE SEMPLICI")
    schermo(doc, "Spiegazione senza jargon + analogia autocomplete + 3 bullet: no coscienza / può sbagliare / il contesto cambia tutto")
    doc.add_paragraph()
    voice(doc, 'GAIA', "Per usare bene questi strumenti, dobbiamo capire cosa c'è sotto il cofano.", VOICES)
    voice(doc, 'GAIA', "I Modelli Linguistici di Grandi Dimensioni (LLM) sono stati addestrati su enormi porzioni di internet, libri e articoli. Il loro compito principale, semplificando, è calcolare statisticamente quale parola ha più senso inserire dopo la precedente.", VOICES)
    voice(doc, 'CATERINA', 'È importante ricordare che non hanno un "pensiero" proprio, né una reale comprensione semantica. Sono meccanismi di predizione estremamente sofisticati.', VOICES)
    voice(doc, 'ALBERTO', "Questo significa che sono soggetti ad \"allucinazioni\": possono produrre risposte completamente errate, ma formulate in modo molto autorevole e convincente. Per questo la verifica umana rimane essenziale.", VOICES)
    doc.add_paragraph()

    # SLIDE 7
    h3(doc, "SLIDE 7 — SOSTENIBILITÀ E CONSUMI")
    schermo(doc, "Tabella: Prompt (~5-10x Google) | Training (energia significativa una tantum) | Scala (miliardi/giorno). Fonte: SciTechDaily.")
    doc.add_paragraph()
    voice(doc, 'GAIA', "Un tema molto dibattuto è l'impatto energetico dell'AI. Spesso leggiamo notizie allarmistiche, ma i dati ci aiutano a contestualizzare.", VOICES)
    voice(doc, 'CATERINA', 'Come evidenzia un recente studio di SciTechDaily, l\'energia richiesta per una singola generazione (un "prompt") equivale a circa 5-10 ricerche Google. Non è un impatto trascurabile, ma è inferiore a quanto viene spesso percepito.', VOICES)
    voice(doc, 'GAIA', "Il vero impatto si verifica durante la fase di \"addestramento\" del modello, che richiede enormi risorse di calcolo, e naturalmente dalla \"scala\" globale: miliardi di query ogni giorno richiedono server farm immense.", VOICES)
    voice(doc, 'CATERINA', "Da qui l'importanza di un \"Prompt Engineering\" efficace: formulare richieste precise significa ridurre il numero di tentativi e iterazioni, ottimizzando sia il nostro tempo che le risorse energetiche.", VOICES)
    doc.add_paragraph()

    # SLIDE 8 — QUIZ
    h3(doc, "SLIDE 8 — QUIZ: QUANTO CONSUMA UN PROMPT?")
    schermo(doc, "A) ☕ Fare un caffè espresso   B) 🔍 5–10 ricerche Google (non 1.000)   C) ✈️ Un decimo di un volo Milano-Roma")
    doc.add_paragraph()
    voice(doc, 'ALBERTO', "Vi proponiamo un piccolo sondaggio. Secondo voi, in termini di energia, un prompt equivale a...?", VOICES)
    stage(doc, "(aspetta le risposte dal pubblico — 30 sec)")
    voice(doc, 'ALBERTO', "La risposta è la B, circa 5-10 ricerche Google. Spesso la percezione è molto più alta a causa del modo in cui i media ne parlano.", VOICES)
    voice(doc, 'SARA', "L'obiettivo non è scoraggiarne l'uso, ma promuovere un approccio consapevole e strutturato.", VOICES)
    doc.add_paragraph()

    # SLIDE 9
    h3(doc, "SLIDE 9 — SEZIONE 02: GESTIONE DEI FILE")
    stage(doc, "(cambio di sezione)")
    doc.add_paragraph()

    # SLIDE 10
    h3(doc, "SLIDE 10 — FORMATI FILE")
    schermo(doc, "✅ .md .txt .csv (ottimali) | ⚠️ .pdf .docx (accettabili) | ❌ PDF scansionati | ❌ .xlsx con formule")
    doc.add_paragraph()
    voice(doc, 'CATERINA', "Cambiamo argomento. Spesso lavoriamo fornendo documenti all'AI per farli analizzare, riassumere o usare come contesto. La scelta del formato è determinante.", VOICES)
    voice(doc, 'SARA', 'L\'AI ragiona in termini di testo. Qualsiasi elemento di formattazione visiva complessa rischia di creare "rumore" o di perdersi.', VOICES)
    voice(doc, 'CATERINA', "I formati ideali sono il testo puro e strutturato: .txt, .csv per i dati, e in particolare il formato .md (Markdown). Meno efficaci sono i PDF complessi o scansionati, e i file Excel in cui il valore deriva da formule nascoste che l'AI non può sempre interpretare.", VOICES)
    voice(doc, 'ALBERTO', "Per ottenere risultati eccellenti, dovremmo abituarci a \"pulire\" le informazioni prima di darle in pasto all'AI.", VOICES)
    doc.add_paragraph()

    # SLIDE 11 — QUIZ
    h3(doc, "SLIDE 11 — QUIZ: COS'È UN FILE .MD?")
    schermo(doc, "A) ⚙️ Un file di log di sistema   B) 🗄️ Un formato proprietario per database relazionali   C) 📝 Markdown — formato di testo puro con sintassi leggera")
    doc.add_paragraph()
    voice(doc, 'ALBERTO', "A proposito di Markdown, quanti di voi sanno cosa rappresenta un file con estensione \".md\"?", VOICES)
    stage(doc, "(aspetta le risposte)")
    voice(doc, 'ALBERTO', "Esatto, è la C. Il Markdown è un formato di testo puro, inventato per formattare contenuti sul web usando solo caratteri standard: un cancelletto per i titoli, asterischi per il grassetto.", VOICES)
    voice(doc, 'GAIA', "Essendo puramente testuale ma altamente strutturato, è il formato che i modelli AI \"digeriscono\" meglio. Riduce le incomprensioni e aumenta la precisione delle analisi. Vi suggeriamo di iniziare a usarlo per i brief strutturati.", VOICES)
    doc.add_paragraph()

    # SLIDE 12
    h3(doc, "SLIDE 12 — SEZIONE 03: PROMPT OPTIMIZATION")
    stage(doc, "(cambio di sezione)")
    doc.add_paragraph()

    # SLIDE 13
    h3(doc, "SLIDE 13 — IL PROMPT INEFFICACE (interattivo)")
    schermo(doc, 'Riquadro rosso: "Crea una presentazione sull\'AI" → output: generico, scolastico. 4 domande mancanti.')
    doc.add_paragraph()
    voice(doc, 'SARA', "Arriviamo alla tecnica: il Prompt Engineering.", VOICES)
    voice(doc, 'ALBERTO', "L'errore più comune che riscontriamo è un approccio simile a quello che usiamo sui motori di ricerca: inseriamo poche parole chiave e ci aspettiamo un elaborato complesso. E quando l'output è piatto o scolastico, pensiamo che lo strumento non funzioni.", VOICES)
    voice(doc, 'SARA', 'Pensiamo a questo input: "Crea una presentazione sull\'AI". Cosa manca per renderlo una richiesta professionale?', VOICES)
    stage(doc, "(raccoglie risposte dal pubblico — 1-2 min)")
    voice(doc, 'ALBERTO', "Manca tutto il contesto essenziale: a chi è rivolto? Che tono di voce dobbiamo usare? Qual è la lunghezza desiderata? L'AI non ha modo di indovinarlo.", VOICES)
    doc.add_paragraph()

    # SLIDE 14
    h3(doc, "SLIDE 14 — LE REGOLE D'ORO")
    schermo(doc, "5 regole: Assegna un RUOLO | Fornisci CONTESTO | Definisci il FORMATO | Dai ESEMPI | ITERA")
    placeholder(doc, "Integrare con slide_ai_prompt_design p.12 + p.15-16")
    doc.add_paragraph()
    voice(doc, 'SARA', "Esistono cinque principi cardine per costruire un prompt solido.", VOICES)
    voice(doc, 'ALBERTO', "Il primo è fondamentale: assegnare un ruolo. \"Agisci come un analista di mercato senior\" configura immediatamente il livello linguistico e la profondità dell'analisi.", VOICES)
    voice(doc, 'SARA', "L'ultimo passaggio è altrettanto cruciale: l'iterazione. L'AI non deve produrre il risultato perfetto al primo colpo; è un processo conversazionale in cui si raffina la richiesta progressivamente.", VOICES)
    doc.add_paragraph()

    # SLIDE 15
    h3(doc, "SLIDE 15 — PRIMA / DOPO")
    schermo(doc, '❌ "Scrivi un\'email di aggiornamento al cliente" → output generico. ✅ Prompt strutturato con Ruolo, Contesto, Obiettivo, Formato e Vincoli')
    placeholder(doc, "Esempio pratico da slide_ai_prompt_design p.18")
    doc.add_paragraph()
    voice(doc, 'CATERINA', "Vediamo un confronto applicato a un caso d'uso quotidiano.", VOICES)
    stage(doc, "(pausa — il pubblico legge i due prompt)")
    voice(doc, 'GAIA', "Investire due minuti per strutturare bene la richiesta vi restituisce un testo che richiederà solo minimi aggiustamenti, anziché doverlo riscrivere da capo.", VOICES)
    doc.add_paragraph()

    # SLIDE 16
    h3(doc, "SLIDE 16 — STRUTTURE AVANZATE")
    placeholder(doc, "Contenuto da slide_ai_prompt_design p.20-21-22 riformulato in chiave accessibile")
    doc.add_paragraph()
    voice(doc, 'SARA', "Quando le attività diventano più complesse, possiamo usare tecniche avanzate per guidare il ragionamento della macchina.", VOICES)
    placeholder(doc, "Script da costruire dopo lettura PDF p.20-21-22")
    doc.add_paragraph()

    # SLIDE 17
    h3(doc, "SLIDE 17 — TOOL DI OTTIMIZZAZIONE: CAVEMAN")
    schermo(doc, '"Ottimizzazione dei token" — github.com/JuliusBrussee/caveman — compressione testo per AI')
    doc.add_paragraph()
    voice(doc, 'CATERINA', "Un breve inciso per chi vuole spingersi oltre. Esistono strumenti pensati per ottimizzare il modo in cui forniamo grandi moli di testo all'AI. Un esempio è Caveman, un progetto open source.", VOICES)
    voice(doc, 'ALBERTO', "L'idea è ridurre il testo rimuovendo tutto ciò che non è semanticamente essenziale per la macchina, risparmiando spazio (i cosiddetti \"token\") e costi, senza compromettere la comprensione da parte del modello.", VOICES)
    voice(doc, 'CATERINA', "È uno strumento utile specialmente quando si iniziano a usare flussi automatizzati complessi. Ne approfondiremo l'impiego nella prossima sessione.", VOICES)
    doc.add_paragraph()

    # SLIDE 18
    h3(doc, "SLIDE 18 — SEZIONE 04: GENERAZIONI INCLUSIVE & ETICA")
    stage(doc, "(cambio di sezione)")
    doc.add_paragraph()

    # SLIDE 19
    h3(doc, "SLIDE 19 — L'AI NON È NEUTRALE")
    schermo(doc, 'Testo: "I modelli riflettono i dati umani, inclusi stereotipi e pregiudizi storici." + callout "L\'impatto dei bias sui risultati"')
    placeholder(doc, "Schema bias da slide_ai_inclusivity p.9 + contenuto p.23-24-25 da slide_ai_prompt_design")
    doc.add_paragraph()
    voice(doc, 'GAIA', "Chiudiamo con un aspetto di estrema rilevanza professionale ed etica: la presunta \"neutralità\" della tecnologia.", VOICES)
    voice(doc, 'CATERINA', "I modelli AI sono stati addestrati su una fotografia del mondo reale, che contiene inevitabilmente pregiudizi, stereotipi storici e squilibri. Di default, la macchina tenderà a riproporli.", VOICES)
    voice(doc, 'CATERINA', "Nel nostro lavoro, produrre output stereotipati significa fallire in termini di qualità e inclusività. Abbiamo la responsabilità di guidare la macchina con prompt espliciti.", VOICES)
    doc.add_paragraph()

    # SLIDE 20
    h3(doc, "SLIDE 20 — VIDEO: PASOLINI / UNGARETTI")
    schermo(doc, "YouTube: https://www.youtube.com/watch?v=A5-kvHUcJw8  |  1964 — Pier Paolo Pasolini, Comizi d'Amore  |  Durata: ~2 min")
    doc.add_paragraph()
    voice(doc, 'SARA', "Per fissare questo concetto, vorremmo mostrarvi un breve frammento storico. È il 1964, e Pier Paolo Pasolini indaga l'opinione degli italiani in \"Comizi d'Amore\".", VOICES)
    stage(doc, "(si avvia il video — 2 min)")
    doc.add_paragraph()

    # SLIDE 21
    h3(doc, "SLIDE 21 — DOPO IL VIDEO: RIFLESSIONE")
    placeholder(doc, "Contenuto da slide_ai_inclusivity p.11-12-14")
    doc.add_paragraph()
    voice(doc, 'GAIA', "Notate come la selezione degli intervistati e la formulazione delle domande influenzino profondamente il quadro che emerge?", VOICES)
    stage(doc, "(breve scambio con il pubblico — 1-2 min)")
    voice(doc, 'CATERINA', "Se chiedessimo oggi a un'AI di sintetizzare l'opinione pubblica su temi complessi, il rischio è ottenere la voce della \"maggioranza statistica\" presente nei suoi dati di addestramento, silenziando altre prospettive.", VOICES)
    voice(doc, 'ALBERTO', "Esserne consapevoli ci permette di inserire vincoli precisi nei nostri prompt per ottenere risultati bilanciati e professionali.", VOICES)
    doc.add_paragraph()

    # PARTE 2
    divider(doc)
    h2(doc, "PARTE 2 — ESERCITAZIONE PRATICA (10 min)")
    divider(doc)
    doc.add_paragraph()

    # SLIDE 22
    h3(doc, "SLIDE 22 — ESERCIZIO")
    schermo(doc, "Step 1: redazione del prompt base | Step 2: applicazione delle Regole d'Oro | Step 3: confronto risultati | ⏱ 7 minuti")
    doc.add_paragraph()
    voice(doc, 'ALBERTO', "Ora mettiamo in pratica i concetti. Vi chiediamo di prendere i vostri laptop.", VOICES)
    voice(doc, 'SARA', "Scegliete un task reale che dovete affrontare oggi: una mail complessa, una sintesi, una bozza di progetto. Scrivete un primo prompt di getto. Dopodiché, in un'altra finestra, strutturatelo seguendo il framework visto prima (Ruolo, Contesto, Formato).", VOICES)
    voice(doc, 'CATERINA', "Abbiamo 7 minuti. Passeremo per un confronto e un supporto in tempo reale.", VOICES)
    stage(doc, "(i 4 oratori si confrontano con i colleghi ai tavoli)")
    doc.add_paragraph()

    h3(doc, "CONDIVISIONE (stessa slide, dopo il timer)")
    voice(doc, 'GAIA', "Se qualcuno vuole condividere l'esperienza: avete notato differenze sostanziali tra i due output?", VOICES)
    stage(doc, "(raccolta volontari — 2-3 esempi, commento e analisi condivisa)")
    voice(doc, 'ALBERTO', "Questo è un caso esemplare: aggiungere il contesto del target e il tono di voce desiderato ha evitato la necessità di una revisione estesa.", VOICES)
    doc.add_paragraph()

    # PARTE 3
    divider(doc)
    h2(doc, "PARTE 3 — CONFRONTO APERTO E CONCLUSIONI (10 min)")
    divider(doc)
    doc.add_paragraph()

    # SLIDE 23
    h3(doc, "SLIDE 23 — Q&A APERTO + LINK APPROFONDIMENTI")
    schermo(doc, '"Riflessioni e Confronto" + 3 domande callout + colonna link: Tokenizer / Caveman / SciTechDaily / The Bunker / Medium')
    doc.add_paragraph()
    voice(doc, 'CATERINA', "Invece del classico Q&A, vi chiediamo: quale aspetto trattato oggi pensate di applicare da subito o vi ha fatto riflettere di più?", VOICES)
    stage(doc, "(gestione del confronto, risposta a domande operative)")
    voice(doc, 'SARA', "Ringraziandovi per la partecipazione, vi anticipiamo che nella prossima sessione affronteremo il tema degli Agenti AI e dell'automazione di workflow strutturati.", VOICES)
    voice(doc, 'ALBERTO', "Sullo schermo trovate alcuni link di approfondimento per continuare l'esplorazione.", VOICES)
    doc.add_paragraph()

    # SLIDE 24
    h3(doc, "SLIDE 24 — GRAZIE")
    voice(doc, 'TUTTI', "Grazie mille a tutti!", VOICES)
    voice(doc, 'CATERINA', "Il nostro suggerimento finale è di non temere gli output imperfetti: ogni iterazione è un'opportunità per capire meglio come interagire con l'intelligenza artificiale. A presto.", VOICES)
    doc.add_paragraph()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PAGE BREAK → PAGINA 2: BIBLIOGRAFIA
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    doc.add_page_break()

    h1(doc, "BIBLIOGRAFIA & FONTI")
    body(doc, "Workshop AI Interno — Sessione 1", bold=True, color=BLUE, size=13)
    doc.add_paragraph()

    h3(doc, "1. Consumo energetico AI")
    body(doc, 'SciTechDaily — "Study Debunks Major Myth: AI\'s Energy Usage Is Significantly Less Than Feared"', size=11)
    body(doc, "https://scitechdaily.com/study-debunks-major-myth-ais-energy-usage-is-significantly-less-than-feared/", color=RGBColor(0x00,0x55,0xaa), size=10)
    doc.add_paragraph()
    body(doc, 'The Bunker — "Does AI Pollute and How Does It Compare to Other Everyday Activities?"', size=11)
    body(doc, "https://www.the-bunker.it/en/rubrica/does-ai-pollute-and-how-does-it-compare-to-other-everyday-activities/", color=RGBColor(0x00,0x55,0xaa), size=10)
    doc.add_paragraph()

    h3(doc, "2. Gestione file e formati")
    body(doc, 'Medium — Lawrence Teixeira: "From Locked PDFs to Limitless AI: The Plain-Text Revolution You Can\'t Ignore"', size=11)
    body(doc, "https://medium.com/@lawrenceteixeira/from-locked-pdfs-to-limitless-ai-the-plain-text-revolution-you-cant-ignore-b1592aae3cb4", color=RGBColor(0x00,0x55,0xaa), size=10)
    doc.add_paragraph()
    body(doc, 'Medium — Cristian Lefter: "Why Markdown Became the Working Language of AI"', size=11)
    body(doc, "https://medium.com/@cristian.lefter/why-markdown-became-the-working-language-of-ai-44a5f19a423c", color=RGBColor(0x00,0x55,0xaa), size=10)
    doc.add_paragraph()

    h3(doc, "3. Prompt Engineering")
    body(doc, "OpenAI Tokenizer — strumento per visualizzare come i modelli spezzano il testo in token", size=11)
    body(doc, "https://platform.openai.com/tokenizer", color=RGBColor(0x00,0x55,0xaa), size=10)
    doc.add_paragraph()
    body(doc, "PDF interno — slide_ai_prompt_design.pdf", size=11, bold=True)
    body(doc, "Pagine usate: p.5 (ecosistema), p.6-7-8 (arricchimento), p.12 (regole base), p.15-16 (tecniche), p.18 (prima/dopo), p.20-21-22 (strutture avanzate), p.23-24-25 (inclusività → prompt)", size=10, color=GREY)
    doc.add_paragraph()

    h3(doc, "4. Inclusività & Etica AI")
    body(doc, "PDF interno — slide_ai_inclusivity.pdf", size=11, bold=True)
    body(doc, "Pagine usate: p.9 (schema bias), p.11-12-14 (riflessione post-video). Approfondimento: p.22-40 (solo link).", size=10, color=GREY)
    doc.add_paragraph()
    body(doc, "PDF interno — dove_inclusive_prompt_images.pdf", size=11, bold=True)
    body(doc, "Immagini e case study di bias visivo nei risultati di generazione AI.", size=10, color=GREY)
    doc.add_paragraph()

    h3(doc, "5. Video")
    body(doc, "Pier Paolo Pasolini — Comizi d'Amore (1964) — Clip con Ungaretti", size=11)
    body(doc, "https://www.youtube.com/watch?v=A5-kvHUcJw8  |  Durata clip: ~2 min", color=RGBColor(0x00,0x55,0xaa), size=10)
    doc.add_paragraph()

    h3(doc, "6. Tool citati")
    body(doc, "Caveman — compressore di output AI, open source (risparmio 30-65% token)", size=11)
    body(doc, "https://github.com/JuliusBrussee/caveman", color=RGBColor(0x00,0x55,0xaa), size=10)
    doc.add_paragraph()

    h3(doc, "7. Corso di riferimento")
    body(doc, "Skool AI Academy — materiale di approfondimento per approfondire i temi trattati", size=11)
    body(doc, "https://www.skool.com/ai-academy-2306/classroom/a6764c58?md=49fd716208a74c8084e37708a01e5f14", color=RGBColor(0x00,0x55,0xaa), size=10)
    doc.add_paragraph()

    divider(doc)
    body(doc, "Nota: i link ai PDF interni non sono pubblici. Richiedere accesso alla cartella condivisa del progetto.", size=9, color=GREY, italic=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # SALVA
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    doc.save(OUT_FILE)
    print(f"✅ Documento salvato: {OUT_FILE}")
    return OUT_FILE

if __name__ == '__main__':
    path = build_doc()
    print(f"\n📎 Per importare in Google Docs:")
    print(f"   1. Apri Google Docs")
    print(f"   2. File → Apri → Carica → seleziona il file:")
    print(f"      {path}")
    print(f"   Oppure trascinalo su drive.google.com")
