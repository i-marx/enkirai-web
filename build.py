#!/usr/bin/env python3
"""Builds enkirai.com: landing page in 5 languages, privacy policy, terms and account deletion (EN + LT)."""
import html, json, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
STORE = Path("/home/claude/store")
CONTACT = "hello@enkirai.com"
SUPA = "https://ohzczlfnhryktjsbmxpb.supabase.co"
SUPA_KEY = "sb_publishable_Wvf7fMkTCJuAI71hea7PEQ_25Q3-Xo4"
UPDATED = "2026-11-25"
LANGS = ["en", "lt", "pl", "lv", "et"]
NAMES = {"en": "English", "lt": "Lietuvių", "pl": "Polski", "lv": "Latviešu", "et": "Eesti"}
SHOT = {"en": "En", "lt": "Lt", "pl": "Pl", "lv": "Lv", "et": "Et"}

T = {
 "en": dict(
  title="Enkirai: a second mind in your ear",
  desc="Enkirai listens to your conversation and whispers answers and tips into your earbud, then gives you notes and tasks.",
  eyebrow="Live conversation assistant",
  h1="A second mind<br>in your ear.",
  sub="Enkirai listens to your meeting, call or negotiation and whispers the answer into your earbud in about 1.7 seconds. After it, notes and tasks are ready.",
  cta="Join the waitlist", soon="Coming soon to Google Play", email_ph="Your email", tester="I want to test it early",
  ok="You're on the list. We'll write when it's ready.", err="Something went wrong. Try again.", dup="You're already on the list.",
  f=[("Answers in your ear", "Someone asks a question, a price, a fact. The short answer is in your earbud before the pause gets awkward."),
     ("Tips, not scripts", "When they ask about your price or experience, you get a direction from your own context, in a few words."),
     ("Looks it up for you", "Double tap the earbud and Enkirai searches the web, your contacts or your calendar."),
     ("Notes in 10 seconds", "Summary, decisions, tasks with owners and deadlines. Copy everything with one tap.")],
  how_t="How it works", how=["Put the phone on the table, one earbud in.", "Tap the orb, or press volume up then down.", "Talk. Enkirai helps only when it's worth it."],
  langs_t="5 languages", langs="Lithuanian, English, Polish, Latvian and Estonian, even when they mix in one conversation.",
  priv_t="Private by design", priv="Transcripts stay on your phone. No ads, no selling data. Tell the people you talk to that you take notes with AI.",
  privacy="Privacy policy", terms="Terms", delete="Delete account", by="A product by m.labs"),
 "lt": dict(
  title="Enkirai: antras protas tavo ausyje",
  desc="Enkirai klauso pokalbio ir per ausinę šnabžda atsakymus bei užuominas, o po jo paruošia užrašus ir užduotis.",
  eyebrow="Gyvo pokalbio asistentas",
  h1="Antras protas<br>tavo ausyje.",
  sub="Enkirai klauso susitikimo, skambučio ar derybų ir per ~1,7 sekundės pašnabžda atsakymą į ausinę. Po pokalbio užrašai ir užduotys jau paruošti.",
  cta="Užsirašyti", soon="Netrukus Google Play", email_ph="Tavo el. paštas", tester="Noriu išbandyti pirmas",
  ok="Esi sąraše. Parašysim, kai bus paruošta.", err="Kažkas nepavyko. Pabandyk dar kartą.", dup="Tu jau esi sąraše.",
  f=[("Atsakymai į ausį", "Kas nors paklausia klausimo, kainos ar fakto. Trumpas atsakymas tavo ausyje, kol pauzė dar nespėjo tapti nejauki."),
     ("Užuominos, ne scenarijai", "Kai klausia apie tavo kainą ar patirtį, gauni kryptį iš tavo konteksto, keliais žodžiais."),
     ("Suranda už tave", "Dukart bakstelk ausinę ir Enkirai ieško internete, kontaktuose ar kalendoriuje."),
     ("Užrašai per 10 sekundžių", "Santrauka, sprendimai, užduotys su atsakingais ir terminais. Viską nukopijuoji vienu paspaudimu.")],
  how_t="Kaip tai veikia", how=["Padedi telefoną ant stalo, vieną ausinę į ausį.", "Bakstelėji orbą arba paspaudi garsą aukštyn, tada žemyn.", "Kalbi. Enkirai padeda tik tada, kai verta."],
  langs_t="5 kalbos", langs="Lietuvių, anglų, lenkų, latvių ir estų, net kai jos maišosi viename pokalbyje.",
  priv_t="Privatumas pirmiausia", priv="Transkriptai lieka tavo telefone. Jokių reklamų, jokio duomenų pardavimo. Pasakyk pašnekovams, kad užrašus darai su AI.",
  privacy="Privatumo politika", terms="Sąlygos", delete="Ištrinti paskyrą", by="m.labs produktas"),
 "pl": dict(
  title="Enkirai: drugi umysł w twoim uchu",
  desc="Enkirai słucha rozmowy i szepcze odpowiedzi oraz wskazówki do słuchawki, a potem przygotowuje notatki i zadania.",
  eyebrow="Asystent rozmów na żywo",
  h1="Drugi umysł<br>w twoim uchu.",
  sub="Enkirai słucha spotkania, rozmowy lub negocjacji i w ~1,7 sekundy szepcze odpowiedź do słuchawki. Po rozmowie notatki i zadania są gotowe.",
  cta="Zapisz się", soon="Wkrótce w Google Play", email_ph="Twój e-mail", tester="Chcę testować jako pierwszy",
  ok="Jesteś na liście. Napiszemy, gdy będzie gotowe.", err="Coś poszło nie tak. Spróbuj ponownie.", dup="Jesteś już na liście.",
  f=[("Odpowiedzi w uchu", "Ktoś pyta o fakt, cenę, szczegół. Krótka odpowiedź jest w słuchawce, zanim pauza zrobi się niezręczna."),
     ("Wskazówki, nie scenariusze", "Gdy pytają o twoją cenę lub doświadczenie, dostajesz kierunek z twojego kontekstu, w kilku słowach."),
     ("Wyszukuje za ciebie", "Stuknij dwa razy słuchawkę, a Enkirai przeszuka internet, kontakty lub kalendarz."),
     ("Notatki w 10 sekund", "Podsumowanie, decyzje, zadania z osobami i terminami. Wszystko kopiujesz jednym stuknięciem.")],
  how_t="Jak to działa", how=["Połóż telefon na stole, jedna słuchawka w uchu.", "Stuknij kulę albo naciśnij głośność w górę, potem w dół.", "Rozmawiaj. Enkirai pomaga tylko wtedy, gdy warto."],
  langs_t="5 języków", langs="Litewski, angielski, polski, łotewski i estoński, nawet gdy mieszają się w jednej rozmowie.",
  priv_t="Prywatność od podstaw", priv="Transkrypcje zostają na twoim telefonie. Bez reklam, bez sprzedaży danych. Powiedz rozmówcom, że robisz notatki z AI.",
  privacy="Polityka prywatności", terms="Warunki", delete="Usuń konto", by="Produkt m.labs"),
 "lv": dict(
  title="Enkirai: otrs prāts tavā ausī",
  desc="Enkirai klausās sarunu un čukst atbildes un padomus austiņā, pēc tam sagatavo piezīmes un uzdevumus.",
  eyebrow="Tiešraides sarunu asistents",
  h1="Otrs prāts<br>tavā ausī.",
  sub="Enkirai klausās tikšanos, zvanu vai pārrunas un ~1,7 sekundēs iečukst atbildi austiņā. Pēc sarunas piezīmes un uzdevumi jau gatavi.",
  cta="Pierakstīties", soon="Drīzumā Google Play", email_ph="Tavs e-pasts", tester="Gribu testēt pirmais",
  ok="Tu esi sarakstā. Uzrakstīsim, kad būs gatavs.", err="Kaut kas nogāja greizi. Mēģini vēlreiz.", dup="Tu jau esi sarakstā.",
  f=[("Atbildes ausī", "Kāds pajautā faktu, cenu, detaļu. Īsa atbilde ir austiņā, pirms pauze kļūst neveikla."),
     ("Padomi, nevis scenāriji", "Kad jautā par tavu cenu vai pieredzi, saņem virzienu no sava konteksta, dažos vārdos."),
     ("Atrod tavā vietā", "Divreiz pieskaries austiņai, un Enkirai meklē internetā, kontaktos vai kalendārā."),
     ("Piezīmes 10 sekundēs", "Kopsavilkums, lēmumi, uzdevumi ar atbildīgajiem un termiņiem. Visu nokopē ar vienu pieskārienu.")],
  how_t="Kā tas strādā", how=["Noliec telefonu uz galda, vienu austiņu ausī.", "Pieskaries lodei vai nospied skaļumu uz augšu, tad uz leju.", "Runā. Enkirai palīdz tikai tad, kad ir vērts."],
  langs_t="5 valodas", langs="Lietuviešu, angļu, poļu, latviešu un igauņu, pat ja tās jaucas vienā sarunā.",
  priv_t="Privātums pirmajā vietā", priv="Transkripcijas paliek tavā telefonā. Bez reklāmām, bez datu pārdošanas. Pasaki sarunu biedriem, ka veic piezīmes ar AI.",
  privacy="Privātuma politika", terms="Noteikumi", delete="Dzēst kontu", by="m.labs produkts"),
 "et": dict(
  title="Enkirai: teine mõistus sinu kõrvas",
  desc="Enkirai kuulab vestlust ja sosistab vastuseid ning vihjeid kõrvaklappi, pärast koostab märkmed ja ülesanded.",
  eyebrow="Reaalajas vestlusabiline",
  h1="Teine mõistus<br>sinu kõrvas.",
  sub="Enkirai kuulab kohtumist, kõnet või läbirääkimisi ja sosistab ~1,7 sekundiga vastuse kõrvaklappi. Pärast vestlust on märkmed ja ülesanded valmis.",
  cta="Liitu ootenimekirjaga", soon="Peagi Google Plays", email_ph="Sinu e-post", tester="Tahan esimesena testida",
  ok="Oled nimekirjas. Kirjutame, kui valmis.", err="Midagi läks valesti. Proovi uuesti.", dup="Oled juba nimekirjas.",
  f=[("Vastused kõrva", "Keegi küsib fakti, hinda, detaili. Lühike vastus on kõrvaklapis enne, kui paus muutub piinlikuks."),
     ("Vihjed, mitte skriptid", "Kui küsitakse sinu hinna või kogemuse kohta, saad suuna oma kontekstist, mõne sõnaga."),
     ("Otsib sinu eest", "Puuduta kõrvaklappi kaks korda ja Enkirai otsib internetist, kontaktidest või kalendrist."),
     ("Märkmed 10 sekundiga", "Kokkuvõte, otsused, ülesanded vastutajate ja tähtaegadega. Kopeeri kõik ühe puudutusega.")],
  how_t="Kuidas see töötab", how=["Pane telefon lauale, üks kõrvaklapp kõrva.", "Puuduta kera või vajuta helitugevust üles, siis alla.", "Räägi. Enkirai aitab ainult siis, kui tasub."],
  langs_t="5 keelt", langs="Leedu, inglise, poola, läti ja eesti keel, isegi kui need ühes vestluses segunevad.",
  priv_t="Privaatsus eelkõige", priv="Transkriptsioonid jäävad sinu telefoni. Reklaame pole, andmeid ei müüda. Ütle vestluskaaslastele, et teed märkmeid AI-ga.",
  privacy="Privaatsuspoliitika", terms="Tingimused", delete="Kustuta konto", by="m.labs toode"),
}

