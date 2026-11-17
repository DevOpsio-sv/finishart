# -*- coding: utf-8 -*-
"""Write the bilingual FinishArt pages into public/."""
import json
import shutil
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent / "public"
SITE = "https://finishart.bg"
PDF = "/_files/ugd/a86e04_1e8507bd40c34be0ba40b41a3c899912.pdf"
PHONE = "+359882820025"
PHONE_TEXT = "0882 820025"
EMAIL = "office@finishart.bg"
KEEP_DIRS = {"assets", "css", "js", "fonts", "files", "_files"}

HERO = "/assets/painted-interior-tall-windows.jpg"
TEXTURE_NOTE = "/assets/beige-plaster-texture.jpg"
PLASTER = "/assets/worker-filling-drywall-seam.jpg"
APARTMENT = "/assets/white-apartment-living-room-kitchen.jpg"
TROWEL = "/assets/gloved-hand-smoothing-plaster.jpg"
ROOM = "/assets/room-during-renovation-with-ladder.jpg"
REVIEW_OWNER = "/assets/review-vladislav-hadzhiangelov.jpg"
REVIEW_MARKETING = "/assets/review-ginka-milanova.jpg"
REVIEW_BROKER = "/assets/review-trifon-trifonov.jpg"
OG = "/assets/finishart-wordmark-social.jpg"
LOGO = "/assets/finishart-logo.png"
FOLIO_APT = "/assets/empty-apartment-wood-floor-balcony.jpg"
FOLIO_BATH = "/assets/bathroom-glass-shower-and-vanity.jpg"
FOLIO_OTHER = "/assets/stairwell-two-tone-walls.jpg"
BEFORE_AFTER = "/assets/living-room-before-and-after.jpg"
HALL_BEFORE = "/assets/hallway-before-plaster-repair.jpg"
HALL_AFTER = "/assets/hallway-after-paint-and-floor.jpg"
BED_BEFORE = "/assets/bedroom-before-window-reveal.jpg"
BED_AFTER = "/assets/bedroom-after-paint-and-floor.jpg"
SOFIA_AFTER = "/assets/sofia-bathroom-after-renovation.jpg"
SOFIA_BEFORE = "/assets/sofia-bathroom-before-renovation.jpg"
HOUSE_1 = "/assets/house-bathroom-towel-rail.jpg"
HOUSE_2 = "/assets/house-bathroom-before-damaged-shower.jpg"
HOUSE_3 = "/assets/house-bathroom-shower-wood-slat-wall.jpg"
HOUSE_4 = "/assets/house-bathroom-vanity-leaf-wallpaper.jpg"
OFFICE_BEFORE = "/assets/office-before-concrete-shell.jpg"
OFFICE_AFTER = "/assets/office-after-painted-columns.jpg"
OFFICE_BEFORE_2 = "/assets/office-before-plasterboard-walls.jpg"
OFFICE_AFTER_2 = "/assets/office-after-painted-walls.jpg"
STAIRS = "/assets/spiral-stair-wood-handrail.jpg"
STAIRS_BEFORE = "/assets/stair-details-before-renovation.jpg"
STAIRS_AFTER = "/assets/stair-details-after-renovation.jpg"

ROUTES = {
    "home": "",
    "portfolio": "/portfolio",
    "apartments": "/portfolio/apartments",
    "apartment": "/portfolio/apartments/private-home-plaster-and-paint",
    "bathrooms": "/portfolio/bathrooms",
    "bath_sofia": "/portfolio/bathrooms/sofia-bathroom-renovation",
    "bath_house": "/portfolio/bathrooms/house-bathroom-renovation",
    "other": "/portfolio/other-projects",
    "office": "/portfolio/other-projects/office-plaster-and-paint",
    "stairs": "/portfolio/other-projects/staircase-renovation",
    "privacy": "/privacy",
    "cookies": "/cookies",
    "terms": "/terms",
    "legal": "/legal",
    "access": "/accessibility",
}

ICONS = """
<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><circle cx="12" cy="9" r="4" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M8 13.5 7 21l5-2.2L17 21l-1-7.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="m8.5 12.2 2.2 2.2 4.8-5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M12 8v4.2l2.6 1.6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
"""

PHONE_ICON = """<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M8.2 3.6h2.1c.4 0 .7.2.8.6l.9 2.6c.1.4 0 .8-.4 1l-1.3.8a9.6 9.6 0 0 0 4.1 4.1l.8-1.3c.2-.4.6-.5 1-.4l2.6.9c.4.1.6.4.6.8v2.1c0 .7-.5 1.3-1.2 1.4-1.2.2-3.4 0-6.4-3S5.4 7.2 5.6 6c.1-.7.7-1.2 1.4-1.2h1.2z"/></svg>"""

PIN_ICON = """<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 21s-6-5.4-6-10a6 6 0 1 1 12 0c0 4.6-6 10-6 10z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><circle cx="12" cy="11" r="2.1" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>"""

CAL_ICON = """<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="4" y="5.5" width="16" height="14" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M4 10h16M8 3.8v3.2M16 3.8v3.2" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>"""


def esc(value):
    return escape(str(value), quote=True)


def url_for(lang, key):
    return f"/{lang}{ROUTES[key]}"


def other_lang(lang):
    return "en" if lang == "bg" else "bg"


def loc(path):
    if path in ("", "/"):
        return SITE + "/"
    encoded = "/".join(quote(part, safe="") for part in path.strip("/").split("/"))
    return SITE + "/" + encoded


def file_for(lang, key):
    suffix = ROUTES[key].strip("/")
    if suffix:
        return f"{lang}/{suffix}/index.html"
    return f"{lang}/index.html"


UI = {
    "bg": {
        "skip": "Премини към основното съдържание",
        "menu": "МЕНЮ",
        "close_menu": "Затвори меню",
        "nav": "Сайт",
        "home": "Начална",
        "about": "За Нас",
        "services": "Услуги",
        "portfolio": "Портфолио",
        "phone": "Телефон",
        "phone_aria": "Обадете се на +359882820025",
        "phone_menu": "Обади се",
        "lang": "Език",
        "logo": "ФинишАрт, начало",
        "footer_nav": "Правни страници",
        "privacy": "Политика за поверителност",
        "cookies": "Политика за бисквитките",
        "terms": "Общи условия",
        "legal": "Данни за търговеца",
        "access": "Достъпност",
        "cookie_settings": "Настройки за бисквитки",
        "enquiry": "Изпратете запитване",
        "email": "Имейл",
        "message": "Запитване",
        "send": "Изпрати",
        "err_email": "Въведете валиден имейл.",
        "err_message": "Напишете запитването си.",
        "sending": "Изпращане…",
        "ok": "Запитването е изпратено. Ще се свържем с вас.",
        "fail": "В момента формата не може да се изпрати. Обадете се на +359882820025.",
        "privacy_note": "Съобщението се използва, за да отговорим на запитването и да подготвим оферта.",
        "contact": "Контакт",
        "address_label": "Адрес",
        "address": "София, бул. „Янко Сакъзов“ 17",
        "company": "Био Дизайн 2021 ЕООД, ЕИК 206494745",
        "copyright": "© 2026 ФинишАрт",
        "credit": "Сайт от",
        "areas_label": "Райони на обслужване",
        "areas_places": "София · Ловеч · Плевен",
        "footer_slogan": "Ремонти и реставрация с внимание към детайла.",
        "close": "Затвори",
        "cookie_title": "Настройки за бисквитки",
        "cookie_lead": "ФинишАрт използва бисквитка за запазване на избрания език.",
        "cookie_item": "Тя не служи за проследяване или реклама.",
        "cookie_duration": "Запазване на езика: 180 дни.",
        "cookie_forget": "Изтрий езиковото предпочитание",
        "cookie_forgotten": "Предпочитанието е изтрито. Следващото отваряне на началния адрес е на български.",
        "cookie_policy": "Политика за бисквитките",
        "back": "‹ Към портфолиото",
        "prev": "Предишен проект",
        "next": "Следващ проект",
        "projects": "Проекти",
    },
    "en": {
        "skip": "Skip to main content",
        "menu": "MENU",
        "close_menu": "Close menu",
        "nav": "Site",
        "home": "Home",
        "about": "About",
        "services": "Services",
        "portfolio": "Portfolio",
        "phone": "Phone",
        "phone_aria": "Call +359882820025",
        "phone_menu": "Call",
        "lang": "Language",
        "logo": "FinishArt, home",
        "footer_nav": "Legal pages",
        "privacy": "Privacy Policy",
        "cookies": "Cookie Policy",
        "terms": "Terms of Use",
        "legal": "Company Information",
        "access": "Accessibility",
        "cookie_settings": "Cookie settings",
        "enquiry": "Send an enquiry",
        "email": "Email",
        "message": "Enquiry",
        "send": "Send",
        "err_email": "Enter a valid email address.",
        "err_message": "Please write your enquiry.",
        "sending": "Sending…",
        "ok": "Your enquiry has been sent. We will get back to you.",
        "fail": "The form cannot be sent right now. Call +359882820025.",
        "privacy_note": "Your message is used to reply to the enquiry and prepare a quote.",
        "contact": "Contact",
        "address_label": "Address",
        "address": "Sofia, 17 Yanko Sakazov Blvd.",
        "company": "Bio Design 2021 Ltd., Company ID 206494745",
        "copyright": "© 2026 FinishArt",
        "credit": "Website by",
        "areas_label": "Service Areas",
        "areas_places": "Sofia · Lovech · Pleven",
        "footer_slogan": "Renovation and restoration with attention to detail.",
        "close": "Close",
        "cookie_title": "Cookie settings",
        "cookie_lead": "FinishArt uses a cookie to remember the language you choose.",
        "cookie_item": "It is not used for tracking or advertising.",
        "cookie_duration": "Language preference: 180 days.",
        "cookie_forget": "Delete language preference",
        "cookie_forgotten": "The preference has been cleared. The next visit to the home address opens in Bulgarian.",
        "cookie_policy": "Cookie policy",
        "back": "‹ Back to portfolio",
        "prev": "Previous project",
        "next": "Next project",
        "projects": "Projects",
    },
}


