from pathlib import Path
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score, f1_score

# 1. Load Data
DATA_PATH = Path("data")
csv_file = list(DATA_PATH.glob("*.csv"))[0]
df = pd.read_csv(csv_file)
print(f"Loaded {csv_file.name} successfully. Rows: {df.shape[0]}, Columns: {df.shape[1]}")

# 2. Required Feature Engineering
def engineer_features(data: pd.DataFrame) -> pd.DataFrame:
    d = data.copy()
    
    # Income to experience ratio
    d["IncomeToExperienceRatio"] = d["MonthlyIncome"] / (d["TotalWorkingYears"] + 1)
    
    # Promotion delay indicator
    d["PromotionDelayIndicator"] = d["YearsSinceLastPromotion"] / (d["YearsAtCompany"] + 1)
    
    # Engagement composite score (scale 1 to 4)
    d["EngagementScore"] = (
        d["JobInvolvement"] + d["JobSatisfaction"] + 
        d["EnvironmentSatisfaction"] + d["RelationshipSatisfaction"]
    ) / 4.0
    
    # Workload stress flag (Overtime + Poor Work-Life Balance)
    d["WorkloadStressFlag"] = ((d["OverTime"] == "Yes") & (d["WorkLifeBalance"] <= 2)).astype(int)
    
    return d

df_feat = engineer_features(df)

# Separate Target and Features
X = df_feat.drop(columns=["Attrition"])
y = df_feat["Attrition"]

# Identify column types
categorical_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()
numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

print(f"Engineered Features: IncomeToExperienceRatio, PromotionDelayIndicator, EngagementScore, WorkloadStressFlag")
print(f"Categorical Columns ({len(categorical_cols)}): {categorical_cols}")
print(f"Numerical Columns ({len(numerical_cols)}): {numerical_cols}")

# 3. Stratified Train-Test Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# 4. Column Transformer Pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False), categorical_cols)
    ]
)

# 5. Model Benchmarking
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=8, class_weight="balanced", random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=120, max_depth=4, learning_rate=0.08, random_state=42)
}

best_model_name = None
best_auc = 0.0
best_pipeline = None

print("\n" + "=" * 55)
print("BENCHMARKING MODELS (EVALUATION ON TEST DATA)")
print("=" * 55)

for name, clf in models.items():
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", clf)
    ])
    pipe.fit(X_train, y_train)
    
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_proba)
    f1 = f1_score(y_test, y_pred)
    
    print(f"\n--- {name} ---")
    print(f"ROC-AUC: {auc:.4f} | F1-Score: {f1:.4f}")
    print(classification_report(y_test, y_pred, target_names=["Stayed (0)", "Left (1)"], digits=3))
    
    if auc > best_auc:
        best_auc = auc
        best_model_name = name
        best_pipeline = pipe

print("=" * 55)
print(f"Selected Best Model: {best_model_name} (ROC-AUC: {best_auc:.4f})")

# 6. Save Pipeline & Metadata
artifacts_dir = Path("artifacts")
artifacts_dir.mkdir(exist_ok=True)

joblib.dump(best_pipeline, artifacts_dir / "best_attrition_pipeline.pkl")
joblib.dump(categorical_cols, artifacts_dir / "categorical_cols.pkl")
joblib.dump(numerical_cols, artifacts_dir / "numerical_cols.pkl")

print(f"Model artifacts successfully saved inside '{artifacts_dir}/'")