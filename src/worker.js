const LEGACY = new Map([
  ["/index.html", "/bg"],
  ["/portfolio", "/bg/portfolio"],
  ["/portfolio-collections/\u0430\u043f\u0430\u0440\u0442\u0430\u043c\u0435\u043d\u0442\u0438", "/bg/portfolio/apartments"],
  [
    "/portfolio-collections/\u0430\u043f\u0430\u0440\u0442\u0430\u043c\u0435\u043d\u0442\u0438/\u0448\u043f\u0430\u043a\u043b\u043e\u0432\u043a\u0430-\u0438-\u0431\u043e\u044f-\u0432-\u0447\u0430\u0441\u0442\u043d\u043e-\u0436\u0438\u043b\u0438\u0449\u0435",
    "/bg/portfolio/apartments/private-home-plaster-and-paint",
  ],
  ["/portfolio-collections/\u0431\u0430\u043d\u044f-\u0438-\u0442\u043e\u0430\u043b\u0435\u0442\u043d\u0430", "/bg/portfolio/bathrooms"],
  [
    "/portfolio-collections/\u0431\u0430\u043d\u044f-\u0438-\u0442\u043e\u0430\u043b\u0435\u0442\u043d\u0430/\u0440\u0435\u043d\u043e\u0432\u0430\u0446\u0438\u044f-\u043d\u0430-\u0431\u0430\u043d\u044f-\u0441\u043e\u0444\u0438\u044f",
    "/bg/portfolio/bathrooms/sofia-bathroom-renovation",
  ],
  [
    "/portfolio-collections/\u0431\u0430\u043d\u044f-\u0438-\u0442\u043e\u0430\u043b\u0435\u0442\u043d\u0430/\u0440\u0435\u043d\u043e\u0432\u0430\u0446\u0438\u044f-\u043d\u0430-\u0431\u0430\u043d\u044f-\u0432-\u043a\u044a\u0449\u0430",
    "/bg/portfolio/bathrooms/house-bathroom-renovation",
  ],
  ["/portfolio-collections/my-portfolio", "/bg/portfolio/other-projects"],
  [
    "/portfolio-collections/my-portfolio/\u0448\u043f\u0430\u043a\u043b\u043e\u0432\u043a\u0430-\u0438-\u0431\u043e\u044f\u0434\u0438\u0441\u0432\u0430\u043d\u0435-\u043d\u0430-\u043e\u0444\u0438\u0441-\u043f\u0440\u043e\u0441\u0442\u0440\u0430\u043d\u0441\u0442\u0432\u0430",
    "/bg/portfolio/other-projects/office-plaster-and-paint",
  ],
  [
    "/portfolio-collections/my-portfolio/\u0440\u0435\u043d\u043e\u0432\u0430\u0446\u0438\u044f-\u043d\u0430-\u0441\u0442\u044a\u043b\u0431\u0438\u0449\u0435",
    "/bg/portfolio/other-projects/staircase-renovation",
  ],
  ["/\u043f\u043e\u043b\u0438\u0442\u0438\u043a\u0430-\u0437\u0430-\u043f\u043e\u0432\u0435\u0440\u0438\u0442\u0435\u043b\u043d\u043e\u0441\u0442", "/bg/privacy"],
  ["/\u0434\u0435\u043a\u043b\u0430\u0440\u0430\u0446\u0438\u044f-\u0437\u0430-\u0434\u043e\u0441\u0442\u044a\u043f", "/bg/accessibility"],
]);

const PREFIXES = [
  ["/portfolio-collections/\u0430\u043f\u0430\u0440\u0442\u0430\u043c\u0435\u043d\u0442\u0438", "/bg/portfolio/apartments"],
  ["/portfolio-collections/\u0431\u0430\u043d\u044f-\u0438-\u0442\u043e\u0430\u043b\u0435\u0442\u043d\u0430", "/bg/portfolio/bathrooms"],
  ["/portfolio-collections/my-portfolio", "/bg/portfolio/other-projects"],
];

const BROKEN = "/portfolio-collections/\u0430\u043f\u0430\u0440\u0442\u0430\ufffd\u043c\u0435\u043d\u0442\u0438";

