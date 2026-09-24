#!/usr/bin/env python3
"""
write_gdoc.py — Scrive script + bibliografia nel Google Doc del workshop
Doc: https://docs.google.com/document/d/1jfs4gcsJnalqJJAGT6TBLhPo88QpucjpgazGHv-3PPw/edit

Esegui DOPO aver autenticato con: python3 scripts/auth.py
"""

import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── CONFIG ────────────────────────────────────────────────────────────────
DOC_ID      = '1jfs4gcsJnalqJJAGT6TBLhPo88QpucjpgazGHv-3PPw'
TOKEN_FILE  = os.path.expanduser('~/.gdoc_token.json')
SCOPES      = ['https://www.googleapis.com/auth/documents']

# ─── AUTH ──────────────────────────────────────────────────────────────────
def get_creds():
    if not os.path.exists(TOKEN_FILE):
        print("❌ Token non trovato. Esegui prima: python3 scripts/auth.py")
        sys.exit(1)
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

# ─── HELPERS ───────────────────────────────────────────────────────────────
def clear_doc(service):
    """Svuota il documento mantenendo la struttura"""
    doc = service.documents().get(documentId=DOC_ID).execute()
    content = doc.get('body', {}).get('content', [])
    end_idx = doc['body']['content'][-1]['endIndex']
    if end_idx > 2:
        service.documents().batchUpdate(
            documentId=DOC_ID,
            body={'requests': [{'deleteContentRange': {
                'range': {'startIndex': 1, 'endIndex': end_idx - 1}
            }}]}
        ).execute()
    print("🗑️  Documento svuotato.")

def insert_text_with_style(requests, index, text, style=None, named_style=None):
    """Aggiunge testo e lo formatta"""
    requests.append({'insertText': {'location': {'index': index}, 'text': text}})
    length = len(text)
    end = index + length
    if named_style:
        requests.append({'updateParagraphStyle': {
            'range': {'startIndex': index, 'endIndex': end},
            'paragraphStyle': {'namedStyleType': named_style},
            'fields': 'namedStyleType'
        }})
    if style:
        requests.append({'updateTextStyle': {
            'range': {'startIndex': index, 'endIndex': end},
            'textStyle': style,
            'fields': ','.join(style.keys())
        }})
    return end

