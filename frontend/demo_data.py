DEMO_PATIENTS = {
    "Select a demo patient...": None,
    "Healthy Recovery (Low Risk)": {
        "race": "Caucasian", "gender": "Female", "age": "[40-50)",
        "admission_type_id": 3, "discharge_disposition_id": 1, "admission_source_id": 1,
        "time_in_hospital": 2, "num_lab_procedures": 15, "num_procedures": 0,
        "num_medications": 5, "number_outpatient": 0, "number_emergency": 0,
        "number_inpatient": 0, "number_diagnoses": 3,
        "diag_1": "V57", "diag_2": "V58", "diag_3": "250",
        "max_glu_serum": "None", "A1Cresult": "None",
        "metformin": "No", "insulin": "No", "change": "No", "diabetesMed": "No"
    },
    "Critical Patient (High Risk)": {
        "race": "AfricanAmerican", "gender": "Male", "age": "[70-80)",
        "admission_type_id": 1, "discharge_disposition_id": 3, "admission_source_id": 7,
        "time_in_hospital": 12, "num_lab_procedures": 65, "num_procedures": 4,
        "num_medications": 25, "number_outpatient": 1, "number_emergency": 2,
        "number_inpatient": 3, "number_diagnoses": 9,
        "diag_1": "428", "diag_2": "414", "diag_3": "250.02",
        "max_glu_serum": ">300", "A1Cresult": ">8",
        "metformin": "Up", "insulin": "Up", "change": "Ch", "diabetesMed": "Yes"
    }
}

DEMO_ECGS = {
    "Normal Beat": ",".join(["0.5" if i in range(70,80) else "0.1" for i in range(187)]),
    "PVC (Premature Ventricular Contraction)": ",".join(["0.9" if i in range(90,110) else "0.0" for i in range(187)]),
    "Supraventricular": ",".join(["0.7" if i % 20 < 5 else "0.2" for i in range(187)]),
}
