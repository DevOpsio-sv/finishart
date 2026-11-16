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

const root = await hit("https://www.finishart.bg/");
if (root.status !== 302 || root.location !== "https://www.finishart.bg/bg") {
  fail(`root redirect ${root.status} ${root.location}`);
}

const english = await hit("https://www.finishart.bg/", {
  headers: { cookie: "finishart-lang=en" },
});
if (english.status !== 302 || english.location !== "https://www.finishart.bg/en") {
  fail(`language cookie redirect ${english.status} ${english.location}`);
}

const apex = await hit("https://finishart.bg/bg/portfolio");
if (apex.status !== 301 || apex.location !== "https://www.finishart.bg/bg/portfolio") {
  fail(`apex redirect ${apex.status} ${apex.location}`);
}

const oldPortfolio = await hit("https://www.finishart.bg/portfolio");
if (oldPortfolio.status !== 301 || oldPortfolio.location !== "https://www.finishart.bg/bg/portfolio") {
  fail(`old portfolio ${oldPortfolio.status} ${oldPortfolio.location}`);
}

const oldProject = await hit(
  "https://www.finishart.bg/portfolio-collections/%D0%B1%D0%B0%D0%BD%D1%8F-%D0%B8-%D1%82%D0%BE%D0%B0%D0%BB%D0%B5%D1%82%D0%BD%D0%B0/%D1%80%D0%B5%D0%BD%D0%BE%D0%B2%D0%B0%D1%86%D0%B8%D1%8F-%D0%BD%D0%B0-%D0%B1%D0%B0%D0%BD%D1%8F-%D1%81%D0%BE%D1%84%D0%B8%D1%8F",
);
if (
  oldProject.status !== 301 ||
  oldProject.location !== "https://www.finishart.bg/bg/portfolio/bathrooms/sofia-bathroom-renovation"
) {
  fail(`old bathroom project ${oldProject.status} ${oldProject.location}`);
}

const page = await hit("https://www.finishart.bg/bg");
if (page.status !== 200 || page.cache !== "public, max-age=300") {
  fail(`html cache ${page.status} ${page.cache}`);
}

const image = await hit("https://www.finishart.bg/assets/painted-interior-tall-windows.jpg");
if (image.status !== 200 || image.cache !== "public, max-age=2592000") {
  fail(`image cache ${image.status} ${image.cache}`);
}

const bad = await hit("https://www.finishart.bg/api/contact", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ email: "not-an-email", message: "hello", lang: "en" }),
});
if (bad.status !== 400 || !bad.body.includes("valid email")) {
  fail(`contact validation ${bad.status} ${bad.body}`);
}

const offline = await hit("https://www.finishart.bg/api/contact", {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({ email: "a@b.co", message: "Need a quote", lang: "bg" }),
});
if (offline.status !== 503 || !offline.body.includes("0882 820025")) {
  fail(`contact offline ${offline.status} ${offline.body}`);
}

const cleared = await hit("https://www.finishart.bg/en/portfolio?forget-lang=1");
if (cleared.status !== 303 || !cleared.location.endsWith("/en/portfolio?lang-cleared=1")) {
  fail(`forget redirect ${cleared.status} ${cleared.location}`);
}
if (!cleared.cookie || !cleared.cookie.includes("Max-Age=0")) {
  fail(`forget cookie ${cleared.cookie}`);
}

if (failures.length) {
  console.log("FAILED");
  for (const item of failures) console.log("-", item);
  process.exit(1);
}
console.log("worker ok");
