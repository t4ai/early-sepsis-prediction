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
This system provides doctors with insights to assess sepsis risk based on patient data, assisting in quick and accurate decision-making in critical care.

The tool will be updated to integrate multiple machine learning models currently under development by the research team, including a Convolutional Neural Network (CNN) and a MicroLSTM. The final step for integration involves standardizing the preprocessing workflow to ensure data compatibility across models and correctly formatting the input data for each model's specific requirements.
""")

# Sidebar for Navigation and Information
st.sidebar.header("Navigation")
st.sidebar.write("""
* Select a Patient ID to predict their sepsis risk
* View associated LIME explanation for each prediction
""")
st.sidebar.header("About Sepsis")
st.sidebar.write("""
Sepsis is a potentially life-threatening condition caused by the body's response to infection. Rapid detection and treatment can prevent severe complications and improve patient outcomes. 
""")

# Sample patient data
sample_data = {
    "Patient_ID": ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008", "P009", "P010", "P011", "P012", "P013"],
    "HR": [120, 115, 130, 95, 100, 105, 70, 65, 75, 80, 85, 60, 68],
    "O2Sat": [85, 88, 80, 95, 97, 90, 99, 98, 97, 96, 95, 100, 99],
    "Temp": [39.5, 39.0, 40.0, 37.2, 37.5, 37.8, 36.5, 36.7, 36.6, 36.8, 37.0, 36.2, 36.4],
    "MAP": [55, 60, 50, 70, 72, 68, 90, 92, 89, 85, 86, 95, 93],
    "Resp": [30, 32, 35, 20, 18, 22, 16, 15, 17, 19, 20, 14, 16],
    "BUN": [45, 40, 50, 20, 25, 22, 10, 9, 11, 12, 13, 8, 9],
    "Creatinine": [2.0, 1.8, 2.2, 1.1, 1.0, 1.2, 0.8, 0.7, 0.9, 1.0, 1.1, 0.6, 0.8],
    "Risk_Level": ["High", "High", "High", "Moderate", "Moderate", "Moderate", "Low", "Low", "Low", "Low", "Low", "Low", "Low"]
}

# Simulated risk probabilities for demonstration
risk_probabilities = {
    "High": [0.85, 0.78, 0.92],
    "Moderate": [0.65, 0.60, 0.70],
    "Low": [0.20, 0.18, 0.25, 0.15, 0.12, 0.10, 0.08]
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
    risk_percentage = round(np.random.choice(risk_probabilities[risk_level]) * 100, 1)  # Simulate risk probability
    features = selected_patient_data.drop(columns=["Patient_ID", "Risk_Level"]).to_dict('records')[0]

    # Main Section - Prediction and Explanation
    if st.button("Generate Prediction"):
        st.subheader(f"Prediction Results for Patient ID: {selected_patient}")
        
        # Display prediction with color-coded label and percentage
        if risk_level == "High":
            st.markdown(f"<h2 style='color:red;'>Prediction: High Risk ({risk_percentage}%)</h2>", unsafe_allow_html=True)
        elif risk_level == "Moderate":
            st.markdown(f"<h2 style='color:orange;'>Prediction: Moderate Risk ({risk_percentage}%)</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 style='color:green;'>Prediction: Low Risk ({risk_percentage}%)</h2>", unsafe_allow_html=True)

        # Generate LIME-style explanation
        st.write("### Explanation")
        explanation_text = (
            f"The prediction for this patient being at **{risk_level}** risk of sepsis with a probability of **{risk_percentage}%** is "
            f"primarily influenced by their **heart rate (HR)** of **{features['HR']} beats per minute**, which significantly impacts the model's score. "
            f"Additional contributors include their **oxygen saturation (O2Sat)** at **{features['O2Sat']}%**, "
            f"**temperature** of **{features['Temp']}°C**, and **mean arterial pressure (MAP)** at **{features['MAP']} mmHg**. "
            f"Their **respiratory rate (Resp)** of **{features['Resp']} breaths per minute** and "
            f"**blood urea nitrogen (BUN)** at **{features['BUN']} mg/dL** further refine the model's assessment. "
            f"These values collectively indicate the patient's sepsis risk."
        )
        st.write(explanation_text)

        st.markdown("""
        **About LIME:**  
        LIME (Local Interpretable Model-Agnostic Explanations) is a technique for explaining individual predictions by approximating the model locally with an interpretable surrogate model. Here, the explanation highlights the features that most significantly contribute to the risk prediction.
        """)

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
**About This Tool**  
The Sepsis Decision Support System demonstrates how to categorize and explain patient risk levels using simulated patient data. Future updates will integrate CNN and MicroLSTM models with a standardized preprocessing workflow.

**Disclaimer**  
This tool is intended for demonstration purposes and should not replace clinical judgment.
""")
st.sidebar.markdown("© 2024 Sepsis Support Tool | Development Version")
