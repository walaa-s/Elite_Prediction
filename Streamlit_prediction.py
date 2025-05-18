import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64
import re

# --- Page Setup ---
st.set_page_config(page_title="Student Completion Predictor", layout="wide")

# --- Load Model Artifacts ---
#model = joblib.load("best_model_extreme_age.pkl")
#scaler = joblib.load("scaler_extreme_age.pkl")
#label_encoders = joblib.load("label_encoders_extreme_age.pkl")

# --- Load Age Mapping ---
age_data = pd.read_csv("train_cleaned_final.csv")[['Program Sub Category Code', 'Age Range by Program']].drop_duplicates()
age_map = dict(zip(age_data['Program Sub Category Code'], age_data['Age Range by Program']))

# --- Optional: Background ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .stButton>button {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("Tuwaiq_mounten.png")

# --- Title & Layout ---
st.title("🎓 Will the Student Complete the Program?")
st.markdown("Enter the student's information below:")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 15, 80, 25)
    gender = st.selectbox("Gender", label_encoders['Gender'].classes_)
    home_region = st.selectbox("Home Region", label_encoders['Home Region'].classes_)
    program_cat = st.selectbox("Program Main Category", label_encoders['Program Main Category Code'].classes_)
    program_sub = st.selectbox("Program Sub Category", label_encoders['Program Sub Category Code'].classes_)
    tech_type = st.selectbox("Technology Type", label_encoders['Technology Type'].classes_)
    skill_level = st.selectbox("Program Skill Level", label_encoders['Program Skill Level'].classes_)
    presentation = st.selectbox("Presentation Method", label_encoders['Program Presentation Method'].classes_)
    program_days = st.slider("Program Days", 1, 100, 30)

with col2:
    completed_degree = st.radio("Completed Degree?", ["Yes", "No"])
    edu_level = st.selectbox("Level of Education", label_encoders['Level of Education'].classes_)
    college = st.selectbox("College", label_encoders['College'].classes_)
    degree_score = st.number_input("University Degree Score", 0.0, 5.0, 3.0)
    score_system = st.selectbox("University Degree Score System", [4.0, 5.0])
    employment = st.selectbox("Employment Status", label_encoders['Employment Status'].classes_)
    job_type = st.selectbox("Job Type", label_encoders['Job Type'].classes_)
    still_working = st.radio("Still Working?", ["Yes", "No"])

# --- Extract Min/Max Age from Program Sub Category ---
age_range_str = age_map.get(program_sub, "20-40")
min_age, max_age = map(int, re.findall(r'\d+', age_range_str))

# --- Compute Derived Age Features ---
age_in_range = 1 if min_age <= age <= max_age else 0
gap_to_min = age - min_age
gap_to_max = max_age - age
extreme_age = 1 if age < min_age - 5 or age > max_age + 5 else 0

# --- Prepare Input Dictionary ---
input_dict = {
    'Age': age,
    'Gender': label_encoders['Gender'].transform([gender])[0],
    'Home Region': label_encoders['Home Region'].transform([home_region])[0],
    'Program Main Category Code': label_encoders['Program Main Category Code'].transform([program_cat])[0],
    'Program Sub Category Code': label_encoders['Program Sub Category Code'].transform([program_sub])[0],
    'Technology Type': label_encoders['Technology Type'].transform([tech_type])[0],
    'Program Skill Level': label_encoders['Program Skill Level'].transform([skill_level])[0],
    'Program Presentation Method': label_encoders['Program Presentation Method'].transform([presentation])[0],
    'Program Days': program_days,
    'Completed Degree': 1 if completed_degree == "Yes" else 0,
    'Level of Education': label_encoders['Level of Education'].transform([edu_level])[0],
    'College': label_encoders['College'].transform([college])[0],
    'University Degree Score': degree_score,
    'University Degree Score System': score_system,
    'Employment Status': label_encoders['Employment Status'].transform([employment])[0],
    'Job Type': label_encoders['Job Type'].transform([job_type])[0],
    'Still Working': 1 if still_working == "Yes" else 0,
    'Program Min Age': min_age,
    'Program Max Age': max_age,
    'Age In Range': age_in_range,
    'Age Gap To Min': gap_to_min,
    'Age Gap To Max': gap_to_max,
    'Extreme Age': extreme_age
}

# --- Scale and Predict ---
input_df = pd.DataFrame([input_dict])
scaled_input = scaler.transform(input_df)

if st.button("Predict"):
    if age > max_age + 10 or age < min_age - 10:
        st.subheader("Prediction Result")
        st.error("⚠️ This age is far outside the expected program range.")
        st.metric("Program Age Range", f"{min_age} - {max_age}")
    else:
        pred = model.predict(scaled_input)[0]
        conf = model.predict_proba(scaled_input)[0][pred]
        result = "✅ Will Complete the Program" if pred == 1 else "❌ Will Quit"
        st.subheader("Prediction Result")
        st.success(result)
        st.metric("Confidence Score", f"{conf * 100:.2f}%")
