(function () {
  const pageContent = document.getElementById("page-content");
  const pageTitle = document.getElementById("current-page-title");
  const navButtons = Array.from(document.querySelectorAll(".nav-button"));
  let currentPage = "overview";

  const titles = {
    overview: "Overview",
    knowledge: "Knowledge",
    files: "Files",
    tasks: "Tasks",
    brain: "Brain",
    developer: "Developer",
    settings: "Settings"
  };

  async function loadPage(page) {
    if (!window.GhostPages || typeof window.GhostPages[page] !== "function") {
      pageContent.innerHTML = window.GhostUI.errorPanel(new Error("This page module could not be loaded."));
      return;
    }
    currentPage = page;
    pageTitle.textContent = titles[page] || "GHOST";
    navButtons.forEach(function (button) {
      const active = button.dataset.page === page;
      button.classList.toggle("active", active);
      button.setAttribute("aria-current", active ? "page" : "false");
    });
    pageContent.setAttribute("aria-busy", "true");
    pageContent.innerHTML = '<div class="loading-state">Loading workspace data…</div>';
    try {
      pageContent.innerHTML = await window.GhostPages[page]();
      observeMotionBlocks();
    } finally {
      pageContent.setAttribute("aria-busy", "false");
    }
  }

  function observeMotionBlocks() {
    const blocks = pageContent.querySelectorAll(".motion-block");
    if (!("IntersectionObserver" in window)) {
      blocks.forEach(function (block) { block.classList.add("is-visible"); });
      return;
    }
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    blocks.forEach(function (block) { observer.observe(block); });
  }

  navButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      loadPage(button.dataset.page);
    });
  });

  pageContent.addEventListener("click", async function (event) {
    const button = event.target.closest("[data-action]");
    if (!button) return;
    const action = button.dataset.action;
    try {
      if (action === "delete-task") {
        if (!window.confirm("Delete this task?")) return;
        await window.GhostAPI.post("/delete-task", { id: Number(button.dataset.id) });
      } else if (action === "delete-document") {
        const filename = button.dataset.filename;
        if (!window.confirm("Delete " + filename + " from the knowledge base?")) return;
        await window.GhostAPI.post("/delete-document?filename=" + encodeURIComponent(filename));
      } else if (action === "refresh-page") {
        await loadPage(currentPage);
        return;
      } else {
        return;
      }
      await loadPage(currentPage);
    } catch (error) {
      window.alert(error.message || "The requested action failed.");
    }
  });

  pageContent.addEventListener("change", async function (event) {
    const input = event.target.closest('[data-action="complete-task"]');
    if (!input) return;
    try {
      await window.GhostAPI.post("/complete-task", { id: Number(input.dataset.id) });
      await loadPage(currentPage);
    } catch (error) {
      window.alert(error.message || "Unable to update the task.");
      await loadPage(currentPage);
    }
  });

  pageContent.addEventListener("submit", async function (event) {
    const form = event.target;
    if (form.id !== "task-form" && form.id !== "pdf-upload-form") return;
    event.preventDefault();
    const submit = form.querySelector('button[type="submit"]');
    submit.disabled = true;
    try {
      if (form.id === "task-form") {
        const value = new FormData(form).get("task");
        await window.GhostAPI.post("/add-task", { task: String(value || "").trim() });
      } else {
        const file = new FormData(form).get("file");
        if (!file || !file.name) throw new Error("Choose a PDF file first.");
        const formData = new FormData();
        formData.append("file", file);
        await window.GhostAPI.upload("/upload-pdf", formData);
      }
      await loadPage(currentPage);
    } catch (error) {
      window.alert(error.message || "The request failed.");
      submit.disabled = false;
    }
  });

  window.GhostNavigation = { loadPage: loadPage };
  loadPage("overview");
})();