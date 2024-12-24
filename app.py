import streamlit as st
import joblib
import os
import sklearn

model_path = "utils/model.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error("Model file not found. Please upload the decision tree model.")
    st.stop()

st.set_page_config(page_title="Diabetes app", layout="centered")

st.title("🩺 Diabetes App")
st.write("This application aims to enhance the diagnosis of Type 2 Diabetes, reduce healthcare costs, and improve the patient's quality of life.")

with st.form("diabetes_form"):
    st.write("**Patient Information**")

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age:", min_value=0, max_value=100, value=None, step=1)
    with col2:
        gender = st.radio("Gender:", ["Male", "Female"], horizontal=True, index=None)
    with col3:
        polyuria = st.radio("Polyuria (Excessive urination):", ["Yes", "No"], horizontal=True, index=None)

    col4, col5, col6 = st.columns(3)
    with col4:
        polydipsia = st.radio("Polydipsia (Excessive thirst):", ["Yes", "No"], horizontal=True, index=None)
    with col5:
        sudden_weight_loss = st.radio("Sudden weight loss:", ["Yes", "No"], horizontal=True, index=None)
    with col6:
        alopecia = st.radio("Alopecia (Hair loss):", ["Yes", "No"], horizontal=True, index=None)

    submitted = st.form_submit_button("Predict", use_container_width=True, type="primary")

    if submitted and (age is None or gender is None or polyuria is None or polydipsia is None or sudden_weight_loss is None or alopecia is None):
        st.error("Please complete all fields in the form.")

decision_paths = {
    (0, 0, 0): "utils/paths/path_polyuria_no_gender_female_alopecia_no.png",
    (0, 0, 1): "utils/paths/path_polyuria_no_gender_female_alopecia_yes.png",
    (0, 1, 0): "utils/paths/path_polyuria_no_gender_male_polydipsia_no.png",
    (0, 1, 1): "utils/paths/path_polyuria_no_gender_male_polydipsia_yes.png",
    (1, 0, 0): "utils/paths/path_polyuria_yes_age_less_than_69_5.png",
    (1, 1, 0): "utils/paths/path_polyuria_yes_age_greater_than_69_5_sudden_weight_loss_no.png",
    (1, 1, 1): "utils/paths/path_polyuria_yes_age_greater_than_69_5_sudden_weight_loss_yes.png",
}

def get_decision_path(polyuria, gender, polydipsia, age, sudden_weight_loss, alopecia):
    if polyuria == "No":
        if gender == "Female":
            return (0, 0, 0 if alopecia == "No" else 1)
        elif gender == "Male":
            return (0, 1, 0 if polydipsia == "No" else 1)
    elif polyuria == "Yes":
        if age is not None and age <= 69.5:
            return (1, 0, 0)
        elif age is not None and age > 69.5:
            return (1, 1, 0 if sudden_weight_loss == "No" else 1)
    return None

st.subheader("Decision Tree", anchor="tree")

if submitted and (age is not None and gender is not None and polyuria is not None and polydipsia is not None and sudden_weight_loss is not None and alopecia is not None):

    input_data = [
        age,
        1 if gender == "Male" else 0,
        1 if polyuria == "Yes" else 0,
        1 if polydipsia == "Yes" else 0,
        1 if sudden_weight_loss == "Yes" else 0,
        1 if alopecia == "Yes" else 0
    ]

    prediction = model.predict([input_data])[0]
    result = "Diabetic" if prediction == 1 else "Non-diabetic"
    st.write(f"The patient is: **{result}**.")

    decision_key = get_decision_path(polyuria, gender, polydipsia, age, sudden_weight_loss, alopecia)
    image_path = decision_paths.get(decision_key, "utils/paths/init.png")
    st.image(image_path, caption="Decision Path Visualization", use_container_width=True)
else:
    st.write(f"Complete the patient's information.")
    st.image("utils/paths/init.png", caption="Generated Decision Tree", use_container_width=True)

st.markdown("---")
st.markdown(
    """
    **Disclaimer**: This tool is an artificial intelligence-based application for supporting healthcare professionals. It is not a substitute for medical advice, and the healthcare provider's judgment should always prevail.
    """
)
st.markdown("First version v1.1")