def lang_links(lang, key):
    bg = url_for("bg", key)
    en = url_for("en", key)
    bg_current = ' aria-current="true"' if lang == "bg" else ""
    en_current = ' aria-current="true"' if lang == "en" else ""
    return f"""<a href="{bg}" hreflang="bg" lang="bg" data-lang-switch data-lang="bg"{bg_current}>BG</a>
    <span aria-hidden="true">|</span>
    <a href="{en}" hreflang="en" lang="en" data-lang-switch data-lang="en"{en_current}>EN</a>"""


def header(lang, key):
    c = UI[lang]
    return f"""
<header class="site-header">
  <a class="logo" href="{url_for(lang, "home")}" aria-label="{esc(c["logo"])}">
    <img src="{LOGO}" alt="FinishArt" width="180" height="50">
  </a>
  <div class="header-actions">
    <a class="phone-link" href="tel:{PHONE}" aria-label="{esc(c["phone_aria"])}">
      {PHONE_ICON}
      <span class="phone-label">{esc(c["phone"])}</span>
    </a>
    <nav class="lang-switch" aria-label="{esc(c["lang"])}">
      {lang_links(lang, key)}
    </nav>
    <button class="menu-btn" type="button" data-menu aria-expanded="false" aria-controls="site-menu">{esc(c["menu"])}</button>
  </div>
</header>
"""


def menu(lang, key):
    c = UI[lang]
    return f"""
<div class="nav-panel" id="site-menu" data-panel hidden>
  <button class="nav-close" type="button" data-close aria-label="{esc(c["close_menu"])}">×</button>
  <nav aria-label="{esc(c["nav"])}">
    <div class="nav-lang" role="group" aria-label="{esc(c["lang"])}">
      {lang_links(lang, key)}
    </div>
    <ul>
      <li><a href="tel:{PHONE}" aria-label="{esc(c["phone_aria"])}">{esc(c["phone_menu"])}</a></li>
      <li><a href="{url_for(lang, "home")}#home">{esc(c["home"])}</a></li>
      <li><a href="{url_for(lang, "home")}#about">{esc(c["about"])}</a></li>
      <li><a href="{url_for(lang, "home")}#services">{esc(c["services"])}</a></li>
      <li><a href="{url_for(lang, "portfolio")}">{esc(c["portfolio"])}</a></li>
    </ul>
  </nav>
</div>
"""


def footer(lang):
    c = UI[lang]
    phone_icon = """<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M8.4 4.2h1.8c.4 0 .7.2.8.6l.7 2.2c.1.4 0 .8-.3 1l-1 .6a8.2 8.2 0 0 0 3.4 3.4l.6-1c.2-.4.6-.5 1-.3l2.2.7c.4.1.6.4.6.8v1.8c0 .6-.4 1.1-1 1.2-1 .2-2.6.1-5-2.4s-2.6-4-2.4-5c.1-.6.6-1 1.2-1h.4z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>"""
    mail_icon = """<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="1.2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="m4.2 7.2 7.8 5.6 7.8-5.6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>"""
    pin_icon = """<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 20.5s-5.2-4.6-5.2-8.7a5.2 5.2 0 1 1 10.4 0c0 4.1-5.2 8.7-5.2 8.7z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><circle cx="12" cy="11.6" r="1.6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>"""
    area_icon = """<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 20.5s-5.2-4.6-5.2-8.7a5.2 5.2 0 1 1 10.4 0c0 4.1-5.2 8.7-5.2 8.7z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M9.4 12.2 12 10.2l2.6 2v2.2H9.4z" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg>"""
    return f"""
<footer class="site-footer" id="contact">
  <div class="footer-wrap">
    <div class="footer-brand">
      <a class="logo" href="{url_for(lang, "home")}" aria-label="{esc(c["logo"])}">
        <img src="{LOGO}" alt="" width="160" height="44">
      </a>
      <p class="footer-slogan">{esc(c["footer_slogan"])}</p>
    </div>
    <div class="footer-grid">
      <div class="footer-form">
        <h2>{esc(c["enquiry"])}</h2>
        <form data-contact novalidate data-err-email="{esc(c["err_email"])}" data-err-message="{esc(c["err_message"])}" data-sending="{esc(c["sending"])}" data-ok="{esc(c["ok"])}" data-fail="{esc(c["fail"])}">
          <p class="hp" aria-hidden="true">
            <label>Website <input name="website" tabindex="-1" autocomplete="off"></label>
          </p>
          <label class="field">
            <span>{esc(c["email"])} *</span>
            <input name="email" type="email" autocomplete="email" required aria-label="{esc(c["email"])}">
          </label>
          <label class="field">
            <span>{esc(c["message"])} *</span>
            <textarea name="message" required aria-label="{esc(c["message"])}"></textarea>
          </label>
          <button class="btn" type="submit">{esc(c["send"])}</button>
          <p class="form-privacy">{esc(c["privacy_note"])} <a href="{url_for(lang, "privacy")}">{esc(c["privacy"])}</a></p>
          <p class="form-status" data-status role="status"></p>
        </form>
      </div>
      <div class="footer-split" aria-hidden="true"></div>
      <div class="contact-details">
        <h2>{esc(c["contact"])}</h2>
        <dl class="contact-list">
          <div>
            <span class="contact-icon" aria-hidden="true">{phone_icon}</span>
            <dt>{esc(c["phone"])}</dt>
            <dd><a href="tel:{PHONE}">{PHONE_TEXT}</a></dd>
          </div>
          <div>
            <span class="contact-icon" aria-hidden="true">{mail_icon}</span>
            <dt>{esc(c["email"])}</dt>
            <dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
          </div>
          <div>
            <span class="contact-icon" aria-hidden="true">{pin_icon}</span>
            <dt>{esc(c["address_label"])}</dt>
            <dd>{esc(c["address"])}</dd>
          </div>
          <div>
            <span class="contact-icon" aria-hidden="true">{area_icon}</span>
            <dt>{esc(c["areas_label"])}</dt>
            <dd>{esc(c["areas_places"])}</dd>
          </div>
        </dl>
      </div>
    </div>
    <div class="footer-meta">
      <nav aria-label="{esc(c["footer_nav"])}">
        <a href="{url_for(lang, "privacy")}">{esc(c["privacy"])}</a>
        <a href="{url_for(lang, "cookies")}">{esc(c["cookies"])}</a>
        <a href="{url_for(lang, "terms")}">{esc(c["terms"])}</a>
        <a href="{url_for(lang, "legal")}">{esc(c["legal"])}</a>
        <a href="{url_for(lang, "access")}">{esc(c["access"])}</a>
      </nav>
      <div class="footer-actions">
        <button class="footer-link" type="button" data-cookie-open>{esc(c["cookie_settings"])}</button>
        <a class="fb" href="https://www.facebook.com/profile.php?id=61577536868457" aria-label="Facebook">
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M14.5 8.5V6.8c0-.7.5-1 1.2-1H17V3h-2.2C12.4 3 11 4.5 11 6.9v1.6H9v2.7h2V21h3v-9.8h2.4l.6-2.7h-3z"/></svg>
        </a>
      </div>
    </div>
    <p class="copy">
      <span>{esc(c["copyright"])}</span>
      <span class="copy-dot" aria-hidden="true">·</span>
      <span>{esc(c["company"])}</span>
      <span class="copy-dot" aria-hidden="true">·</span>
      <span>{esc(c["credit"])} <a href="https://devopsio.co" target="_blank" rel="noopener">DevOpsio</a></span>
    </p>
  </div>
</footer>
<dialog class="cookie-settings" data-cookie-dialog>
  <h2>{esc(c["cookie_title"])}</h2>
  <p>{esc(c["cookie_lead"])}</p>
  <p>{esc(c["cookie_item"])}</p>
  <p>{esc(c["cookie_duration"])}</p>
  <p data-cookie-note hidden>{esc(c["cookie_forgotten"])}</p>
  <div class="cookie-actions">
    <a class="btn" href="?forget-lang=1">{esc(c["cookie_forget"])}</a>
    <a class="btn" href="{url_for(lang, "cookies")}">{esc(c["cookie_policy"])}</a>
    <form method="dialog"><button class="btn" type="submit">{esc(c["close"])}</button></form>
  </div>
</dialog>
<dialog class="lightbox">
  <form method="dialog"><button type="submit">{esc(c["close"])}</button></form>
  <img alt="">
</dialog>
"""


