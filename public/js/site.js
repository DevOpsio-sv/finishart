(function () {
  const menuBtn = document.querySelector("[data-menu]");
  const panel = document.querySelector("[data-panel]");
  const closeBtn = document.querySelector("[data-close]");

  function setMenu(open) {
    if (!panel || !menuBtn) return;
    panel.hidden = !open;
    menuBtn.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("menu-open", open);
    if (open && closeBtn) closeBtn.focus();
  }

  if (menuBtn && panel) {
    menuBtn.addEventListener("click", function () {
      setMenu(panel.hidden);
    });
    closeBtn.addEventListener("click", function () {
      setMenu(false);
      menuBtn.focus();
    });
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setMenu(false);
      });
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !panel.hidden) {
        setMenu(false);
        menuBtn.focus();
      }
    });
  }

  const slides = Array.from(document.querySelectorAll("[data-slide]"));
  const dots = Array.from(document.querySelectorAll("[data-dot]"));
  let index = 0;

  function show(next) {
    if (!slides.length) return;
    index = (next + slides.length) % slides.length;
    slides.forEach(function (slide, i) {
      slide.classList.toggle("is-active", i === index);
    });
    dots.forEach(function (dot, i) {
      dot.setAttribute("aria-selected", String(i === index));
    });
  }

  document.querySelectorAll("[data-dir]").forEach(function (button) {
    button.addEventListener("click", function () {
      show(index + Number(button.getAttribute("data-dir")));
    });
  });
  dots.forEach(function (dot, i) {
    dot.addEventListener("click", function () {
      show(i);
    });
  });

  const form = document.querySelector("[data-contact]");
  if (form) {
    const status = form.querySelector("[data-status]");
    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      const data = new FormData(form);
      const email = String(data.get("email") || "").trim();
      const message = String(data.get("message") || "").trim();
      const website = String(data.get("website") || "");
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        status.textContent = "Въведете валиден имейл.";
        status.className = "form-status is-error";
        return;
      }
      if (message.length < 2) {
        status.textContent = "Напишете запитването си.";
        status.className = "form-status is-error";
        return;
      }
      const submit = form.querySelector("[type=submit]");
      submit.disabled = true;
      status.className = "form-status";
      status.textContent = "Изпращане…";
      try {
        const response = await fetch("/api/contact", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: email, message: message, website: website }),
        });
        const payload = await response.json().catch(function () {
          return {};
        });
        if (!response.ok || !payload.ok) {
          throw new Error(payload.error || "Запитването не беше изпратено.");
        }
        form.reset();
        status.className = "form-status";
        status.textContent = "Запитването е изпратено. Ще се свържем с вас.";
      } catch (error) {
        status.className = "form-status is-error";
        status.textContent =
          error.message ||
          "В момента формата не може да се изпрати. Обадете се на 0882 820025.";
      } finally {
        submit.disabled = false;
      }
    });
  }

  const dialog = document.querySelector("dialog.lightbox");
  if (dialog) {
    document.querySelectorAll("[data-zoom]").forEach(function (image) {
      image.addEventListener("click", function () {
        const full = dialog.querySelector("img");
        full.src = image.currentSrc || image.src;
        full.alt = image.alt;
        dialog.showModal();
      });
    });
  }
})();
