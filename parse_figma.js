const fs = require('fs');
const files = [
  '/Users/cate/.gemini/antigravity/brain/6f991ac0-1981-4ed4-bc44-b1af846c031f/.system_generated/steps/253/output.txt',
  '/Users/cate/.gemini/antigravity/brain/6f991ac0-1981-4ed4-bc44-b1af846c031f/.system_generated/steps/257/output.txt',
  '/Users/cate/.gemini/antigravity/brain/6f991ac0-1981-4ed4-bc44-b1af846c031f/.system_generated/steps/259/output.txt'
];

let allNodes = [];
function extractNodes(obj) {
  if (obj.id && obj.type === "TEXT") {
    allNodes.push({id: obj.id, content: obj.content});
  }
  if (obj.children) {
    obj.children.forEach(extractNodes);
  }
}

files.forEach(f => {
  const txt = fs.readFileSync(f, 'utf8');
  const jsonStr = txt.replace(/^[0-9]+: /gm, ''); // remove line numbers if any
  try {
    const data = JSON.parse(jsonStr);
    extractNodes(data.tree);
  } catch (e) {
    console.log("Error parsing", f);
  }
});

const titles = [
  { t: "01 \u2014 Ecosistema AI & Consumi", s: "Cos'è l'AI, chi sono i player, quanto consuma un prompt" },
  { t: "ECOSISTEMA: I PLAYER", s: "AI Generativa vs AI Classica" },
  { t: "COME FUNZIONA? IN PAROLE SEMPLICI", s: "Spiegazione senza jargon + analogia autocomplete" },
  { t: "SOSTENIBILITÀ E CONSUMI", s: "Tabella: Prompt vs Training vs Scala" },
  { t: "QUIZ: QUANTO CONSUMA UN PROMPT?", s: "A) Fare un caffè | B) 5-10 ricerche Google | C) Volo Milano-Roma" },
  { t: "02 \u2014 Gestione dei File", s: "Migliori pratiche per i formati dei documenti" },
  { t: "FORMATI FILE", s: "✅ .md .txt .csv   ⚠️ .pdf .docx   ❌ PDF scansionati / .xlsx con formule" },
  { t: "QUIZ: COS'È UN FILE .MD?", s: "A) Log di sistema | B) Database | C) Markdown \u2014 testo puro" },
  { t: "03 \u2014 Prompt Optimization", s: "Principi per comunicare efficacemente" },
  { t: "IL PROMPT INEFFICACE", s: "Crea una presentazione sull'AI \u2192 Mancano contesto, formato, ruolo." },
  { t: "DOMANDE E RISPOSTE / GRAZIE!", s: " " }
];

let code = '';
let titleIdx = 0;

allNodes.forEach(n => {
  if (n.content === 'Jakala  x Snam' || n.content === 'JAKALA x Snam') {
    code += `await figma.modify("${n.id}", { characters: "Workshop AI Interno" });\n`;
  }
  
  if (n.content === 'Jarvis by Snam' || n.content === 'Titolo slide' || n.content === 'Titolo secondario' || n.content === 'Grazie!') {
    if (titleIdx < titles.length) {
      code += `await figma.modify("${n.id}", { characters: "${titles[titleIdx].t}" });\n`;
      titleIdx++;
    }
  }
  
});

// Since the titles and subtitles don't always come strictly as Title then Subtitle,
// let's do a pass just on subtitles
let subIdx = 0;
allNodes.forEach(n => {
  if (n.content === 'Framework UX' || n.content === 'Sottotitolo slide' || n.content === 'punto 1\\npunto 2' || n.content === 'Sottititolo elemento') {
    // Only replace one subtitle per slide
    if (n.content === 'Sottititolo elemento' && Math.random() > 0) {
       // well, there are multiple "Sottititolo elemento" per slide! Let's just target the first one or we can just replace 'Framework UX' and 'Sottotitolo slide'
       // Wait, on the list slides, there are multiple elements. Let's just keep it simple.
    }
    
    if (subIdx < titles.length && (n.content === 'Framework UX' || n.content === 'Sottotitolo slide' || n.content === 'punto 1\\npunto 2')) {
       code += `await figma.modify("${n.id}", { characters: "${titles[subIdx].s}" });\n`;
       subIdx++;
    }
  }
});

console.log(code);
