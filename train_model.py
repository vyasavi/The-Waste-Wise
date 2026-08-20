"""Train the demand-forecasting model and serialize it to `workfile`.

Run this to regenerate the model from the generated dataset:

    python train_model.py

The model is a scikit-learn Pipeline: the month is one-hot encoded (a separate
effect per month, so the model can capture seasonal demand), while Inflation and
Disposable Income pass through as numeric. LinearRegression is the estimator.

Encoding lives inside the pipeline, so inference (`demo.py`) just feeds the same
raw three-column frame -- Inflation as a fraction, Disposable Income, and Month
of the Year -- with no separate feature prep to keep in sync.
"""

import pickle

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_FILE = "new_file.csv"
MODEL_FILE = "workfile"
FEATURES = ["Inflation", "Disposable Income", "Month of the Year"]
TARGET = "Sold"


def train():
    data = pd.read_csv(DATA_FILE)
    X = data[FEATURES]
    y = data[TARGET]

    # Preprocess inside the pipeline so training and inference share identical
    # feature preparation:
    #   - month  -> one-hot (a distinct effect per month, captures seasonality)
    #   - numeric -> standardized (zero mean / unit variance, so the linear
    #     coefficients are comparable and interpretable)
    preprocess = ColumnTransformer(
        transformers=[
            ("month",
             OneHotEncoder(categories=[list(range(1, 13))], handle_unknown="ignore",
                           sparse_output=False),
             ["Month of the Year"]),
            ("numeric", StandardScaler(), ["Inflation", "Disposable Income"]),
        ],
    )
    # No intercept: the 12 month dummies already span the baseline, so dropping
    # the intercept avoids the dummy trap (rank-deficient design) and makes the
    # coefficients unique. Each month coefficient then reads directly as the
    # expected units for that month at average inflation / income.
    model = Pipeline([
        ("preprocess", preprocess),
        ("model", LinearRegression(fit_intercept=False)),
    ])
    model.fit(X, y)

    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)

    r2 = model.score(X, y)
    print(f"Trained on {len(data)} rows. R^2 = {r2:.3f}. Saved -> {MODEL_FILE}")

    # Sanity-check prediction (matches demo.py defaults: 3% inflation, $3000, June)
    sample = pd.DataFrame(
        {"Inflation": [0.03], "Disposable Income": [3000.0], "Month of the Year": [6]}
    )
    print(f"Sample prediction (units sold): {int(model.predict(sample)[0]):,}")


if __name__ == "__main__":
    train()
