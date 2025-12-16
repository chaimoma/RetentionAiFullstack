import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report

#loadit cleaned data
data = pd.read_csv("data/cleaned_data.csv")

# select x and y 
X = data.drop(columns=['Attrition'])
y = data['Attrition']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# numerical and categorial columns
numerical_cols = X.select_dtypes(include=['int64','float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

# processing
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_cols),
    ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_cols)
])

# SMOTE (bach n equilibriw data)
smote = SMOTE(random_state=42)

# models
models = {
    'LogisticRegression': LogisticRegression(max_iter=500, random_state=42),
    'RandomForest': RandomForestClassifier(random_state=42)
}

# hyperparameter grids
param_grids = {
    'LogisticRegression': {
        'model__C': [0.1, 1, 10],
        'model__solver': ['lbfgs']
    },
    'RandomForest': {
        'model__n_estimators': [50, 100],
        'model__max_depth': [5, 10, None]
    }
}

# train w evaluate
for name, model in models.items():
    print(f"\n=== Training {name} ===")
    
    # Pipeline: preprocessing -> SMOTE -> model
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('smote', smote),
        ('model', model)
    ])
    
    # GridSearchCV
    grid = GridSearchCV(pipeline, param_grids[name], cv=5, scoring='accuracy')
    grid.fit(X_train, y_train)
    
    # Predictions
    y_pred = grid.predict(X_test)
    
    # Evaluation
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    print("Best parameters:", grid.best_params_)
    print("Best CV score:", grid.best_score_)
