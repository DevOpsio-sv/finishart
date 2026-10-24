# -*- coding: utf-8 -*-
"""Write the static FinishArt pages into public/."""
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent / "public"
SITE = "https://www.finishart.bg"
PDF = "/_files/ugd/a86e04_1e8507bd40c34be0ba40b41a3c899912.pdf"

MENU = """
<div class="nav-panel" id="site-menu" data-panel hidden>
  <button class="nav-close" type="button" data-close aria-label="Затвори меню">×</button>
  <nav aria-label="Сайт">
    <ul>
      <li><a href="/#nachalna">Начална</a></li>
      <li><a href="/#za-nas">За Нас</a></li>
      <li><a href="/#uslugi">Услуги</a></li>
      <li><a href="/portfolio">Портфолио</a></li>
    </ul>
  </nav>
</div>
"""

HEADER = """
<header class="site-header">
  <a class="logo" href="/" aria-label="ФинишАрт, начало">
    <img src="/assets/logo.png" alt="FinishArt" width="180" height="50">
  </a>
  <button class="menu-btn" type="button" data-menu aria-expanded="false" aria-controls="site-menu">МЕНЮ</button>
</header>
"""

FOOTER = f"""
<footer class="site-footer">
  <div class="footer-logo">
    <a class="logo" href="/" aria-label="ФинишАрт, начало">
      <img src="/assets/logo.png" alt="" width="160" height="44">
    </a>
  </div>
  <div class="footer-grid">
    <div>
      <h2>Изпратете запитване</h2>
      <form data-contact novalidate>
        <p class="hp" aria-hidden="true">
          <label>Уебсайт <input name="website" tabindex="-1" autocomplete="off"></label>
        </p>
        <label class="field">
          <span>Имейл *</span>
          <input name="email" type="email" autocomplete="email" required aria-label="Имейл">
        </label>
        <label class="field">
          <span>Запитване *</span>
          <textarea name="message" required aria-label="Запитване"></textarea>
        </label>
        <button class="btn" type="submit">Изпрати</button>
        <p class="form-status" data-status role="status"></p>
      </form>
    </div>
    <div class="contact-block">
      <p><a href="tel:+359882820025">0882 820025</a></p>
      <p><a href="mailto:alex.finishart@gmail.com">alex.finishart@gmail.com</a></p>
    </div>
    <div class="contact-block">
      <p>София 1505,</p>
      <p>бул. Янко Сакъзов 17</p>
    </div>
  </div>
  <div class="footer-meta">
    <nav aria-label="Правни страници">
      <a href="/политика-за-поверителност">Политика за поверителност</a>
      <a href="/декларация-за-достъп">Декларация за достъпност</a>
    </nav>
    <a class="fb" href="https://www.facebook.com/profile.php?id=61577536868457" aria-label="Facebook">
      <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M14.5 8.5V6.8c0-.7.5-1 1.2-1H17V3h-2.2C12.4 3 11 4.5 11 6.9v1.6H9v2.7h2V21h3v-9.8h2.4l.6-2.7h-3z"/></svg>
    </a>
  </div>
  <p class="copy">© 2026 by FinishArt</p>
</footer>
<dialog class="lightbox">
  <form method="dialog"><button type="submit">Затвори</button></form>
  <img alt="">
</dialog>
"""

ICONS = """
<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><circle cx="12" cy="9" r="4" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M8 13.5 7 21l5-2.2L17 21l-1-7.5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="m8.5 12.2 2.2 2.2 4.8-5" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M12 8v4.2l2.6 1.6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
"""


def layout(title, description, path, body, home=False, verify=False):
    canonical = loc(path)
    klass = "home" if home else "inner"
    verify_meta = ""
    if verify:
        verify_meta = """
  <meta name="google-site-verification" content="ou8d_j-1cycgAh7CnWuF3WQm-mbM-jUDU7NVq-bElx4">
  <meta name="msvalidate.01" content="82C6436E0F3D5F09BDD7B1C13E81EC5F">"""
    return f"""<!DOCTYPE html>
<html lang="bg">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/og.jpg">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Alex">
  <meta property="og:locale" content="bg_BG">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE}/assets/og.jpg">
  <meta name="theme-color" content="#823c2e">
  <link rel="icon" href="/assets/logo.png" type="image/png">{verify_meta}
  <link rel="stylesheet" href="/css/styles.css">
</head>
<body class="{klass}">
  <a class="skip" href="#main">Премини към основното съдържание</a>
  {HEADER}
  {MENU}
  <main id="main">
{body}
  </main>
  {FOOTER}
  <script src="/js/site.js"></script>
</body>
</html>
"""


