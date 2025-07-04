from flask import Flask , request , jsonify
import pandas as pd
import numpy as np
import pickle
import ast
from flask_cors import CORS , cross_origin
from werkzeug.exceptions import HTTPException
from statistics import mode
app = Flask(__name__)
CORS(app , support_credentials=True)
#loading the database
precautions = pd.read_csv("datasets/new_precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medication = pd.read_csv("datasets/medications.csv")
diets = pd.read_csv("datasets/diets.csv")

#loading the models
KNN = pickle.load(open("models/KNN.pkl",'rb'))
RF = pickle.load(open("models/RF.pkl",'rb'))
SVC = pickle.load(open("models/SVC.pkl",'rb'))
NB = pickle.load(open("models/NB.pkl",'rb'))

def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis]['Precautions']
    pre = [pre for pre in pre.values]

    med = medication[medication['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis] ['workout']

    return desc,pre,med,die,wrkout
symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = ['(vertigo) Paroymsal  Positional Vertigo', 'AIDS', 'Acne','Alcoholic hepatitis', 'Allergy', 'Arthritis', 'Bronchial Asthma',
'Cervical spondylosis', 'Chicken pox', 'Chronic cholestasis','Common Cold', 'Dengue', 'Diabetes ','Dimorphic hemmorhoids(piles)', 'Drug Reaction',
'Fungal infection', 'GERD', 'Gastroenteritis', 'Heart attack','Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E','Hypertension ', 'Hyperthyroidism', 'Hypoglycemia','Hypothyroidism', 'Impetigo', 'Jaundice', 'Malaria', 'Migraine','Osteoarthristis', 'Paralysis (brain hemorrhage)','Peptic ulcer diseae', 'Pneumonia', 'Psoriasis', 'Tuberculosis','Typhoid', 'Urinary tract infection', 'Varicose veins','hepatitis A']
# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))

    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return mode([diseases_list[KNN.predict([input_vector])[0]] , diseases_list[RF.predict([input_vector])[0]] , diseases_list[NB.predict([input_vector])[0]] , diseases_list[SVC.predict([input_vector])[0]]])
def get_formatted_data(disease):
    desc, pre, med, die, wrkout = helper(disease)
    pre = pre[0]
    med = med[0]
    die = die[0]
    tmp = []
    med = ast.literal_eval(med)
    die = ast.literal_eval(die)
    pre = ast.literal_eval(pre)
    for i in wrkout:
        tmp.append(i)
    wrkout = tmp
    data = {
        "disease" : disease,
        "description" : desc,
        "precautions" : pre,
        "medications" : med,
        "diet" : die,
        "workout" : wrkout
    }
    return jsonify(data)
#routes

@app.route('/predict' , methods = ['POST'])
@cross_origin(supports_credentials=True)
def predict():
    try:
        json_data = request.json
        symptoms = []
        if("symptoms" in json_data):
            symptoms = json_data["symptoms"]
        else:
            return jsonify({'error': 'Symptoms key is missing from JSON data'}), 400
        predicted_disease = get_predicted_value(symptoms)

        data = get_formatted_data(predicted_disease)

        data.headers['Content-Type'] = 'application/json'
        data.status = 200
        return data
    except HTTPException as e:
        # Catch HTTP exceptions and return appropriate error response
        print(e)
        return jsonify({'HTTP error occured': str(e)}), e.code

    except Exception as e:
        # Catch all other exceptions and return a generic error response
        print(e)
        return jsonify({'Error Occured': 'Internal Server Error'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

