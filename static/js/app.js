const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const messages = document.querySelector("#messages");
const sendButton = document.querySelector("#send-button");

function addMessage(text, kind) {
  const item = document.createElement("div");
  item.className = `message ${kind}-message`;
  item.textContent = text;
  messages.appendChild(item);
  messages.scrollTop = messages.scrollHeight;
  return item;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message || sendButton.disabled) return;

  addMessage(message, "user");
  input.value = "";
  sendButton.disabled = true;
  sendButton.textContent = "Thinking…";
  const pending = addMessage("Checking your question and preparing a response…", "assistant");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    pending.textContent = data.answer || "No response was returned.";
  } catch (error) {
    pending.textContent = "Unable to reach the local server. Check that the Flask application is running.";
  } finally {
    sendButton.disabled = false;
    sendButton.innerHTML = 'Send <span aria-hidden="true">↗</span>';
    input.focus();
    messages.scrollTop = messages.scrollHeight;
  }
});
