# The Waste Wise 
### 3rd Place 🏆 HackWesTX 2023

A machine learning web app that predicts manufacturing sales from economic inputs and generates per-unit resource consumption estimates, helping manufacturers reduce waste across raw materials, packaging, and energy.

---

## Overview

Manufacturing waste is often a consequence of inaccurate demand forecasting. The Waste Wise addresses this by training a Linear Regression model on simulated economic data with seasonal demand patterns, then using predicted sales figures to estimate resource requirements before production begins.

Given three economic inputs — inflation rate, disposable income, and month of year — the app outputs:

- Predicted units sold
- Raw material requirement (kg)
- Packaging material requirement (kg)
- Energy consumption (kWh)
- Transportation waste estimate (bags)

---

## Demo Link

https://the-waste-wise.streamlit.app/

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Frontend / UI | Streamlit |
| ML Model | scikit-learn (LinearRegression, StandardScaler) |
| Data Processing | pandas |
| Model Serialization | pickle |
| Data Generation | Python (random, pandas) |

---

## How It Works

**1. Data Generation (`data_generation_and_training.ipynb`)**

Synthetic economic data is generated for every month from 1960 to 2022 (756 rows). Each row includes:
- Production volume (1M–3M units)
- Inflation rate (1%–5%)
- Disposable income ($2,000–$5,000)
- Seasonal demand modifiers (higher sales in May–Aug and December)
- Derived resource consumption values (fixed ratios of production)

**2. Model Training (`train_model.py`)**

The model is a scikit-learn `Pipeline` (`OneHotEncoder` → `LinearRegression`)
trained on three features:
- `Inflation`
- `Disposable Income`
- `Month of the Year` — **one-hot encoded** (12 categories)

Target variable: `Sold` (units sold)

Month is treated as categorical rather than a single numeric term, so the model
learns a distinct effect per month and can capture the seasonal demand peaks
(May–Aug and December). The encoding lives inside the pipeline, so training and
inference share the exact same feature preparation — no scaler or separate
encoder to keep in sync. Running `python train_model.py` regenerates the
serialized model (`workfile`).

**3. Prediction & Waste Estimation (`demo.py`)**

The trained model predicts sales for user-provided inputs. Resource consumption is estimated using fixed per-unit ratios:

| Resource | Ratio |
|----------|-------|
| Raw Material | 0.142 kg/unit |
| Packaging Material | 0.028 kg/unit |
| Energy Consumption | 0.3 kWh/unit |
| Transportation Waste | 0.025 bags/unit |

---

## Getting Started

### Prerequisites

Python 3.9–3.12 (the pinned `scikit-learn==1.3.2` has no wheels for 3.13).

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run the App

```bash
python train_model.py   # (optional) regenerate the model from data
streamlit run demo.py
```

The app will open in your browser at `http://localhost:8501`.

### Usage

1. Enter economic inputs — inflation, disposable income, and month
2. The forecast, resource estimates, and seasonal-demand chart update live
3. Optionally upload a CSV (`Inflation`, `Disposable Income`, `Month of the Year`, `Sold`) to preview your own data

### Deploying to Streamlit Community Cloud

Point the app at `demo.py` and set the **Python version to 3.12** in the app's
advanced settings so the pinned dependencies install from wheels.

---

## Project Structure

```
The-Waste-Wise/
├── demo.py                                 # Streamlit app (landing + predictor)
├── train_model.py                          # Trains LinearRegression -> workfile
├── data_generation_and_training.ipynb      # Synthetic data generation notebook
├── new_file.csv                            # Generated training dataset
├── workfile                                # Serialized trained model (pickle)
├── requirements.txt                        # Pinned dependencies
├── .streamlit/config.toml                  # App theme
├── screen.png                              # CSV-format screenshot
├── icon.png                                # App icon
└── logo-no-background.png
```

---

## Built With

- [Streamlit](https://streamlit.io/) — web app framework
- [scikit-learn](https://scikit-learn.org/) — machine learning
- [pandas](https://pandas.pydata.org/) — data manipulation

---

*This project was built at HackWesTX 2023. The repository was migrated to my personal GitHub in 2025.*
