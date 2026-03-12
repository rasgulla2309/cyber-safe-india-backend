const API_BASE = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");

/* =========================
   AUTH GUARD
========================= */
if (!token) {
    window.location.href = "index.html";
}

/* =========================
   JWT → USER ID
========================= */
function parseJwt(token) {
    try {
        return JSON.parse(atob(token.split(".")[1]));
    } catch {
        return null;
    }
}

const payload = parseJwt(token);
const userId = payload?.user_id;

if (!userId) {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

/* =========================
   AUTH FETCH (DB BACKUP)
========================= */
async function authFetch(url, options = {}) {
    const res = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
            ...(options.headers || {})
        }
    });

    if (res.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "index.html";
        throw new Error("Unauthorized");
    }

    return res;
}

/* =========================
   WEBSOCKET (REAL-TIME)
========================= */
const ws = new WebSocket(`wss://127.0.0.1:8000/ws/chat/${userId}`);

ws.onopen = () => {
    console.log("🟢 Real-time chat connected");
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    // ignore own echo
    if (data.user_id == userId && data.sender === "user") return;

    if (data.sender === "admin") {
        appendMessage("Admin", data.message);
    }
};

ws.onclose = () => {
    console.log("🔴 Real-time connection closed");
};

/* =========================
   UI HELPERS
========================= */
function appendMessage(sender, message) {
    const box = document.getElementById("chatBox");

    box.innerHTML += `
        <div class="chat ${sender === "You" ? "user-chat" : "admin-chat"}">
            <b>${sender}:</b>
            <div class="${sender === "You" ? "user-msg" : "reply"}">
                ${message}
            </div>
            <div style="font-size:11px;color:#6c757d">
                ${new Date().toLocaleString()}
            </div>
        </div>
    `;

    box.scrollTop = box.scrollHeight;
}

/* =========================
   SEND MESSAGE
========================= */
async function submitChat() {
    const input = document.getElementById("message");
    const message = input.value.trim();

    if (!message) return;

    appendMessage("You", message);

    ws.send(JSON.stringify({
        sender: "user",
        message: message
    }));

    await authFetch(`${API_BASE}/chat/submit`, {
        method: "POST",
        body: JSON.stringify({ message })
    });

    input.value = "";
}

/* =========================
   LOAD OLD CHAT
========================= */
async function loadChats() {
    const res = await authFetch(`${API_BASE}/chat/my-chats`);
    const chats = await res.json();

    const box = document.getElementById("chatBox");
    box.innerHTML = "";

    if (chats.length === 0) {
        box.innerHTML = `
            <div class="chat">
                <b>🤖 Cyber Safe India</b>
                <div class="reply">
                    👋 Hello! Welcome to Cyber Safe India Help Desk.
                </div>
            </div>
        `;
        return;
    }

    chats.forEach(chat => {
        appendMessage(
            chat.sender === "user" ? "You" : "Admin",
            chat.message
        );
    });
}

async function clearChat() {
    if (!confirm("Clear entire chat?")) return;

    await authFetch(`${API_BASE}/chat/clear`, {
        method: "PUT"
    });

    document.getElementById("chatBox").innerHTML = "";
}

window.onload = loadChats;
