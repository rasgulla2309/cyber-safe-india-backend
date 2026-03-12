const API = "http://127.0.0.1:8000";
let userPhone = "";

// =============================
// AUTO LOGIN CHECK
// =============================
document.addEventListener("DOMContentLoaded", () => {

    // 🔥 Agar already login hai → dashboard
    const token = localStorage.getItem("token");
    if (token) {
        window.location.href = "main_index.html";
        return;
    }

    document
        .getElementById("sendOtpBtn")
        .addEventListener("click", sendOTP);

    document
        .getElementById("verifyOtpBtn")
        .addEventListener("click", verifyOTP);
});


// =============================
// SEND OTP
// =============================
function sendOTP(event) {

    if (event) event.preventDefault();

    const status = document.getElementById("status");
    userPhone = document.getElementById("phone").value.trim();

    if (!userPhone) {
        status.innerText = "Enter phone number";
        status.style.color = "red";
        return;
    }

    status.innerText = "Sending OTP...";
    status.style.color = "#0d6efd";

    fetch(`${API}/auth/user/send-otp`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            phone_number: userPhone
        })
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to send OTP");
        return res.json();
    })
    .then(() => {

        document.getElementById("phoneBox").style.display = "none";
        document.getElementById("otpBox").style.display = "block";

        status.innerText = "OTP sent ✓";
        status.style.color = "green";
    })
    .catch(err => {
        status.innerText = err.message;
        status.style.color = "red";
    });
}


// =============================
// VERIFY OTP
// =============================
function verifyOTP(event) {

    if (event) event.preventDefault();

    const status = document.getElementById("status");
    const otp = document.getElementById("otp").value.trim();

    if (!otp) {
        status.innerText = "Enter OTP";
        status.style.color = "red";
        return;
    }

    status.innerText = "Verifying...";
    status.style.color = "#0d6efd";

    fetch(`${API}/auth/user/verify-otp`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            phone_number: userPhone,
            otp: otp
        })
    })
    .then(res => {
        if (!res.ok) throw new Error("Invalid or expired OTP");
        return res.json();
    })
    .then(data => {

        // 🔐 SAVE LOGIN TOKEN
        localStorage.setItem("token", data.access_token);

        status.innerText = "Login Success ✓";
        status.style.color = "green";

        // Redirect after small delay
        setTimeout(() => {
            window.location.href = "main_index.html";
        }, 600);
    })
    .catch(err => {
        status.innerText = err.message;
        status.style.color = "red";
    });
}
