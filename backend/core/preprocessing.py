import json
from typing import Any

import pandas as pd


DEFAULT_PATIENT_PROFILE = {
    "race": "Caucasian",
    "gender": "Female",
    "age": "[50-60)",
    "admission_type_id": 1,
    "discharge_disposition_id": 1,
    "admission_source_id": 1,
    "time_in_hospital": 3,
    "num_lab_procedures": 40,
    "num_procedures": 1,
    "num_medications": 10,
    "number_outpatient": 0,
    "number_emergency": 0,
    "number_inpatient": 0,
    "number_diagnoses": 5,
    "diag_1": "250.83",
    "diag_2": "401.9",
    "diag_3": "272.4",
    "max_glu_serum": "None",
    "A1Cresult": "None",
    "metformin": "No",
    "insulin": "No",
    "change": "No",
    "diabetesMed": "No",
}


def map_icd9_to_category(code: Any) -> str:
    if code is None or (isinstance(code, float) and pd.isna(code)):
        return "Other"

    code_str = str(code).strip()
    if not code_str or code_str == "?":
        return "Other"

    if code_str.startswith(("V", "E")):
        return "Other"

    try:
        value = float(code_str)
    except ValueError:
        return "Other"

    if 390 <= value <= 459 or value == 785:
        return "Circulatory"
    if 460 <= value <= 519 or value == 786:
        return "Respiratory"
    if 520 <= value <= 579 or value == 787:
        return "Digestive"
    if int(value) == 250:
        return "Diabetes"
    if 800 <= value <= 999:
        return "Injury"
    if 710 <= value <= 739:
        return "Musculoskeletal"
    if 580 <= value <= 629 or value == 788:
        return "Genitourinary"
    if 140 <= value <= 239:
        return "Neoplasms"
    return "Other"


def encode_medication_value(value: Any) -> int:
    mapping = {
        "Down": 0,
        "No": 1,
        "Steady": 2,
        "Up": 3,
    }
    return mapping.get(str(value).strip(), mapping["No"])


def encode_change_value(value: Any) -> int:
    mapping = {
        "Ch": 0,
        "No": 1,
    }
    return mapping.get(str(value).strip(), mapping["No"])


def encode_diabetesmed_value(value: Any) -> int:
    mapping = {
        "No": 0,
        "Yes": 1,
    }
    return mapping.get(str(value).strip(), mapping["No"])


def normalize_patient_profile(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = DEFAULT_PATIENT_PROFILE.copy()
    normalized.update({k: v for k, v in payload.items() if v is not None})
    return normalized


def build_ann_feature_vector(
    patient_profile: dict[str, Any],
    expected_columns: list[str],
) -> list[float]:
    profile = normalize_patient_profile(patient_profile)

    row = pd.DataFrame([profile])

    for col in ("diag_1", "diag_2", "diag_3"):
        row[col] = row[col].apply(map_icd9_to_category)

    row["metformin"] = row["metformin"].apply(encode_medication_value)
    row["insulin"] = row["insulin"].apply(encode_medication_value)
    row["change"] = row["change"].apply(encode_change_value)
    row["diabetesMed"] = row["diabetesMed"].apply(encode_diabetesmed_value)

    categorical_columns = [
        "race",
        "gender",
        "age",
        "diag_1",
        "diag_2",
        "diag_3",
        "max_glu_serum",
        "A1Cresult",
    ]

    row = pd.get_dummies(
        row,
        columns=categorical_columns,
        drop_first=True,
    )

    row = row.reindex(columns=expected_columns, fill_value=0)

    return row.iloc[0].astype(float).tolist()


def parse_signal_payload(signal_input: Any) -> list[float]:
    if isinstance(signal_input, list):
        return [float(value) for value in signal_input]

    if isinstance(signal_input, str):
        signal_text = signal_input.strip()

        if not signal_text:
            raise ValueError("Signal input is empty.")

        try:
            parsed = json.loads(signal_text)
            if isinstance(parsed, list):
                return [float(value) for value in parsed]
        except json.JSONDecodeError:
            pass

        flattened = signal_text.replace("\n", ",").replace("\r", ",")
        values = [part.strip() for part in flattened.split(",") if part.strip()]
        return [float(value) for value in values]

    raise ValueError("Signal must be provided as a list or comma-separated string.")


def validate_signal_187(signal: list[float]) -> list[float]:
    if len(signal) != 187:
        raise ValueError(f"RNN expects exactly 187 ECG values. Received {len(signal)}.")
    return signal
