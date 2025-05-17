# 🎓 Student Completion Predictor

> Can we predict who will finish their program and who will quit?  
> With a little machine learning magic — **yes, we can.**

---

## 🚀 What This Project Does

This app predicts whether a student will **complete** a training program or **quit**, using their background information, education history, and program attributes.

It uses:
- 🔬 **Machine Learning** (Random Forest, SVM, Logistic Regression, etc.)
- 🧠 **Smart features** like age range alignment, employment status, and program difficulty
- ⚠️ **Manual logic override** for extremely unrealistic ages (because age 85 in a beginner bootcamp? Probably not.)

---

## 🛠 How It Works

1. **Training**  
   - The model is trained using real-world student + program data  
   - Special attention is given to age logic using features like:
     - `Age In Range`
     - `Extreme Age`
     - `Gap to Min/Max Age`
   - We used `GridSearchCV` to find the best model from Logistic Regression, SVM, Random Forest, and Decision Tree

2. **Prediction App (Streamlit)**  
   - A clean and fast interface  
   - User enters student details  
   - Model returns:
     - ✅ Will Complete  
     - ❌ Will Quit  
     - 🎯 Confidence Score  
   - If the student is way outside the age range → we gently throw shade with a warning

---

## 🧪 Try It Locally

Clone this repo:

```bash
git clone https://github.com/Mhndv/Elite_Prediction.git
cd Elite_Prediction
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

---

## 🧠 Features We Love

- 📊 Real-world data with custom feature engineering  
- 🎯 22+ feature columns aligned to model  
- ⚠️ Safety check for extreme age edge cases  
- 🌍 Arabic/localized dataset ready  
- 🌄 Optional background with Tuwaiq mountains 🏔️ (style points!)

---

## 📁 Project Structure

```
├── app.py                      # Streamlit frontend
├── train_cleaned_final.csv     # Main dataset
├── best_model_extreme_age.pkl  # Trained model
├── scaler_extreme_age.pkl      # Feature scaler
├── label_encoders_extreme_age.pkl
├── requirements.txt
└── README.md
```

---

## 📸 Screenshot

<img width="1728" alt="Screenshot 1446-11-20 at 2 10 27 AM" src="https://github.com/user-attachments/assets/ee0bbcec-b883-4bc8-a3ad-0f30cb14ea19" />
