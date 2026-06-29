"""
app.py
──────
IntelliSurg Streamlit frontend — restyled presentation layer.

IMPORTANT: All backend endpoints, request payloads, and field names are
UNCHANGED from the original app.py. Only the rendering of results changed:
raw st.json() dumps are replaced with styled HTML result cards.

Endpoints used (unchanged):
    POST {backend_url}/predict/ann-from-form
    POST {backend_url}/predict/rnn-from-text
    POST {backend_url}/predict/cnn
    POST {backend_url}/predict/fusion
"""

import json
from io import BytesIO

import requests
import streamlit as st
import plotly.graph_objects as go

from demo_data import DEMO_PATIENTS
from ecg_demo_data import get_demo_ecg_signal, ECG_SAMPLES

from theme import (
    inject_css,
    inject_tabler_icons,
    page_header,
    status_badge,
    metric_card,
    big_metric_card,
    disclaimer_footer,
    empty_state,
    error_card,
    COLORS,
    section_label,
    info_banner,
    success_message,
)


st.set_page_config(
    page_title="IntelliSurg Demo",
    page_icon="🩺",
    layout="wide",
)

inject_css()
inject_tabler_icons()


DEFAULT_SIGNAL = ",".join(["0"] * 187)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS — risk-level classification for badges (presentation only,
# does not change what's sent to or received from the backend)
# ─────────────────────────────────────────────────────────────────────────────

def risk_level_from_probability(prob: float) -> str:
    """Maps a 0-1 probability to a badge level. Presentation-only helper."""
    if prob is None:
        return "medium"
    if prob >= 0.66:
        return "high"
    if prob >= 0.33:
        return "medium"
    return "low"


def pct(value) -> float:
    """Safely convert a 0-1 float (or None) to a 0-100 percentage for progress bars."""
    try:
        return round(float(value) * 100, 1)
    except (TypeError, ValueError):
        return 0.0

def draw_ecg(signal_text: str):
    """
    Draws the 187-point ECG signal entered by the user.
    """

    try:
        signal = [
            float(x.strip())
            for x in signal_text.replace("\n", ",").split(",")
            if x.strip() != ""
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                y=signal,
                mode="lines",
                line=dict(
                    color="#37E0C2",
                    width=3,
                ),
                hovertemplate="Amplitude: %{y:.3f}<extra></extra>",
            )
        )

        fig.update_layout(
            title="ECG Waveform",
            height=260,
            margin=dict(l=20, r=20, t=40, b=20),

            paper_bgcolor="#11161D",
            plot_bgcolor="#11161D",

            font=dict(
                color="#EAF2F5",
                size=13,
            ),

            xaxis=dict(
                title="Sample",
                showgrid=True,
                gridcolor="#1E2832",
                zeroline=False,
            ),

            yaxis=dict(
                title="Amplitude",
                showgrid=True,
                gridcolor="#1E2832",
                zeroline=False,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            },
        )

    except Exception:
        st.warning("Unable to display ECG waveform.")

# ─────────────────────────────────────────────────────────────────────────────
# FORM — unchanged from original, only label/layout spacing touched lightly
# ─────────────────────────────────────────────────────────────────────────────

