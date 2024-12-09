import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Sepsis Decision Support System", layout="wide")

# Title and Header
st.title("🩺 Sepsis Decision Support System")
st.markdown("""
#### A Real-Time Prediction and Decision Support Tool for Healthcare Professionals
This system provides doctors with insights to assess sepsis risk based on patient data, assisting in quick and accurate decision-making in critical care.
""")

# Sidebar for navigation
st.sidebar.header("Navigation")
st.sidebar.write("""
* Select a Patient ID to predict their sepsis risk
* View associated feature analysis and LIME explanations
""")
st.sidebar.header("About Sepsis")
st.sidebar.write("""
Sepsis is a potentially life-threatening condition caused by the body's response to infection. Rapid detection and treatment can prevent severe complications and improve patient outcomes.
""")

# Define lab and clinical feature columns
lab_feature_cols = ['WBC', 'Platelets', 'Creatinine', 'Glucose', 'Lactate', 'Hct', 'BUN', 'Potassium', 'Magnesium', 'Calcium']
clinical_feature_cols = ['HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'DBP', 'Resp', 'EtCO2']

# Helper: Assign risk level based on thresholds
def assign_risk_level(row):
    if row['HR'] > 120 or row['Lactate'] > 2.5 or row['O2Sat'] < 90:
        return "High"
    else:
        return "Low"

# Simulated patient data with lab and clinical features
np.random.seed(42)
sample_data = {
    "Patient_ID": [f"P{i:03}" for i in range(1, 14)],
    "HR": np.random.randint(60, 140, 13),
    "O2Sat": np.random.randint(85, 100, 13),
    "Temp": np.round(np.random.uniform(36.0, 40.0, 13), 1),
    "SBP": np.random.randint(90, 160, 13),
    "MAP": np.random.randint(50, 100, 13),
    "DBP": np.random.randint(50, 90, 13),
    "Resp": np.random.randint(12, 40, 13),
    "EtCO2": np.random.randint(30, 50, 13),
    "WBC": np.random.uniform(4.0, 12.0, 13),
    "Platelets": np.random.randint(150, 400, 13),
    "Creatinine": np.random.uniform(0.6, 2.5, 13),
    "Glucose": np.random.randint(70, 200, 13),
    "Lactate": np.random.uniform(0.5, 4.0, 13),
    "Hct": np.random.uniform(30, 50, 13),
    "BUN": np.random.randint(5, 50, 13),
    "Potassium": np.random.uniform(3.5, 5.5, 13),
    "Magnesium": np.random.uniform(1.5, 2.5, 13),
    "Calcium": np.random.uniform(8.5, 10.5, 13)
}

sample_df = pd.DataFrame(sample_data)
sample_df['Risk_Level'] = sample_df.apply(assign_risk_level, axis=1)

# Sidebar - Patient Selection
st.sidebar.subheader("Select Patient ID")
patient_options = [""] + sample_df["Patient_ID"].tolist()
selected_patient = st.sidebar.selectbox("Choose Patient ID:", patient_options)

# Helper: Generate Risk Probability
def simulate_risk_probability(risk_level):
    risk_mapping = {
        "High": np.random.uniform(0.75, 0.95),
        "Low": np.random.uniform(0.10, 0.49)
    }
    return round(risk_mapping[risk_level] * 100, 1)

# Helper: Generate LIME Explanation Table
def generate_lime_explanation(features, risk_level):
    np.random.seed(42)
    importance_values = {key: np.random.uniform(-1, 1) for key in features.keys()}
    explanation_df = pd.DataFrame({
        "Feature": list(features.keys()),
        "Value": list(features.values()),
        "Importance": [round(importance_values[key], 2) for key in features.keys()],
        "Contribution": ["Positive" if importance_values[key] > 0 else "Negative" for key in features.keys()]
    })
    explanation_df["Absolute Importance"] = explanation_df["Importance"].abs()
    explanation_df.sort_values(by="Absolute Importance", ascending=False, inplace=True)
    return explanation_df.drop(columns=["Absolute Importance"])

if selected_patient:
    selected_patient_data = sample_df[sample_df["Patient_ID"] == selected_patient]
    risk_level = selected_patient_data["Risk_Level"].values[0]
    risk_percentage = simulate_risk_probability(risk_level)
    features = selected_patient_data.drop(columns=["Patient_ID", "Risk_Level"]).to_dict('records')[0]

    if st.button("Generate Prediction"):
        st.subheader(f"Prediction Results for Patient ID: {selected_patient}")

        # Display prediction
        if risk_level == "High":
            st.markdown(f"<h2 style='color:red;'>Prediction: High Risk ({risk_percentage}%)</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 style='color:green;'>Prediction: Low Risk ({risk_percentage}%)</h2>", unsafe_allow_html=True)

        # Generate and display LIME explanation visualization
        lime_explanation = generate_lime_explanation(features, risk_level)
        st.write("### LIME Feature Contribution Visualization")
        st.write("The following chart visualizes the contributions of each feature to the prediction:")

        # Create a bar plot for feature contributions
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=lime_explanation,
            x="Importance",
            y="Feature",
            hue="Contribution",
            dodge=False,
            palette={"Positive": "green", "Negative": "red"}
        )
        plt.title("Feature Contributions to Risk Prediction")
        plt.xlabel("Importance (Magnitude of Contribution)")
        plt.ylabel("Feature")
        plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
        plt.legend(title="Contribution")
        plt.tight_layout()

        # Display the plot
        st.pyplot(plt)

        # Explanation Summary
        st.write("### Explanation Summary")
        explanation_text = f"""
        The prediction for this patient being at **{risk_level}** risk of sepsis with a probability of **{risk_percentage}%** 
        is supported by Local Interpretable Model-agnostic Explanations (LIME). 
        LIME highlights how individual features (e.g., heart rate, lactate levels) contribute to the risk prediction. 
        Features with a **positive contribution** increase the risk, while those with a **negative contribution** decrease it.
        This transparency helps healthcare professionals make informed, reliable decisions based on the model's outputs.
        """
        st.write(explanation_text)

        st.dataframe(lime_explanation)

# Footer
st.markdown("---")
st.markdown("© 2024 Sepsis Support Tool | For Demonstration Purposes Only")
