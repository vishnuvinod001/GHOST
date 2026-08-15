//--------------------------------------------------------------
// Overview Page HTML
//--------------------------------------------------------------

const overviewHTML = `
    <div class="overview">

                    <section class="hero-card">

                        <h1>Good Evening, Vishnu</h1>

                        <p>
                            Welcome back to GHOST.
                        </p>

                        <div class="daily-brief">

                            <h3>Today's Brief</h3>

                            <ul>
                                <li>Browser MCP operational</li>
                                <li>Filesystem MCP operational</li>
                                <li>43 documents indexed</li>
                                <li>2 active MCP tools</li>
                            </ul>

                        </div>

                    </section>

                    <section class="stats-grid">

                        <div class="card">
                            <h3>Documents</h3>
                            <p>43</p>
                        </div>

                        <div class="card">
                            <h3>Memories</h3>
                            <p>112</p>
                        </div>

                        <div class="card">
                            <h3>Projects</h3>
                            <p>4</p>
                        </div>

                        <div class="card">
                            <h3>Tools</h3>
                            <p>2</p>
                        </div>

                    </section>

                    <section class="recent-activity card">

                        <h2>Recent Activity</h2>

                        <ul>
                            <li>Browser MCP completed</li>
                            <li>Filesystem MCP completed</li>
                            <li>3 documents uploaded</li>
                            <li>Memory updated</li>
                        </ul>

                    </section>

                    <section class="system-status card">

                        <h2>System Status</h2>

                        <ul>
                            <li>Qwen3 8B - Online</li>
                            <li>Router - Online</li>
                            <li>ChromaDB - Online</li>
                            <li>Filesystem MCP - Online</li>
                        </ul>

                    </section>

                </div>
`;

//--------------------------------------------------------------
// Knowledge Page HTML
//--------------------------------------------------------------

const knowledgeHTML = `

<div class="knowledge-page">

    <section class="knowledge-header">

        <h1>Knowledge Base</h1>

        <p>
            Documents, embeddings, chunks and indexed knowledge.
        </p>

    </section>

    <section class="knowledge-stats">

        <div class="card">
            <h3>Documents</h3>
            <p>43</p>
        </div>

        <div class="card">
            <h3>Chunks</h3>
            <p>159</p>
        </div>

        <div class="card">
            <h3>Embeddings</h3>
            <p>159</p>
        </div>

        <div class="card">
            <h3>Status</h3>
            <p>Ready</p>
        </div>

    </section>

    <section class="card">

        <h2>Recent Documents</h2>

        <ul>
            <li>research_paper.pdf</li>
            <li>machine_learning_notes.pdf</li>
            <li>llm_architecture.pdf</li>
        </ul>

    </section>

    <section class="card">

        <h2>Knowledge Status</h2>

        <ul>
            <li>Vector Store Active</li>
            <li>Embeddings Loaded</li>
            <li>Search Available</li>
        </ul>

    </section>

</div>

`;

//--------------------------------------------------------------
// Files Page HTML
//--------------------------------------------------------------

const filesHTML = `

<div class="files-page">

    <section class="files-header">

        <h1>Files</h1>

        <p>
            Browse and manage files using Filesystem MCP.
        </p>

    </section>

    <section class="files-stats">

        <div class="card">
            <h3>Total Files</h3>
            <p>124</p>
        </div>

        <div class="card">
            <h3>Folders</h3>
            <p>18</p>
        </div>

        <div class="card">
            <h3>Recent Changes</h3>
            <p>12</p>
        </div>

        <div class="card">
            <h3>Status</h3>
            <p>Ready</p>
        </div>

    </section>

    <section class="card">

        <h2>Recent Files</h2>

        <ul>
            <li>main.py</li>
            <li>knowledge.db</li>
            <li>notes.md</li>
        </ul>

    </section>

    <section class="card">

        <h2>Filesystem MCP</h2>

        <ul>
            <li>Read File</li>
            <li>Create File</li>
            <li>Edit File</li>
            <li>Delete File</li>
            <li>Search Files</li>
        </ul>

    </section>

</div>

`;

//--------------------------------------------------------------
// Tasks Page HTML
//--------------------------------------------------------------