CSS = """
:root{--bg:#07080c;--s1:#10121a;--ink:rgba(255,255,255,.95);--mut:rgba(255,255,255,.58);--faint:rgba(255,255,255,.34);--gold:#e8b45a;--line:rgba(255,255,255,.09)}
*{box-sizing:border-box;margin:0;padding:0}
html{background:var(--bg);color:var(--ink);font:16px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}
body{min-height:100vh;background:radial-gradient(900px 600px at 80% -10%,rgba(232,180,90,.16),transparent 60%),radial-gradient(700px 500px at -10% 30%,rgba(90,120,232,.10),transparent 60%),var(--bg)}
a{color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:0 24px}
nav{display:flex;align-items:center;justify-content:space-between;padding:22px 0}
.logo{display:flex;align-items:center;gap:10px;font-weight:600;letter-spacing:.02em;text-decoration:none}
.orb{width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff3d6,#e8b45a 45%,#7a5212 100%);box-shadow:0 0 24px rgba(232,180,90,.55)}
.langs{display:flex;gap:4px;flex-wrap:wrap}
.langs a{font-size:13px;color:var(--mut);text-decoration:none;padding:6px 10px;border-radius:99px;border:1px solid transparent}
.langs a.on,.langs a:hover{color:var(--ink);border-color:var(--line);background:rgba(255,255,255,.04)}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center;padding:56px 0 72px}
.eyebrow{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin-bottom:18px}
h1{font-size:clamp(40px,6.2vw,72px);line-height:1.02;letter-spacing:-.035em;font-weight:650}
.sub{color:var(--mut);font-size:19px;margin:22px 0 30px;max-width:34em}
form{display:flex;flex-direction:column;gap:12px;max-width:460px}
.row{display:flex;gap:8px}
input[type=email]{flex:1;min-width:0;background:rgba(255,255,255,.05);border:1px solid var(--line);color:var(--ink);border-radius:99px;padding:14px 18px;font:inherit;outline:none}
input[type=email]:focus{border-color:rgba(232,180,90,.6)}
button{background:var(--gold);color:#1a1206;border:0;border-radius:99px;padding:14px 22px;font:inherit;font-weight:600;cursor:pointer;white-space:nowrap;transition:transform .15s ease,filter .15s ease}
button:hover{filter:brightness(1.06)}button:active{transform:scale(.97)}
label.chk{display:flex;gap:10px;align-items:center;color:var(--mut);font-size:14px;cursor:pointer}
label.chk input{accent-color:var(--gold);width:16px;height:16px}
.msg{font-size:14px;color:var(--gold);min-height:20px}
.soon{font-size:13px;color:var(--faint);margin-top:6px}
.phone{justify-self:center;width:min(320px,80vw);aspect-ratio:1440/3120;border-radius:44px;padding:10px;background:linear-gradient(160deg,#2a2c35,#0b0c10);box-shadow:0 40px 120px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.08) inset}
.phone img{width:100%;height:100%;object-fit:cover;border-radius:36px;display:block}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding:8px 0 72px}
.card{background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.02));border:1px solid var(--line);border-radius:24px;padding:22px}
.card h3{font-size:17px;font-weight:600;margin-bottom:8px}.card p{color:var(--mut);font-size:15px}
.band{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;padding-bottom:80px}
.band h2{font-size:22px;letter-spacing:-.01em;margin-bottom:10px}
ol{padding-left:20px;color:var(--mut)}ol li{margin:4px 0}
.shots{display:flex;gap:18px;overflow-x:auto;padding:4px 0 80px;scroll-snap-type:x mandatory}
.shots img{height:440px;border-radius:28px;scroll-snap-align:start;border:1px solid var(--line)}
footer{border-top:1px solid var(--line);padding:28px 0 40px;color:var(--faint);font-size:14px;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
footer a{color:var(--mut);text-decoration:none;margin-right:18px}footer a:hover{color:var(--ink)}
.doc{max-width:760px;padding:24px 0 80px}
.doc h1{font-size:40px;margin-bottom:6px}.doc .upd{color:var(--faint);font-size:14px;margin-bottom:32px}
.doc h2{font-size:20px;margin:32px 0 10px}.doc p,.doc li{color:var(--mut);margin:8px 0}.doc ul{padding-left:20px}
.doc strong{color:var(--ink);font-weight:600}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:14px}td,th{border:1px solid var(--line);padding:8px 10px;text-align:left;color:var(--mut);vertical-align:top}th{color:var(--ink);font-weight:600}
@media (max-width:900px){.hero{grid-template-columns:1fr;padding-top:24px}.grid{grid-template-columns:1fr 1fr}.band{grid-template-columns:1fr}}
@media (max-width:560px){.grid{grid-template-columns:1fr}.row{flex-direction:column}.shots img{height:360px}}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

def page(lang, title, desc, body, path, alt=True):
    hreflang = ""
    if alt:
        hreflang = "".join(f'<link rel="alternate" hreflang="{l}" href="https://enkirai.com{"/" if l=="en" else f"/{l}/"}">' for l in LANGS)
    return f"""<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}"><meta name="theme-color" content="#07080c">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://enkirai.com/img/og.png"><meta property="og:url" content="https://enkirai.com{path}">
