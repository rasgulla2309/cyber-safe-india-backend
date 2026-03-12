const API_BASE = "http://127.0.0.1:8000";
const chatList = document.getElementById("chatList");
const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "community-login.html";
}

const authHeaders = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + token
};

/* =========================
   ADMIN WEBSOCKET
========================= */
const adminSocket = new WebSocket(`wss://127.0.0.1:8000/ws/chat/999`);

adminSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.sender === "user") {
        loadChats();
    }
};

/* =========================
   LOAD USER CHAT THREADS
========================= */
function loadChats() {
    fetch(`${API_BASE}/admin/chats`, {
        headers: authHeaders
    })
    .then(res => {
        if (res.status === 401) {
            localStorage.clear();
            window.location.href = "community-login.html";
        }
        return res.json();
    })
    .then(data => {
        chatList.innerHTML = "";

        if (!data || data.length === 0) {
            chatList.innerHTML = "<p>No active chats</p>";
            return;
        }

        data.forEach(chat => {
            chatList.innerHTML += `
                <div class="chat">
                    <b>${chat.name || "Unknown User"}</b><br>
                    📞 ${chat.phone_number}<br><br>

                    <small><b>Last message:</b><br>
                    ${chat.last_message}</small>

                    <textarea
                        id="reply-${chat.user_id}"
                        placeholder="Type admin reply here..."
                    ></textarea>

                    <div class="btn-group">
                        <button onclick="sendReply(${chat.user_id})">Reply</button>
                        <button onclick="resolveChat(${chat.user_id})">Resolve</button>
                        <button onclick="closeChat(${chat.user_id})">Close</button>
                    </div>
                </div>
            `;
        });
    });
}

/* =========================
   SEND REPLY
========================= */
function sendReply(userId) {
    const replyBox = document.getElementById(`reply-${userId}`);
    const replyText = replyBox.value.trim();

    if (!replyText) {
        alert("Reply cannot be empty");
        return;
    }

    fetch(`${API_BASE}/admin/chat/${userId}/reply`, {
        method: "PUT",
        headers: authHeaders,
        body: JSON.stringify({ reply: replyText })
    })
    .then(res => res.json())
    .then(data => {
        replyBox.value = "";

        adminSocket.send(JSON.stringify({
            sender: "admin",
            message: replyText
        }));

        loadChats();
    });
}

function resolveChat(userId) {
    fetch(`${API_BASE}/admin/chat/${userId}/resolve`, {
        method: "PUT",
        headers: authHeaders
    }).then(() => loadChats());
}

function closeChat(userId) {
    if (!confirm("Are you sure you want to close this chat?")) return;

    fetch(`${API_BASE}/admin/chat/${userId}/close`, {
        method: "PUT",
        headers: authHeaders
    }).then(() => loadChats());
}

loadChats();