const tasksHTML = `

<div class="tasks-page">

    <section class="tasks-header">

        <h1>Tasks</h1>

        <p>
            Projects, todos, deadlines and automations.
        </p>

    </section>

    <section class="tasks-stats">

        <div class="card">
            <h3>Total Tasks</h3>
            <p>18</p>
        </div>

        <div class="card">
            <h3>Active</h3>
            <p>7</p>
        </div>

        <div class="card">
            <h3>Completed</h3>
            <p>11</p>
        </div>

        <div class="card">
            <h3>Overdue</h3>
            <p>0</p>
        </div>

    </section>

    <section class="card">

        <h2>Current Tasks</h2>

        <ul>
            <li>Build Brain Page</li>
            <li>Build Developer Page</li>
            <li>Reconnect Chat</li>
            <li>Connect Knowledge Backend</li>
        </ul>

    </section>

    <section class="card">

        <h2>Upcoming Tasks</h2>

        <ul>
            <li>GitHub MCP</li>
            <li>Terminal MCP</li>
            <li>Voice Integration</li>
            <li>Knowledge Graph</li>
        </ul>

    </section>

</div>

`;

//--------------------------------------------------------------
// Brain Page HTML
//--------------------------------------------------------------

const brainHTML = `

<div class="brain-page">

    <section class="brain-header">

        <h1>Brain</h1>

        <p>
            Memory, learning, projects and knowledge evolution.
        </p>

    </section>

    <section class="brain-stats">

        <div class="card">
            <h3>Memories</h3>
            <p>112</p>
        </div>

        <div class="card">
            <h3>Projects</h3>
            <p>4</p>
        </div>

        <div class="card">
            <h3>Concepts</h3>
            <p>27</p>
        </div>

        <div class="card">
            <h3>Skills</h3>
            <p>15</p>
        </div>

    </section>

    <section class="card">

        <h2>Recent Memories</h2>

        <ul>
            <li>Filesystem MCP completed</li>
            <li>Knowledge Base expanded</li>
            <li>UI v2 development started</li>
        </ul>

    </section>

    <section class="card">

        <h2>Timeline</h2>

        <ul>
            <li>Browser MCP completed</li>
            <li>Filesystem MCP completed</li>
            <li>Knowledge dashboard created</li>
        </ul>

    </section>

</div>

`;

//--------------------------------------------------------------
// Developer Page HTML
//--------------------------------------------------------------

const developerHTML = `

<div class="developer-page">

    <section class="developer-header">

        <h1>Developer</h1>

        <p>
            System diagnostics, MCP activity and model statistics.
        </p>

    </section>

    <section class="developer-stats">

        <div class="card">
            <h3>Tool Calls</h3>
            <p>124</p>
        </div>

        <div class="card">
            <h3>MCP Servers</h3>
            <p>2</p>
        </div>

        <div class="card">
            <h3>Response Time</h3>
            <p>1.2s</p>
        </div>

        <div class="card">
            <h3>Status</h3>
            <p>Online</p>
        </div>

    </section>

    <section class="card">

        <h2>Recent Activity</h2>

        <ul>
            <li>Browser MCP executed</li>
            <li>Filesystem MCP executed</li>
            <li>Knowledge search completed</li>
        </ul>

    </section>

    <section class="card">

        <h2>System Logs</h2>

        <ul>
            <li>Router active</li>
            <li>Qwen3 8B loaded</li>
            <li>ChromaDB connected</li>
        </ul>

    </section>

</div>

`;

//--------------------------------------------------------------
// Settings Page HTML
//--------------------------------------------------------------

const settingsHTML = `

<div class="settings-page">

    <section class="settings-header">

        <h1>Settings</h1>

        <p>
            Configure models, memory and system behavior.
        </p>

    </section>

    <section class="settings-grid">

        <div class="card">
            <h3>Model</h3>
            <p>Qwen3 8B</p>
        </div>

        <div class="card">
            <h3>Router</h3>
            <p>Qwen3 0.6B</p>
        </div>

        <div class="card">
            <h3>Memory</h3>
            <p>Enabled</p>
        </div>

        <div class="card">
            <h3>MCP</h3>
            <p>Enabled</p>
        </div>

    </section>

    <section class="card">

        <h2>Available Features</h2>

        <ul>
            <li>Memory</li>
            <li>Knowledge Base</li>
            <li>Filesystem MCP</li>
            <li>Browser MCP</li>
        </ul>

    </section>

</div>

`;