def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(rel)


def loc(path):
    if path in ("", "/"):
        return SITE + "/"
    encoded = "/".join(quote(part) for part in path.strip("/").split("/"))
    return SITE + "/" + encoded


def home():
    desc = "Професионална шпакловка, боядисване и довършителни ремонти от Финиш Арт ООД. Надеждно изпълнение, коректност и перфектен завършек."
    ribbon, check, clock = ICONS.strip().split("\n")
    body = f"""
    <section class="hero" id="nachalna">
      <div class="hero-copy">
        <h1>Качествено<br>боядисване и<br>шпакловка</h1>
        <p class="hero-lead">Вашият доверен партньор за частни домове и мащабни проекти.</p>
        <p class="hero-lead">Предлагаме прецизност в детайла, стриктни срокове, безупречна чистота, както до 24 месеца гаранция за изпълнението.</p>
        <a class="btn" href="tel:+359882820025">Вземете безплатна оферта</a>
        <p class="hero-note">* Цени от 8–22 евро/кв.м според състоянието на стените и вида на услугата.</p>
      </div>
      <div class="hero-media">
        <img src="/assets/hero.jpg" alt="Светъл интериор с високи прозорци след боядисване" width="1536" height="2048">
      </div>
    </section>
    <section id="za-nas" aria-labelledby="why-title">
      <h2 class="why-title" id="why-title">Защо ние?</h2>
      <div class="why">
        <div class="why-grid">
          <article class="why-card">
            <p class="why-num">1</p>
            <h3>Точност:<br>Планираме алгоритмично, изпълняваме в срок</h3>
            <p>Времето е най-ценният ресурс и затова го ценим, колкото вас.</p>
            <p>Не просто гоним крайни дати, а планираме всеки етап от обекта алгоритмично.</p>
            <p>Това ни позволява да гарантираме 100% спазване на сроковете, без значение дали работим с частни обекти или като подизпълнител в мащабен проект.</p>
          </article>
          <article class="why-card">
            <p class="why-num">2</p>
            <h3>Чистота и Защита:<br>Вашият комфорт е наш приоритет</h3>
            <p>Ремонтът не трябва да спира живота ви.</p>
            <p>Процесите ни са оптимизирани така, че да работим безпроблемно, дори в обитаеми помещения.</p>
            <p>Обучени сме да балансираме между максимална бързина и абсолютна чистота.</p>
          </article>
          <article class="why-card">
            <p class="why-num">3</p>
            <h3>Експертиза и Технология: Основани през 2018, водени от иновациите</h3>
            <p>Съчетаваме натрупания опит с най-съвременните стандарти в довършителните работи.</p>
            <p>Използваме съвременни технологии и методи за нанасяне, които гарантират перфектно гладки повърхности.</p>
            <p>Следим отблизо еволюцията на материалите и технологиите, за да предложим на нашите клиенти най-доброто от пазара днес.</p>
          </article>
        </div>
      </div>
    </section>
    <section class="commit" aria-labelledby="commit-title">
      <div class="commit-copy">
        <h2 id="commit-title">Нашият ангажимент</h2>
        <p>Във Финиш Арт сме специализирани в услуги по боядисване и шпакловане, които превръщат вашата идея в реалност.</p>
        <p>Нашето внимание към детайла и качественото майсторство гарантират, че всеки проект отговаря на вашите изисквания, като същевременно подобрява и облагородява вашето пространство.</p>
        <a class="btn" href="/portfolio">Разгледай портфолио</a>
      </div>
      <div class="commit-media">
        <img src="/assets/plaster.jpg" alt="Шпакловка на стена в София" width="1600" height="900">
      </div>
    </section>
    <section class="services" id="uslugi" aria-labelledby="services-title">
      <h2 id="services-title">Нашите услуги</h2>
      <p class="sub">Освежителен или основен ремонт с внимание към детайла</p>
      <p class="price-line">Цени от 8 €/кв.м.</p>
      <a class="btn" href="{PDF}">Виж актуални цени</a>
      <ul class="perks">
        <li>{ribbon} Качествени материали</li>
        <li>{check} Прецизна работа</li>
        <li>{clock} Коректни срокове</li>
      </ul>
      <div class="service-panel">
        <figure class="service-card">
          <img src="/assets/apartment.jpg" alt="Ремонтиран апартамент в София" width="800" height="980">
          <figcaption>Интериорно боядисване</figcaption>
        </figure>
        <figure class="service-card">
          <img src="/assets/trowel.jpg" alt="Ръка с маламашка при шпакловане" style="object-position:center 42%" width="800" height="980">
          <figcaption>Шпакловка</figcaption>
        </figure>
        <figure class="service-card">
          <img src="/assets/room.jpg" alt="Стая по време на ремонт" style="object-position:72% center" width="800" height="980">
          <figcaption>Основен ремонт</figcaption>
        </figure>
      </div>
    </section>
    <section class="reviews" aria-labelledby="reviews-title">
      <h2 id="reviews-title">Какво казват клиентите?</h2>
      <div class="review-stage">
        <button class="arrow" type="button" data-dir="-1" aria-label="Предишна">←</button>
        <div>
          <article class="review is-active" data-slide>
            <img src="/assets/review-owner.jpg" alt="Владислав Хаджиангелов, собственик на БГ Бар" width="800" height="1100" style="object-position:center 30%">
            <div class="review-copy">
              <p>„Много съм доволен от работата, която свършиха в заведението, както и от отношението. Поздравления за бързата и качествена работа.“</p>
              <p class="who">Владислав Хаджиангелов, собственик, „БГ Бар“</p>
            </div>
          </article>
          <article class="review" data-slide>
            <img src="/assets/review-marketing.jpg" alt="Гинка Миланова, бранд мениджър" width="800" height="1100" style="object-position:center 20%">
            <div class="review-copy">
              <p>„Финиш Арт направиха, каквото обещаха, въпреки че бях скептична, защото имах негативен опит с други фирми. Благодаря!“</p>
              <p class="who">Гинка Миланова, Бранд мениджър</p>
            </div>
          </article>
          <article class="review" data-slide>
            <img src="/assets/review-broker.jpg" alt="Брокер на недвижими имоти, доволен от Финиш Арт" width="800" height="1100">
            <div class="review-copy">
              <p>„Момчетата са отговорни и коректни, работят на достъпни цени и ги препоръчвам, както на клиенти, така и на мои близки.“</p>
              <p class="who">Трифон Трифонов - Тиката, Брокер</p>
            </div>
          </article>
        </div>
        <button class="arrow" type="button" data-dir="1" aria-label="Напред">→</button>
      </div>
      <div class="dots" role="tablist" aria-label="Слайдове">
        <button type="button" data-dot role="tab" aria-label="Собственик" aria-selected="true"></button>
        <button type="button" data-dot role="tab" aria-label="Меркетинг" aria-selected="false"></button>
        <button type="button" data-dot role="tab" aria-label="Брокер" aria-selected="false"></button>
      </div>
    </section>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "HomeAndConstructionBusiness",
      "name": "ФинишАрт",
      "url": "https://www.finishart.bg/",
      "image": "https://www.finishart.bg/assets/og.jpg",
      "telephone": "+359882820025",
      "email": "alex.finishart@gmail.com",
      "foundingDate": "2018",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "бул. Янко Сакъзов 17",
        "addressLocality": "София",
        "postalCode": "1505",
        "addressCountry": "BG"
      }}
    }}
    </script>
"""
    # The home body is interpolated above with an f-string, so JSON braces were doubled.
    write("index.html", layout("Начална | ФинишАрт - шпакловка и боя", desc, "/", body, home=True, verify=True))


