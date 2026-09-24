#!/usr/bin/env python3
"""
make_docx.py — Genera il documento Word del workshop dal file Markdown
Crea: SCRIPT_WORKSHOP_AI_S1.docx (Script + Bibliografia)
Poi aprilo su Google Docs via File > Apri > Carica
"""

from docx import Document
from docx.shared import Pt, RGBColor, Inches
import os
import re

OUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SCRIPT_WORKSHOP_AI_S1.docx')
IN_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'SCRIPT_WORKSHOP_AI_S1.md')

BLUE  = RGBColor(0x06, 0x00, 0x6b)
RED   = RGBColor(0xf0, 0x0a, 0x0a)
GREY  = RGBColor(0x55, 0x55, 0x55)
BLACK = RGBColor(0x00, 0x00, 0x00)
ORANGE = RGBColor(0xff, 0x99, 0x00)
SCHERMO_COLOR = RGBColor(0x00, 0x55, 0xaa)

VOICES = {
    'SARA':     RGBColor(0x06, 0x00, 0x6b),   # blu
    'ALBERTO':  RGBColor(0xf0, 0x0a, 0x0a),   # rosso
    'GAIA':     RGBColor(0x00, 0x88, 0x44),   # verde
    'CATERINA': RGBColor(0x88, 0x00, 0x88),   # viola
    'TUTTI':    BLACK,
}

def build_doc():
    doc = Document()

    # Imposta margini
    for section in doc.sections:
        section.top_margin    = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin   = Inches(1.2)
        section.right_margin  = Inches(1.2)

    with open(IN_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            doc.add_paragraph()
            continue
            
        if line.startswith('# '):
            p = doc.add_heading(line[2:], level=1)
            p.runs[0].font.color.rgb = BLUE
            p.runs[0].font.size = Pt(20)
        elif line.startswith('## '):
            p = doc.add_heading(line[3:], level=2)
            p.runs[0].font.color.rgb = BLUE
            p.runs[0].font.size = Pt(15)
        elif line.startswith('### '):
            p = doc.add_heading(line[4:], level=3)
            p.runs[0].font.color.rgb = RED
            p.runs[0].font.size = Pt(12)
        elif line.startswith('---'):
            p = doc.add_paragraph("─" * 70)
            p.runs[0].font.size = Pt(8)
            p.runs[0].font.color.rgb = GREY
        elif line.startswith('> **[schermo]**') or line.startswith('>'):
            text = line.replace('> **[schermo]**', '[schermo]').replace('>', '').strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            r = p.add_run(text)
            r.font.size = Pt(10)
            r.font.color.rgb = SCHERMO_COLOR
        elif line.startswith('*(') and line.endswith(')*'):
            p = doc.add_paragraph()
            r = p.add_run(line)
            r.font.size = Pt(10)
            r.font.italic = True
            r.font.color.rgb = GREY
        elif line.startswith('**[VIDEO') or line.startswith('**[slide'):
            p = doc.add_paragraph()
            r = p.add_run(line)
            r.font.size = Pt(10)
            r.font.italic = True
            r.font.color.rgb = GREY
        elif line.startswith('*[ PLACEHOLDER'):
            p = doc.add_paragraph()
            r = p.add_run(line)
            r.font.size = Pt(10)
            r.font.italic = True
            r.font.color.rgb = ORANGE
        elif line.startswith('**') and ':' in line:
            # Voice line
            speaker_match = re.match(r'\*\*([A-Z]+)\*\*:(.*)', line)
            if speaker_match:
                speaker = speaker_match.group(1)
                text = speaker_match.group(2).strip()
                p = doc.add_paragraph()
                r_name = p.add_run(f"{speaker}: ")
                r_name.font.bold = True
                r_name.font.size = Pt(11)
                r_name.font.color.rgb = VOICES.get(speaker, BLACK)
                
                # strip quotes if present
                if text.startswith('"') and text.endswith('"'):
                    text = text[1:-1]
                    
                r_text = p.add_run(text)
                r_text.font.size = Pt(11)
            else:
                p = doc.add_paragraph(line)
        else:
            p = doc.add_paragraph(line)

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