def layout(lang, key, title, description, body, home=False, verify=False, noindex=False, alternates=True):
    c = UI[lang]
    path = url_for(lang, key) if key else "/404.html"
    canonical = loc(path)
    klass = "home" if home else "inner"
    locale = "bg_BG" if lang == "bg" else "en_US"
    alt_locale = "en_US" if lang == "bg" else "bg_BG"
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    canonical_tag = "" if noindex else f'\n  <link rel="canonical" href="{canonical}">'
    alternate = ""
    if alternates and key:
        bg = loc(url_for("bg", key))
        en = loc(url_for("en", key))
        alternate = f"""
  <link rel="alternate" hreflang="bg" href="{bg}">
  <link rel="alternate" hreflang="en" href="{en}">
  <link rel="alternate" hreflang="x-default" href="{bg}">"""
    verify_meta = ""
    if verify:
        verify_meta = """
  <meta name="google-site-verification" content="ou8d_j-1cycgAh7CnWuF3WQm-mbM-jUDU7NVq-bElx4">
  <meta name="msvalidate.01" content="82C6436E0F3D5F09BDD7B1C13E81EC5F">"""
    og_url = "" if noindex else f'\n  <meta property="og:url" content="{canonical}">'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">{canonical_tag}{alternate}{robots}
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">{og_url}
  <meta property="og:image" content="{SITE}{OG}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="FinishArt">
  <meta property="og:locale" content="{locale}">
  <meta property="og:locale:alternate" content="{alt_locale}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{SITE}{OG}">
  <meta name="theme-color" content="#823c2e">
  <link rel="icon" href="{LOGO}" type="image/png">{verify_meta}
  <link rel="stylesheet" href="/css/styles.css?v=20261117e">
</head>
<body class="{klass}">
  <a class="skip" href="#main">{esc(c["skip"])}</a>
  {header(lang, key or "home")}
  {menu(lang, key or "home")}
  <main id="main">
{body}
  </main>
  {footer(lang)}
  <script src="/js/site.js?v=20261116d"></script>
