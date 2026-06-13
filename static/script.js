const input = document.getElementById("message");

input.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

async function sendMessage() {
  const chatBox = document.getElementById("chat-box");

  const userMessage = input.value;

  chatBox.innerHTML += `
        <div class = "user-message">
          ${userMessage}
        </div>
    `;

  chatBox.scrollTop = chatBox.scrollHeight;

  chatBox.innerHTML += `
    <p id="thinking">
        <b>GHOST:</b> Thinking...
    </p>
    `;

  chatBox.scrollTop = chatBox.scrollHeight;

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: userMessage,
    }),
  });

  const data = await response.json();

  document.getElementById("thinking").remove();

  chatBox.innerHTML += `
  <div class="ai-message">
  GHOST:
        
  ${data.reply.trim()}

  </div>
  `;

  chatBox.scrollTop = chatBox.scrollHeight;

  input.value = "";
}

async function clearMemory() {
  console.log("Button clicked");

  await fetch("/clear", {
    method: "POST",
  });

  document.getElementById("chat-box").innerHTML = "";

  alert("Memory Cleared");
}

async function uploadPDF() {
  const fileInput = document.getElementById("pdfFile");

  const formData = new FormData();

  formData.append("file", fileInput.files[0]);

  const response = await fetch("/upload-pdf", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  loadDocuments();

  alert(data.message);
}

async function loadDocuments() {

  const response = await fetch("/documents");
  const documents = await response.json();

  console.log(documents);

  const pdfList = document.getElementById("pdf-list");

  pdfList.innerHTML = "";
  documents.forEach((pdf) => {
    pdfList.innerHTML += `
      <div>
        📄 ${pdf}
      </div>
    `;
  });
}

async function loadTasks() {
  const response = await fetch("/tasks");
  const tasks = await response.json();

  const taskList = document.getElementById("task-list");

  taskList.innerHTML = "";
  tasks.forEach((task) => {
    taskList.innerHTML += `
    <div class = "task-item">
    
      <input
          type = "checkbox"
          ${task.completed ? "checked" : ""}
          onchange = "completeTask(${task.id})"
      >
      ${task.task}

      <button onclick = "deleteTask(${task.id})">
        🗑
      </button>
    </div>
    `;
  });
}

loadTasks();

async function addTask() {
  const taskInput = document.getElementById("task-input");
  const taskText = taskInput.value;

  if (taskText === "") {
    alert("Please enter a task");
    return;
  }

  const response = await fetch("/add-task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      task: taskText,
    }),
  });

  const data = await response.json();
  console.log(data);

  loadTasks();
  taskInput.value = "";
}

async function completeTask(id) {
  const response = await fetch("/complete-task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
    }),
  });

  const data = await response.json();
  console.log(data);
  loadTasks();
}

async function deleteTask(id) {
  const response = await fetch("/delete-task", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
    }),
  });

  const data = await response.json();
  console.log(data);
}
loadTasks();
loadDocuments();
