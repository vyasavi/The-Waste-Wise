import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import pickle

# Load the trained model
model_filename = 'workfile'
with open(model_filename, 'rb') as f:
    copy_of_model = pickle.load(f)


def main():
    st.title('Sales Prediction to Reduce Waste')

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        X = data[["Inflation", "Disposable Income", "Month of the Year"]]
        y = data["Sold"]

        scaler = StandardScaler()
        X_normalized = scaler.fit_transform(X)

        model = LinearRegression()
        model.fit(X_normalized, y)
        st.write('Model trained successfully!')

        inflation = st.number_input('Inflation in Percents:', min_value=0.0)
        disposable_income = st.number_input('Disposable Income:')
        month_of_year = st.number_input('Month of the Year (1-12):', min_value=1, max_value=12)

        if st.button('Predict Sales'):
            x_input = {
                "Inflation": [inflation / 100],
                "Disposable Income": [disposable_income],
                "Month of the Year": [month_of_year],
            }
            predict = pd.DataFrame.from_dict(x_input)
            predicted_sales = copy_of_model.predict(predict)

            pre_dict = {
                "Raw Material (KGs)": [int(int(predicted_sales) * 0.142)],
                "Packaging Material (KGs)": [int(int(predicted_sales) * 0.028)],
                "Energy Consumption (kWh)": [int(predicted_sales) * 0.3],
                "Waste in Transportation (Number of Bags)": [int(int(predicted_sales) * 0.025)],
                "Predicted Sale (Number of Bags)": [int(predicted_sales)],
            }

            pre_data = pd.DataFrame.from_dict(pre_dict)

            st.subheader('Predicted Results')
            st.dataframe(pre_data.T, width=600)


if __name__ == "__main__":
    main()
