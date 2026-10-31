(function () {
  const input = document.getElementById("message");
  const sendButton = document.getElementById("send-button");
  const chatHistory = document.getElementById("chat-history");

  function appendMessage(role, text) {
    const message = document.createElement("div");
    message.className = role === "user" ? "user-message" : "assistant-message";
    message.textContent = text;
    chatHistory.appendChild(message);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return message;
  }

  async function sendMessage() {
    const text = input.value.trim();
    if (!text || sendButton.disabled) return;

    appendMessage("user", text);
    input.value = "";
    sendButton.disabled = true;
    input.disabled = true;

    const thinking = document.createElement("div");
    thinking.className = "assistant-message thinking";
    thinking.setAttribute("aria-label", "GHOST is thinking");
    thinking.innerHTML = '<span></span><span></span><span></span>';
    chatHistory.appendChild(thinking);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "GHOST could not process that message.");
      appendMessage("assistant", data.reply || "GHOST returned an empty response.");
    } catch (error) {
      appendMessage("assistant", "Unable to reach GHOST: " + (error.message || "Unknown error"));
    } finally {
      thinking.remove();
      sendButton.disabled = false;
      input.disabled = false;
      input.focus();
    }
  }

  sendButton.addEventListener("click", sendMessage);
  input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });
})();