const BROKEN = "/portfolio-collections/\u0430\u043f\u0430\u0440\u0442\u0430\ufffd\u043c\u0435\u043d\u0442\u0438";
const CLEAN = "/portfolio-collections/\u0430\u043f\u0430\u0440\u0442\u0430\u043c\u0435\u043d\u0442\u0438";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/contact") {
      if (request.method !== "POST") {
        return json({ ok: false, error: "Методът не е позволен." }, 405);
      }
      return handleContact(request, env);
    }

    let path = url.pathname;
    try {
      path = decodeURIComponent(url.pathname);
    } catch {
      path = url.pathname;
    }
    if (path === BROKEN || path.startsWith(BROKEN + "/")) {
      const target = new URL(request.url);
      target.pathname = path.replace(BROKEN, CLEAN);
      return Response.redirect(target.toString(), 301);
    }

    return env.ASSETS.fetch(request);
  },
};

async function handleContact(request, env) {
  const ip = request.headers.get("cf-connecting-ip") || "unknown";
  if (await tooSoon(ip)) {
    return json({ ok: false, error: "Моля, изчакайте малко преди ново запитване." }, 429);
  }

  let body;
  try {
    const raw = await request.text();
    if (raw.length > 20000) {
      return json({ ok: false, error: "Запитването е твърде дълго." }, 400);
    }
    body = JSON.parse(raw);
  } catch {
    return json({ ok: false, error: "Невалидни данни." }, 400);
  }

  const website = String(body.website || "");
  if (website) return json({ ok: true });

  const email = String(body.email || "").trim();
  const message = String(body.message || "").trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 200) {
    return json({ ok: false, error: "Въведете валиден имейл." }, 400);
  }
  if (message.length < 2 || message.length > 5000) {
    return json({ ok: false, error: "Напишете запитване между 2 и 5000 знака." }, 400);
  }

  if (!env.RESEND_API_KEY || !env.CONTACT_FROM) {
    return json(
      {
        ok: false,
        error: "Формата още не е свързана с поща. Обадете се на 0882 820025 или пишете на alex.finishart@gmail.com.",
      },
      503,
    );
  }

  const to = env.CONTACT_TO || "alex.finishart@gmail.com";
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
      subject: "Запитване от finishart.bg",
      text: `Имейл: ${email}\n\n${message}`,
    }),
  });

  if (!sent.ok) {
    return json({ ok: false, error: "Съобщението не беше доставено. Опитайте отново или се обадете." }, 502);
  }

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
