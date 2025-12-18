from app.main import generate_retention_plan, RetentionRequest
from unittest.mock import patch

def test_generate_retention_plan_mock():
    # fake employee request(high churn proba)
    request = RetentionRequest(
        employee_id="E001",
        Age=30,
        BusinessTravel="Travel_Rarely",
        Department="Sales",
        Education=3,
        EducationField="Marketing",
        EnvironmentSatisfaction=3,
        Gender="Male",
        JobInvolvement=3,
        JobLevel=2,
        JobRole="Sales Executive",
        JobSatisfaction=4,
        MaritalStatus="Single",
        MonthlyIncome=5000,
        OverTime="Yes",
        PerformanceRating=3,
        RelationshipSatisfaction=3,
        StockOptionLevel=1,
        TotalWorkingYears=5,
        WorkLifeBalance=3,
        YearsAtCompany=3,
        YearsInCurrentRole=2,
        YearsWithCurrManager=2,
        churn_probability=0.8  
    )

    # mocking llm
    with patch("app.main.client.models.generate_content") as mock_generate:
        mock_generate.return_value.text = '{"retention_plan": ["Action 1", "Action 2", "Action 3"]}'

        # mocking user
        mock_user = type('obj', (object,), {'id': 1})()
        plan = generate_retention_plan(request, current_user=mock_user)

        # checking for 3actions
        assert len(plan["retention_plan"]) == 3
        print("Mocked retention plan test passed:", plan)