<link rel="icon" href="/img/icon.png">{hreflang}<link rel="stylesheet" href="/style.css"></head><body>{body}</body></html>"""

def nav(lang, here):
    links = "".join(f'<a class="{"on" if l==lang else ""}" href="{here(l)}">{l.upper()}</a>' for l in LANGS)
    home = "/" if lang == "en" else f"/{lang}/"
    return f'<div class="wrap"><nav><a class="logo" href="{home}"><span class="orb"></span>Enkirai</a><div class="langs">{links}</div></nav></div>'

def foot(lang):
    t = T[lang]; p = "" if lang == "en" else ("/lt" if lang == "lt" else "")
    return f"""<div class="wrap"><footer><div><a href="{p}/privacy/">{t['privacy']}</a><a href="{p}/terms/">{t['terms']}</a><a href="{p}/delete/">{t['delete']}</a><a href="mailto:{CONTACT}">{CONTACT}</a></div><div>© 2026 · {t['by']}</div></footer></div>"""

def landing(lang):
    t = T[lang]
    feats = "".join(f'<div class="card"><h3>{html.escape(a)}</h3><p>{html.escape(b)}</p></div>' for a, b in t["f"])
    how = "".join(f"<li>{html.escape(x)}</li>" for x in t["how"])
    shots = "".join(f'<img loading="lazy" src="/img/{lang}-{i}.webp" alt="">' for i in range(1, 6))
    js = f"""<script>
