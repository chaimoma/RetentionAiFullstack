const BASE_URL = "http://localhost:8081";

async function login(username, password) {
    const res = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });
    if (!res.ok) throw await res.json();
    return res.json();
}

async function predict(employeeData) {
    const res = await fetch(`${BASE_URL}/predict`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify(employeeData)
    });
    if (!res.ok) throw await res.json();
    return res.json();
}

async function generateRetentionPlan(employeeData) {
    const res = await fetch(`${BASE_URL}/generate-retention-plan`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${getToken()}`
        },
        body: JSON.stringify(employeeData)
    });
    if (!res.ok) throw await res.json();
    return res.json();
}
