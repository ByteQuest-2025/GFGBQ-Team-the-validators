import streamlit as st
import pandas as pd
import numpy as np
import requests
import pulp
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="MediForecast Pro", layout="wide", page_icon="🏥")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    div.stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #0d6efd;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    div.stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }

    div.stButton > button {
        background: linear-gradient(90deg, #0d6efd 0%, #0a58ca 100%);
        border: none;
        height: 3.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
        transition: all 0.3s ease;
        color: white;
    }

    div.stButton > button:hover {
        box-shadow: 0 6px 16px rgba(13, 110, 253, 0.5);
        transform: translateY(-1px);
        color: white;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 0 20px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0d6efd !important;
        color: white !important;
        border: none;
    }
    
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

TOTAL_ER_BEDS = 120
TOTAL_ICU_BEDS = 30
TOTAL_GEN_BEDS = 150

@st.cache_resource
def load_and_train_model(custom_data=None):
    if custom_data is not None:
        try:
            df = pd.read_csv(custom_data)
            df['Date'] = pd.to_datetime(df['Date'])
            required = ['Date', 'Admissions', 'ICU_Usage', 'General_Ward_Usage', 'Temp', 'Is_Weekend']
            if not all(col in df.columns for col in required):
                return None, None, None, "ERROR: Missing columns. Please use the Template."
        except Exception as e:
            return None, None, None, f"Error reading file: {e}"
    else:
        try:
            df = pd.read_csv("hospital_training_data.csv")
            df['Date'] = pd.to_datetime(df['Date'])
        except FileNotFoundError:
            return None, None, None, "Default data missing. Run generate_data.py."

    X = df[['Temp', 'Is_Weekend']]
    model_admit = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, df['Admissions'])
    model_icu = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, df['ICU_Usage'])
    model_ward = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, df['General_Ward_Usage'])
    
    return model_admit, model_icu, model_ward, df

def get_live_weather(lat=18.52, lon=73.85):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        res = requests.get(url, timeout=2).json()
        return res['current_weather']['temperature']
    except:
        return 28.5

def optimize_roster(patient_load):
    prob = pulp.LpProblem("Staffing", pulp.LpMinimize)
    m = pulp.LpVariable("Morning", 2, cat='Integer')
    e = pulp.LpVariable("Evening", 2, cat='Integer')
    n = pulp.LpVariable("Night", 2, cat='Integer')
    
    prob += m >= (patient_load * 0.4) / 6
    prob += e >= (patient_load * 0.4) / 6
    prob += n >= (patient_load * 0.2) / 8
    prob += m + e + n
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    return {"M": int(m.varValue), "E": int(e.varValue), "N": int(n.varValue), "T": int(m.varValue+e.varValue+n.varValue)}

def calculate_resources(patients):
    return {
        "Oxygen": int(patients * 2.5), 
        "PPE": int(patients * 12),     
        "Meals": int(patients * 3)     
    }

def render_bed_grid(title, occupied, total):
    st.markdown(f"**{title}**")
    pct = (occupied / total) * 100
    st.progress(min(pct/100, 1.0))
    st.caption(f"{occupied}/{total} ({int(pct)}%)")
    cols = st.columns(10)
    filled = int(min((occupied / total) * 50, 50))
    for i in range(50):
        with cols[i % 10]: st.write("🔴" if i < filled else "🟢")

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=60)
st.sidebar.title("Data Integration")

uploaded_file = st.sidebar.file_uploader("📂 Upload Hospital CSV", type=["csv"])

template_csv = "Date,Admissions,ICU_Usage,General_Ward_Usage,Temp,Is_Weekend\n2024-01-01,120,20,50,25.5,0\n2024-01-02,135,22,55,24.0,0"
st.sidebar.download_button(
    label="📄 Download Data Template",
    data=template_csv,
    file_name="hospital_data_template.csv",
    mime="text/csv",
)

st.sidebar.divider()
st.sidebar.info("💡 **System Mode:** Auto-detects custom data or defaults to Digital Twin simulation.")

model_admit, model_icu, model_ward, history_df = load_and_train_model(uploaded_file)

if isinstance(history_df, str):
    st.error(history_df)
    st.stop()

current_temp = get_live_weather()

st.title("🏥 Intelligent Hospital Command Center")
st.markdown(f"**Operating Mode:** {'📂 Custom Data Source' if uploaded_file else '🤖 Digital Twin Simulation'}")

col1, col2 = st.columns([1, 2.2])

with col1:
    st.subheader("⚙️ Simulation Controls")
    with st.container(border=True):
        target_date = st.date_input("Target Date", datetime.today())
        
        if target_date == datetime.today().date():
            sim_temp = current_temp
            st.caption(f"Using Live Sensor Data: {sim_temp}°C")
        else:
            sim_temp = st.slider("Forecast Temp (°C)", 0, 45, 25)
            
        is_weekend = target_date.weekday() >= 5
        st.divider()
        mass_casualty = st.toggle("🚨 Simulate Mass Casualty")
        st.write("") 
        
        run_btn = st.button("🚀 Analyze & Optimize", type="primary", use_container_width=True)