def portfolio():
    desc = "Портфолио на ФинишАрт: апартаменти, бани и други жилищни и бизнес проекти."
    body = """
    <div class="folio">
      <a href="/portfolio-collections/апартаменти">
        <img src="/assets/portfolio-apartments.jpg" alt="Апартамент след ремонт с дървен под и големи прозорци">
        <span>Апартаменти - от къртене до ключ</span>
      </a>
      <a href="/portfolio-collections/баня-и-тоалетна">
        <img src="/assets/portfolio-bath.jpg" alt="Баня със стъклена душ кабина и бял фаянс">
        <span>Баня и тоалетна - прецизност до посления детайл</span>
      </a>
      <a href="/portfolio-collections/my-portfolio">
        <img src="/assets/portfolio-other.jpg" alt="Стълбище в жилищен вход след боядисване">
        <span>Други обекти - жилищни и бизнес проекти</span>
      </a>
    </div>
"""
    write("portfolio/index.html", layout("Портфолио | Alex", desc, "/portfolio", body))


def collection(folder, title, description, intro, cards):
    thumbs = "\n".join(
        f"""      <a href="{href}">
        <img src="{src}" alt="{alt}">
      </a>"""
        for href, src, alt in cards
    )
    list_html = f'\n    <div class="project-list">\n{thumbs}\n    </div>' if cards else ""
    intro_html = f"\n      <p>{intro}</p>" if intro else ""
    body = f"""
    <p class="back"><a href="/portfolio">‹ Back to Portfolio</a></p>
    <header class="page-intro">
      <h1>{title}</h1>{intro_html}
    </header>{list_html}
"""
    write(
        f"portfolio-collections/{folder}/index.html",
        layout(title, description or title, f"/portfolio-collections/{folder}", body),
    )


