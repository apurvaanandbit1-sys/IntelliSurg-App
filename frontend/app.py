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
    st.markdown('<p class="section-label">Demographics</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        race = st.selectbox(
            "Race",
            ["Caucasian", "AfricanAmerican", "Asian", "Hispanic", "Other"],
            key=f"{prefix}_race",
        )
        gender = st.selectbox(
            "Gender",
            ["Female", "Male", "Unknown/Invalid"],
            key=f"{prefix}_gender",
        )
        age = st.selectbox(
            "Age Group",
            ["[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)", "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)"],
            index=5,
            key=f"{prefix}_age",
        )
        max_glu_serum = st.selectbox(
            "Max Glucose Serum",
            ["None", "Norm", ">200", ">300"],
            key=f"{prefix}_max_glu",
        )

    with col2:
        admission_type_id = st.number_input("Admission Type ID", min_value=1, value=1, key=f"{prefix}_admission_type")
        discharge_disposition_id = st.number_input("Discharge Disposition ID", min_value=1, value=1, key=f"{prefix}_discharge")
        admission_source_id = st.number_input("Admission Source ID", min_value=1, value=1, key=f"{prefix}_admission_source")
        time_in_hospital = st.number_input("Time In Hospital", min_value=1, value=3, key=f"{prefix}_time_hospital")
        A1Cresult = st.selectbox(
            "A1C Result",
            ["None", "Norm", ">7", ">8"],
            key=f"{prefix}_a1c",
        )

    with col3:
        num_lab_procedures = st.number_input("Lab Procedures", min_value=0, value=40, key=f"{prefix}_lab")
        num_procedures = st.number_input("Procedures", min_value=0, value=1, key=f"{prefix}_procedures")
        num_medications = st.number_input("Medications", min_value=0, value=10, key=f"{prefix}_medications")
        number_outpatient = st.number_input("Outpatient Visits", min_value=0, value=0, key=f"{prefix}_outpatient")
        number_emergency = st.number_input("Emergency Visits", min_value=0, value=0, key=f"{prefix}_emergency")
        number_inpatient = st.number_input("Inpatient Visits", min_value=0, value=0, key=f"{prefix}_inpatient")
        number_diagnoses = st.number_input("Number of Diagnoses", min_value=1, value=5, key=f"{prefix}_diagnoses")

    st.markdown('<p class="section-label">Diagnosis & medication</p>', unsafe_allow_html=True)
    diag_col1, diag_col2, diag_col3, med_col = st.columns(4)

    with diag_col1:
        diag_1 = st.text_input("Diagnosis Code 1", value="250.83", key=f"{prefix}_diag1")
    with diag_col2:
        diag_2 = st.text_input("Diagnosis Code 2", value="401.9", key=f"{prefix}_diag2")
    with diag_col3:
        diag_3 = st.text_input("Diagnosis Code 3", value="272.4", key=f"{prefix}_diag3")
    with med_col:
        metformin = st.selectbox("Metformin", ["No", "Steady", "Up", "Down"], key=f"{prefix}_metformin")
        insulin = st.selectbox("Insulin", ["No", "Steady", "Up", "Down"], key=f"{prefix}_insulin")
        change = st.selectbox("Medication Change", ["No", "Ch"], key=f"{prefix}_change")
        diabetes_med = st.selectbox("Diabetes Medication", ["No", "Yes"], key=f"{prefix}_diabetesmed")

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
        "diabetesMed": diabetes_med,
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

    html = big_metric_card(
        eyebrow="ANN prediction",
        title="Readmission risk",
        big_value=f"{pct(prob)}%" if prob is not None else "—",
        big_label=label,
        pct=pct(prob),
        badge_level=level,
        sub_cards_html=f"""
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:4px;">
            {metric_card('ti-list-details', 'Features used', str(payload.get('feature_count', '—')), 100, COLORS['accent'])}
            {metric_card('ti-checkbox', 'Model input', 'Ready' if payload.get('model_input_ready') else 'Incomplete', 100 if payload.get('model_input_ready') else 30, COLORS['accent'])}
        </div>
        """
    )
    st.markdown(html, unsafe_allow_html=True)


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

    st.caption(
        f"Predicted class index: {class_index}"
    )

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
        html = big_metric_card(
            eyebrow="Wound classification",
            title="Predicted wound type",
            big_value=str(wound_class).upper(),
            big_label=f"{pct(confidence)}% confidence" if confidence is not None else "",
            pct=pct(confidence),
            badge_level=risk_level_from_probability(confidence if isinstance(confidence, (int, float)) else None),
        )
        st.markdown(html, unsafe_allow_html=True)


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

    sub_cards = f"""
    <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; margin-top:4px;">
        {metric_card('ti-heartbeat', 'ANN readmission', str(ann_label), pct(payload.get('readmission_risk')), COLORS['accent'])}
        {metric_card('ti-activity', 'ECG beat class', str(ecg_label), pct(payload.get('ecg_confidence')), '#C98A2E')}
        {metric_card('ti-bandage', 'Wound status', str(wound_label), pct(payload.get('wound_confidence')), '#C2483F')}
    </div>
    """

    html = big_metric_card(
        eyebrow="Fusion dashboard",
        title="Overall assessment",
        big_value=f"{pct(criticality)}%" if criticality is not None else "—",
        big_label="criticality index",
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

st.markdown(
    page_header(
        eyebrow="Multimodal clinical AI",
        title="IntelliSurg",
        subtitle="Post-operative monitoring demo — ANN readmission risk, ECG beat classification, "
                  "wound imaging, and a fused criticality score.",
    ),
    unsafe_allow_html=True,
)

backend_url = st.sidebar.text_input("Backend URL", value="http://127.0.0.1:8000")
st.sidebar.markdown(
    f"""<p style="font-size:12px; color:{COLORS['text_muted']};">
    Points at your local FastAPI server. Update this after deployment.
    </p>""",
    unsafe_allow_html=True,
)
st.sidebar.markdown(disclaimer_footer(), unsafe_allow_html=True)


tab_ann, tab_rnn, tab_cnn, tab_fusion = st.tabs(
    ["ANN Risk", "ECG RNN", "Wound CNN", "Fusion Demo"]
)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — ANN
# ─────────────────────────────────────────────────────────────────────────────

with tab_ann:
    st.markdown(
        page_header("Tabular model", "Readmission risk prediction",
                     "Enter patient demographics and clinical history."),
        unsafe_allow_html=True,
    )
    profile = patient_profile_form("ann")


    if st.button("Run ANN prediction", key="ann_submit"):
        with st.spinner("Running ANN inference..."):
            response = requests.post(
                f"{backend_url}/predict/ann-from-form",
                json=profile,
                timeout=60,
            )
        show_response(response, render_ann_result)
    else:
        st.markdown(empty_state("ti-heartbeat", "Run a prediction to see the readmission risk score."),
                    unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — RNN / ECG
# ─────────────────────────────────────────────────────────────────────────────

with tab_rnn:
    st.markdown(
        page_header("Sequential model", "ECG beat classification",
                     "Paste a 187-value ECG beat or upload a file."),
        unsafe_allow_html=True,
    )

    signal_text = st.text_area(
        "ECG signal",
        value=DEFAULT_SIGNAL,
        height=200,
        key="rnn_signal",
    )

    

    signal_file = st.file_uploader(
        "Optional ECG text/CSV file",
        type=["txt", "csv", "json"],
        key="rnn_file",
    )

    if signal_file is not None:
        signal_text = signal_file.getvalue().decode("utf-8")
        st.markdown(
            f"""<p style="font-size:12px; color:{COLORS['accent_dark']};">
            <i class="ti ti-check" style="font-size:13px;"></i> Loaded signal from uploaded file.
            </p>""",
            unsafe_allow_html=True,
        )

    if st.button("Run RNN prediction", key="rnn_submit"):
        with st.spinner("Running ECG inference..."):
            response = requests.post(
                f"{backend_url}/predict/rnn-from-text",
                json={"signal_text": signal_text},
                timeout=60,
            )
        show_response(response, render_rnn_result)
    else:
        st.markdown(empty_state("ti-activity", "Run a prediction to see the ECG beat classification."),
                    unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ECG Waveform")
    draw_ecg(signal_text)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — CNN / Wound
# ─────────────────────────────────────────────────────────────────────────────

with tab_cnn:
    st.markdown(
        page_header("Vision model", "Wound image classification",
                     "Upload a wound photograph for classification."),
        unsafe_allow_html=True,
    )

    image_file = st.file_uploader("Upload wound image", type=["jpg", "jpeg", "png", "bmp", "webp"], key="cnn_image")

    if st.button("Run CNN prediction", key="cnn_submit"):
        if image_file is None:
            st.markdown(error_card("Please upload an image first."), unsafe_allow_html=True)
        else:
            files = {
                "file": (image_file.name, BytesIO(image_file.getvalue()), image_file.type or "application/octet-stream")
            }
            with st.spinner("Running wound classification..."):
                response = requests.post(
                    f"{backend_url}/predict/cnn",
                    files=files,
                    timeout=60,
                )
            show_response(response, render_cnn_result, image_file)
    else:
        if image_file is not None:
            st.image(image_file, caption="Selected image", use_container_width=True)
        st.markdown(empty_state("ti-bandage", "Upload an image and run a prediction to see the wound classification."),
                    unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — FUSION
# ─────────────────────────────────────────────────────────────────────────────

with tab_fusion:
    st.markdown(
        page_header("Fusion dashboard", "Combined patient assessment",
                     "Submits patient data, ECG signal, and wound image together for a fused criticality score."),
        unsafe_allow_html=True,
    )

    fusion_profile = patient_profile_form("fusion")
    fusion_signal = st.text_area("Fusion ECG signal", value=DEFAULT_SIGNAL, height=180, key="fusion_signal")
    fusion_image = st.file_uploader(
        "Upload wound image for fusion",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        key="fusion_image",
    )

    if st.button("Run fusion demo", key="fusion_submit"):
        if fusion_image is None:
            st.markdown(error_card("Please upload a wound image for the fusion demo."), unsafe_allow_html=True)
        else:
            data = {
                "patient_profile": json.dumps(fusion_profile),
                "signal": fusion_signal,
            }
            files = {
                "file": (
                    fusion_image.name,
                    BytesIO(fusion_image.getvalue()),
                    fusion_image.type or "application/octet-stream",
                )
            }
            with st.spinner("Running ANN, CNN, RNN and fusing results..."):
                response = requests.post(
                    f"{backend_url}/predict/fusion",
                    data=data,
                    files=files,
                    timeout=120,
                )
            show_response(response, render_fusion_result)
    else:
        st.markdown(
            empty_state("ti-stack-2", "Submit patient data, an ECG signal, and a wound image to see the fused criticality score."),
            unsafe_allow_html=True,
        )
