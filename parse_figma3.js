const fs = require('fs');
const lines = `await figma.modify("1:367", { characters: "Workshop AI Interno" });
await figma.modify("2:523", { characters: "01 — Ecosistema AI & Consumi" }); // was: Jarvis by Snam
await figma.modify("6:798", { characters: "Workshop AI Interno" });
await figma.modify("6:803", { characters: "ECOSISTEMA: I PLAYER" }); // was: Jarvis by Snam
await figma.modify("6:812", { characters: "Workshop AI Interno" });
await figma.modify("3:584", { characters: "Workshop AI Interno" });
await figma.modify("3:589", { characters: "COME FUNZIONA? IN PAROLE SEMPLICI" }); // was: Titolo secondario
await figma.modify("3:599", { characters: "Workshop AI Interno" });
await figma.modify("3:600", { characters: "SOSTENIBILITÀ E CONSUMI" }); // was: Titolo secondario
await figma.modify("1:384", { characters: "QUIZ: QUANTO CONSUMA UN PROMPT?" }); // was: Titolo slide
await figma.modify("2:467", { characters: "Workshop AI Interno" });
await figma.modify("2:516", { characters: "02 — Gestione dei File" }); // was: Titolo slide
await figma.modify("2:475", { characters: "Workshop AI Interno" });
await figma.modify("2:517", { characters: "FORMATI FILE" }); // was: Titolo slide
await figma.modify("3:729", { characters: "Workshop AI Interno" });
await figma.modify("3:734", { characters: "QUIZ: COS'È UN FILE .MD?" }); // was: Titolo slide
await figma.modify("3:650", { characters: "Workshop AI Interno" });
await figma.modify("3:680", { characters: "03 — Prompt Optimization" }); // was: Titolo slide
await figma.modify("13:871", { characters: "Workshop AI Interno" });
await figma.modify("13:875", { characters: "DOMANDE E RISPOSTE / GRAZIE!" }); // was: Grazie!
await figma.modify("2:524", { characters: "Cos'è l'AI, chi sono i player, quanto consuma un prompt" }); // was: Framework UX
await figma.modify("6:804", { characters: "AI Generativa vs AI Classica" }); // was: Framework UX
await figma.modify("3:590", { characters: "Spiegazione senza jargon + analogia autocomplete" }); // was: punto 1\\npunto 2
await figma.modify("3:601", { characters: "Tabella: Prompt vs Training vs Scala" }); // was: punto 1\\npunto 2
await figma.modify("1:387", { characters: "A) Fare un caffè | B) 5-10 ricerche Google | C) Volo Milano-Roma" }); // was: Sottotitolo slide
await figma.modify("3:682", { characters: "Migliori pratiche per i formati dei documenti" }); // was: Sottotitolo slide
await figma.modify("3:735", { characters: "✅ .md .txt .csv   ⚠️ .pdf .docx   ❌ PDF scansionati / .xlsx con formule" }); // was: Sottotitolo slide
await figma.modify("3:681", { characters: "Principi per comunicare efficacemente" }); // was: Sottotitolo slide`;

console.log(lines.replace(/await figma.modify\("([^"]+)",\s*\{\s*characters:\s*"([^"]+)"\s*\}\);/g, 'await figma.modify({ id: "$1", characters: "$2" });'));
