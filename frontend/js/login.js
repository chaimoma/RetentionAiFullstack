document.getElementById("loginBtn").addEventListener("click", async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const alertBox = document.getElementById("alert");
    alertBox.style.display = "none";

    try {
        const data = await login(username, password);
        setToken(data.access_token);
        window.location.href = "dashboard.html";
    } catch(err) {
        alertBox.style.display = "block";
        alertBox.textContent = err.detail || "Login failed";
    }
});