const COPY = {
  bg: {
    method: "Методът не е позволен.",
    wait: "Моля, изчакайте малко преди ново запитване.",
    long: "Запитването е твърде дълго.",
    bad: "Невалидни данни.",
    email: "Въведете валиден имейл.",
    message: "Напишете запитване между 2 и 5000 знака.",
    offline:
      "Формата още не е свързана с поща. Обадете се на 0882 820025 или пишете на alx.voynov@yahoo.com.",
    send: "Съобщението не беше доставено. Опитайте отново или се обадете.",
    subject: "Запитване от finishart.bg",
  },
  en: {
    method: "Method not allowed.",
    wait: "Please wait a moment before sending another enquiry.",
    long: "The enquiry is too long.",
    bad: "Invalid data.",
    email: "Enter a valid email address.",
    message: "Write an enquiry between 2 and 5000 characters.",
    offline:
      "The form is not connected to email yet. Call 0882 820025 or write to alx.voynov@yahoo.com.",
    send: "The message was not delivered. Try again or call us.",
    subject: "Enquiry from finishart.bg",
  },
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const hostChanged = url.hostname === "finishart.bg";
    if (hostChanged) url.hostname = "www.finishart.bg";

    if (request.method === "GET" && url.searchParams.has("forget-lang")) {
      url.searchParams.delete("forget-lang");
      url.searchParams.set("lang-cleared", "1");
      const secure = url.protocol === "https:" ? "; Secure" : "";
      const headers = new Headers({
        Location: url.toString(),
        "Cache-Control": "no-store",
      });
      headers.append("Set-Cookie", "finishart-lang=; Max-Age=0; Path=/; SameSite=Lax" + secure);
      return new Response(null, { status: 303, headers });
    }

    if (url.pathname === "/api/contact") {
      if (hostChanged) return Response.redirect(url.toString(), 301);
      if (request.method !== "POST") return json({ ok: false, error: COPY.bg.method }, 405);
      return handleContact(request, env);
    }

    let path = url.pathname;
    try {
      path = decodeURIComponent(url.pathname);
    } catch {
      path = url.pathname;
    }
    if (path.length > 1 && path.endsWith("/")) path = path.slice(0, -1);

    let target = null;
    if (path === "/" || path === "") {
      target = preferredLang(request) === "en" ? "/en" : "/bg";
    } else if (path === BROKEN || path.startsWith(BROKEN + "/")) {
      target = "/bg/portfolio/apartments";
    } else if (LEGACY.has(path)) {
      target = LEGACY.get(path);
    } else {
      for (const [from, to] of PREFIXES) {
        if (path.startsWith(from + "/")) {
          target = to;
          break;
        }
      }
    }

    if (target || hostChanged) {
      url.pathname = target || path || "/";
      const status = path === "/" || path === "" ? 302 : 301;
      return Response.redirect(url.toString(), status);
    }

    return serveAsset(request, env, path);
  },
};

async function serveAsset(request, env, path) {
  const response = await env.ASSETS.fetch(request);
  if (response.status >= 300 && response.status < 400) return response;
  const headers = new Headers(response.headers);
  const type = headers.get("content-type") || "";
  if (path.startsWith("/assets/") || path.startsWith("/fonts/") || path.startsWith("/_files/")) {
    headers.set("Cache-Control", "public, max-age=2592000");
  } else if (path.startsWith("/css/") || path.startsWith("/js/")) {
    headers.set("Cache-Control", "public, max-age=86400");
  } else if (type.includes("text/html")) {
    headers.set("Cache-Control", "public, max-age=300");
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

function preferredLang(request) {
  const raw = request.headers.get("cookie") || "";
  const match = raw.match(/(?:^|;\s*)finishart-lang=(bg|en)(?:\s*;|$)/);
  return match ? match[1] : "bg";
}

async function handleContact(request, env) {
  let body;
  try {
    const raw = await request.text();
    if (raw.length > 20000) return json({ ok: false, error: COPY.bg.long }, 400);
    body = JSON.parse(raw);
  } catch {
    return json({ ok: false, error: COPY.bg.bad }, 400);
  }
  if (!body || typeof body !== "object" || Array.isArray(body)) {
    return json({ ok: false, error: COPY.bg.bad }, 400);
  }

  const text = COPY[body.lang === "en" ? "en" : "bg"];
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  if (await tooSoon(ip)) return json({ ok: false, error: text.wait }, 429);

  const website = String(body.website || "");
  if (website) return json({ ok: true });

  const email = String(body.email || "").trim();
  const message = String(body.message || "").trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 200) {
    return json({ ok: false, error: text.email }, 400);
  }
  if (message.length < 2 || message.length > 5000) {
    return json({ ok: false, error: text.message }, 400);
  }

  if (!env.RESEND_API_KEY || !env.CONTACT_FROM) {
    return json({ ok: false, error: text.offline }, 503);
  }

  const to = env.CONTACT_TO || "alx.voynov@yahoo.com";
  const sent = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: env.CONTACT_FROM,
      to: [to],
      reply_to: email,
      subject: text.subject,
      text: `Email: ${email}\nLanguage: ${body.lang === "en" ? "en" : "bg"}\n\n${message}`,
    }),
  });

  if (!sent.ok) return json({ ok: false, error: text.send }, 502);

  await markSent(ip);
  return json({ ok: true });
}

async function tooSoon(ip) {
  const hit = await caches.default.match(rateRequest(ip));
  return Boolean(hit);
}

async function markSent(ip) {
  await caches.default.put(
    rateRequest(ip),
    new Response("1", { headers: { "Cache-Control": "max-age=60" } }),
  );
}

function rateRequest(ip) {
  return new Request(`https://finishart-rate.local/${encodeURIComponent(ip)}`);
}

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}