def project(folder, slug, title, page_title, description, facts, story, images, prev_href=None, next_href=None):
    facts_html = "\n".join(
        f"""        <div class="meta"><h2>{label}</h2><p>{value}</p></div>""" for label, value in facts
    )
    story_html = f'<p class="project-story">{story}</p>' if story else ""
    figs = "\n".join(
        f"""      <figure>
        <img src="{src}" alt="{alt}" data-zoom>
        <figcaption>{alt}</figcaption>
      </figure>"""
        for src, alt in images
    )
    pager = ""
    if prev_href or next_href:
        left = f'<a href="{prev_href}">Предишен проект</a>' if prev_href else "<span></span>"
        right = f'<a href="{next_href}">Следващ проект</a>' if next_href else "<span></span>"
        pager = f'\n    <nav class="pager" aria-label="Проекти">{left}{right}</nav>'
    body = f"""
    <p class="back"><a href="/portfolio-collections/{folder}">‹ Back to Portfolio</a></p>
    <article class="project">
      <div>
        <h1>{title}</h1>
{facts_html}
      </div>
      <div>{story_html}</div>
    </article>
    <div class="gallery">
{figs}
    </div>{pager}
"""
    path = f"/portfolio-collections/{folder}/{slug}"
    write(
        f"portfolio-collections/{folder}/{slug}/index.html",
        layout(page_title, description, path, body),
    )


def legal_privacy():
    body = """
    <article class="legal">
      <h1>Политика за поверителност</h1>
      <h2>1. Администратор на лични данни</h2>
      <p>„FinishArt“<br>Email: <a href="mailto:alex.finishart@gmail.com">alex.finishart@gmail.com</a><br>Телефон: <a href="tel:+359882820025">+359 882820025</a></p>
      <h2>2. Какви данни събираме</h2>
      <p>Ние можем да събираме следните данни:</p>
      <ul>
        <li>Име и фамилия</li>
        <li>Телефонен номер</li>
        <li>Имейл адрес</li>
        <li>Данни от запитвания чрез контакт форма</li>
        <li>IP адрес и данни за използване на сайта</li>
      </ul>
      <h2>3. Цел на обработката</h2>
      <p>Вашите данни се използват за:</p>
      <ul>
        <li>Свързване с Вас по запитване</li>
        <li>Предоставяне на оферти за ремонтни услуги</li>
        <li>Подобряване на услугите ни</li>
        <li>Спазване на законови изисквания</li>
      </ul>
      <h2>4. Основание за обработка</h2>
      <p>Обработката се извършва на основание:</p>
      <ul>
        <li>Вашето съгласие</li>
        <li>Договорни отношения</li>
        <li>Законови задължения</li>
      </ul>
      <h2>5. Срок за съхранение</h2>
      <p>Личните данни се съхраняват само за периода, необходим за изпълнение на целите, или съгласно законовите изисквания.</p>
      <h2>6. Споделяне на данни</h2>
      <p>Ние не продаваме и не предоставяме Вашите данни на трети лица, освен когато:</p>
      <ul>
        <li>Това е необходимо за изпълнение на услуга</li>
        <li>Изисква се по закон</li>
      </ul>
      <h2>7. Вашите права</h2>
      <p>Имате право да:</p>
      <ul>
        <li>Получите достъп до Вашите данни</li>
        <li>Коригирате или изтриете данните си</li>
        <li>Ограничите обработката</li>
        <li>Подадете жалба до КЗЛД</li>
      </ul>
      <h2>8. Сигурност</h2>
      <p>Ние предприемаме технически и организационни мерки за защита на личните данни.</p>
      <h2>9. Контакти</h2>
      <p>Ако имате въпроси относно тази политика, можете да се свържете с нас на:<br>Email: <a href="mailto:alex.finishart@gmail.com">alex.finishart@gmail.com</a></p>
    </article>
"""
    write(
        "политика-за-поверителност/index.html",
        layout(
            "Политика за поверителност | Alex",
            "Политика за поверителност на FinishArt: какви данни събираме, защо и какви права имате.",
            "/политика-за-поверителност",
            body,
        ),
    )


