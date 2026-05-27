/* ELEMENTS */

const aiButton = document.getElementById("aiButton");

const chatWindow = document.getElementById("chatWindow");

const closeChat = document.getElementById("closeChat");

const sendBtn = document.getElementById("sendBtn");

const chatInput = document.getElementById("chatInput");

const chatBody = document.getElementById("chatBody");

/* OPEN CHAT */

aiButton.addEventListener("click", () => {
  chatWindow.style.display = "flex";
});

/* CLOSE CHAT */

closeChat.addEventListener("click", () => {
  chatWindow.style.display = "none";
});

/* CREATE MESSAGE */

function createMessage(message, type) {
  const div = document.createElement("div");

  div.className = type === "user" ? "user-message" : "bot-message";

  div.innerText = message;

  chatBody.appendChild(div);

  chatBody.scrollTop = chatBody.scrollHeight;
}

/* TYPING INDICATOR */

function createTyping() {
  const div = document.createElement("div");

  div.className = "bot-message";

  div.id = "typing";

  div.innerHTML = `
Thinking...
`;

  chatBody.appendChild(div);

  chatBody.scrollTop = chatBody.scrollHeight;
}

/* REMOVE TYPING */

function removeTyping() {
  const typing = document.getElementById("typing");

  if (typing) {
    typing.remove();
  }
}

/* SEND MESSAGE */

async function sendMessage() {
  const message = chatInput.value.trim();

  if (!message) return;

  /* USER MESSAGE */

  createMessage(message, "user");

  chatInput.value = "";

  /* SHOW TYPING */

  createTyping();

  try {
    const response = await fetch(
      "https://lahari-portfolio-backend.onrender.com/chat",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          message: message,
        }),
      },
    );

    const data = await response.json();

    /* REMOVE TYPING */

    removeTyping();

    /* BOT RESPONSE */

    createMessage(data.reply, "bot");
  } catch (error) {
    removeTyping();

    createMessage("Unable to connect to AI backend.", "bot");

    console.log(error);
  }
}

/* BUTTON CLICK */

sendBtn.addEventListener("click", sendMessage);

/* ENTER KEY */

chatInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});
