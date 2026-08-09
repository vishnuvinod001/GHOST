const pageContent = document.getElementById("page-content");

const navButtons = document.querySelectorAll(".nav-button");

const pages = {
  overview: `
        <div class="overview">
            <h1>Overview</h1>
            <p>Welcome back to GHOST.</p>
        </div>
    `,

  knowledge: `
        <div>
            <h1>Knowledge</h1>
            <p>Knowledge Base Dashboard</p>
        </div>
    `,

  files: `
        <div>
            <h1>Files</h1>
            <p>Filesystem MCP Interface</p>
        </div>
    `,

  tasks: `
        <div>
            <h1>Tasks</h1>
            <p>Task Management System</p>
        </div>
    `,

  brain: `
        <div>
            <h1>Brain</h1>
            <p>Memory and Knowledge Graph</p>
        </div>
    `,

  developer: `
        <div>
            <h1>Developer</h1>
            <p>System Diagnostics</p>
        </div>
    `,

  settings: `
        <div>
            <h1>Settings</h1>
            <p>Configuration Center</p>
        </div>
    `,
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