import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const store = new Map();
globalThis.caches = {
  default: {
    async match(request) {
      const hit = store.get(request.url);
      if (!hit || hit.expires < Date.now()) return undefined;
      return hit.response;
    },
    async put(request, response) {
      const age = Number((response.headers.get("cache-control") || "").match(/max-age=(\d+)/)?.[1] || 0);
      store.set(request.url, { expires: Date.now() + age * 1000, response });
    },
  },
};

const { default: worker } = await import("../src/worker.js");
const publicDir = join(dirname(fileURLToPath(import.meta.url)), "..", "public");
const CANONICAL = "https://finishart.bg";

const assets = {
  async fetch(request) {
    const url = new URL(request.url);
    const type = url.pathname.startsWith("/assets/")
      ? "image/jpeg"
      : url.pathname.startsWith("/css/")
        ? "text/css"
        : "text/html; charset=utf-8";
    return new Response("ok", { status: 200, headers: { "content-type": type } });
  },
};

const failures = [];

function fail(message) {
  failures.push(message);
}

async function hit(url, init = {}) {
  const response = await worker.fetch(new Request(url, init), { ASSETS: assets });
  return {
    status: response.status,
    location: response.headers.get("location"),
    cache: response.headers.get("cache-control"),
    cookie: response.headers.get("set-cookie"),
    body: await response.text(),
  };
}

// The Worker must not change hostnames. www → https://finishart.bg is the
// Cloudflare Redirect Rule; an apex → www redirect here would loop with it.
for (const host of ["finishart.bg", "www.finishart.bg"]) {
  const origin = `https://${host}`;

  const root = await hit(`${origin}/`);
  if (root.status !== 302 || root.location !== `${origin}/bg`) {
    fail(`${host} root redirect ${root.status} ${root.location}`);
  }

  const english = await hit(`${origin}/`, {
    headers: { cookie: "finishart-lang=en" },
  });
  if (english.status !== 302 || english.location !== `${origin}/en`) {
    fail(`${host} language cookie redirect ${english.status} ${english.location}`);
  }

  const bulgarian = await hit(`${origin}/bg`);
  if (bulgarian.status !== 200 || bulgarian.location) {
    fail(`${host} /bg ${bulgarian.status} ${bulgarian.location}`);
  }

  const englishPage = await hit(`${origin}/en`);
  if (englishPage.status !== 200 || englishPage.location) {
    fail(`${host} /en ${englishPage.status} ${englishPage.location}`);
  }

  const portfolio = await hit(`${origin}/bg/portfolio`);
  if (portfolio.status !== 200 || portfolio.location) {
    fail(`${host} /bg/portfolio ${portfolio.status} ${portfolio.location}`);
  }

  const oldPortfolio = await hit(`${origin}/portfolio`);
  if (oldPortfolio.status !== 301 || oldPortfolio.location !== `${origin}/bg/portfolio`) {
    fail(`${host} old portfolio ${oldPortfolio.status} ${oldPortfolio.location}`);
  }

  const cleared = await hit(`${origin}/en/portfolio?forget-lang=1`);
  if (cleared.status !== 303 || cleared.location !== `${origin}/en/portfolio?lang-cleared=1`) {
    fail(`${host} forget redirect ${cleared.status} ${cleared.location}`);
  }

  const landed = await hit(root.location);
  if (landed.status !== 200 || landed.location) {
    fail(`${host} root target ${landed.status} ${landed.location}`);
  }
}

const oldProject = await hit(
  "https://finishart.bg/portfolio-collections/%D0%B1%D0%B0%D0%BD%D1%8F-%D0%B8-%D1%82%D0%BE%D0%B0%D0%BB%D0%B5%D1%82%D0%BD%D0%B0/%D1%80%D0%B5%D0%BD%D0%BE%D0%B2%D0%B0%D1%86%D0%B8%D1%8F-%D0%BD%D0%B0-%D0%B1%D0%B0%D0%BD%D1%8F-%D1%81%D0%BE%D1%84%D0%B8%D1%8F",
);
if (
  oldProject.status !== 301 ||
  oldProject.location !== "https://finishart.bg/bg/portfolio/bathrooms/sofia-bathroom-renovation"
) {
  fail(`old bathroom project ${oldProject.status} ${oldProject.location}`);
}