</body>
</html>
"""


def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(rel)


def emit(lang, key, title, description, body, **opts):
    write(file_for(lang, key), layout(lang, key, title, description, body, **opts))


def img(src, alt, width=None, height=None, lazy=True, priority=False, zoom=False):
    attrs = [f'src="{src}"', f'alt="{esc(alt)}"']
    if width:
        attrs.append(f'width="{width}"')
        attrs.append(f'height="{height}"')
    if priority:
        attrs.append('fetchpriority="high"')
    elif lazy:
        attrs.append('loading="lazy"')
    if zoom:
        attrs.append("data-zoom")
    return "<img " + " ".join(attrs) + ">"


def home(lang):
    ribbon, check, clock = [line for line in ICONS.strip().split("\n") if line.strip()]
    if lang == "bg":
        title = "Начална | ФинишАрт — шпакловка и боя"
        desc = "Професионална шпакловка, боядисване и довършителни ремонти от ФинишАрт. Надеждно изпълнение, коректност и перфектен завършек."
        hero_title = "Качествено<br>боядисване и<br>шпакловка"
        lead1 = "Вашият доверен партньор за частни домове и мащабни проекти."
        lead2 = "Предлагаме прецизност в детайла, стриктни срокове, безупречна чистота, както до 24 месеца гаранция за изпълнението."
        offer = "Вземете безплатна оферта"
        note = "* Цени от 8–22 евро/кв.м според състоянието на стените и вида на услугата."
        hero_alt = "Боядисан интериор с високи сиви рамки на прозорци и светъл дървен под"
        hero_areas = "София · Ловеч · Плевен и областите"
        areas_kicker = "РАЙОНИ НА ОБСЛУЖВАНЕ"
        areas_title = "Работим близо до Вас."
        areas_lead = "Предлагаме професионални ремонти и довършителни дейности в София, Ловеч, Плевен и околните населени места."
        areas_cta = "Поискайте оферта →"
        areas_places = [
            ("София", "и Софийска област"),
            ("Ловеч", "и област Ловеч"),
            ("Плевен", "и област Плевен"),
        ]
        areas_note = "Обслужваме и населени места по предварителна уговорка."
        why = "Защо ние?"
        cards = [
            ("1", "Точност:<br>Планираме алгоритмично, изпълняваме в срок", [
                "Времето е най-ценният ресурс и затова го ценим, колкото вас.",
                "Не просто гоним крайни дати, а планираме всеки етап от обекта алгоритмично.",
                "Това ни позволява да гарантираме 100% спазване на сроковете, без значение дали работим с частни обекти или като подизпълнител в мащабен проект.",
            ]),
            ("2", "Чистота и Защита:<br>Вашият комфорт е наш приоритет", [
                "Ремонтът не трябва да спира живота ви.",
                "Процесите ни са оптимизирани така, че да работим безпроблемно, дори в обитаеми помещения.",
                "Обучени сме да балансираме между максимална бързина и абсолютна чистота.",
            ]),
            ("3", "Експертиза и Технология: Основани през 2018, водени от иновациите", [
                "Съчетаваме натрупания опит с най-съвременните стандарти в довършителните работи.",
                "Използваме съвременни технологии и методи за нанасяне, които гарантират перфектно гладки повърхности.",
                "Следим отблизо еволюцията на материалите и технологиите, за да предложим на нашите клиенти най-доброто от пазара днес.",
            ]),
        ]
        commit_title = "Нашият ангажимент"
        commit = [
            "Във Финиш Арт сме специализирани в услуги по боядисване и шпакловане, които превръщат вашата идея в реалност.",
            "Нашето внимание към детайла и качественото майсторство гарантират, че всеки проект отговаря на вашите изисквания, като същевременно подобрява и облагородява вашето пространство.",
        ]
        commit_alt = "Работник запълва фуга на стена с шпакла"
        portfolio_btn = "Разгледай портфолио"
        services_title = "Нашите услуги"
        sub = "Освежителен или основен ремонт с внимание към детайла"
        price = "Цени от 8 €/кв.м."
        prices = "Виж актуални цени"
        perks = ["Качествени материали", "Прецизна работа", "Коректни срокове"]
        service_alts = [
            "Бял апартамент с дневна, балконска врата и кухня",
            "Ръка с ръкавица заглажда мазилка по стена",
            "Стая по време на ремонт със стълба и бояджийски материали",
        ]
        service_names = ["Интериорно боядисване", "Шпакловка", "Основен ремонт"]
        reviews_title = "Какво казват клиентите?"
        prev = "Предишна"
        nxt = "Напред"
        slides_label = "Слайдове"
        dots = ["Собственик", "Маркетинг", "Брокер"]
        quotes = [
            ("Много съм доволен от работата, която свършиха в заведението, както и от отношението. Поздравления за бързата и качествена работа.", "Владислав Хаджиангелов, собственик, „БГ Бар“", "Владислав Хаджиангелов в бар, с вдигнати ръце"),
            ("Финиш Арт направиха, каквото обещаха, въпреки че бях скептична, защото имах негативен опит с други фирми. Благодаря!", "Гинка Миланова, Бранд мениджър", "Портрет на Гинка Миланова"),
            ("Момчетата са отговорни и коректни, работят на достъпни цени и ги препоръчвам, както на клиенти, така и на мои близки.", "Трифон Трифонов - Тиката, Брокер", "Трифон Трифонов на улица пред къщи"),
        ]
        business = "ФинишАрт"
        street = "бул. Янко Сакъзов 17"
        city = "София"
    else:
        title = "Home | FinishArt — plastering and painting"
        desc = "Professional plastering, painting and finishing by FinishArt. Reliable delivery, fair dealing and a precise finish."
        hero_title = "Quality<br>painting and<br>plastering"
        lead1 = "A reliable partner for private homes and large projects."
        lead2 = "We work precisely, keep to the schedule, leave the place clean, and provide up to 24 months’ warranty on the work."
        offer = "Request a free quote"
        note = "* Prices from €8–22 per m², depending on the condition of the walls and the type of work."
        hero_alt = "Painted interior with tall grey window frames and a light wood floor"
        hero_areas = "Sofia · Lovech · Pleven and surrounding regions"
        areas_kicker = "SERVICE AREAS"
        areas_title = "Working Near You."
        areas_lead = "We offer professional repairs and finishing work in Sofia, Lovech, Pleven, and the surrounding settlements."
        areas_cta = "Request a quote →"
        areas_places = [
            ("Sofia", "and Sofia Province"),
            ("Lovech", "and Lovech Province"),
            ("Pleven", "and Pleven Province"),
        ]
        areas_note = "We also serve other settlements by prior arrangement."
        why = "Why us?"
        cards = [
            ("1", "Accuracy:<br>We plan the work in stages and deliver on time", [
                "Time is the most valuable resource, so we treat yours with the same care as our own.",
                "We do not simply chase a final date. We plan every stage of the job.",
                "That is how we commit to meeting the agreed schedule, whether the work is a private home or our part of a larger project.",
            ]),
            ("2", "Cleanliness and protection:<br>Your comfort comes first", [
                "A renovation should not put your life on hold.",
                "Our process is set up so we can work in homes that are still occupied.",
                "We are trained to balance speed with leaving the space clean.",
            ]),
            ("3", "Experience and method: working since 2018, guided by current practice", [
                "We combine experience on site with current standards for finishing work.",
                "We use present-day materials and application methods aimed at smooth, even surfaces.",
                "We follow how materials and methods change, so clients get a finish that matches current practice.",
            ]),
        ]
        commit_title = "Our commitment"
        commit = [
            "At FinishArt we specialise in painting and plastering that turn a brief into a finished space.",
            "Attention to detail and sound workmanship mean each project follows your requirements and improves the room it is in.",
        ]
        commit_alt = "A worker filling a drywall seam with a putty knife"
        portfolio_btn = "View the portfolio"
        services_title = "Our services"
        sub = "A refresh or a full renovation, with attention to detail"
        price = "Prices from €8/m²."
        prices = "See current prices"
        perks = ["Quality materials", "Precise work", "Reliable schedules"]
        service_alts = [
            "White apartment with a living room, balcony door and kitchen",
            "A gloved hand smoothing plaster on a wall",
            "A room during renovation, with a ladder and painting supplies",
        ]
        service_names = ["Interior painting", "Plastering", "Full renovation"]
        reviews_title = "What clients say"
        prev = "Previous"
        nxt = "Next"
        slides_label = "Slides"
        dots = ["Owner", "Marketing", "Broker"]
        quotes = [
            ("I am very pleased with the work they did in the venue, and with the way they treated us. Congratulations on a fast, high-quality job.", "Vladislav Hadzhiangelov, owner, BG Bar", "Vladislav Hadzhiangelov in a bar, arms raised"),
            ("FinishArt did what they promised, even though I was sceptical after poor experiences with other companies. Thank you.", "Ginka Milanova, brand manager", "Portrait of Ginka Milanova"),
            ("The team is responsible and fair, the prices are reasonable, and I recommend them both to clients and to people close to me.", "Trifon Trifonov – Tikata, broker", "Trifon Trifonov on a street in front of houses"),
        ]
        business = "FinishArt"
        street = "17 Yanko Sakazov Blvd."
        city = "Sofia"
    why_html = "\n".join(
        "<article class=\"why-card\">"
        f"<p class=\"why-num\">{num}</p><h3>{heading}</h3>"
        + "".join(f"<p>{esc(part)}</p>" for part in parts)
        + "</article>"
        for num, heading, parts in cards
    )
    services = [
        (APARTMENT, service_alts[0], service_names[0]),
        (TROWEL, service_alts[1], service_names[1]),
        (ROOM, service_alts[2], service_names[2]),
    ]
    service_html = "\n".join(
        f"""        <figure class="service-card">
          {img(src, alt, 276, 325)}
          <figcaption>{esc(name)}</figcaption>
        </figure>"""
        for src, alt, name in services
    )
    review_src = [REVIEW_OWNER, REVIEW_MARKETING, REVIEW_BROKER]
    review_size = [(1536, 1024), (950, 2000), (1024, 1536)]
    review_html = "\n".join(
        f"""          <article class="review{' is-active' if i == 0 else ''}" data-slide>
            {img(review_src[i], quotes[i][2], review_size[i][0], review_size[i][1])}
            <div class="review-copy">
              <p>„{esc(quotes[i][0])}“</p>
              <p class="who">{esc(quotes[i][1])}</p>
            </div>
          </article>"""
        for i in range(3)
    )
    dot_html = "\n".join(
        f"""        <button type="button" data-dot role="tab" aria-label="{esc(label)}" aria-selected="{'true' if i == 0 else 'false'}"></button>"""
        for i, label in enumerate(dots)
    )
    area_html = "\n".join(
        "        <li>"
        f"{PIN_ICON}<span class=\"area-city\">{esc(city)}</span>"
        f"<span class=\"area-region\">{esc(region)}</span></li>"
        for city, region in areas_places
    )
    map_svg = (ROOT / "assets" / "bulgaria-map.svg").read_text(encoding="utf-8")
    map_svg = map_svg.split("<svg ", 1)[1]
    map_svg = "<svg aria-hidden=\"true\" focusable=\"false\" " + map_svg
    schema = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": business,
        "url": loc(url_for(lang, "home")),
        "image": SITE + OG,
        "telephone": PHONE,
        "email": EMAIL,
        "foundingDate": "2018",
        "inLanguage": lang,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": street,
            "addressLocality": city,
            "postalCode": "1504",
            "addressCountry": "BG",
        },
    }
    schema_html = json.dumps(schema, ensure_ascii=False, indent=2)
    body = f"""
    <section class="hero" id="home">
      <span class="anchor" id="nachalna"></span>
      <div class="hero-copy">
        <h1>{hero_title}</h1>
        <p class="hero-lead">{esc(lead1)}</p>
        <p class="hero-lead">{esc(lead2)}</p>
        <p class="hero-areas">{PIN_ICON}<span>{esc(hero_areas)}</span></p>
        <a class="btn" href="tel:{PHONE}">{esc(offer)}</a>
        <p class="hero-note">{esc(note)}</p>
      </div>
      <div class="hero-media">
        {img(HERO, hero_alt, 1328, 2048, lazy=False, priority=True)}
      </div>
    </section>
    <section id="about" aria-labelledby="why-title">
      <span class="anchor" id="za-nas"></span>
      <h2 class="why-title" id="why-title">{esc(why)}</h2>
      <div class="why">
        <div class="why-grid">
          {why_html}
        </div>
      </div>
    </section>
    <section class="commit" aria-labelledby="commit-title">
      <div class="commit-copy">
        <h2 id="commit-title">{esc(commit_title)}</h2>
        <p>{esc(commit[0])}</p>
        <p>{esc(commit[1])}</p>
        <a class="btn" href="{url_for(lang, "portfolio")}">{esc(portfolio_btn)}</a>
      </div>
      <div class="commit-media">
        {img(PLASTER, commit_alt, 2400, 1309)}
      </div>
    </section>
    <section class="services" id="services" aria-labelledby="services-title">
      <span class="anchor" id="uslugi"></span>
      <h2 id="services-title">{esc(services_title)}</h2>
      <p class="sub">{esc(sub)}</p>
      <p class="price-line">{esc(price)}</p>
      <a class="btn" href="{PDF}">{esc(prices)}</a>
      <ul class="perks">
        <li>{ribbon} {esc(perks[0])}</li>
        <li>{check} {esc(perks[1])}</li>
        <li>{clock} {esc(perks[2])}</li>
      </ul>
      <div class="service-panel">
{service_html}
      </div>
    </section>
    <section class="areas" id="areas" aria-labelledby="areas-title">
      <div class="areas-map" aria-hidden="true">
        __BULGARIA_MAP__
      </div>
      <div class="areas-layout">
        <div class="areas-copy">
          <p class="areas-kicker">{esc(areas_kicker)}</p>
          <h2 id="areas-title">{esc(areas_title)}</h2>
          <p class="areas-lead">{esc(areas_lead)}</p>
          <a class="btn areas-cta" href="#contact">{esc(areas_cta)}</a>
        </div>
        <div class="areas-split" aria-hidden="true"></div>
        <div class="areas-places">
          <ul class="area-list">
{area_html}
          </ul>
          <p class="areas-note">{CAL_ICON}<span>{esc(areas_note)}</span></p>
        </div>
      </div>
    </section>
    <section class="reviews" aria-labelledby="reviews-title">
      <h2 id="reviews-title">{esc(reviews_title)}</h2>
      <div class="review-stage">
        <button class="arrow" type="button" data-dir="-1" aria-label="{esc(prev)}">←</button>
        <div>
{review_html}
        </div>
        <button class="arrow" type="button" data-dir="1" aria-label="{esc(nxt)}">→</button>
      </div>
      <div class="dots" role="tablist" aria-label="{esc(slides_label)}">
{dot_html}
      </div>
    </section>
    <script type="application/ld+json">
{schema_html}
    </script>
