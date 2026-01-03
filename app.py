import streamlit as st
import pandas as pd
import numpy as np
import requests
import pulp
import plotly.express as px
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor


st.set_page_config(page_title="MediForecast Pro", layout="wide", page_icon="🏥")

st.markdown("""
<style>
    div.stMetric {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #0d6efd;
    }
</style>
""", unsafe_allow_html=True)



@st.cache_resource
def load_and_train_model():
    try:
        df = pd.read_csv("hospital_training_data.csv")
    except FileNotFoundError:
        st.error("Data file not found. Please run 'generate_data.py' first.")
        st.stop()
        
    X = df[['Temp', 'Is_Weekend']]
    y = df['Admissions']
    
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)
    
    return model, df

def get_live_weather(city_lat=18.52, city_lon=73.85):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={city_lat}&longitude={city_lon}&current_weather=true"
        response = requests.get(url).json()
        return response['current_weather']['temperature']
    except:
        return 25.0

def optimize_roster(predicted_load):
    
    prob = pulp.LpProblem("Staff_Optimization", pulp.LpMinimize)
    
    morning = pulp.LpVariable("Morning_Staff", lowBound=2, cat='Integer')
    evening = pulp.LpVariable("Evening_Staff", lowBound=2, cat='Integer')
    night = pulp.LpVariable("Night_Staff", lowBound=2, cat='Integer')
    
 
    prob += morning >= (predicted_load * 0.4) / 5
    prob += evening >= (predicted_load * 0.4) / 5
    prob += night   >= (predicted_load * 0.2) / 8
    
    prob += morning + evening + night
    
   
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    return {
        "Morning": int(morning.varValue),
        "Evening": int(evening.varValue),
        "Night": int(night.varValue),
        "Total": int(morning.varValue + evening.varValue + night.varValue)
    }



model, history_df = load_and_train_model()
current_temp = get_live_weather()



st.title("🏥 Intelligent Hospital Command Center")
st.markdown("**PS 06: Predictive Hospital Resource & Emergency Load Intelligence System**")

st.info(f"📡 System Online | Live Weather: {current_temp}°C | Location: Pune HQ")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Prediction Parameters")
    
    target_date = st.date_input("Target Date", datetime.today())
    
    if target_date == datetime.today().date():
        sim_temp = current_temp
        st.caption(f"Using Live Sensor Data: {sim_temp}°C")
    else:
        sim_temp = st.slider("Forecasted Temp (°C)", 0, 45, 25)
        
    is_weekend = target_date.weekday() >= 5
    if is_weekend:
        st.caption("⚠️ Weekend Trauma Protocols Active")
        
  
    run_prediction = st.button("🚀 Analyze & Optimize", type="primary", use_container_width=True)

with col2:
    if run_prediction:
       
        pred_input = pd.DataFrame([[sim_temp, is_weekend]], columns=['Temp', 'Is_Weekend'])
        pred_admissions = int(model.predict(pred_input)[0])
        
       
        roster = optimize_roster(pred_admissions)
        icu_demand = int(pred_admissions * 0.12)
        
        st.subheader(f"📊 Intelligence Report: {target_date.strftime('%d %b %Y')}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted ER Influx", f"{pred_admissions} Patients", delta="Normal" if pred_admissions < 95 else "High Load")
        m2.metric("Optimal Staff Count", f"{roster['Total']} Nurses", delta="Cost Optimized")
        m3.metric("ICU Beds Needed", f"{icu_demand} Beds", delta="Critical Care")
        
        st.divider()
        
        st.subheader("📋 AI-Optimized Shift Roster (Linear Programming Output)")
        roster_data = pd.DataFrame([
            {"Shift Phase": "Morning (07:00 - 15:00)", "Staff Required": roster['Morning'], "Load Allocation": "40%"},
            {"Shift Phase": "Evening (15:00 - 23:00)", "Staff Required": roster['Evening'], "Load Allocation": "40%"},
            {"Shift Phase": "Night (23:00 - 07:00)", "Staff Required": roster['Night'], "Load Allocation": "20%"}
        ])
        
      
        st.dataframe(roster_data, hide_index=True, use_container_width=True)
        
        if pred_admissions > 100:
            st.error("🚨 CRITICAL SURGE: Activate Overflow Ward B")
        elif pred_admissions > 90:
            st.warning("⚠️ HIGH LOAD: Alert On-Call Residents")
        else:
            st.success("✅ STABLE: Standard Operations")
            
    else:
        st.subheader("📈 Historical Trends")
        fig = px.line(history_df, x='Date', y='Admissions', title='Emergency Department Volume (Last 2 Years)')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)