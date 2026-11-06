
const chatArea = document.getElementById("chatArea");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const welcomeMessage = document.getElementById("welcomeMessage");

let messages = [];
let isLoading = false;


// Create chat bubble safely
function addMessage(role, content) {

    const message = document.createElement("div");
    message.className = `message ${role}`;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = role === "user" ? "U" : "⚡";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = role === "user" ? "YOU" : "SIGMA";

    const text = document.createElement("div");
    text.textContent = content;

    bubble.appendChild(label);
    bubble.appendChild(text);

    message.appendChild(avatar);
    message.appendChild(bubble);

    chatArea.appendChild(message);

    chatArea.scrollTop = chatArea.scrollHeight;

    return message;
}


// Typing animation
function showTyping() {

    const wrapper = document.createElement("div");
    wrapper.className = "message assistant";
    wrapper.id = "typingIndicator";

    wrapper.innerHTML = `
        <div class="avatar">⚡</div>
        <div class="bubble">
            <div class="message-label">SIGMA IS THINKING</div>
            <div class="typing">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;

    chatArea.appendChild(wrapper);
    chatArea.scrollTop = chatArea.scrollHeight;
}


// Send message
async function sendMessage(text) {

    text = text.trim();

    if (!text || isLoading) return;

    if (welcomeMessage) {
        welcomeMessage.style.display = "none";
    }

    isLoading = true;
    sendBtn.disabled = true;

    addMessage("user", text);

    messages.push({
        role: "user",
        content: text
    });

    userInput.value = "";
    userInput.style.height = "auto";

    showTyping();

    try {

        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: messages
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        document.getElementById("typingIndicator")?.remove();

        const answer = data.reply;

        addMessage("assistant", answer);

        messages.push({
            role: "assistant",
            content: answer
        });

    } catch (error) {

        document.getElementById("typingIndicator")?.remove();

        addMessage(
            "assistant",
            "SIGMA ERROR: " + error.message
        );

        // Remove failed user request from conversation history
        messages.pop();

    } finally {

        isLoading = false;
        sendBtn.disabled = false;
        userInput.focus();

    }
}


// Send button
sendBtn.addEventListener("click", () => {
    sendMessage(userInput.value);
});


// Enter to send, Shift + Enter for new line
userInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage(userInput.value);
    }

});


// Auto resize textarea
userInput.addEventListener("input", () => {

    userInput.style.height = "auto";

    userInput.style.height =
        Math.min(userInput.scrollHeight, 120) + "px";

});


// Clear conversation
clearBtn.addEventListener("click", () => {

    messages = [];

    chatArea.innerHTML = `
        <div class="welcome-message" id="welcomeMessage">
            <div class="welcome-tag">YOUR PERSONAL REALITY CHECK</div>
            <h3>WHAT'S ON YOUR MIND?</h3>
            <p>Go ahead. Ask something.</p>

            <div class="suggestions">
                <button class="suggestion" data-prompt="Roast my lifestyle.">Roast my lifestyle</button>
                <button class="suggestion" data-prompt="Am I wasting my potential?">Reality check</button>
                <button class="suggestion" data-prompt="Tell me why my excuses are pathetic.">Expose my excuses</button>
            </div>
        </div>
    `;

});


// Suggested prompts
chatArea.addEventListener("click", (event) => {

    const button = event.target.closest(".suggestion");

    if (!button) return;

    const prompt = button.dataset.prompt;

    sendMessage(prompt);

});