const f=document.getElementById('w'),m=document.getElementById('m');
f.addEventListener('submit',async e=>{{e.preventDefault();m.textContent='…';
 try{{const r=await fetch('{SUPA}/rest/v1/waitlist',{{method:'POST',headers:{{'apikey':'{SUPA_KEY}','Authorization':'Bearer {SUPA_KEY}','Content-Type':'application/json','Prefer':'return=minimal'}},
 body:JSON.stringify({{email:f.email.value.trim(),lang:'{lang}',wants_test:f.test.checked}})}});
 m.textContent=r.ok?{json.dumps(t['ok'])}:(r.status===409?{json.dumps(t['dup'])}:{json.dumps(t['err'])});if(r.ok)f.reset();}}catch(_){{m.textContent={json.dumps(t['err'])};}}}});
</script>"""
    redirect = ""
    if lang == "en":
        redirect = """<script>try{if(!sessionStorage.getItem('stay')&&!location.search){const l=(navigator.language||'').slice(0,2);if(['lt','pl','lv','et'].includes(l))location.replace('/'+l+'/');}document.querySelectorAll('.langs a').forEach(a=>a.addEventListener('click',()=>sessionStorage.setItem('stay','1')))}catch(_){}</script>"""
    body = nav(lang, lambda l: "/" if l == "en" else f"/{l}/") + f"""