# ─── CONTENUTO PAGINA 1: SCRIPT ────────────────────────────────────────────
SCRIPT_BLOCKS = [
    # (testo, named_style, bold, size)
    ("SCRIPT — Workshop AI: Sessione 1\n", "HEADING_1", True, 20),
    ("\"Manuale di sopravvivenza all'AI\"\n", "HEADING_2", False, 14),
    ("Durata: ~50 min  |  Oratori: Sara · Alberto · Gaia · Caterina\n", "NORMAL_TEXT", False, 11),
    ("Formato: 30' teoria + 10' esercizio + 10' confronto  |  24 slide\n\n", "NORMAL_TEXT", False, 11),

    # LEGENDA
    ("LEGENDA\n", "HEADING_3", True, 13),
    ("[slide →] = cambio slide     [schermo] = cosa appare     (regia) = indicazioni\n", "NORMAL_TEXT", False, 10),
    ("[PLACEHOLDER] = contenuto da completare con i PDF\n\n", "NORMAL_TEXT", False, 10),

    # PARTE 1
    ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "NORMAL_TEXT", False, 8),
    ("PARTE 1 — TEORIA DIALOGICA (30 min)\n", "HEADING_2", True, 16),
    ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n", "NORMAL_TEXT", False, 8),

    ("SLIDE 1 — COVER\n", "HEADING_3", True, 13),
    ("[schermo] \"Manuale di sopravvivenza all'AI\" | \"Ecosistema · Prompt Engineering · Sfide Etiche\"\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Benvenuti. Siamo Sara, Alberto, Gaia e io, Caterina. Abbiamo deciso di parlarvi di AI — non perché siamo i maestri di qualcosa, ma perché ci siamo ritrovati a usarla ogni giorno e abbiamo pensato: meglio capire cosa stiamo facendo.\n\n", "NORMAL_TEXT", False, 11),
    ("SARA: E soprattutto: meglio smettere di avere paura di sbagliare qualcosa.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: Quindi questo non è un corso. È più una condivisione tra pari. Tipo un caffè, ma con le slide.\n\n", "NORMAL_TEXT", False, 11),
    ("GAIA: Caffè che, come vedremo tra poco, consuma molta meno energia di quello che pensate.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 2 — SCALETTA\n", "HEADING_3", True, 13),
    ("[schermo] 4 punti: 01 Ecosistema AI & Consumi | 02 Gestione dei File | 03 Prompt Optimization | 04 Generazioni Inclusive & Etica\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Eccoci qua. In 50 minuti proviamo a coprire quattro aree — teoria dialogica, poi un esercizio pratico, poi apriamo a domande e confronto.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: Interrompete quando volete. Anzi, è previsto.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 3 — ROMPIGHIACCIO\n", "HEADING_3", True, 13),
    ("[schermo] \"Prima di partire — Alzate la mano: chi ha già usato un tool di AI al lavoro?\"\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Prima di iniziare, vogliamo capire da dove partiamo tutti. Alzate la mano — chi ha già usato ChatGPT, Copilot, Gemini o qualsiasi altra AI al lavoro?\n\n", "NORMAL_TEXT", False, 11),
    ("SARA: Perfetto. E chi non ha alzato la mano — tranquilli, è esattamente per questo che siamo qui.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: Questo non è un corso. È una conversazione tra pari.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 4 — SEZIONE 01: ECOSISTEMA AI & CONSUMI\n", "HEADING_3", True, 13),
    ("[Cambio di sezione]\n\n", "NORMAL_TEXT", False, 10),

    ("SLIDE 5 — ECOSISTEMA: I PLAYER\n", "HEADING_3", True, 13),
    ("[schermo] AI Generativa: ChatGPT/OpenAI, Claude/Anthropic, Gemini/Google, Copilot/Microsoft, Midjourney/DALL·E\n", "NORMAL_TEXT", False, 10),
    ("[schermo] AI Classica: filtro spam, Netflix, Face ID, traduzione automatica\n\n", "NORMAL_TEXT", False, 10),
    ("SARA: Quando diciamo \"AI\" stiamo in realtà parlando di un universo molto vasto. Ci sono due grandi famiglie.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: L'AI generativa — quella che genera testo, immagini, codice, audio — è quella di cui parleremo oggi. I player principali sono OpenAI con ChatGPT, Anthropic con Claude, Google con Gemini, Microsoft con Copilot.\n\n", "NORMAL_TEXT", False, 11),
    ("SARA: E poi c'è l'AI classica, quella che riconosce pattern, fa previsioni, filtra spam. Quella già la usate da anni senza saperlo — il filtro antispam, l'algoritmo di Netflix, il Face ID del vostro telefono.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 6 — COME FUNZIONA? IN PAROLE SEMPLICI\n", "HEADING_3", True, 13),
    ("[schermo] Spiegazione senza jargon + analogia autocomplete + 3 bullet: no coscienza / può sbagliare / il contesto cambia tutto\n\n", "NORMAL_TEXT", False, 10),
    ("GAIA: Prima di andare avanti — una domanda: qualcuno sa, anche vagamente, come funzionano questi strumenti?\n\n", "NORMAL_TEXT", False, 11),
    ("GAIA: In parola semplice: questi modelli sono stati addestrati su quantità enormi di testo — libri, articoli, siti web, codice. Hanno imparato a prevedere quale parola viene dopo, in modo statisticamente probabile.\n\n", "NORMAL_TEXT", False, 11),
    ("CATERINA: Non \"pensano\" come noi. Non hanno coscienza, non capiscono davvero. Ma sono straordinariamente bravi a sembrarlo. Pensate a un autocomplete avanzatissimo che ha letto tutto internet.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: E questo ha una conseguenza pratica importante: possono sbagliare — e farlo con sicurezza. Quindi vanno sempre verificati.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 7 — SOSTENIBILITÀ E CONSUMI\n", "HEADING_3", True, 13),
    ("[schermo] Tabella: Prompt (~5-10x Google) | Training (energia significativa una tantum) | Scala (miliardi/giorno)\n\n", "NORMAL_TEXT", False, 10),
    ("GAIA: Parliamo di qualcosa di cui si sente spesso dire cose contrastanti — l'impatto ambientale dell'AI.\n\n", "NORMAL_TEXT", False, 11),
    ("CATERINA: C'è una narrativa catastrofista — \"l'AI sta distruggendo il pianeta\" — e una che minimizza tutto. La realtà sta nel mezzo.\n\n", "NORMAL_TEXT", False, 11),
    ("GAIA: Uno studio recente ha sfatato alcuni miti: un singolo prompt su ChatGPT consuma circa 5-10 volte una ricerca Google. Non poco, ma molto meno di quanto si pensi.\n\n", "NORMAL_TEXT", False, 11),
    ("CATERINA: Prompt ben scritti non sono solo più efficaci — sono anche più sostenibili. Meno tentativi, meno consumo.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 8 — QUIZ: QUANTO CONSUMA UN PROMPT?\n", "HEADING_3", True, 13),
    ("[schermo] A) Fare un caffè espresso  B) 5–10 ricerche Google  C) Volare da Milano a New York\n\n", "NORMAL_TEXT", False, 10),
    ("ALBERTO: Quiz veloce. Secondo voi, quanto consuma un prompt?\n", "NORMAL_TEXT", False, 11),
    ("(aspetta le risposte dal pubblico — 30 sec)\n\n", "NORMAL_TEXT", False, 10),
    ("ALBERTO: Risposta: B. Circa 5-10 ricerche Google. Non un caffè, non un volo. La C è la narrativa catastrofista che gira in rete, ma i dati non la supportano.\n\n", "NORMAL_TEXT", False, 11),
    ("SARA: Il che non significa che sia irrilevante — significa che possiamo usarla consapevolmente senza sensi di colpa esagerati.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 9 — SEZIONE 02: GESTIONE DEI FILE\n", "HEADING_3", True, 13),
    ("[Cambio di sezione]\n\n", "NORMAL_TEXT", False, 10),

    ("SLIDE 10 — FORMATI FILE\n", "HEADING_3", True, 13),
    ("[schermo] ✅ .md .txt .csv | ⚠️ .pdf .docx | ❌ PDF scansionati | ❌ .xlsx con formule\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Cambio tema — i file. Quando lavorate con un'AI e dovete darle del contesto, il formato conta moltissimo.\n\n", "NORMAL_TEXT", False, 11),
    ("SARA: L'AI non \"legge\" come facciamo noi. Elabora testo. Quindi più il testo è pulito e strutturato, meglio funziona.\n\n", "NORMAL_TEXT", False, 11),
    ("CATERINA: I formati migliori sono i file di testo puro: .txt, .csv, e soprattutto .md. Quelli peggiori? PDF scansionati — che per l'AI sono praticamente immagini — e file Excel con formule.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: Questo vale anche per i nostri brief, le nostre ricerche. Prima di incollare qualcosa in ChatGPT, vale la pena chiedersi: sto dando testo pulito o rumore?\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 11 — QUIZ: COS'È UN FILE .MD?\n", "HEADING_3", True, 13),
    ("[schermo] A) Un supermercato molto swag  B) Una droga sintetica  C) Markdown — testo strutturato con sintassi leggera\n\n", "NORMAL_TEXT", False, 10),
    ("ALBERTO: (con finta serietà) Quiz culturale. Cos'è un file .md?\n", "NORMAL_TEXT", False, 11),
    ("(aspetta con divertimento le risposte)\n\n", "NORMAL_TEXT", False, 10),
    ("ALBERTO: Markdown. Un formato di testo semplicissimo dove si usano simboli leggeri per strutturare: # per i titoli, ** per il grassetto, - per le liste.\n\n", "NORMAL_TEXT", False, 11),
    ("GAIA: Le AI lo adorano perché capiscono perfettamente la struttura senza dover interpretare formattazione complessa. Se non lo usate già, è il momento di iniziare.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 12 — SEZIONE 03: PROMPT OPTIMIZATION\n", "HEADING_3", True, 13),
    ("[Cambio di sezione]\n\n", "NORMAL_TEXT", False, 10),

    ("SLIDE 13 — IL PROMPT PESSIMO (interattivo)\n", "HEADING_3", True, 13),
    ("[schermo] Riquadro rosso: \"fammi una presentazione sull'AI\" → output: generico, inutile\n\n", "NORMAL_TEXT", False, 10),
    ("SARA: Arriviamo alla parte più pratica — come si parla bene a un'AI.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: Il problema più comune: le persone usano l'AI come fosse Google. Scrivono 3 parole e si aspettano magia.\n\n", "NORMAL_TEXT", False, 11),
    ("SARA: Guardate questo prompt. \"Fammi una presentazione sull'AI\". Cosa manca? Ditecelo voi.\n", "NORMAL_TEXT", False, 11),
    ("(raccoglie risposte dal pubblico — 1-2 min)\n\n", "NORMAL_TEXT", False, 10),
    ("ALBERTO: Esatto. Manca: a chi è rivolta? Che formato? Quante slide? Che tono? Che obiettivo? Il contesto è tutto.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 14 — LE REGOLE D'ORO\n", "HEADING_3", True, 13),
    ("[schermo] 5 regole: Dai un RUOLO | Specifica il CONTESTO | Definisci il FORMATO | Dai ESEMPI | ITERA\n", "NORMAL_TEXT", False, 10),
    ("[PLACEHOLDER: integrare con slide_ai_prompt_design p.12 + p.15-16]\n\n", "NORMAL_TEXT", False, 10),
    ("SARA: Ecco le regole d'oro. Cinque principi che trasformano un prompt mediocre in uno efficace.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: La più ignorata è la prima: dare un ruolo. \"Sei un copywriter senior che lavora nel settore fintech\" è un inizio completamente diverso da \"scrivi un testo\".\n\n", "NORMAL_TEXT", False, 11),
    ("SARA: E la più potente è l'ultima: iterare. L'AI non è un oracolo — è una conversazione.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 15 — PRIMA / DOPO\n", "HEADING_3", True, 13),
    ("[schermo] Confronto: ❌ \"scrivi un'email al cliente\" vs ✅ prompt strutturato con ruolo + contesto + formato\n", "NORMAL_TEXT", False, 10),
    ("[PLACEHOLDER: esempio pratico da slide_ai_prompt_design p.18]\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Guardate questo confronto pratico.\n", "NORMAL_TEXT", False, 11),
    ("(pausa — il pubblico legge i due prompt)\n\n", "NORMAL_TEXT", False, 10),
    ("GAIA: La differenza di qualità dell'output è abissale. E il prompt migliore non è necessariamente più lungo — è più preciso.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 16 — STRUTTURE AVANZATE\n", "HEADING_3", True, 13),
    ("[PLACEHOLDER: contenuto da slide_ai_prompt_design p.20-21-22]\n\n", "NORMAL_TEXT", False, 10),
    ("SARA: Per chi vuole andare un po' più in profondità — ci sono tecniche più avanzate.\n\n", "NORMAL_TEXT", False, 11),
    ("[PLACEHOLDER: script da costruire dopo lettura PDF p.20-21-22]\n\n", "NORMAL_TEXT", False, 10),

    ("SLIDE 17 — CAVEMAN\n", "HEADING_3", True, 13),
    ("[schermo] \"Why use many token when few token do trick?\" | github.com/JuliusBrussee/caveman\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Prima di passare all'ultima parte — una curiosità per chi vuole approfondire. Esiste uno strumento open source che si chiama Caveman.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: Il suo principio è disarmante: perché usare molti token quando pochi token bastano? Può ridurre il volume delle risposte del 30-65% senza perdere le informazioni critiche.\n\n", "NORMAL_TEXT", False, 11),
    ("CATERINA: Non è per uso quotidiano di tutti — ma se userete mai AI con agenti o flussi automatizzati, tenerlo a mente ha senso. Nella prossima sessione ci torniamo.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 18 — SEZIONE 04: GENERAZIONI INCLUSIVE & ETICA\n", "HEADING_3", True, 13),
    ("[Cambio di sezione]\n\n", "NORMAL_TEXT", False, 10),

    ("SLIDE 19 — L'AI NON È NEUTRALE\n", "HEADING_3", True, 13),
    ("[schermo] Testo: \"Addestrata su dati umani, con tutti i loro bias\" + callout + [PLACEHOLDER schema bias]\n\n", "NORMAL_TEXT", False, 10),
    ("GAIA: Ultima parte della teoria — forse la più importante. L'AI non è neutrale.\n\n", "NORMAL_TEXT", False, 11),
    ("CATERINA: È addestrata su dati prodotti da esseri umani. Con tutti i loro bias, i loro pregiudizi, le loro lacune. E quei bias si riproducono nell'output se non stiamo attenti.\n\n", "NORMAL_TEXT", False, 11),
    ("[PLACEHOLDER: contenuto da slide_ai_prompt_design p.23-24-25 + slide_ai_inclusivity p.9]\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Un output che esclude metà del pubblico non è solo poco etico — è un output sbagliato. Punto.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 20 — VIDEO: PASOLINI / UNGARETTI\n", "HEADING_3", True, 13),
    ("https://www.youtube.com/watch?v=A5-kvHUcJw8  |  Durata: ~2 min\n\n", "NORMAL_TEXT", False, 10),
    ("SARA: Ora vi facciamo vedere un video. Due minuti. È il 1964 — Pasolini gira per l'Italia e chiede alla gente domande scomode.\n\n", "NORMAL_TEXT", False, 11),
    ("[VIDEO — 2 min]\n\n", "NORMAL_TEXT", False, 10),

    ("SLIDE 21 — DOPO IL VIDEO: RIFLESSIONE\n", "HEADING_3", True, 13),
    ("[PLACEHOLDER: contenuto da slide_ai_inclusivity p.11-12-14]\n\n", "NORMAL_TEXT", False, 10),
    ("GAIA: Avete notato qualcosa? Nelle risposte, nelle reazioni, in chi Pasolini sceglieva di intervistare?\n", "NORMAL_TEXT", False, 11),
    ("(breve scambio con il pubblico — 1-2 min)\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Adesso immaginate di chiedere a ChatGPT le stesse domande. Cosa risponderebbe? Chi rappresenta? Chi esclude?\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: Guidare l'AI verso output inclusivi non è solo etica — è qualità.\n\n", "NORMAL_TEXT", False, 11),

    # PARTE 2
    ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "NORMAL_TEXT", False, 8),
    ("PARTE 2 — MANI IN PASTA (10 min)\n", "HEADING_2", True, 16),
    ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n", "NORMAL_TEXT", False, 8),

    ("SLIDE 22 — ESERCIZIO\n", "HEADING_3", True, 13),
    ("[schermo] Step 1: prompt istintivo | Step 2: riscrivi con regole d'oro | Step 3: confronta output | Timer: 7 min\n\n", "NORMAL_TEXT", False, 10),
    ("ALBERTO: Ok, si smette di ascoltare e si inizia a fare. Prendete il vostro telefono o laptop.\n\n", "NORMAL_TEXT", False, 11),
    ("SARA: Pensate a qualcosa di reale: una mail difficile, un brief da riassumere, una ricerca. Scrivete il prompt come lo scrivereste adesso, poi riscrivetelo applicando quello che abbiamo visto: ruolo, contesto, formato.\n\n", "NORMAL_TEXT", False, 11),
    ("CATERINA: Avete 7 minuti. Noi giriamo e guardiamo — senza giudicare.\n\n", "NORMAL_TEXT", False, 11),
    ("(i 4 oratori circolano tra il pubblico durante l'esercizio)\n\n", "NORMAL_TEXT", False, 10),
    ("CONDIVISIONE (stesso timer)\n\n", "HEADING_3", True, 12),
    ("GAIA: Tempo! Chi vuole leggere il suo prompt \"prima\" e il suo \"dopo\"?\n", "NORMAL_TEXT", False, 11),
    ("(raccolta volontari — 2-3 esempi dal pubblico, breve commento degli oratori)\n\n", "NORMAL_TEXT", False, 10),

    # PARTE 3
    ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "NORMAL_TEXT", False, 8),
    ("PARTE 3 — CONFRONTO APERTO (10 min)\n", "HEADING_2", True, 16),
    ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n", "NORMAL_TEXT", False, 8),

    ("SLIDE 23 — Q&A APERTO + LINK APPROFONDIMENTI\n", "HEADING_3", True, 13),
    ("[schermo] \"Cosa vi ha sorpreso?\" + link: Tokenizer / Caveman / SciTechDaily / The Bunker / Medium\n\n", "NORMAL_TEXT", False, 10),
    ("CATERINA: Non \"avete domande?\" — ma: cosa vi ha sorpreso di più?\n", "NORMAL_TEXT", False, 11),
    ("(gestione libera del confronto)\n\n", "NORMAL_TEXT", False, 10),
    ("SARA: La prossima sessione ci addentriamo negli agenti AI — cosa sono, come funzionano, come si automatizzano flussi di lavoro reali.\n\n", "NORMAL_TEXT", False, 11),
    ("ALBERTO: Stay tuned. E nel frattempo — usate quello che avete imparato oggi. Anche solo una cosa.\n\n", "NORMAL_TEXT", False, 11),

    ("SLIDE 24 — GRAZIE\n", "HEADING_3", True, 13),
    ("TUTTI: Grazie!\n\n", "NORMAL_TEXT", False, 11),
    ("CATERINA: Il miglior modo per imparare l'AI è usarla. Anche male. Soprattutto male, all'inizio.\n\n", "NORMAL_TEXT", False, 11),
]

