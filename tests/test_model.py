from app.main import model, EmployeeData
import pandas as pd

def test_model_prediction_simple():
    #fake employee input
    employee = EmployeeData(
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
        YearsWithCurrManager=2
    )

    #prepare data for model
    data = employee.model_dump()
    data.pop("employee_id")
    X = pd.DataFrame([data])

    #predict
    probability = model.predict_proba(X)[0][1]

    #check validation of proba (0-1)
    assert 0 <= probability <= 1

    print("ML model loaded correctly and prediction is valid:", probability)