def legal_access():
    body = """
    <article class="legal">
      <h1>Декларация за Достъпност</h1>
      <p>Настоящата декларация беше актуализирана на: 01.02.2026 г.</p>
      <p>Ние от „FinishArt“ работим за това нашият уебсайт <a href="https://www.finishart.bg">https://www.finishart.bg</a> да бъде достъпен за всички потребители, включително хора с увреждания.</p>
      <p>Достъпният уебсайт позволява на всички посетители да го използват с еднаква или сходна лекота и удобство, включително чрез помощни технологии.</p>
      <p>Този сайт е съобразен с изискванията на WCAG 2.1 и е разработен с цел постигане на ниво AA на достъпност.</p>
      <p>Съдържанието на сайта е адаптирано да работи с помощни технологии като екранни четци и навигация чрез клавиатура.</p>
      <p>Като част от усилията за достъпност:</p>
      <ul>
        <li>Използвани са ясни структури и заглавия</li>
        <li>Добавен е алтернативен текст към изображения</li>
        <li>Осигурен е достатъчен контраст между цветовете</li>
        <li>Намалено е използването на анимации</li>
        <li>Съдържанието е организирано за лесна навигация</li>
      </ul>
      <p>Възможно е част от съдържанието да зависи от външни услуги, за които не можем да гарантираме пълна съвместимост.</p>
      <p>Ако срещнете затруднения при използването на сайта или имате нужда от съдействие, моля свържете се с нас:</p>
      <p>Email: <a href="mailto:alex.finishart@gmail.com">alex.finishart@gmail.com</a><br>Телефон: <a href="tel:+359882820025">+359 882 820025</a></p>
      <p>Ние ще направим необходимото, за да осигурим достъп до необходимата информация.</p>
    </article>
"""
    write(
        "декларация-за-достъп/index.html",
        layout(
            "Декларация за достъп | Alex",
            "Декларация за достъпност на уебсайта на FinishArt, актуализирана на 01.02.2026 г.",
            "/декларация-за-достъп",
            body,
        ),
    )


def missing():
    body = """
    <div class="missing">
      <div>
        <h1>Страницата не е намерена</h1>
        <p><a class="btn" href="/">Към началото</a></p>
      </div>
    </div>
"""
    write(
        "404.html",
        layout("Страницата не е намерена | ФинишАрт", "Търсената страница не съществува.", "/404.html", body),
    )


def robots_and_sitemap(paths):
    (ROOT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://www.finishart.bg/sitemap.xml\n",
        encoding="utf-8",
    )
    urls = "\n".join(
        f"  <url><loc>{loc(path)}</loc><lastmod>2026-10-25</lastmod></url>" for path in paths
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n",
        encoding="utf-8",
    )
    print("robots.txt sitemap.xml")


