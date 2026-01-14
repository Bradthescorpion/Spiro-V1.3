# AIOS-onderwijs Spirometrie Simulator – Inspiratie & Expiratie
# Run met: streamlit run spirometrie_simulator.py

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="AIOS Spirometrie Onderwijs", layout="wide")

st.title("🫁 Spirometrie – AIOS onderwijs")
st.markdown("Flow–volume-loop met **expiratie (boven x-as)** en **inspiratie (onder x-as)**, vergelijkbaar met klinische spirometrie-uitdraaien.")

# =====================
# Presets
# =====================
presets = {
    "Normaal": {"FVC": 5.0, "ratio": 0.80, "PEF": 8.0},
    "COPD": {"FVC": 4.5, "ratio": 0.55, "PEF": 4.0},
    "Astma": {"FVC": 5.0, "ratio": 0.60, "PEF": 5.0},
    "Restrictief (ILD)": {"FVC": 3.0, "ratio": 0.82, "PEF": 7.0},
}

# =====================
# Sidebar – instellingen
# =====================
st.sidebar.header("Instellingen")
preset_name = st.sidebar.selectbox("Preset", presets.keys())
preset = presets[preset_name]

FVC_pred = st.sidebar.slider("Voorspelde FVC (L)", 3.0, 7.0, 5.0, 0.1)
LLN_ratio = st.sidebar.slider("LLN FEV1/FVC", 0.55, 0.75, 0.70, 0.01)

FVC = st.sidebar.slider("Gemeten FVC (L)", 1.5, 7.0, preset["FVC"], 0.1)
ratio = st.sidebar.slider("Gemeten FEV1/FVC", 0.30, 0.90, preset["ratio"], 0.01)
PEF = st.sidebar.slider("PEF (L/s)", 2.0, 10.0, preset["PEF"], 0.1)

# =====================
# Berekeningen
# =====================
time = np.linspace(0, 6, 600)
FEV1 = ratio * FVC

# Expiratie (boven x-as)
concavity = max(0.6, 1.3 - ratio)
vol_exp = FVC * np.exp(-time / (2.0 / concavity))
flow_exp = PEF * np.exp(-time) * (vol_exp / FVC) ** concavity

# Inspiratie (onder x-as)
vol_insp = np.linspace(0, FVC, len(time))
flow_insp = -0.6 * PEF * np.sin(np.linspace(0, np.pi, len(time)))

# =====================
# Interpretatie
# =====================
if ratio < LLN_ratio:
    interpretation = "🔴 Obstructief patroon"
elif FVC < 0.8 * FVC_pred:
    interpretation = "🟠 Restrictief patroon (verdacht)"
else:
    interpretation = "🟢 Normaal patroon"

# =====================
# Layout
# =====================
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    ax.plot(vol_exp, flow_exp, label="Expiratie", linewidth=2)
    ax.plot(vol_insp, flow_insp, label="Inspiratie", linewidth=2)
    ax.axhline(0)
    ax.invert_xaxis()
    ax.set_xlabel("Volume (L)")
    ax.set_ylabel("Flow (L/s)")
    ax.set_title("Flow–Volume Loop")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

with col2:
    st.subheader("Spirometrieparameters")
    st.table({
        "Parameter": ["FVC", "FEV1", "FEV1/FVC", "PEF"],
        "Gemeten": [
            f"{FVC:.2f} L",
            f"{FEV1:.2f} L",
            f"{ratio:.2f}",
            f"{PEF:.1f} L/s",
        ],
        "% voorspeld": [
            f"{100 * FVC / FVC_pred:.0f}%",
            f"{100 * FEV1 / (FVC_pred * 0.8):.0f}%",
            "–",
            "–",
        ],
    })

    st.subheader("Interpretatie")
    st.markdown(f"### {interpretation}")

st.caption("Educatieve simulatie voor AIOS – visueel en interpretatief klinisch correct, geen exacte longfysiologie")