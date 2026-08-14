const pageContent = document.getElementById("page-content");

const navButtons = document.querySelectorAll(".nav-button");

const pages = {
  overview: overviewHTML,
  knowledge: knowledgeHTML,
  files: filesHTML,
  tasks: tasksHTML,
  brain: brainHTML,
  developer: developerHTML,
  settings: settingsHTML,
};

navButtons.forEach(button => {
    button.addEventListener("click", () => {

        navButtons.forEach(btn => {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        const page = button.dataset.page;

        pageContent.innerHTML = pages[page];
    });
});

pageContent.innerHTML = overviewHTML;