let hopped = "https://finishart.bg/bg";
for (let i = 0; i < 4; i++) {
  const step = await hit(hopped);
  if (step.status < 300 || step.status >= 400 || !step.location) {
    if (step.status !== 200 || hopped !== "https://finishart.bg/bg") {
      fail(`apex /bg chain ended ${step.status} at ${hopped}`);
    }
    hopped = "";
    break;
  }
  if (new URL(step.location).hostname !== "finishart.bg") {
    fail(`apex /bg redirected to ${step.location}`);
  }
  hopped = step.location;
}
if (hopped) fail(`apex /bg did not settle ${hopped}`);

const page = await hit("https://finishart.bg/bg");
if (page.status !== 200 || page.cache !== "public, max-age=300") {
  fail(`html cache ${page.status} ${page.cache}`);
}

const image = await hit("https://finishart.bg/assets/painted-interior-tall-windows.jpg");
if (image.status !== 200 || image.cache !== "public, max-age=2592000") {
  fail(`image cache ${image.status} ${image.cache}`);
}

const bad = await hit("https://finishart.bg/api/contact", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ email: "not-an-email", message: "hello", lang: "en" }),
});
if (bad.status !== 400 || bad.location || !bad.body.includes("valid email")) {
  fail(`contact validation ${bad.status} ${bad.location} ${bad.body}`);
}

const offline = await hit("https://finishart.bg/api/contact", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ email: "a@b.co", message: "Need a quote", lang: "bg" }),
});
if (offline.status !== 503 || offline.location || !offline.body.includes("0882 820025")) {
  fail(`contact offline ${offline.status} ${offline.location} ${offline.body}`);
}

const cleared = await hit("https://finishart.bg/en/portfolio?forget-lang=1");
if (!cleared.cookie || !cleared.cookie.includes("Max-Age=0")) {
  fail(`forget cookie ${cleared.cookie}`);
}

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) walk(path, out);
    else if (/\.(html|xml|txt)$/.test(name)) out.push(path);
  }
  return out;
}

for (const path of walk(publicDir)) {
  const text = readFileSync(path, "utf8");
  if (text.includes("www.finishart.bg")) fail(`www host still published in ${path}`);
}

const bgHome = readFileSync(join(publicDir, "bg", "index.html"), "utf8");
const enHome = readFileSync(join(publicDir, "en", "index.html"), "utf8");
for (const [name, html, path] of [
  ["bg", bgHome, "/bg"],
  ["en", enHome, "/en"],
]) {
  if (!html.includes(`<link rel="canonical" href="${CANONICAL}${path}">`)) {
    fail(`${name} canonical`);
  }
  if (!html.includes(`<meta property="og:url" content="${CANONICAL}${path}">`)) {
    fail(`${name} og:url`);
  }
  if (!html.includes(`hreflang="bg" href="${CANONICAL}/bg"`)) fail(`${name} hreflang bg`);
  if (!html.includes(`hreflang="en" href="${CANONICAL}/en"`)) fail(`${name} hreflang en`);
  if (!html.includes(`hreflang="x-default" href="${CANONICAL}/bg"`)) fail(`${name} hreflang default`);
}

const sitemap = readFileSync(join(publicDir, "sitemap.xml"), "utf8");
if (!sitemap.includes(`<loc>${CANONICAL}/bg</loc>`) || !sitemap.includes(`<loc>${CANONICAL}/en</loc>`)) {
  fail("sitemap language locs");
}
const robots = readFileSync(join(publicDir, "robots.txt"), "utf8");
if (!robots.includes(`Sitemap: ${CANONICAL}/sitemap.xml`)) fail(`robots sitemap ${robots}`);

if (failures.length) {
  console.log("FAILED");
  for (const item of failures) console.log("-", item);
  process.exit(1);
}
console.log("worker ok");
