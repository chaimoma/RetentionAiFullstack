// Step navigation
let currentStep = 1;
const totalSteps = 3;

function showStep(n){
    for(let i=1; i<=totalSteps; i++){
        document.getElementById("step"+i).style.display = i===n ? "block" : "none";
    }
}

document.getElementById("next1").addEventListener("click", () => { currentStep = 2; showStep(currentStep); });
document.getElementById("back2").addEventListener("click", () => { currentStep = 1; showStep(currentStep); });
document.getElementById("next2").addEventListener("click", () => { currentStep = 3; showStep(currentStep); });
document.getElementById("back3").addEventListener("click", () => { currentStep = 2; showStep(currentStep); });

// Logout button
document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
});

// Predict Risk
document.getElementById("predictBtn").addEventListener("click", async () => {
    const employeeData = {
        employee_id: document.getElementById("employee_id").value,
        Age: parseInt(document.getElementById("Age").value),
        Gender: document.getElementById("Gender").value,
        BusinessTravel: document.getElementById("BusinessTravel").value,
        Department: document.getElementById("Department").value,
        JobRole: document.getElementById("JobRole").value,
        MaritalStatus: document.getElementById("MaritalStatus").value,
        OverTime: document.getElementById("OverTime").value,
        Education: parseInt(document.getElementById("Education").value),
        EducationField: document.getElementById("EducationField").value,
        EnvironmentSatisfaction: parseInt(document.getElementById("EnvironmentSatisfaction").value),
        JobInvolvement: parseInt(document.getElementById("JobInvolvement").value),
        JobLevel: parseInt(document.getElementById("JobLevel").value),
        JobSatisfaction: parseInt(document.getElementById("JobSatisfaction").value),
        PerformanceRating: parseInt(document.getElementById("PerformanceRating").value),
        RelationshipSatisfaction: parseInt(document.getElementById("RelationshipSatisfaction").value),
        WorkLifeBalance: parseInt(document.getElementById("WorkLifeBalance").value),
        MonthlyIncome: parseFloat(document.getElementById("MonthlyIncome").value),
        TotalWorkingYears: parseInt(document.getElementById("TotalWorkingYears").value),
        YearsAtCompany: parseInt(document.getElementById("YearsAtCompany").value),
        YearsInCurrentRole: parseInt(document.getElementById("YearsInCurrentRole").value),
        YearsWithCurrManager: parseInt(document.getElementById("YearsWithCurrManager").value),
        StockOptionLevel: parseInt(document.getElementById("StockOptionLevel").value)
    };

    const token = localStorage.getItem("token");
    if(!token){ alert("You are not logged in"); return; }

    try {
        const res = await fetch("http://backend:8081/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify(employeeData)
        });
        const data = await res.json();
        document.getElementById("result").style.display = "block";
        document.getElementById("churnProbability").textContent = (data.churn_probability*100).toFixed(2) + "%";

        // If high risk, generate retention plan
        if(data.churn_probability > 0.5){
            const retentionRes = await fetch("http://backend:8081/generate-retention-plan", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify({...employeeData, churn_probability: data.churn_probability})
            });
            const plan = await retentionRes.json();
            const ul = document.getElementById("retentionPlan");
            ul.innerHTML = "";
            plan.retention_plan.forEach(a => {
                const li = document.createElement("li");
                li.textContent = a;
                ul.appendChild(li);
            });
        } else {
            document.getElementById("retentionPlan").innerHTML = "<li>No retention needed.</li>";
        }
    } catch(err){
        alert("Error: "+err.message);
    }
});
