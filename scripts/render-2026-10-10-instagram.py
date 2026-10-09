from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

ROOT = Path("assets/instagram/2026-10-10")
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

POSTS = {
 "clarity-clic-senza-risposta": [
  ("CLIC SENZA\nRISPOSTA?", "Microsoft Clarity aiuta a individuare le interazioni che non producono l'effetto atteso.", "UX / ANALISI"),
  ("FILTRA LE\nSESSIONI MOBILE", "In Clarity combina Device: Mobile e Insights: Dead clicks, poi guarda le registrazioni.", "PASSO 01"),
  ("UN CLIC NON\nÈ UNA PROVA", "Un dead click è un indizio: riproduci il comportamento sul telefono prima di parlare di bug.", "PASSO 02"),
  ("TROVA. VERIFICA.\nCORREGGI.", "Dopo l'intervento controlla nuove registrazioni. Non correggere ciò che non hai confermato.", "CHECKLIST"),
 ],
 "utm-link-instagram": [
  ("DA DOVE ARRIVANO\nLE VISITE?", "Bio e Stories: con i parametri UTM distingui i link e confronti il traffico.", "ANALYTICS / TRACKING"),
  ("TRE CAMPI\nDA USARE", "utm_source, utm_medium e utm_campaign: crea una convenzione di nomi e rispettala.", "PASSO 01"),
  ("UTM_CONTENT\nFA LA DIFFERENZA", "Scrivi bio oppure story_01 per distinguere i posizionamenti della stessa campagna.", "PASSO 02"),
  ("COSA MISURI\nDAVVERO?", "Gli UTM aiutano a leggere le visite in Analytics. Non misurano le visualizzazioni del post.", "CHECKLIST"),
 ],
 "shopify-canvas": [
  ("SHOPIFY\nCANVAS", "Un nuovo spazio per osservare più pagine dello store e progettare l'esperienza complessiva.", "SHOPIFY / NOVITÀ"),
  ("PERCHÉ\nÈ INTERESSANTE", "Può aiutare a valutare coerenza delle pagine e modifiche con Sidekick.", "POSSIBILITÀ"),
  ("VERIFICA\nI LIMITI", "Al lancio esistono vincoli per temi, Markets, traduzioni e integrazioni con app.", "ATTENZIONE"),
  ("TESTA SU\nUNA COPIA", "Controlla compatibilità e aggiornamenti del tema prima di qualsiasi intervento.", "CHECKLIST"),
 ],
}

def font(size, bold=False):
 return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def lines_by_width(draw, message, face, width):
 result = []
 for paragraph in message.split("\n"):
  line = ""
  for word in paragraph.split():
   proposed = (line + " " + word).strip()
   if draw.textbbox((0,0), proposed, font=face)[2] <= width:
    line = proposed
   else:
    if line: result.append(line)
    line = word
  result.append(line)
 return result

def render(slug, index, kicker, headline, detail, total):
 w = h = 1080
 dark = "#10191B"
 soft = "#F0EFE6"
 lime = "#CBEE7B"
 foreground = dark if index == 0 else soft
 bg = soft if index == 0 else dark
 accent = dark if index == 0 else lime
 im = Image.new("RGB", (w,h),bg)
 d = ImageDraw.Draw(im)
 d.rounded_rectangle((64,62,152,150), radius=18, fill=dark if index == 0 else lime)
 d.text((85,79),"SC", fill=soft if index == 0 else dark, font=font(39,True))
 d.text((181,91), "SIMONE CIRIELLO  /  DIGITAL NOTES", fill=foreground, font=font(20,True))
 d.line((66,177,1015,177), fill=foreground, width=2)
 d.rounded_rectangle((66,233,66+min(900,len(kicker)*19+62),286), radius=12, fill=accent)
 d.text((88,244),kicker,fill=bg,font=font(22,True))
 fit = font(74,True)
 title_lines = lines_by_width(d,headline,fit,945)
 while any(d.textbbox((0,0),l,font=fit)[2]>930 for l in title_lines):
  fit=font(fit.size-2,True);title_lines=lines_by_width(d,headline,fit,945)
 yy=347
 for ln in title_lines:
  d.text((66,yy), ln, fill=foreground,font=fit,stroke_width=0)
  yy+=fit.size+20
 yy=max(yy+45,630)
 detailfont=font(37)
 for line in lines_by_width(d,detail,detailfont,935):
  d.text((70,yy),line,fill=foreground,font=detailfont)
  yy+=63
 d.line((66,969,1015,969),fill=foreground,width=2)
 d.text((66,991), "@simoneciriello.it",fill=foreground,font=font(22,True))
 d.text((917,991),f"{index+1:02}/{total:02}",fill=foreground,font=font(22,True))
 output=ROOT/slug/f"slide-{index+1:02}.jpg"
 output.parent.mkdir(parents=True,exist_ok=True)
 im.save(output,"JPEG",quality=92,optimize=True,subsampling=0)
 print(output,output.stat().st_size)

if __name__=="__main__":
 for slug, slides in POSTS.items():
  for i,(headline,detail,kicker) in enumerate(slides):
   render(slug,i,kicker,headline,detail,len(slides))