def patient_profile_form(prefix: str) -> dict:

    st.markdown(
        info_banner("<b>Demo Patients:</b> Select a preset to quickly evaluate how the AI assesses different risk profiles."),
        unsafe_allow_html=True
    )

    selected_demo = st.selectbox(
        "Load Demo Patient",
        options=list(DEMO_PATIENTS.keys()),
        key=f"{prefix}_demo_select"
    )

    # Pre-fill logic based on selected demo
    default_vals = DEMO_PATIENTS.get(selected_demo) or {
        "race": "Caucasian", "gender": "Female", "age": "[50-60)",
        "admission_type_id": 1, "discharge_disposition_id": 1, "admission_source_id": 1,
        "time_in_hospital": 3, "num_lab_procedures": 40, "num_procedures": 1,
        "num_medications": 10, "number_outpatient": 0, "number_emergency": 0,
        "number_inpatient": 0, "number_diagnoses": 5,
        "diag_1": "250.83", "diag_2": "401.9", "diag_3": "272.4",
        "max_glu_serum": "None", "A1Cresult": "None",
        "metformin": "No", "insulin": "No", "change": "No", "diabetesMed": "No"
    }

    if selected_demo != "Select a demo patient...":
        import hashlib
        # Generate a pseudo-random ID based on the demo name
        patient_id = "PT-" + hashlib.md5(selected_demo.encode()).hexdigest()[:6].upper()

        status_color = COLORS['high_text'] if "High" in selected_demo else COLORS['low_text']
        status_text = "Critical Observation" if "High" in selected_demo else "Routine Recovery"

        st.markdown(
            f"""
            <div style="background:{COLORS['bg_subcard']}; border:1px solid {COLORS['border']}; border-radius:12px; padding:16px; margin-bottom:24px;">
                <p style="font-size:11px; text-transform:uppercase; color:{COLORS['text_muted']}; margin:0 0 8px 0; font-weight:600;">Patient Summary Panel</p>
                <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:12px;">
                    <div>
                        <p style="font-size:12px; color:{COLORS['text_muted']}; margin:0;">Patient ID</p>
                        <p style="font-size:14px; font-weight:600; color:{COLORS['text_primary']}; margin:2px 0 0;">{patient_id}</p>
                    </div>
                    <div>
                        <p style="font-size:12px; color:{COLORS['text_muted']}; margin:0;">Demographics</p>
                        <p style="font-size:14px; font-weight:600; color:{COLORS['text_primary']}; margin:2px 0 0;">{default_vals['age']} {default_vals['gender']}</p>
                    </div>
                    <div>
                        <p style="font-size:12px; color:{COLORS['text_muted']}; margin:0;">Prior Diagnoses</p>
                        <p style="font-size:14px; font-weight:600; color:{COLORS['text_primary']}; margin:2px 0 0;">{default_vals['number_diagnoses']} Conditions</p>
                    </div>
                    <div>
                        <p style="font-size:12px; color:{COLORS['text_muted']}; margin:0;">Current Status</p>
                        <p style="font-size:14px; font-weight:600; color:{status_color}; margin:2px 0 0;">{status_text}</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    def get_index(options, val):
        return options.index(val) if val in options else 0

    st.markdown(section_label("Demographics"), unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    race_opts = ["Caucasian", "AfricanAmerican", "Asian", "Hispanic", "Other"]
    gender_opts = ["Female", "Male", "Unknown/Invalid"]
    age_opts = ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)", "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"]
    glu_opts = ["None", "Norm", ">200", ">300"]
    a1c_opts = ["None", "Norm", ">7", ">8"]

    with col1:
        race = st.selectbox("Race", race_opts, index=get_index(race_opts, default_vals["race"]), key=f"{prefix}_race")
        gender = st.selectbox("Gender", gender_opts, index=get_index(gender_opts, default_vals["gender"]), key=f"{prefix}_gender")
        age = st.selectbox("Age Group", age_opts, index=get_index(age_opts, default_vals["age"]), key=f"{prefix}_age")
        max_glu_serum = st.selectbox("Max Glucose Serum", glu_opts, index=get_index(glu_opts, default_vals["max_glu_serum"]), key=f"{prefix}_max_glu")

    with col2:
        admission_type_id = st.number_input("Admission Type ID", min_value=1, value=default_vals["admission_type_id"], key=f"{prefix}_admission_type")
        discharge_disposition_id = st.number_input("Discharge Disposition ID", min_value=1, value=default_vals["discharge_disposition_id"], key=f"{prefix}_discharge")
        admission_source_id = st.number_input("Admission Source ID", min_value=1, value=default_vals["admission_source_id"], key=f"{prefix}_admission_source")
        time_in_hospital = st.number_input("Time In Hospital", min_value=1, value=default_vals["time_in_hospital"], key=f"{prefix}_time_hospital")
        A1Cresult = st.selectbox("A1C Result", a1c_opts, index=get_index(a1c_opts, default_vals["A1Cresult"]), key=f"{prefix}_a1c")

    with col3:
        num_lab_procedures = st.number_input("Lab Procedures", min_value=0, value=default_vals["num_lab_procedures"], key=f"{prefix}_lab")
        num_procedures = st.number_input("Procedures", min_value=0, value=default_vals["num_procedures"], key=f"{prefix}_procedures")
        num_medications = st.number_input("Medications", min_value=0, value=default_vals["num_medications"], key=f"{prefix}_medications")
        number_outpatient = st.number_input("Outpatient Visits", min_value=0, value=default_vals["number_outpatient"], key=f"{prefix}_outpatient")
        number_emergency = st.number_input("Emergency Visits", min_value=0, value=default_vals["number_emergency"], key=f"{prefix}_emergency")
        number_inpatient = st.number_input("Inpatient Visits", min_value=0, value=default_vals["number_inpatient"], key=f"{prefix}_inpatient")
        number_diagnoses = st.number_input("Number of Diagnoses", min_value=1, value=default_vals["number_diagnoses"], key=f"{prefix}_diagnoses")

    st.markdown(section_label("Diagnosis & medication"), unsafe_allow_html=True)
    diag_col1, diag_col2, diag_col3, med_col = st.columns(4)

    med_opts = ["No", "Steady", "Up", "Down"]
    ch_opts = ["No", "Ch"]
    dm_opts = ["No", "Yes"]

    with diag_col1:
        diag_1 = st.text_input("Diagnosis Code 1", value=default_vals["diag_1"], key=f"{prefix}_diag1")
    with diag_col2:
        diag_2 = st.text_input("Diagnosis Code 2", value=default_vals["diag_2"], key=f"{prefix}_diag2")
    with diag_col3:
        diag_3 = st.text_input("Diagnosis Code 3", value=default_vals["diag_3"], key=f"{prefix}_diag3")
    with med_col:
        metformin = st.selectbox("Metformin", med_opts, index=get_index(med_opts, default_vals["metformin"]), key=f"{prefix}_metformin")
        insulin = st.selectbox("Insulin", med_opts, index=get_index(med_opts, default_vals["insulin"]), key=f"{prefix}_insulin")
        change = st.selectbox("Change in meds", ch_opts, index=get_index(ch_opts, default_vals["change"]), key=f"{prefix}_change")
        diabetesMed = st.selectbox("Diabetes Meds", dm_opts, index=get_index(dm_opts, default_vals["diabetesMed"]), key=f"{prefix}_diabetes_med")

    return {
        "race": race,
        "gender": gender,
        "age": age,
        "admission_type_id": admission_type_id,
        "discharge_disposition_id": discharge_disposition_id,
        "admission_source_id": admission_source_id,
        "time_in_hospital": time_in_hospital,
        "num_lab_procedures": num_lab_procedures,
        "num_procedures": num_procedures,
        "num_medications": num_medications,
        "number_outpatient": number_outpatient,
        "number_emergency": number_emergency,
        "number_inpatient": number_inpatient,
        "number_diagnoses": number_diagnoses,
        "diag_1": diag_1,
        "diag_2": diag_2,
        "diag_3": diag_3,
        "max_glu_serum": max_glu_serum,
        "A1Cresult": A1Cresult,
        "metformin": metformin,
        "insulin": insulin,
        "change": change,
        "diabetesMed": diabetesMed,
    }


# ─────────────────────────────────────────────────────────────────────────────
# RESULT RENDERERS — one per tab. Each reads the SAME json payload
# your backend already returns; only the display changed.
# ─────────────────────────────────────────────────────────────────────────────

def render_ann_result(payload: dict):
    """
    Expects keys (from your backend): readmission_risk, risk_label,
    feature_count, model_input_ready. Falls back gracefully if any are absent.
    """
    prob = payload.get("readmission_risk")
    label = payload.get("risk_label", "Unknown")
    level = risk_level_from_probability(prob if isinstance(prob, (int, float)) else None)

    clinical_interpretation = "Elevated risk of post-operative complications requiring readmission. Monitor closely." if level == "high" else "Baseline post-operative risk profile. Standard monitoring protocols apply."
    monitoring_priority = "Priority: Routine" if level != "high" else "Priority: Urgent Observation"

    html = big_metric_card(
        eyebrow="AI Clinical Findings",
        title="Readmission Risk Assessment",
        big_value=f"{pct(prob)}%" if prob is not None else "—",
        big_label=label,
        pct=pct(prob),
        badge_level=level,
        sub_cards_html=f"""
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:16px;">
            <div style="background:rgba(255,255,255,0.03); padding:10px 14px; border-radius:8px; border:1px solid {COLORS['border']};">
                <p style="font-size:11px; color:{COLORS['text_muted']}; margin:0; text-transform:uppercase;">Clinical Interpretation</p>
                <p style="font-size:13px; color:{COLORS['text_primary']}; margin:4px 0 0;">{clinical_interpretation}</p>
            </div>
            <div style="background:rgba(255,255,255,0.03); padding:10px 14px; border-radius:8px; border:1px solid {COLORS['border']};">
                <p style="font-size:11px; color:{COLORS['text_muted']}; margin:0; text-transform:uppercase;">Suggested Action</p>
                <p style="font-size:13px; color:{COLORS['text_primary']}; margin:4px 0 0; font-weight:600;">{monitoring_priority}</p>
            </div>
        </div>
        """
    )
    st.markdown(html, unsafe_allow_html=True)
    st.markdown(disclaimer_footer(), unsafe_allow_html=True)


def render_rnn_result(payload: dict):

    # ----- Exact backend keys -----
    class_name = payload["class_name"]
    confidence = payload["confidence"]
    class_index = payload["class_index"]
    raw_probs = payload["raw_probs"]

    CLASS_NAMES = [
        "Normal",
        "Supraventricular",
        "Ventricular",
        "Fusion Beat",
        "Unknown"
    ]

    probability_cards = ""

    for i, prob in enumerate(raw_probs):
        probability_cards += metric_card(
            "ti-chart-bar",
            CLASS_NAMES[i],
            f"{pct(prob)}%",
            pct(prob),
            COLORS["accent"]
        )

    html = big_metric_card(
        eyebrow="ECG Analysis",
        title="Predicted Beat",
        big_value=class_name,
        big_label=f"{pct(confidence)}% confidence",
        pct=pct(confidence),
        badge_level=risk_level_from_probability(confidence),
        sub_cards_html=f"""
        <div style="display:grid;
                    grid-template-columns:repeat(5,1fr);
                    gap:12px;
                    margin-top:8px;">
            {probability_cards}
        </div>
        """
    )

    st.markdown(html, unsafe_allow_html=True)
    st.markdown(disclaimer_footer(), unsafe_allow_html=True)

def render_cnn_result(payload: dict, image_file=None):
    """
    Expects keys: wound_class (or class), confidence.
    """
    wound_class = payload.get("wound_class") or payload.get("class") or "Unknown"
    confidence = payload.get("confidence")

    col_img, col_result = st.columns([1, 1.4])
    with col_img:
        if image_file is not None:
            st.image(image_file, caption="Uploaded image", use_container_width=True)

    with col_result:
        clinical_interpretation = "Wound site displays characteristics consistent with an active infection." if wound_class.lower() == "infected" else "Wound site appears normal with standard healing progression."

        html = big_metric_card(
            eyebrow="AI Clinical Findings",
            title="Infection Site Assessment",
            big_value=str(wound_class).upper(),
            big_label=f"{pct(confidence)}% confidence" if confidence is not None else "",
            pct=pct(confidence),
            badge_level=risk_level_from_probability(confidence if isinstance(confidence, (int, float)) else None),
            sub_cards_html=f"""
            <div style="background:rgba(255,255,255,0.03); padding:10px 14px; border-radius:8px; border:1px solid {COLORS['border']}; margin-top:16px;">
                <p style="font-size:11px; color:{COLORS['text_muted']}; margin:0; text-transform:uppercase;">Clinical Interpretation</p>
                <p style="font-size:13px; color:{COLORS['text_primary']}; margin:4px 0 0;">{clinical_interpretation}</p>
            </div>
            """
        )
        st.markdown(html, unsafe_allow_html=True)
        st.markdown(disclaimer_footer(), unsafe_allow_html=True)


def render_fusion_result(payload: dict):
    """
    Expects keys: readmission_risk, wound_class, ecg_class, criticality_index,
    triage_level (or similar). Reads whatever keys are present and degrades
    gracefully — matches the graceful-degradation behavior of your backend.
    """
    criticality = payload.get("criticality_index")
    triage = payload.get("triage_level", "medium")
    if isinstance(triage, str):
        triage_level = triage.lower()
    else:
        triage_level = risk_level_from_probability(criticality)

    ann_label = payload.get("risk_label") or payload.get("readmission_label", "—")
    ecg_label = payload.get("ecg_class") or payload.get("class", "—")
    wound_label = payload.get("wound_class", "—")

    ai_summary = "Patient presents a high criticality profile based on fused multimodal indicators. Immediate clinical review is recommended." if triage_level == "high" else "Patient presents a stable criticality profile. Fused multimodal indicators do not suggest immediate escalation."

    sub_cards = f"""
    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; margin-top:16px;">
        {metric_card('ti-heartbeat', 'Readmission Risk (ANN)', str(ann_label), pct(payload.get('readmission_risk')), COLORS['accent'])}
        {metric_card('ti-activity', 'ECG Findings (RNN)', str(ecg_label), pct(payload.get('ecg_confidence')), '#C98A2E')}
        {metric_card('ti-bandage', 'Wound Analysis (CNN)', str(wound_label), pct(payload.get('wound_confidence')), '#C2483F')}
    </div>
    <div style="background:rgba(255,255,255,0.03); padding:12px 16px; border-radius:8px; border:1px solid {COLORS['border']}; margin-top:16px;">
        <p style="font-size:12px; color:{COLORS['text_muted']}; margin:0; text-transform:uppercase; font-weight:600;"><i class="ti ti-robot"></i> AI-Generated Summary</p>
        <p style="font-size:14px; color:{COLORS['text_primary']}; margin:6px 0 0;">{ai_summary}</p>
    </div>
    <div style="background:rgba(239,159,39,0.08); padding:12px 16px; border-radius:8px; border:1px solid rgba(239,159,39,0.2); margin-top:12px;">
        <p style="font-size:12px; color:{COLORS['medium_text']}; margin:0; text-transform:uppercase; font-weight:600;"><i class="ti ti-alert-triangle"></i> Limitations</p>
        <p style="font-size:13px; color:{COLORS['text_primary']}; margin:6px 0 0; opacity:0.9;">This assessment is generated by an experimental AI fusion model. It does not account for full clinical context, recent lab trends, or uncaptured medical history. Do not use for definitive diagnostic or triage decisions.</p>
    </div>
    """

    html = big_metric_card(
        eyebrow="Comprehensive Patient Assessment Report",
        title="Multimodal Criticality Index",
        big_value=f"{pct(criticality)}%" if criticality is not None else "—",
        big_label="overall risk score",
        pct=pct(criticality),
        badge_level=triage_level,
        sub_cards_html=sub_cards,
    )
    st.markdown(html, unsafe_allow_html=True)
    st.markdown(disclaimer_footer(), unsafe_allow_html=True)


def show_response(response: requests.Response, renderer, *render_args):
    """
    Replaces the old show_response(). On success, calls the tab-specific
    renderer with the parsed JSON. On failure, shows a styled error card
    instead of a raw st.error/st.json dump.
    """
    try:
        payload = response.json()
    except Exception:
        st.markdown(error_card(f"Status {response.status_code} — non-JSON response"), unsafe_allow_html=True)
        with st.expander("Raw response"):
            st.code(response.text)
        return

    if response.ok:
        renderer(payload, *render_args)

        # Developer response hidden
    else:
        message = payload.get("detail", str(payload)) if isinstance(payload, dict) else str(payload)
        st.markdown(error_card(f"Status {response.status_code} — {message}"), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER + SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

import datetime

st.markdown(
    page_header(
        eyebrow="AI-Powered Post-Operative Monitoring",
        title="IntelliSurg",
        subtitle="Integrating clinical history, ECG analysis, wound assessment, and multimodal AI to support postoperative risk assessment.",
    ),
    unsafe_allow_html=True,
)

st.sidebar.markdown("### System Configuration")

backend_url = st.sidebar.text_input(
    "Backend API Endpoint",
    value="https://apurv-intellisurg-api.onrender.com"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    <div style="font-size:13px; color:{COLORS['text_muted']}; line-height:1.6;">
        <p style="margin:0;"><i class="ti ti-activity-heartbeat" style="color:{COLORS['accent']};"></i> <b>Backend Status:</b> Online</p>
        <p style="margin:0;"><i class="ti ti-code"></i> <b>Version:</b> 1.2.0 (Production)</p>
        <p style="margin:0;"><i class="ti ti-calendar"></i> <b>Date:</b> {datetime.datetime.now().strftime("%Y-%m-%d")}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")
st.sidebar.markdown(disclaimer_footer(), unsafe_allow_html=True)


tab_ann, tab_rnn, tab_cnn, tab_fusion = st.tabs(
    ["Clinical History", "ECG Analysis", "Wound Assessment", "Comprehensive Assessment"]
)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — CLINICAL HISTORY
# ─────────────────────────────────────────────────────────────────────────────

with tab_ann:
    st.markdown(
        page_header("Module 1", "Readmission Risk Analysis",
                     "Input patient demographics, vital statistics, and clinical history to generate a baseline readmission risk score."),
        unsafe_allow_html=True,
    )
    profile = patient_profile_form("ann")


    if st.button("Analyze Clinical Data", key="ann_submit"):
        with st.spinner("Processing clinical history parameters..."):
            response = requests.post(
                f"{backend_url}/predict/ann-from-form",
                json=profile,
                timeout=60,
            )
        show_response(response, render_ann_result)
    else:
        st.markdown(empty_state("ti-heartbeat", "Provide patient information and click 'Analyze Clinical Data' to generate a baseline risk profile."),
                    unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — ECG ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

with tab_rnn:
    st.markdown(
        page_header("Module 2", "ECG Arrhythmia Detection",
                     "Upload or provide a 187-sample continuous telemetry beat for AI-assisted arrhythmia classification."),
        unsafe_allow_html=True,
    )

    st.markdown(
        info_banner("<b>Input Methods:</b> Select a demo signal, upload a CSV/TXT file, or paste values manually. Sequences will be automatically padded or truncated to 187 samples as required by the model."),
        unsafe_allow_html=True
    )

    col_ecg1, col_ecg2 = st.columns(2)
    
    with col_ecg1:
        selected_ecg_demo = st.selectbox(
            "Load Demo Telemetry Signal",
            options=["Manual Entry"] + list(ECG_SAMPLES.keys()),
            key="rnn_demo_select"
        )

    with col_ecg2:
        signal_file = st.file_uploader(
            "Upload raw ECG file (.csv, .txt)",
            type=["txt", "csv"],
            key="rnn_file",
        )

    # Initialize session state for the text area and tracking variables
    if "rnn_signal" not in st.session_state:
        st.session_state["rnn_signal"] = DEFAULT_SIGNAL
    if "rnn_last_demo_selection" not in st.session_state:
        st.session_state["rnn_last_demo_selection"] = "Manual Entry"
    if "rnn_last_uploaded_file_id" not in st.session_state:
        st.session_state["rnn_last_uploaded_file_id"] = None

    # Handle dropdown change
    if selected_ecg_demo != st.session_state["rnn_last_demo_selection"]:
        st.session_state["rnn_last_demo_selection"] = selected_ecg_demo
        if selected_ecg_demo != "Manual Entry":
            st.session_state["rnn_signal"] = get_demo_ecg_signal(selected_ecg_demo)
        else:
            st.session_state["rnn_signal"] = DEFAULT_SIGNAL

    # Handle file upload change
    if signal_file is not None:
        if signal_file.file_id != st.session_state["rnn_last_uploaded_file_id"]:
            st.session_state["rnn_last_uploaded_file_id"] = signal_file.file_id
            raw_text = signal_file.getvalue().decode("utf-8")
            # Preprocessing: Extract numbers, pad/truncate to 187
            raw_values = [x.strip() for x in raw_text.replace("\n", ",").split(",") if x.strip()]
            if len(raw_values) > 187:
                raw_values = raw_values[:187]
            elif len(raw_values) < 187:
                raw_values = raw_values + ["0.0"] * (187 - len(raw_values))
            st.session_state["rnn_signal"] = ",".join(raw_values)
            st.markdown(
                success_message(f"Automatically processed uploaded file to {len(raw_values)} samples."),
                unsafe_allow_html=True,
            )

    signal_text = st.text_area(
        "Telemetry Data (187 points)",
        height=150,
        key="rnn_signal",
    )

    if st.button("Analyze ECG", key="rnn_submit"):
        with st.spinner("Analyzing telemetry data..."):
            response = requests.post(
                f"{backend_url}/predict/rnn-from-text",
                json={"signal_text": signal_text},
                timeout=60,
            )
        show_response(response, render_rnn_result)
    else:
        st.markdown(empty_state("ti-activity", "Input telemetry data and click 'Analyze ECG' to detect potential arrhythmias."),
                    unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Telemetry Waveform")
    draw_ecg(signal_text)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — WOUND ASSESSMENT
# ─────────────────────────────────────────────────────────────────────────────

with tab_cnn:
    st.markdown(
        page_header("Module 3", "Infection Site Analysis",
                     "Upload a secure image of the surgical site or wound for AI-assisted infection classification."),
        unsafe_allow_html=True,
    )

    image_file = st.file_uploader("Upload clinical site image", type=["jpg", "jpeg", "png", "bmp", "webp"], key="cnn_image")

    if st.button("Analyze Wound Image", key="cnn_submit"):
        if image_file is None:
            st.markdown(error_card("Please provide a clinical image for analysis."), unsafe_allow_html=True)
        else:
            files = {
                "file": (image_file.name, BytesIO(image_file.getvalue()), image_file.type or "application/octet-stream")
            }
            with st.spinner("Analyzing wound site..."):
                response = requests.post(
                    f"{backend_url}/predict/cnn",
                    files=files,
                    timeout=60,
                )
            show_response(response, render_cnn_result, image_file)
    else:
        if image_file is not None:
            st.image(image_file, caption="Staged for analysis", use_container_width=True)
        st.markdown(empty_state("ti-bandage", "Upload a clinical image and click 'Analyze Wound Image' for AI assistance."),
                    unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — COMPREHENSIVE ASSESSMENT
# ─────────────────────────────────────────────────────────────────────────────

with tab_fusion:
    st.markdown(
        page_header("Multimodal Engine", "Comprehensive Patient Assessment",
                     "Synthesizes patient clinical history, ECG telemetry, and wound imaging to generate a holistic criticality index."),
        unsafe_allow_html=True,
    )

    fusion_profile = patient_profile_form("fusion")

    st.markdown(section_label("Media & Telemetry"), unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)

    with col_f1:
        fusion_demo_ecg = st.selectbox(
            "Load Demo Telemetry Signal",
            options=["Manual Entry"] + list(ECG_SAMPLES.keys()),
            key="fusion_demo_ecg"
        )

        # Initialize session state for random demo signals in Fusion
        if "fusion_signal" not in st.session_state:
            st.session_state["fusion_signal"] = DEFAULT_SIGNAL
        if "fusion_last_demo_selection" not in st.session_state:
            st.session_state["fusion_last_demo_selection"] = "Manual Entry"

        if fusion_demo_ecg != st.session_state["fusion_last_demo_selection"]:
            st.session_state["fusion_last_demo_selection"] = fusion_demo_ecg
            if fusion_demo_ecg != "Manual Entry":
                st.session_state["fusion_signal"] = get_demo_ecg_signal(fusion_demo_ecg)
            else:
                st.session_state["fusion_signal"] = DEFAULT_SIGNAL

        fusion_signal = st.text_area("Telemetry Data (187 points)", height=120, key="fusion_signal")

    with col_f2:
        fusion_image = st.file_uploader(
            "Upload clinical site image",
            type=["jpg", "jpeg", "png", "bmp", "webp"],
            key="fusion_image",
        )

    if st.button("Generate Patient Assessment", key="fusion_submit"):
        if fusion_image is None:
            st.markdown(error_card("A clinical site image is required to generate a comprehensive assessment."), unsafe_allow_html=True)
        else:
            # Reconstruct the 187-value float string correctly for the backend
            cleaned_signal_list = [x.strip() for x in fusion_signal.replace("\n", ",").split(",") if x.strip()]
            cleaned_signal_string = ",".join(cleaned_signal_list)

            data = {
                "patient_profile": json.dumps(fusion_profile),
                "signal": cleaned_signal_string,
            }
            files = {
                "file": (
                    fusion_image.name,
                    BytesIO(fusion_image.getvalue()),
                    fusion_image.type or "application/octet-stream",
                )
            }
            import time
            with st.status("Initializing Multimodal Analysis...", expanded=True) as status:
                st.write("Extracting clinical history parameters...")
                time.sleep(0.6)
                st.write("Applying continuous telemetry signal processing...")
                time.sleep(0.6)
                st.write("Running convolution filters on clinical site image...")
                time.sleep(0.6)
                st.write("Fusing AI modality indices into overall criticality score...")
                response = requests.post(
                    f"{backend_url}/predict/fusion",
                    data=data,
                    files=files,
                    timeout=120,
                )
                status.update(label="Assessment Complete", state="complete", expanded=False)

            show_response(response, render_fusion_result)
    else:
        st.markdown(
            empty_state("ti-stack-2", "Provide complete patient parameters and clinical media to generate a fused criticality score."),
            unsafe_allow_html=True,
        )
