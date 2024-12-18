# :stethoscope: SepsiSCT: A Stacked Convolutional Transformer Model for Early Sepsis Detection in ICU Patients


## Overview

Sepsis, a severe inflammatory response to infection, can progress quickly and is a leading cause of mortality in intensive care settings.  This project addresses the critical challenge of predicting sepsis onset in ICU patients by applying machine learning techniques to clinical data that is commonly available in the ICU. 

### Stacked Convolutional Transformer (SCT) Model
A key outcome of this project was the development of a novel model architecture that combined the feature extraction capabilities of CNNs with the long context understanding of the attention-based transformer.  Through experimentation with separate CNN and Transformer models, an optimal base architecture for each was developed and combined into a stacked hybrid model, resulting in the Stacked Convolutional Transformer (SCT) Model architecture.

![SCT Architecture Diagram](https://github.com/t4ai/early-sepsis-prediction/blob/7d475e63f22aeb86798254acac6d42050bd316ba/app/sct_diagram.png)

### Deterioration Index (DI) Feature
A novel feature, the Deterioration Index (DI), was engineered to encode changes in overall patient health over time.  The DI was a calculated score designed to monitor changes in a patient’s vital signs and lab values, enabling the detection of rapid trends or deviations that may signal clinical deterioration, such as the onset of sepsis.  Effectively, the DI encodes medical knowledge that a human doctor or nurse may apply in a clinical setting in order to detect degradation in a patient’s overall condition, potentially leading to sepsis.  The feature also incorporates a rate of change from the previous time step, providing time-based trend information as to whether a patient is deteriorating or improving.

## Project Structure

The repository is organized as follows:

- **0 - Load Datalake.ipynb**: Notebook for loading the dataset for processing.
- **1 - Exploratory Data Analysis.ipynb**: Performs exploratory data analysis to understand the dataset, time series characteristics, feature relationships and any correlations.
- **2 - Feature Selection and Data Cleansing.ipynb**: Processes for selecting relevant features and cleaning the data.  Decision Tree Classifier used to determine feature importance.
- **3 - Feature Engineering and Data Prep.ipynb**: Addition of lag features, Deterioration Index and preparation tasks such as encoding, noramalization and time-series patient filtering.
- **4.1 - CNN Model Experiments.ipynb**: Experiments with Convolutional Neural Networks (CNN) for sepsis prediction.
- **4.2 - Ultra Light LSTM Experiment.ipynb**: Development of an ultra-light LSTM model for efficient prediction.
- **4.3 - Transformer and SCT Model Experiments.ipynb**: Exploration of Transformer and Self-attention based models.  Stacked Convolutional Transformer hyper model definition and tuning job.
- **4.4 - Baseline Linear Regression + Deterioration Index.ipynb**: Basline experiments that combines linear regression with a deterioration index for prediction.
- **4.5 - Baseline Random forest CNN.ipynb**: Basline experiments that combines simple random forest model with baseline cnn. 
- **5.0 - Performance Evaluation.ipynb**: Evaluation of top CNN, Transformer and SCT performance against key project metrics.
- **environment-setup.ipynb**: Instructions and scripts for setting up the development environment.
- **sepsis_helpers.py**: Utility class to perform the Deterioration Index calculation and scoring.

- **app/**: Contains the application code for mock UI.
- **models/lstm-light/**: Includes the implementation of a lightweight Long Short-Term Memory (LSTM) model tailored for sepsis prediction.


## 🛡️ Badges

![Contributors](https://img.shields.io/github/contributors/t4ai/early-sepsis-prediction)

## ❤️ Acknowledgments

This project is the Captsone Project (AAI-590) for Team 3: Tyler Foreman, Ahmed Ahmed, Eric Barnes and Ryan Laxamana.

University of San Diego - M.S.c in Applied Artificial Intelligence

Summer 2023 Cohort

---

