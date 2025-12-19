document.getElementById("registerBtn").addEventListener("click", async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const alertBox = document.getElementById("alert");
    alertBox.style.display = "none";

    if(!username || !password){
        alertBox.style.display = "block";
        alertBox.textContent = "Please fill in both fields";
        return;
    }

    try {
        const res = await fetch("http://localhost:8081/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        if(!res.ok) throw await res.json();
        alertBox.style.display = "block";
        alertBox.style.background = "#2ecc71"; 
        alertBox.textContent = "Registration successful! Redirecting to login...";
        setTimeout(() => { window.location.href = "index.html"; }, 2000);
    } catch(err) {
        alertBox.style.display = "block";
        alertBox.style.background = "#e74c3c";
        alertBox.textContent = err.detail || "Registration failed";
    }
});