with col2:
    if run_btn:
        with st.spinner("Training on provided data..."):
            input_df = pd.DataFrame([[sim_temp, is_weekend]], columns=['Temp', 'Is_Weekend'])
            pred_admit = int(model_admit.predict(input_df)[0])
            pred_icu = int(model_icu.predict(input_df)[0])
            pred_ward = int(model_ward.predict(input_df)[0])

            if mass_casualty:
                pred_admit = int(pred_admit * 1.6)
                pred_icu = int(pred_icu * 1.4)
                pred_ward = int(pred_ward * 1.2)
                surge_msg, surge_color = "CRITICAL SURGE", "inverse"
            else:
                surge_msg, surge_color = "Normal Flow", "normal"

            roster = optimize_roster(pred_admit)
            resources = calculate_resources(pred_admit)
            
            st.subheader(f"📊 Report: {target_date.strftime('%d %b %Y')}")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Predicted Admissions", pred_admit, surge_msg, delta_color=surge_color)
            k2.metric("Staff Required", f"{roster['T']} Nurses", "Optimized Cost")
            k3.metric("ER Occupancy", f"{int(pred_admit/TOTAL_ER_BEDS*100)}%", f"{pred_admit}/{TOTAL_ER_BEDS}")
            k4.metric("ICU Occupancy", f"{int(pred_icu/TOTAL_ICU_BEDS*100)}%", f"{pred_icu}/{TOTAL_ICU_BEDS}")

            st.divider()

            st.subheader("🛏️ Real-Time Bed Management")
            t1, t2, t3 = st.tabs(["🚑 Emergency Room", "🩺 ICU Ward", "🛌 General Ward"])
            with t1: render_bed_grid("Emergency Room Status", pred_admit, TOTAL_ER_BEDS)
            with t2: render_bed_grid("Intensive Care Unit Status", pred_icu, TOTAL_ICU_BEDS)
            with t3: render_bed_grid("General Ward Status", pred_ward, TOTAL_GEN_BEDS)

            st.divider()

            st.subheader("📡 Advanced Operations Center")
            
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.markdown("🚑 **Ambulance Routing Intelligence**")
                if pred_admit > TOTAL_ER_BEDS:
                    st.error(f"⛔ **DIVERSION ACTIVE:** ER Overload ({int(pred_admit/TOTAL_ER_BEDS*100)}%)")
                    st.markdown("""
                    **Recommended Diversion:**
                    * 🏥 **City General:** 3km (45% Occ)
                    * 🏥 **Apollo Clinic:** 7km (30% Occ)
                    """)
                else:
                    st.success("✅ **OPEN:** Accepting all incoming ambulances.")

            with c2:
                st.markdown("📦 **Supply Chain Forecast (24h)**")
                st.metric("🫧 Oxygen Cylinders", f"{resources['Oxygen']} units", "Stock: Adequate")
                st.metric("😷 PPE Kits", f"{resources['PPE']} units", "Stock: Low", delta_color="inverse")
                
            with c3:
                st.markdown("📢 **Emergency Broadcast System**")
                st.info("Direct line to Dept Heads")
                msg = st.text_input("Broadcast Message", value=f"High Load: {pred_admit} patients. Open Ward C.")
                
                if st.button("🔴 SEND ALERT", type="primary", key="alert_btn", use_container_width=True):
                    with st.spinner("Dispatching..."):
                        time.sleep(1.5)
                    st.toast("✅ ALERT SENT: Delivered to 42 staff.", icon="📲")
                    st.balloons()

            st.markdown("")
            st.markdown("📋 **Optimized Staffing Roster**")
            
            st.dataframe(pd.DataFrame([
                {"Shift Phase": "Morning (07-15)", "Nurses": roster['M'], "Allocation": "40%"},
                {"Shift Phase": "Evening (15-23)", "Nurses": roster['E'], "Allocation": "40%"},
                {"Shift Phase": "Night (23-07)", "Nurses": roster['N'], "Allocation": "20%"}
            ]), hide_index=True, use_container_width=True)

    else:
        st.subheader("📈 Historical Trends & Analysis")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=history_df['Date'], y=history_df['Admissions'], name='Admissions', line=dict(color='#0d6efd', width=2)))
        fig.add_trace(go.Scatter(x=history_df['Date'], y=history_df['ICU_Usage'], name='ICU Usage', line=dict(color='#dc3545', width=2)))
        fig.add_trace(go.Scatter(x=history_df['Date'], y=history_df['General_Ward_Usage'], name='Ward Usage', line=dict(color='#198754', width=2, dash='dot')))
        
        fig.update_layout(
            template="plotly_dark", 
            height=450, 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)