# ─── CONTENUTO PAGINA 2: BIBLIOGRAFIA ──────────────────────────────────────
BIBLIOGRAPHY_BLOCKS = [
    ("\n\n\n", "NORMAL_TEXT", False, 11),  # page break simulation

    ("BIBLIOGRAFIA & FONTI\n", "HEADING_1", True, 20),
    ("Workshop AI Interno — Sessione 1\n\n", "HEADING_2", False, 14),

    ("1. CONSUMO ENERGETICO AI\n", "HEADING_3", True, 13),
    ("SciTechDaily — \"Study Debunks Major Myth: AI's Energy Usage Is Significantly Less Than Feared\"\n", "NORMAL_TEXT", False, 11),
    ("https://scitechdaily.com/study-debunks-major-myth-ais-energy-usage-is-significantly-less-than-feared/\n\n", "NORMAL_TEXT", False, 10),
    ("The Bunker — \"Does AI Pollute and How Does It Compare to Other Everyday Activities?\"\n", "NORMAL_TEXT", False, 11),
    ("https://www.the-bunker.it/en/rubrica/does-ai-pollute-and-how-does-it-compare-to-other-everyday-activities/\n\n", "NORMAL_TEXT", False, 10),

    ("2. GESTIONE FILE E FORMATI\n", "HEADING_3", True, 13),
    ("Medium — Lawrence Teixeira: \"From Locked PDFs to Limitless AI: The Plain-Text Revolution You Can't Ignore\"\n", "NORMAL_TEXT", False, 11),
    ("https://medium.com/@lawrenceteixeira/from-locked-pdfs-to-limitless-ai-the-plain-text-revolution-you-cant-ignore-b1592aae3cb4\n\n", "NORMAL_TEXT", False, 10),
    ("Medium — Cristian Lefter: \"Why Markdown Became the Working Language of AI\"\n", "NORMAL_TEXT", False, 11),
    ("https://medium.com/@cristian.lefter/why-markdown-became-the-working-language-of-ai-44a5f19a423c\n\n", "NORMAL_TEXT", False, 10),

    ("3. PROMPT ENGINEERING\n", "HEADING_3", True, 13),
    ("OpenAI Tokenizer — strumento per visualizzare come i modelli spezzano il testo in token\n", "NORMAL_TEXT", False, 11),
    ("https://platform.openai.com/tokenizer\n\n", "NORMAL_TEXT", False, 10),
    ("PDF di riferimento interno — slide_ai_prompt_design.pdf\n", "NORMAL_TEXT", False, 11),
    ("(pagine usate: p.5, p.6-7-8, p.12, p.15-16, p.18, p.20-21-22, p.23-24-25)\n\n", "NORMAL_TEXT", False, 10),

    ("4. INCLUSIVITÀ & ETICA AI\n", "HEADING_3", True, 13),
    ("PDF di riferimento interno — slide_ai_inclusivity.pdf\n", "NORMAL_TEXT", False, 11),
    ("(pagine usate: p.9, p.11-12-14; approfondimento: p.22-40)\n\n", "NORMAL_TEXT", False, 10),
    ("PDF di riferimento interno — dove_inclusive_prompt_images.pdf\n", "NORMAL_TEXT", False, 11),
    ("(immagini e case study bias visivo)\n\n", "NORMAL_TEXT", False, 10),

    ("5. VIDEO\n", "HEADING_3", True, 13),
    ("Pier Paolo Pasolini — Comizi d'Amore (1964) — Clip con Ungaretti\n", "NORMAL_TEXT", False, 11),
    ("https://www.youtube.com/watch?v=A5-kvHUcJw8  |  Durata: ~2 min\n\n", "NORMAL_TEXT", False, 10),

    ("6. TOOL CITATI\n", "HEADING_3", True, 13),
    ("Caveman — compressore di output AI, open source\n", "NORMAL_TEXT", False, 11),
    ("https://github.com/JuliusBrussee/caveman\n\n", "NORMAL_TEXT", False, 10),

    ("7. CORSO DI RIFERIMENTO\n", "HEADING_3", True, 13),
    ("Skool AI Academy — materiale di approfondimento\n", "NORMAL_TEXT", False, 11),
    ("https://www.skool.com/ai-academy-2306/classroom/a6764c58?md=49fd716208a74c8084e37708a01e5f14\n\n", "NORMAL_TEXT", False, 10),

    ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n", "NORMAL_TEXT", False, 8),
    ("Note: i link ai PDF interni non sono pubblici. Richiedere accesso alla cartella condivisa del progetto.\n", "NORMAL_TEXT", False, 10),
]