"""
    emit(lang, "home", title, desc, body.replace("__BULGARIA_MAP__", map_svg), home=True, verify=(lang == "bg"))


def portfolio(lang):
    if lang == "bg":
        title = "Портфолио | ФинишАрт"
        desc = "Портфолио на ФинишАрт: апартаменти, бани и други жилищни и бизнес проекти."
        cards = [
            ("apartments", FOLIO_APT, "Празен апартамент с дървен под и врата към балкон", "Апартаменти - от къртене до ключ", 2400, 1309),
            ("bathrooms", FOLIO_BATH, "Баня със стъклена душ кабина и бял шкаф с мивка", "Баня и тоалетна - прецизност до посления детайл", 1536, 1024),
            ("other", FOLIO_OTHER, "Стълбище с двуцветни стени и метален парапет", "Други обекти - жилищни и бизнес проекти", 1536, 1024),
        ]
    else:
        title = "Portfolio | FinishArt"
        desc = "FinishArt portfolio: apartments, bathrooms and other residential and business projects."
        cards = [
            ("apartments", FOLIO_APT, "Empty apartment with a wood floor and a balcony door", "Apartments — from strip-out to handover", 2400, 1309),
            ("bathrooms", FOLIO_BATH, "Bathroom with a glass shower and a white vanity", "Bathrooms — precision down to the last detail", 1536, 1024),
            ("other", FOLIO_OTHER, "Stairwell with two-tone walls and a metal handrail", "Other projects — homes and business spaces", 1536, 1024),
        ]
    links = "\n".join(
        f"""      <a href="{url_for(lang, key)}">
        {img(src, alt, width, height)}
        <span>{esc(label)}</span>
      </a>"""
        for key, src, alt, label, width, height in cards
    )
    body = f"""
    <div class="folio">
{links}
    </div>
"""
    emit(lang, "portfolio", title, desc, body)


def collection(lang, key, back_key, title, description, intro, cards):
    c = UI[lang]
    thumbs = "\n".join(
        f"""      <a href="{url_for(lang, href)}">
        {img(src, alt)}
      </a>"""
        for href, src, alt in cards
    )
    list_html = f'\n    <div class="project-list">\n{thumbs}\n    </div>' if cards else ""
    intro_html = f"\n      <p>{esc(intro)}</p>" if intro else ""
    body = f"""
    <p class="back"><a href="{url_for(lang, back_key)}">{esc(c["back"])}</a></p>
    <header class="page-intro">
      <h1>{esc(title)}</h1>{intro_html}
    </header>{list_html}
"""
    emit(lang, key, title, description or title, body)


def project(lang, key, back_key, title, page_title, description, facts, story, images, prev_key=None, next_key=None):
    c = UI[lang]
    facts_html = "\n".join(
        f"""        <div class="meta"><h2>{esc(label)}</h2><p>{esc(value)}</p></div>""" for label, value in facts
    )
    story_html = f'<p class="project-story">{esc(story)}</p>' if story else ""
    figs = "\n".join(
        f"""      <figure>
        {img(src, alt, zoom=True)}
        <figcaption>{esc(alt)}</figcaption>
      </figure>"""
        for src, alt in images
    )
    left = f'<a href="{url_for(lang, prev_key)}">{esc(c["prev"])}</a>' if prev_key else "<span></span>"
    right = f'<a href="{url_for(lang, next_key)}">{esc(c["next"])}</a>' if next_key else "<span></span>"
    pager = ""
    if prev_key or next_key:
        pager = f'\n    <nav class="pager" aria-label="{esc(c["projects"])}">{left}{right}</nav>'
    body = f"""
    <p class="back"><a href="{url_for(lang, back_key)}">{esc(c["back"])}</a></p>
    <article class="project">
      <div>
        <h1>{esc(title)}</h1>
{facts_html}
      </div>
      <div>{story_html}</div>
    </article>
    <div class="gallery">
{figs}
    </div>{pager}
