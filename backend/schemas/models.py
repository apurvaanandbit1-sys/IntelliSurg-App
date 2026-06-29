from typing import Any, List

from pydantic import BaseModel, Field


class ANNRequest(BaseModel):
    features: List[float]


class RNNRequest(BaseModel):
    signal: List[float]


class SignalTextRequest(BaseModel):
    signal_text: str = Field(..., description="Comma-separated or JSON-array ECG beat values.")


class PatientProfileRequest(BaseModel):
    race: str = "Caucasian"
    gender: str = "Female"
    age: str = "[50-60)"
    admission_type_id: int = 1
    discharge_disposition_id: int = 1
    admission_source_id: int = 1
    time_in_hospital: int = 3
    num_lab_procedures: int = 40
    num_procedures: int = 1
    num_medications: int = 10
    number_outpatient: int = 0
    number_emergency: int = 0
    number_inpatient: int = 0
    number_diagnoses: int = 5
    diag_1: str = "250.83"
    diag_2: str = "401.9"
    diag_3: str = "272.4"
    max_glu_serum: str = "None"
    A1Cresult: str = "None"
    metformin: str = "No"
    insulin: str = "No"
    change: str = "No"
    diabetesMed: str = "No"