# ─── WRITE TO DOC ──────────────────────────────────────────────────────────
def write_all_blocks(service, blocks):
    """Scrive tutti i blocchi di testo nel documento in batch"""
    # First, get current doc to find end
    doc = service.documents().get(documentId=DOC_ID).execute()
    
    # Build all text first, then insert in one shot
    full_text = ''
    for (text, _, _, _) in blocks:
        full_text += text
    
    # Insert all text at once
    requests = [{'insertText': {'location': {'index': 1}, 'text': full_text}}]
    service.documents().batchUpdate(documentId=DOC_ID, body={'requests': requests}).execute()
    print(f"✅ Testo inserito ({len(full_text)} caratteri)")
    
    # Now apply formatting in a second pass
    print("🎨 Applicazione formattazione...")
    format_requests = []
    cursor = 1
    
    for (text, named_style, bold, font_size) in blocks:
        length = len(text)
        end = cursor + length
        
        if named_style != "NORMAL_TEXT":
            format_requests.append({'updateParagraphStyle': {
                'range': {'startIndex': cursor, 'endIndex': end},
                'paragraphStyle': {'namedStyleType': named_style},
                'fields': 'namedStyleType'
            }})
        
        text_style = {}
        if bold:
            text_style['bold'] = True
        if font_size:
            text_style['fontSize'] = {'magnitude': font_size, 'unit': 'PT'}
        
        if text_style:
            format_requests.append({'updateTextStyle': {
                'range': {'startIndex': cursor, 'endIndex': end},
                'textStyle': text_style,
                'fields': ','.join(text_style.keys())
            }})
        
        cursor = end
        
        # Batch in groups of 50 to avoid API limits
        if len(format_requests) >= 50:
            service.documents().batchUpdate(documentId=DOC_ID, body={'requests': format_requests}).execute()
            format_requests = []
            time.sleep(0.3)
    
    if format_requests:
        service.documents().batchUpdate(documentId=DOC_ID, body={'requests': format_requests}).execute()
    
    print(f"✅ Formattazione applicata.")

def main():
    print(f"📄 Scrittura nel Google Doc: {DOC_ID}")
    
    creds = get_creds()
    service = build('docs', 'v1', credentials=creds)
    
    # Svuota il documento
    clear_doc(service)
    time.sleep(0.5)
    
    # Combina script + bibliografia
    all_blocks = SCRIPT_BLOCKS + BIBLIOGRAPHY_BLOCKS
    write_all_blocks(service, all_blocks)
    
    print(f"\n✅ Completato!")
    print(f"📎 Apri il doc: https://docs.google.com/document/d/{DOC_ID}/edit")

if __name__ == '__main__':
    main()
