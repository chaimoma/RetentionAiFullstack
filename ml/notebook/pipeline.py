import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, f1_score, roc_auc_score, roc_curve
import matplotlib.pyplot as plt

# load cleaned data
data = pd.read_csv("/home/chaima/Documents/RetentionAI/backend/ml/data/cleaned_data.csv")

X = data.drop(columns=['Attrition'])
y = data['Attrition']

# split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# columns
numcateg_cols = [
    'Education',
    'EnvironmentSatisfaction',
    'JobInvolvement',
    'JobSatisfaction',
    'PerformanceRating',
    'RelationshipSatisfaction',
    'WorkLifeBalance'
]

num_cols = [col for col in X.select_dtypes(include=['int64','float64']).columns 
            if col not in numcateg_cols]

cat_cols = X.select_dtypes(include=['object']).columns.tolist()

# preprocessing
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_cols)
],
 remainder='passthrough'
 )

# SMOTE
smote = SMOTE(random_state=42)

# models
models = {
    'LogisticRegression': LogisticRegression(max_iter=500, random_state=42),
    'RandomForest': RandomForestClassifier(random_state=42)
}

param_grids = {
    'LogisticRegression': {'model__C': [0.1, 1, 10], 'model__solver': ['lbfgs']},
    'RandomForest': {'model__n_estimators': [50, 100], 'model__max_depth': [5, 10, None]}
}

for name, model in models.items():
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('smote', smote),
        ('model', model)
    ])
    
    grid = GridSearchCV(pipeline, param_grids[name], cv=5, scoring='accuracy')
    grid.fit(X_train, y_train)
    
    y_pred = grid.predict(X_test)
    y_prob = grid.predict_proba(X_test)[:,1]  # for ROC
    
    # output evaluation
    print(f"\nEvaluation - {name}")
    print("Matrice de confusion:\n", confusion_matrix(y_test, y_pred))
    print("\nRapport de classification:\n", classification_report(y_test, y_pred))
    print(f"f1-score: {f1_score(y_test, y_pred):.2f}")
    
    # roc curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.figure()
    plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc_score(y_test, y_prob):.2f})')
    plt.plot([0,1], [0,1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Courbe ROC - {name}')
    plt.legend()
    plt.show()
    
    # save model
    joblib.dump(grid.best_estimator_, f"{name}_model.pkl")
