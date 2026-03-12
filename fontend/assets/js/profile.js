// ===============================
// CONFIG
// ===============================
const API_BASE_URL = "http://127.0.0.1:8000";

// ===============================
// AUTH TOKEN
// ===============================
const token = localStorage.getItem("token");

if (!token) {
    // Token nahi hai → login page
    window.location.href = "index.html";
}

// ===============================
// LOGOUT
// ===============================
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

// ===============================
// LOAD PROFILE ON PAGE LOAD
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    loadProfile();

    const form = document.getElementById("profileForm");
    form.addEventListener("submit", updateProfile);
});

// ===============================
// GET /profile/me
// ===============================
async function loadProfile() {
    try {
        const res = await fetch(`${API_BASE_URL}/profile/me`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            throw new Error("Unauthorized");
        }

        const data = await res.json();
        renderProfile(data);

    } catch (err) {
        console.error(err);
        logout();
    }
}

// ===============================
// RENDER PROFILE DATA
// ===============================
function renderProfile(profile) {

    // Profile card
    document.getElementById("profileName").innerText =
        profile.name || "Your Name";

    document.getElementById("profilePhone").innerText =
        "Phone: " + profile.phone_number;

    // Badge
    const badgeEl = document.getElementById("profileBadge");
    badgeEl.className = "badge " + profile.badge;

    if (profile.badge === "trusted") {
        badgeEl.innerText = "Trusted ⭐";
    } else if (profile.badge === "verified") {
        badgeEl.innerText = "Verified ✔";
    } else {
        badgeEl.innerText = "No Badge";
    }

    // Progress
    document.getElementById("progressBar").style.width =
        profile.completion_percentage + "%";

    document.getElementById("completionText").innerText =
        profile.completion_percentage + "% Complete";

    // ===== FORM FILL =====
    document.getElementById("name").value = profile.name || "";
    document.getElementById("email").value = profile.email || "";
    document.getElementById("location").value = profile.location || "";
    document.getElementById("work").value = profile.work || "";
    document.getElementById("company").value = profile.company || "";
    document.getElementById("bio").value = profile.bio || "";
}

// ===============================
// PUT /profile/me
// ===============================
async function updateProfile(e) {
    e.preventDefault();

    const payload = {
        name: document.getElementById("name").value.trim(),
        email: document.getElementById("email").value.trim(),
        location: document.getElementById("location").value.trim(),
        work: document.getElementById("work").value.trim(),
        company: document.getElementById("company").value.trim(),
        bio: document.getElementById("bio").value.trim()
    };

    try {
        const res = await fetch(`${API_BASE_URL}/profile/me`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            throw new Error("Update failed");
        }

        const updatedProfile = await res.json();
        renderProfile(updatedProfile);

        alert("Profile updated successfully!");

        // ✅ Profile verified hone ke baad dashboard
        if (updatedProfile.completion_percentage >= 40) {
            window.location.href = "main_index.html";
        }

    } catch (err) {
        console.error(err);
        alert("Something went wrong. Please try again.");
    }
}
