const input = document.getElementById("message");
const sendButton = document.getElementById("send-button");
const chatHistory = document.getElementById("chat-history");

sendButton.addEventListener("click", sendMessage);

input.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

// Debug
console.log(document.getElementById("message"));
console.log(document.getElementById("send-button"));
console.log(document.getElementById("chat-history"));

// Function to send the message to the server and display the response

async function sendMessage() {
  const message = input.value.trim();

  if (!message) return;

  chatHistory.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

  input.value = "";

  chatHistory.innerHTML += `
        <div id="thinking">
            Ghost is thinking...
        </div>
    `;

  const response = await fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: message,
    }),
  });

  const data = await response.json();

  document.getElementById("thinking").remove();

  chatHistory.innerHTML += `
        <div class = "assistant-message">
            ${data.reply}
        </div>
    `;

  chatHistory.scrollTop = chatHistory.scrollHeight;
}