<div class="wrap"><section class="hero"><div>
<div class="eyebrow">{t['eyebrow']}</div><h1>{t['h1']}</h1><p class="sub">{html.escape(t['sub'])}</p>
<form id="w"><div class="row"><input type="email" name="email" required placeholder="{html.escape(t['email_ph'])}" autocomplete="email"><button>{t['cta']}</button></div>
<label class="chk"><input type="checkbox" name="test">{html.escape(t['tester'])}</label><div class="msg" id="m" aria-live="polite"></div>
<div class="soon">{t['soon']}</div></form></div>
<div class="phone"><img src="/img/{lang}-hero.webp" alt="Enkirai"></div></section>
<section class="grid">{feats}</section>
<section class="band"><div class="card"><h2>{t['how_t']}</h2><ol>{how}</ol></div>
<div class="card"><h2>{t['langs_t']}</h2><p>{html.escape(t['langs'])}</p></div>
<div class="card"><h2>{t['priv_t']}</h2><p>{html.escape(t['priv'])}</p></div></section>
<section class="shots">{shots}</section></div>""" + foot(lang) + js + redirect
    return page(lang, t["title"], t["desc"], body, "/" if lang == "en" else f"/{lang}/")

def doc(lang, kind):
    src = (ROOT / "legal" / f"{kind}.{lang}.html").read_text().replace("{CONTACT}", CONTACT).replace("{UPDATED}", UPDATED)
    title = src.split("<h1>")[1].split("</h1>")[0]
    other = "lt" if lang == "en" else "en"
    here = lambda l: (f"/{kind}/" if l == "en" else f"/lt/{kind}/") if l in ("en", "lt") else f"/{l}/"
    body = nav(lang, here) + f'<div class="wrap"><article class="doc">{src}</article></div>' + foot(lang)
    return page(lang, f"{title} · Enkirai", title, body, here(lang), alt=False)

def images():
    img = DIST / "img"; img.mkdir(parents=True, exist_ok=True)
    order = ["m2_answer", "m3_tip", "m4_research", "m5_notes", "m6_history"]
    for l in LANGS:
        for i, n in enumerate(order, 1):
            im = Image.open(STORE / f"ai.enkirai.app_Marketing{SHOT[l]}_{n}.png").convert("RGB")
            im.thumbnail((720, 1560)); im.save(img / f"{l}-{i}.webp", quality=82)
            if i == 1: im.save(img / f"{l}-hero.webp", quality=86)
    og = Image.open(STORE / "out/en/Enkirai-en-feature-graphic.png").convert("RGB"); og.save(img / "og.png")
    Image.open(ROOT / "icon.png").resize((192, 192)).save(img / "icon.png"); return

def main():
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    (DIST / "style.css").write_text(CSS)
    images()
    for l in LANGS:
        d = DIST if l == "en" else DIST / l; d.mkdir(exist_ok=True)
        (d / "index.html").write_text(landing(l))
    for kind in ("privacy", "terms", "delete"):
        for l in ("en", "lt"):
            d = (DIST / kind) if l == "en" else (DIST / "lt" / kind); d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(doc(l, kind))
    (DIST / "CNAME").write_text("enkirai.com\n")
    (DIST / "404.html").write_text(page("en", "Not found · Enkirai", "Not found", nav("en", lambda l: "/" if l=="en" else f"/{l}/") + '<div class="wrap"><article class="doc"><h1>404</h1><p><a href="/">enkirai.com</a></p></article></div>', "/404"))
    (DIST / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://enkirai.com/sitemap.xml\n")
    urls = ["/"] + [f"/{l}/" for l in LANGS[1:]] + [f"/{k}/" for k in ("privacy","terms","delete")] + [f"/lt/{k}/" for k in ("privacy","terms","delete")]
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://enkirai.com{u}</loc></url>" for u in urls) + "</urlset>")
    print("built", sum(1 for _ in DIST.rglob("*") if _.is_file()), "files")

if __name__ == "__main__":
    main()