"""
    emit(lang, key, page_title, description, body)


def projects(lang):
    if lang == "bg":
        collection(
            lang, "apartments", "portfolio",
            "Апартаменти - от къртене до ключ",
            "Изпълняваме цялостни основни ремонти на апартаменти и къщи.",
            "Изпълняваме цялостни основни ремонти на апартаменти и къщи.",
            [("apartment", BEFORE_AFTER, "Дневна преди и след ремонта")],
        )
        collection(
            lang, "bathrooms", "portfolio",
            "Баня и тоалетна - прецизност до посления детайл",
            "Баня и тоалетна - прецизност до посления детайл",
            "",
            [
                ("bath_sofia", SOFIA_AFTER, "Баня след ремонта, със светъл плочник и кръгло огледало"),
                ("bath_house", HOUSE_1, "Бели хавлии на хромиран държач в душ"),
            ],
        )
        collection(
            lang, "other", "portfolio",
            "Други обекти - жилищни и бизнес проекти",
            "Разгледайте част от нашите реализирани проекти в областта на шпакловката и боядисването.",
            "Разгледайте част от нашите реализирани проекти в областта на шпакловката и боядисването. Всеки обект е изпълнен с прецизност, качествени материали и внимание към всеки детайл. Нашето портфолио отразява стремежа ни към отличен резултат, дълготрайност и красиво завършени пространства.",
            [
                ("office", OFFICE_BEFORE, "Недовършен бетонен офис преди шпакловка"),
                ("stairs", STAIRS, "Винтова стълба с дървен парапет"),
            ],
        )
        project(
            lang, "apartment", "apartments",
            "Реновация на частно жилище",
            "Реновация на частно жилище | ФинишАрт",
            "Шпакловка, боядисване и основен ремонт на частно жилище в София, март 2026.",
            [
                ("Дата:", "Март 2026"),
                ("Локация:", "гр.София"),
                ("Извършени услуги:", "Шпакловка, боядисване, обръщане на врати и прозорци, подмяна на ВиК и ел. инсталации, поставяне на настилки."),
            ],
            "Финиш Арт с гордост представя своя последен проект - прецизен ремонт на частен дом, демонстриращ експертни решения в шпакловката и боядисването, които подобряват както естетиката, така и дълготрайността. Този проект е пример за нашия ангажимент към качествената изработка и индивидуалния подход, като преобразява жилищните пространства с прецизност и внимание.",
            [
                (HALL_BEFORE, "Антре преди ремонта, с открита мазилка"),
                (HALL_AFTER, "Антре след боя и дървена настилка"),
                (BED_BEFORE, "Спалня преди обръщане на прозореца"),
                (BED_AFTER, "Спалня след боя и дървена настилка"),
            ],
        )
        project(
            lang, "bath_sofia", "bathrooms",
            "Реновация на баня - София",
            "Реновация на баня - София | ФинишАрт",
            "Къртене, шпакловка, фаянс и санитария. София, ноември 2025.",
            [
                ("Локация:", "гр. София"),
                ("Дата:", "Ноември 2025"),
                ("Извършени услуги:", "Къртене и демонтаж, шпакловка, поставяне на фаянс и санитария."),
            ],
            "",
            [
                (SOFIA_AFTER, "Баня след ремонта, със светъл плочник и кръгло огледало"),
                (SOFIA_BEFORE, "Баня преди ремонта, със стар фаянс и мивка на колона"),
            ],
            next_key="bath_house",
        )
        project(
            lang, "bath_house", "bathrooms",
            "Реновация на баня в селска къща",
            "Реновация на баня в селска къща | ФинишАрт",
            "Основен ремонт на баня в с.Ъглен, декември 2025.",
            [
                ("Дата:", "Декември 2025"),
                ("Локация:", "с.Ъглен"),
                ("Извършени услуги:", "Основен ремонт на баня."),
            ],
            "Финиш Арт представя демонстрира професионални решения за шпакловка и боядисване, преобразили една разрушена постройка в модерно и свежо пространство. Тази реновация подчертава нашата отдаденост към качествената изработка и индивидуалния подход, вдъхвайки нов живот и стил на традиционните домове.",
            [
                (HOUSE_1, "Бели хавлии на хромиран държач в душ"),
                (HOUSE_2, "Баня преди ремонта, с увредена душ зона"),
                (HOUSE_3, "Душ със стъклена преграда и дървени ламели"),
                (HOUSE_4, "Мивка и стена с тапет на листа"),
            ],
            prev_key="bath_sofia",
        )
        project(
            lang, "office", "other",
            "Шпакловка и боядисване на офис пространства",
            "Шпакловка и боядисване на офис пространства | ФинишАрт",
            "Шпакловане и боядисване, полагане на настилки. София, май 2025.",
            [
                ("Локация:", "гр. София"),
                ("Дата:", "Май 2025"),
                ("Извършени услуги:", "Шпакловане и боядисване, полагане на настилки"),
            ],
            "",
            [
                (OFFICE_BEFORE, "Офис преди ремонта, с видим бетон"),
                (OFFICE_AFTER, "Офис след боядисване на колоните и пода"),
                (OFFICE_BEFORE_2, "Офис преди ремонта, с гипскартон по стените"),
                (OFFICE_AFTER_2, "Офис след боядисване на стените и тавана"),
            ],
            next_key="stairs",
        )
        project(
            lang, "stairs", "other",
            "Реновация на стълбище",
            "Реновация на стълбище | ФинишАрт",
            "Шпакловка, боядисване и реставрация на стъпала. София, януари 2026.",
            [
                ("Дата:", "Януари 2026"),
                ("Локация:", "гр.София"),
                ("Извършени услуги:", "Шпакловка, боядисване, реставрация на стъпала."),
            ],
            "Финиш Арт с гордост представя проект, който демонстрира професионални решения за шпакловка и боядисване, преобразяващи стълбищни пространства с прецизност и качествена изработка. Тази реновация е пример за нашия ангажимент към отличното изпълнение, като подобрява както естетиката, така и издръжливостта на жилищни и търговски пространства.",
            [
                (STAIRS, "Винтова стълба с дървен парапет и бели балюстри"),
                (STAIRS_BEFORE, "Детайли от стълба преди ремонта"),
                (STAIRS_AFTER, "Детайли от стълба след боя и нови стъпала"),
            ],
            prev_key="office",
        )
    else:
        collection(
            lang, "apartments", "portfolio",
            "Apartments — from strip-out to handover",
            "We carry out full renovations of apartments and houses.",
            "We carry out full renovations of apartments and houses.",
            [("apartment", BEFORE_AFTER, "Living room before and after the renovation")],
        )
        collection(
            lang, "bathrooms", "portfolio",
            "Bathrooms — precision down to the last detail",
            "Bathrooms — precision down to the last detail.",
            "",
            [
                ("bath_sofia", SOFIA_AFTER, "Bathroom after renovation, with light tiles and a round mirror"),
                ("bath_house", HOUSE_1, "White towels on a chrome rail in a shower"),
            ],
        )
        collection(
            lang, "other", "portfolio",
            "Other projects — homes and business spaces",
            "A selection of completed plastering and painting projects.",
            "A selection of completed plastering and painting projects. Each one was carried out with care, sound materials and attention to detail. The portfolio shows the standard we aim for: a durable finish and a well-resolved space.",
            [
                ("office", OFFICE_BEFORE, "Unfinished concrete office before plastering"),
                ("stairs", STAIRS, "Spiral staircase with a wooden handrail"),
            ],
        )
        project(
            lang, "apartment", "apartments",
            "Renovation of a private home",
            "Renovation of a private home | FinishArt",
            "Plastering, painting and a full renovation of a private home in Sofia, March 2026.",
            [
                ("Date:", "March 2026"),
                ("Location:", "Sofia"),
                ("Work carried out:", "Plastering, painting, finishing around doors and windows, replacement of plumbing and electrical installations, and new flooring."),
            ],
            "FinishArt presents a recent project: a careful renovation of a private home, with plastering and painting chosen to improve both the look of the rooms and how they wear. It shows the standard we work to, and an approach shaped around the particular home.",
            [
                (HALL_BEFORE, "Hallway before the renovation, with exposed plaster"),
                (HALL_AFTER, "Hallway after painting and a wood floor"),
                (BED_BEFORE, "Bedroom before the window reveal was finished"),
                (BED_AFTER, "Bedroom after painting and a wood floor"),
            ],
        )
        project(
            lang, "bath_sofia", "bathrooms",
            "Bathroom renovation — Sofia",
            "Bathroom renovation — Sofia | FinishArt",
            "Strip-out, plastering, wall tiles and sanitaryware. Sofia, November 2025.",
            [
                ("Location:", "Sofia"),
                ("Date:", "November 2025"),
                ("Work carried out:", "Strip-out and removal, plastering, wall tiles and sanitaryware."),
            ],
            "",
            [
                (SOFIA_AFTER, "Bathroom after renovation, with light tiles and a round mirror"),
                (SOFIA_BEFORE, "Bathroom before renovation, with old tiles and a pedestal basin"),
            ],
            next_key="bath_house",
        )
        project(
            lang, "bath_house", "bathrooms",
            "Bathroom renovation in a country house",
            "Bathroom renovation in a country house | FinishArt",
            "Full bathroom renovation in the village of Uglen, December 2025.",
            [
                ("Date:", "December 2025"),
                ("Location:", "Uglen"),
                ("Work carried out:", "Full bathroom renovation."),
            ],
            "FinishArt presents plastering and painting that turned a badly damaged building into a fresh, modern space. The renovation shows our commitment to sound workmanship and an approach shaped to the particular home, giving a traditional house a new finish.",
            [
                (HOUSE_1, "White towels on a chrome rail in a shower"),
                (HOUSE_2, "Bathroom before renovation, with a damaged shower"),
                (HOUSE_3, "Shower with a glass screen and wood-slat walls"),
                (HOUSE_4, "Basin and a wall covered in leaf-pattern wallpaper"),
            ],
            prev_key="bath_sofia",
        )
        project(
            lang, "office", "other",
            "Plastering and painting of office space",
            "Plastering and painting of office space | FinishArt",
            "Plastering, painting and flooring. Sofia, May 2025.",
            [
                ("Location:", "Sofia"),
                ("Date:", "May 2025"),
                ("Work carried out:", "Plastering and painting, and laying flooring"),
            ],
            "",
            [
                (OFFICE_BEFORE, "Office before the work, with exposed concrete"),
                (OFFICE_AFTER, "Office after the columns and floor were finished"),
                (OFFICE_BEFORE_2, "Office before the work, with plasterboard on the walls"),
                (OFFICE_AFTER_2, "Office after the walls and ceiling were painted"),
            ],
            next_key="stairs",
        )
        project(
            lang, "stairs", "other",
            "Staircase renovation",
            "Staircase renovation | FinishArt",
            "Plastering, painting and restoration of the steps. Sofia, January 2026.",
            [
                ("Date:", "January 2026"),
                ("Location:", "Sofia"),
                ("Work carried out:", "Plastering, painting and restoration of the steps."),
            ],
            "FinishArt presents a staircase brought back with plastering and painting, carried out with care and sound workmanship. The renovation is an example of the finish we aim for, improving both the appearance and the durability of the space.",
            [
                (STAIRS, "Spiral staircase with a wooden handrail and white balusters"),
                (STAIRS_BEFORE, "Stair details before the renovation"),
                (STAIRS_AFTER, "Stair details after painting and new treads"),
            ],
            prev_key="office",
        )


def legal_article(lang, key, title, description, inner):
    body = f"""
    <article class="legal">
{inner}
    </article>
