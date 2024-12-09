import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration for better display on Streamlit
st.set_page_config(page_title="Sepsis Decision Support System", layout="wide")

# Title and Header
st.title("🩺 Sepsis Decision Support System")
st.markdown("""
#### A Real-Time Prediction and Decision Support Tool for Healthcare Professionals
This system provides insights to assess sepsis risk based on patient data, assisting in quick and accurate decision-making in critical care.

The tool demonstrates predictive capabilities using simulated data and feature analysis to help healthcare professionals interpret risk levels.
""")

# Sidebar for Navigation and Information
st.sidebar.header("Navigation")
st.sidebar.write("""
* Select a Patient ID to predict their sepsis risk
* View associated explanation for each prediction
""")
st.sidebar.header("About Sepsis")
st.sidebar.write("""
Sepsis is a potentially life-threatening condition caused by the body's response to infection. Rapid detection and treatment can improve patient outcomes significantly.
""")

# Sample patient data
sample_data = {
    "Patient_ID": [f"P{i:03}" for i in range(1, 14)],
    "HR": np.random.randint(60, 140, 13),
    "O2Sat": np.random.randint(85, 100, 13),
    "Temp": np.round(np.random.uniform(36.0, 40.0, 13), 1),
    "MAP": np.random.randint(50, 100, 13),
    "Resp": np.random.randint(12, 40, 13),
    "BUN": np.random.randint(5, 50, 13),
    "Creatinine": np.round(np.random.uniform(0.6, 2.5, 13), 1),
    "Risk_Level": np.random.choice(["High", "Moderate", "Low"], 13, p=[0.3, 0.4, 0.3])
}

sample_df = pd.DataFrame(sample_data)

# Sidebar - Patient Selection
st.sidebar.subheader("Select Patient ID")
patient_options = [""] + sample_df["Patient_ID"].tolist()  # Add empty option as default
selected_patient = st.sidebar.selectbox("Choose Patient ID:", patient_options)

# Ensure the user selects a valid Patient ID
if selected_patient:
    # Extract the selected patient's data
    selected_patient_data = sample_df[sample_df["Patient_ID"] == selected_patient]
    risk_level = selected_patient_data["Risk_Level"].values[0]
    risk_percentage = round(np.random.uniform(0.75, 0.95) * 100 if risk_level == "High" else
                            np.random.uniform(0.50, 0.74) * 100 if risk_level == "Moderate" else
                            np.random.uniform(0.10, 0.49) * 100, 1)
    features = selected_patient_data.drop(columns=["Patient_ID", "Risk_Level"]).to_dict('records')[0]

    # Main Section - Prediction and Explanation
    if st.button("Generate Prediction"):
        st.subheader(f"Prediction Results for Patient ID: {selected_patient}")
        
        # Display prediction with color-coded label and percentage
        color = "red" if risk_level == "High" else "orange" if risk_level == "Moderate" else "green"
        st.markdown(f"<h2 style='color:{color};'>Prediction: {risk_level} Risk ({risk_percentage}%)</h2>", unsafe_allow_html=True)

        # Generate Explanation
        st.write("### Explanation")
        explanation_text = (
            f"The prediction indicates a **{risk_level}** risk of sepsis with a probability of **{risk_percentage}%**. "
            f"This assessment is influenced by the following features: "
            f"**Heart Rate (HR)**: {features['HR']} bpm, **Oxygen Saturation (O2Sat)**: {features['O2Sat']}%, "
            f"**Temperature**: {features['Temp']}°C, **Mean Arterial Pressure (MAP)**: {features['MAP']} mmHg, "
            f"**Respiratory Rate (Resp)**: {features['Resp']} breaths per minute, and "
            f"**Blood Urea Nitrogen (BUN)**: {features['BUN']} mg/dL."
        )
        st.write(explanation_text)

        # Visual aid: Feature bar plot
        st.write("### Patient Feature Values")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=list(features.values()), y=list(features.keys()), palette="viridis", ax=ax)
        ax.set_title("Patient Feature Values")
        ax.set_xlabel("Value")
        st.pyplot(fig)
else:
    st.subheader("Please select a Patient ID and click 'Generate Prediction' to view results.")

# Footer with Additional Information and Resources
st.markdown("---")
st.markdown("""
**Disclaimer:**  
This tool is for demonstration purposes and is not intended to replace clinical judgment. It uses simulated data to illustrate decision support capabilities.
""")
st.sidebar.markdown("© 2024 Sepsis Support Tool | Development Version")
