import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Generate Random Dataset
# -----------------------------
@st.cache_data
def load_data(n=200):
    np.random.seed(42)
    data = {
        "PM2.5": np.random.randint(10, 300, n),
        "PM10": np.random.randint(20, 400, n),
        "NO2": np.random.randint(5, 150, n),
        "SO2": np.random.randint(2, 80, n),
        "CO": np.random.uniform(0.1, 5.0, n),
        "O3": np.random.randint(10, 250, n),
        "Temperature": np.random.uniform(10, 40, n),
        "Humidity": np.random.uniform(20, 90, n),
        "Wind": np.random.uniform(0, 10, n),
        "date": pd.date_range("2023-01-01", periods=n, freq="D")
    }
    df = pd.DataFrame(data)
    # Simple AQI formula (demo only)
    df["AQI"] = (
        df["PM2.5"]*0.4 + df["PM10"]*0.2 +
        df["NO2"]*0.15 + df["SO2"]*0.1 +
        df["CO"]*10 + df["O3"]*0.05
    ).clip(0, 500)
    return df

df = load_data()

st.title("🌍 Air Quality Prediction & Visualization Dashboard")
st.write("Demo dashboard using **randomly generated air quality data**.")

# -----------------------------
# Section 1: Dataset Overview
# -----------------------------
st.subheader("📑 Dataset Overview")
st.write(df.head())

# -----------------------------
# Section 2: Pollutant Distributions
# -----------------------------
st.subheader("📊 Pollutant Distributions")

pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
selected_pollutant = st.selectbox("Select pollutant to visualize:", pollutants)

fig, ax = plt.subplots(figsize=(6,4))
sns.histplot(df[selected_pollutant], kde=True, bins=30, ax=ax, color="skyblue")
ax.set_title(f"Distribution of {selected_pollutant}")
st.pyplot(fig)

# -----------------------------
# Section 3: AQI Trend Over Time
# -----------------------------
st.subheader("📈 AQI Trend Over Time")
fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(data=df, x="date", y="AQI", ax=ax, color="green")
ax.set_title("AQI Over Time")
st.pyplot(fig)

# -----------------------------
# Section 4: Correlation Heatmap
# -----------------------------
st.subheader("🔗 Correlation Heatmap")
fig, ax = plt.subplots(figsize=(8,6))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap of Pollutants")
st.pyplot(fig)

# -----------------------------
# Section 5: Pair Plot
# -----------------------------
st.subheader("📉 Pair Plot of Pollutants")
st.info("This may take time for large datasets.")
if st.button("Generate Pairplot"):
    fig = sns.pairplot(df[pollutants])
    st.pyplot(fig)

# -----------------------------
# Section 6: AQI Prediction (Rule-based)
# -----------------------------
st.subheader("🤖 AQI Prediction (Predefined Rules)")

st.sidebar.header("🔧 Enter Pollutant & Weather Values")
pm25 = st.sidebar.number_input("PM2.5", min_value=0.0, max_value=500.0, value=50.0)
pm10 = st.sidebar.number_input("PM10", min_value=0.0, max_value=500.0, value=80.0)
no2  = st.sidebar.number_input("NO2",  min_value=0.0, max_value=200.0, value=30.0)
so2  = st.sidebar.number_input("SO2",  min_value=0.0, max_value=200.0, value=20.0)
co   = st.sidebar.number_input("CO",   min_value=0.0, max_value=50.0, value=1.0)
o3   = st.sidebar.number_input("O3",   min_value=0.0, max_value=300.0, value=40.0)
temp = st.sidebar.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0)
humid= st.sidebar.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
wind = st.sidebar.number_input("Wind Speed (m/s)", min_value=0.0, max_value=20.0, value=2.0)

if st.sidebar.button("Predict AQI"):
    # Rule-based formula
    prediction = (
        pm25*0.4 + pm10*0.2 + no2*0.15 +
        so2*0.1 + co*10 + o3*0.05
    )
    prediction = min(prediction, 500)

    # AQI Category
    if prediction <= 50:
        category = "Good 😊"
        color = "green"
    elif prediction <= 100:
        category = "Moderate 😐"
        color = "yellow"
    elif prediction <= 200:
        category = "Poor 😷"
        color = "orange"
    elif prediction <= 300:
        category = "Very Poor 🤢"
        color = "red"
    else:
        category = "Severe ☠️"
        color = "darkred"

    st.success(f"### Predicted AQI: {prediction:.2f} ({category})")

    # Gauge-like visualization
    fig, ax = plt.subplots(figsize=(6,1.5))
    ax.barh(["AQI"], [prediction], color=color)
    ax.set_xlim(0, 500)
    ax.set_title("Predicted AQI Level")
    st.pyplot(fig)