"""
    emit(lang, key, title, description, body)


def privacy(lang):
    if lang == "bg":
        legal_article(lang, "privacy", "Политика за поверителност | ФинишАрт",
            "Как ФинишАрт обработва запитванията от сайта и какви права имате по GDPR.",
            f"""
      <h1>Политика за поверителност</h1>
      <p>ФинишАрт уважава Вашата поверителност. Администратор на личните данни е „Био Дизайн 2021“ ЕООД, ЕИК 206494745, със седалище и адрес на управление бул. „Янко Сакъзов“ 17, район „Сердика“, София 1504, България.</p>
      <p>За въпроси и искания: <a href="mailto:{EMAIL}">{EMAIL}</a>, телефон <a href="tel:{PHONE}">+359882820025</a>.</p>
      <h2>Запитвания</h2>
      <p>Когато изпратите запитване чрез сайта, обработваме предоставените от Вас данни — имейл адрес и текста на съобщението — единствено за комуникация, изготвяне на оферта и последващо обслужване във връзка със запитването. Ако в текста посочите име или телефон, те се обработват като част от същото съобщение.</p>
      <p>Обработването се основава на предприемане на стъпки преди сключване на договор или на законен интерес да отговорим на получено запитване, според характера на запитването (чл. 6, пар. 1, б. „б“ и б. „е“ от Регламент (ЕС) 2016/679). Сайтът не изпраща бюлетини и не използва данните за реклама.</p>
      <p>Имейлът и съобщението са необходими, за да отговорим чрез формата. Без тях запитването не може да бъде изпратено. Можете да се свържете с нас и по телефона. Връзката за обаждане отваря приложението на устройството Ви. Сайтът не записва разговора.</p>
      <h2>Срокове за съхранение</h2>
      <p>Сайтът не поддържа собствена база със запитвания. Съобщението се изпраща по електронна поща и се съхранява в пощенската кутия, докато е необходимо за отговора и последващото обслужване по същото запитване. Когато от кореспонденцията възникне договор или счетоводен документ, той се пази за срока, изискван от приложимото счетоводно и данъчно законодателство. Ако изпращането не успее, съобщението не се съхранява на сайта.</p>
      <p>При изпращане на формата IP адресът се използва до 60 секунди единствено за ограничаване на повторни изпращания и не се записва в база. Бисквитката за езика се пази 180 дни или докато я изтриете.</p>
      <h2>Получатели</h2>
      <p>За функционирането и защитата на сайта използваме необходимите технически услуги. Доставчици на инфраструктура и електронна поща могат да обработват данни от наше име:</p>
      <ul>
        <li>Cloudflare — доставка и защита на сайта, включително кратката обработка на IP адреса при формата;</li>
        <li>Resend — изпращане на запитването по електронна поща;</li>
        <li>Yahoo — пощенската кутия <a href="mailto:{EMAIL}">{EMAIL}</a>, когато писмото бъде доставено.</li>
      </ul>
      <p>Данните не се продават и не се предоставят за реклама на трети лица.</p>
      <h2>Предаване извън Европейското икономическо пространство</h2>
      <p>Resend и Yahoo могат да обработват съдържанието на запитването в Съединените щати. Cloudflare може да обработва технически данни извън Европейското икономическо пространство, за да достави и защити сайта. Предаването се извършва при приложимите изисквания на глава V от GDPR. В настройките на сайта не е записан отделен договорен механизъм за това предаване, например стандартни договорни клаузи.</p>
      <h2>Бисквитки</h2>
      <p>Сайтът използва бисквитка за избрания език. Подробности има в <a href="{url_for("bg", "cookies")}">политиката за бисквитките</a>. Към момента не се използват аналитични или маркетингови бисквитки.</p>
      <h2>Вашите права</h2>
      <p>Имате право на достъп, коригиране, изтриване, ограничаване на обработването, възражение срещу обработване на основание законен интерес и, когато се прилага, преносимост. Исканията се изпращат на <a href="mailto:{EMAIL}">{EMAIL}</a>. Ще отговорим в срок до един месец, освен ако регламентът не позволява удължаване.</p>
      <p>Имате право да подадете жалба до Комисията за защита на личните данни — <a href="https://www.cpdp.bg">www.cpdp.bg</a>, София 1592, бул. „Проф. Цветан Лазаров“ № 2, <a href="mailto:kzld@cpdp.bg">kzld@cpdp.bg</a>.</p>
      <p>Не се извършва автоматизирано вземане на решения, включително профилиране.</p>
""")
    else:
        legal_article(lang, "privacy", "Privacy Policy | FinishArt",
            "How FinishArt uses enquiries sent through the website, and the rights you have under the GDPR.",
            f"""
      <h1>Privacy Policy</h1>
      <p>FinishArt respects your privacy. The controller of personal data is „Био Дизайн 2021“ ЕООД, company number 206494745, with its registered office at 17 Yanko Sakazov Blvd., Serdika District, Sofia 1504, Bulgaria.</p>
      <p>For questions and requests: <a href="mailto:{EMAIL}">{EMAIL}</a>, telephone <a href="tel:{PHONE}">+359882820025</a>.</p>
      <h2>Enquiries</h2>
      <p>When you send an enquiry through the website, we use the details you provide — your email address and the text of the message — only to correspond with you, prepare a quote and follow up on that enquiry. If you include a name or telephone number in the message, we treat it as part of the same enquiry.</p>
      <p>The processing is based on steps taken before entering into a contract, or on the legitimate interest in replying to an enquiry we have received, depending on what you ask (Article 6(1)(b) and (f) of Regulation (EU) 2016/679). The website does not send newsletters and does not use these details for advertising.</p>
      <p>The email address and the message are needed if we are to reply through the form. Without them, the enquiry cannot be sent. You can also contact us by telephone. The telephone link opens the calling app on your device. The website does not record the call.</p>
      <h2>How long we keep information</h2>
      <p>The website does not keep its own database of enquiries. The message is sent by email and kept in the mailbox for as long as it is needed to reply and to follow up on the same enquiry. Where the correspondence becomes a contract or an accounting record, it is kept for the period required by applicable accounting and tax law. If sending fails, the message is not stored on the website.</p>
      <p>When the form is submitted, the IP address is used for up to 60 seconds, only to limit repeat submissions, and is not written to a database. The language cookie is kept for 180 days, or until you delete it.</p>
      <h2>Recipients</h2>
      <p>We use the technical services needed to run and protect the website. Infrastructure and email providers may process data on our behalf:</p>
      <ul>
        <li>Cloudflare — delivery and protection of the website, including the short-lived use of the IP address when the form is submitted;</li>
        <li>Resend — sending the enquiry by email;</li>
        <li>Yahoo — the mailbox <a href="mailto:{EMAIL}">{EMAIL}</a>, once the message is delivered.</li>
      </ul>
      <p>We do not sell personal data or pass it to third parties for advertising.</p>
      <h2>Transfers outside the European Economic Area</h2>
      <p>Resend and Yahoo may process the content of an enquiry in the United States. Cloudflare may process technical data outside the European Economic Area in order to deliver and protect the website. Any such transfer is made under Chapter V of the GDPR. The website configuration does not record a separate contractual transfer tool, such as standard contractual clauses.</p>
      <h2>Cookies</h2>
      <p>The website uses a cookie to remember the language you choose. Details are in the <a href="{url_for("en", "cookies")}">Cookie Policy</a>. The website does not currently use analytics or marketing cookies.</p>
      <h2>Your rights</h2>
      <p>You have the right of access, rectification, erasure and restriction, the right to object to processing based on legitimate interests and, where it applies, the right to data portability. Send requests to <a href="mailto:{EMAIL}">{EMAIL}</a>. We will reply within one month, unless the Regulation allows an extension.</p>
      <p>You have the right to lodge a complaint with the Commission for Personal Data Protection — <a href="https://www.cpdp.bg">www.cpdp.bg</a>, 2 Prof. Tsvetan Lazarov Blvd., Sofia 1592, <a href="mailto:kzld@cpdp.bg">kzld@cpdp.bg</a>.</p>
      <p>We do not make decisions based solely on automated processing, including profiling.</p>
""")


def cookies(lang):
    if lang == "bg":
        legal_article(lang, "cookies", "Политика за бисквитките | ФинишАрт",
            "Сайтът на ФинишАрт използва бисквитка за избрания език. Няма аналитични или маркетингови бисквитки.",
            f"""
      <h1>Политика за бисквитките</h1>
      <p>Сайтът на ФинишАрт използва бисквитка за запазване на избрания език.</p>
      <p>Бисквитката <code>finishart-lang</code> съхранява предпочитанието Ви за български или английски език (стойност bg или en) за срок от 180 дни. Записва се, когато изберете език, и отваря началния адрес на този език. Тя не се използва за реклама или проследяване.</p>
      <p>Можете да я премахнете чрез настройките за бисквитки или на браузъра. Бутонът „Настройки за бисквитки“ отваря панел с действие „Изтрий езиковото предпочитание“. След изтриване началният адрес се отваря на български, докато не изберете друг език.</p>
      <p>Към момента сайтът не използва аналитични или маркетингови бисквитки и не зарежда проследяващи скриптове.</p>
      <p>Cloudflare, който доставя сайта, може да запише кратка техническа бисквитка, за да защити сайта от автоматизиран трафик. Тя не служи за реклама или статистика.</p>
      <p>Връзката към Facebook води към друга страница. Бисквитка на Facebook се появява само ако я отворите.</p>
      <p>Повече за обработката има в <a href="{url_for("bg", "privacy")}">политиката за поверителност</a>.</p>
""")
    else:
        legal_article(lang, "cookies", "Cookie Policy | FinishArt",
            "The FinishArt website uses a cookie to remember your language. It does not use analytics or marketing cookies.",
            f"""
      <h1>Cookie Policy</h1>
      <p>The FinishArt website uses a cookie to remember the language you choose.</p>
      <p>The cookie <code>finishart-lang</code> stores your preference for Bulgarian or English (the value bg or en) for 180 days. It is saved when you choose a language, and it opens the home address in that language. It is not used for advertising or tracking.</p>
      <p>You can remove it in Cookie settings or in your browser. The “Cookie settings” button opens a panel with the action “Delete language preference”. After you delete it, the home address opens in Bulgarian until you choose another language.</p>
      <p>The website does not currently use analytics or marketing cookies, and it does not load tracking scripts.</p>
      <p>Cloudflare, which delivers the website, may store a short-lived technical cookie to protect the site from automated traffic. That cookie is not used for advertising or statistics.</p>
      <p>The Facebook link leaves this website. A Facebook cookie is set only if you open that page.</p>
      <p>More about how we use personal data is in the <a href="{url_for("en", "privacy")}">Privacy Policy</a>.</p>