def main():
    apt = "/portfolio-collections/апартаменти/шпакловка-и-боя-в-частно-жилище"
    bath_sofia = "/portfolio-collections/баня-и-тоалетна/реновация-на-баня-софия"
    bath_house = "/portfolio-collections/баня-и-тоалетна/реновация-на-баня-в-къща"
    home()
    portfolio()
    collection(
        "апартаменти",
        "Апартаменти - от къртене до ключ",
        "Изпълняваме цялостни основни ремонти на апартаменти и къщи.",
        "Изпълняваме цялостни основни ремонти на апартаменти и къщи.",
        [(apt, "/assets/project-before-after.jpg", "ремонт-софия-преди-след")],
    )
    collection(
        "баня-и-тоалетна",
        "Баня и тоалетна - прецизност до посления детайл",
        "Баня и тоалетна - прецизност до посления детайл",
        "",
        [
            (bath_sofia, "/assets/bath-sofia-after.jpg", "баня-ремонт-софия-след"),
            (bath_house, "/assets/bath-house.jpg", "ремонт-баня"),
        ],
    )
    collection(
        "my-portfolio",
        "Други обекти - жилищни и бизнес проекти",
        "Разгледайте част от нашите реализирани проекти в областта на шпакловката и боядисването.",
        "Разгледайте част от нашите реализирани проекти в областта на шпакловката и боядисването. Всеки обект е изпълнен с прецизност, качествени материали и внимание към всеки детайл. Нашето портфолио отразява стремежа ни към отличен резултат, дълготрайност и красиво завършени пространства.",
        [],
    )
    project(
        "апартаменти",
        "шпакловка-и-боя-в-частно-жилище",
        "Реновация на частно жилище",
        "Реновация на частно жилище | Alex",
        "Шпакловка, боядисване и основен ремонт на частно жилище в София, март 2026.",
        [
            ("Дата:", "Март 2026"),
            ("Локация:", "гр.София"),
            ("Извършени услуги:", "Шпакловка, боядисване, обръщане на врати и прозорци, подмяна на ВиК и ел. инсталации, поставяне на настилки."),
        ],
        "Финиш Арт с гордост представя своя последен проект - прецизен ремонт на частен дом, демонстриращ експертни решения в шпакловката и боядисването, които подобряват както естетиката, така и дълготрайността. Този проект е пример за нашия ангажимент към качествената изработка и индивидуалния подход, като преобразява жилищните пространства с прецизност и внимание.",
        [
            ("/assets/antre-before.jpg", "Антре - преди"),
            ("/assets/antre-after.jpg", "Антре - след"),
            ("/assets/bedroom-before.jpg", "Спялня - преди"),
            ("/assets/bedroom-after.jpg", "Спалня - след"),
        ],
    )
    project(
        "баня-и-тоалетна",
        "реновация-на-баня-софия",
        "Реновация на баня - София",
        "Реновация на баня - София | Alex",
        "Къртене, шпакловка, фаянс и санитария. София, ноември 2025.",
        [
            ("Локация:", "гр. София"),
            ("Дата:", "Ноември 2025"),
            ("Извършени услуги:", "Къртене и демонтаж, шпакловка, поставяне на фаянс и санитария."),
        ],
        "",
        [
            ("/assets/bath-sofia-before.jpg", "Баня - преди"),
            ("/assets/bath-sofia-after.jpg", "баня-ремонт-софия-след"),
        ],
        next_href=bath_house,
    )
    project(
        "баня-и-тоалетна",
        "реновация-на-баня-в-къща",
        "Реновация на баня в селска къща",
        "Реновация на баня в селска къща | Alex",
        "Основен ремонт на баня в с.Ъглен, декември 2025.",
        [
            ("Дата:", "Декември 2025"),
            ("Локация:", "с.Ъглен"),
            ("Извършени услуги:", "Основен ремонт на баня."),
        ],
        "Финиш Арт представя демонстрира професионални решения за шпакловка и боядисване, преобразили една разрушена постройка в модерно и свежо пространство. Тази реновация подчертава нашата отдаденост към качествената изработка и индивидуалния подход, вдъхвайки нов живот и стил на традиционните домове.",
        [
            ("/assets/bath-house-2.jpg", "Бяна - преди"),
            ("/assets/bath-house-3.jpg", "ремонт-баня"),
            ("/assets/bath-house.jpg", "ремонт-баня"),
            ("/assets/bath-house-4.jpg", "Баня - след"),
        ],
        prev_href=bath_sofia,
    )
    legal_privacy()
    legal_access()
    missing()
    robots_and_sitemap([
        "/",
        "/portfolio",
        "/portfolio-collections/апартаменти",
        apt,
        "/portfolio-collections/баня-и-тоалетна",
        bath_sofia,
        bath_house,
        "/portfolio-collections/my-portfolio",
        "/политика-за-поверителност",
        "/декларация-за-достъп",
    ])


if __name__ == "__main__":
    main()