""")


def terms(lang):
    if lang == "bg":
        legal_article(lang, "terms", "Общи условия | ФинишАрт",
            "Общи условия за ползване на сайта на ФинишАрт. Цените са ориентировъчни, а запитването не сключва договор.",
            f"""
      <h1>Общи условия за ползване</h1>
      <p>Сайтът finishart.bg представя услугите на ФинишАрт, предоставяни от „Био Дизайн 2021“ ЕООД, ЕИК 206494745. Данните за дружеството са на страницата <a href="{url_for("bg", "legal")}">Данни за търговеца</a>.</p>
      <p>Публикуваната информация има представителен характер. Посочените цени са ориентировъчни, освен ако изрично не е посочено друго. Окончателната стойност на услугите се определя след уточняване на обхвата на работата и изготвяне на индивидуална оферта.</p>
      <p>Изпращането на запитване не представлява автоматично сключване на договор.</p>
      <p>Текстовете, изображенията и останалото съдържание са защитени съгласно приложимото законодателство, доколкото дружеството притежава съответните права.</p>
      <p>За въпроси и информация: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <p>Прилага се законодателството на Република България, без ограничаване на задължителните права на потребителите.</p>
      <p>Обработването на лични данни е описано в <a href="{url_for("bg", "privacy")}">политиката за поверителност</a>.</p>
""")
    else:
        legal_article(lang, "terms", "Terms of Use | FinishArt",
            "Terms of use for the FinishArt website. Prices are a guide, and an enquiry does not form a contract.",
            f"""
      <h1>Terms of Use</h1>
      <p>The website finishart.bg presents the services of FinishArt, provided by „Био Дизайн 2021“ ЕООД, company number 206494745. Company details are on the <a href="{url_for("en", "legal")}">Company Information</a> page.</p>
      <p>The information published on the website is for presentation. Prices shown are a guide unless we expressly say otherwise. The final price is set once the scope of work has been agreed and an individual quote has been prepared.</p>
      <p>Sending an enquiry does not, by itself, form a contract.</p>
      <p>The text, images and other content are protected by applicable law, to the extent the company holds the relevant rights.</p>
      <p>For questions and information: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <p>The law of the Republic of Bulgaria applies, without limiting consumers’ mandatory rights.</p>
      <p>Use of personal data is described in the <a href="{url_for("en", "privacy")}">Privacy Policy</a>.</p>
""")


def company(lang):
    if lang == "bg":
        legal_article(lang, "legal", "Данни за търговеца | ФинишАрт",
            "Био Дизайн 2021 ЕООД, ЕИК 206494745, търговска марка ФинишАрт. Седалище, телефон и имейл.",
            f"""
      <h1>Данни за търговеца</h1>
      <p>ФинишАрт е търговска марка, под която „Био Дизайн 2021“ ЕООД представя своите ремонтни и довършителни услуги.</p>
      <ul>
        <li>Дружество: Био Дизайн 2021 ЕООД</li>
        <li>ЕИК: 206494745</li>
        <li>Седалище и адрес на управление: бул. „Янко Сакъзов“ 17, район „Сердика“, София 1504, България</li>
        <li>Телефон: <a href="tel:{PHONE}">+359882820025</a></li>
        <li>Имейл: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>Уебсайт: <a href="{SITE}">finishart.bg</a></li>
        <li>Регистър: Търговски регистър към Агенцията по вписванията</li>
        <li>ДДС: дружеството не е регистрирано по Закона за данък върху добавената стойност и няма ДДС номер</li>
      </ul>
""")
    else:
        legal_article(lang, "legal", "Company Information | FinishArt",
            "Био Дизайн 2021 ЕООД, company number 206494745, trading as FinishArt. Registered office, telephone and email.",
            f"""
      <h1>Company Information</h1>
      <p>FinishArt is the trading name under which „Био Дизайн 2021“ ЕООД presents its renovation and finishing services.</p>
      <ul>
        <li>Company: Био Дизайн 2021 ЕООД (“Bio Design 2021” Ltd.)</li>
        <li>Company number (EIK): 206494745</li>
        <li>Registered office: 17 Yanko Sakazov Blvd., Serdika District, Sofia 1504, Bulgaria</li>
        <li>Telephone: <a href="tel:{PHONE}">+359882820025</a></li>
        <li>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>Website: <a href="{SITE}">finishart.bg</a></li>
        <li>Register: Commercial Register at the Registry Agency</li>
        <li>VAT: the company is not registered for VAT and has no VAT number</li>
      </ul>
""")


def access(lang):
    if lang == "bg":
        legal_article(lang, "access", "Достъпност | ФинишАрт",
            "Как ФинишАрт се стреми сайтът да бъде удобен за всички посетители и как да съобщите за затруднение.",
            f"""
      <h1>Достъпност</h1>
      <p>Стремим се сайтът на ФинишАрт да бъде лесен и удобен за използване от всички посетители.</p>
      <p>Работим за ясна навигация, четлив текст, подходящ цветови контраст и достъпност чрез клавиатура и помощни технологии.</p>
      <p>Ако срещнете затруднение при използването на сайта или достъпа до информация, свържете се с нас на <a href="mailto:{EMAIL}">{EMAIL}</a> или <a href="tel:{PHONE}">+359882820025</a>.</p>
      <p>Ще съдействаме за предоставяне на необходимата информация в достъпен формат.</p>
""")
    else:
        legal_article(lang, "access", "Accessibility | FinishArt",
            "How FinishArt aims to keep the website usable for every visitor, and how to tell us if something gets in the way.",
            f"""
      <h1>Accessibility</h1>
      <p>We want the FinishArt website to be straightforward and comfortable for every visitor.</p>
      <p>We work towards clear navigation, readable text, suitable colour contrast, and access by keyboard and assistive technology.</p>
      <p>If you have difficulty using the website or reaching the information you need, contact us at <a href="mailto:{EMAIL}">{EMAIL}</a> or <a href="tel:{PHONE}">+359882820025</a>.</p>
      <p>We will help provide the information in an accessible form.</p>
""")


def missing():
    body = """
    <div class="missing">
      <div>
        <h1>Страницата не е намерена</h1>
        <p>Page not found.</p>
        <p><a class="btn" href="/bg">Към началото</a> <a class="btn" href="/en">Home</a></p>
      </div>
    </div>
"""
    write(
        "404.html",
        layout(
            "bg",
            None,
            "Страницата не е намерена | ФинишАрт",
            "Търсената страница не съществува.",
            body,
            noindex=True,
            alternates=False,
        ),
    )


def robots_and_sitemap():
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8",
    )
    keys = [
        "home", "portfolio", "apartments", "apartment", "bathrooms", "bath_sofia", "bath_house",
        "other", "office", "stairs", "privacy", "cookies", "terms", "legal", "access",
    ]
    blocks = []
    for key in keys:
        bg = loc(url_for("bg", key))
        en = loc(url_for("en", key))
        for page in (bg, en):
            blocks.append(
                "  <url>\n"
                f"    <loc>{page}</loc>\n"
                "    <lastmod>2026-11-16</lastmod>\n"
                f'    <xhtml:link rel="alternate" hreflang="bg" href="{bg}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{bg}"/>\n'
                "  </url>"
            )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(blocks)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("robots.txt sitemap.xml")


def clean():
    for child in ROOT.iterdir():
        if child.name in KEEP_DIRS or child.name.startswith("."):
            continue
        if child.is_dir():
            shutil.rmtree(child)
        elif child.suffix in {".html", ".xml", ".txt"}:
            child.unlink()


def main():
    clean()
    for lang in ("bg", "en"):
        home(lang)
        portfolio(lang)
        projects(lang)
        privacy(lang)
        cookies(lang)
        terms(lang)
        company(lang)
        access(lang)
    missing()
    root_fallback()
    robots_and_sitemap()


def root_fallback():
    write(
        "index.html",
        f"""<!DOCTYPE html>
<html lang="bg">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ФинишАрт</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE}/bg">
  <meta http-equiv="refresh" content="0; url=/bg">
  <script>location.replace("/bg");</script>
</head>
<body>
  <p><a href="/bg">ФинишАрт</a> · <a href="/en">English</a></p>
</body>
</html>
""",
    )


if __name__ == "__main__":
    main()
