<table align="center">
  <tr>
    <td align="left" width="300"><strong>1️⃣ Problem Statement</strong></td>
    <td align="left">PS 06: Predictive Hospital Resource & Emergency Load Intelligence System</td>
  </tr>
  <tr>
    <td align="left"><strong>2️⃣ Project Name</strong></td>
    <td align="left"><strong>Hospital Command Center (MediForecast Pro)</strong></td>
  </tr>
  <tr>
    <td align="left"><strong>3️⃣ Team Name</strong></td>
    <td align="left">The Validators</td>
  </tr>
  <tr>
    <td align="left"><strong>4️⃣ Deployed Link</strong></td>
    <td align="left">
      <a href="https://gfgbq-team-the-validators-rbfwypfev6kbzqyj2ue3qi.streamlit.app/">🔗 Deploy Link</a>
    </td>
  </tr>
  <tr>
    <td align="left"><strong>5️⃣ Demo Video</strong></td>
    <td align="left">
      <a href="https://youtu.be/your-link](https://drive.google.com/file/d/1Aufy7bJBXVn50V4hxqki93o6UB3eElug/view">▶️ Watch 2-Minute Demo</a>
    </td>
  </tr>
  <tr>
    <td align="left"><strong>6️⃣ PPT Link</strong></td>
    <td align="left">
      <a href="https://drive.google.com/file/d/1GCAmBzSgGGxTZW128TrlNW2cZIkMtCYq/view?usp=drive_link">📄 View Presentation Deck</a>
    </td>
  </tr>
</table>

<br>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![PuLP](https://img.shields.io/badge/PuLP-Optimization-green?style=for-the-badge)](https://pypi.org/project/PuLP/)

</div>

---

## ✅ Project Overview

**The Problem:** Hospitals currently operate on historical averages, leading to **critical staff shortages** during sudden surges and **wasted resources** during quiet periods. Furthermore, during city-wide crises, lack of coordination leads to "Patient Stacking" where one hospital is overwhelmed while another nearby is empty.

**Our Solution:** The **Hospital Command Center** is a SaaS-ready platform that acts as a "Digital Twin" for hospital operations. It utilizes:

1.  **AI-Driven Forecasting:** Random Forest models predict patient influx using weather & calendar data.
2.  **Resource Optimization:** Linear Programming (PuLP) mathematically minimizes staffing costs while ensuring safety ratios.
3.  **City-Wide Load Balancing:** Automatically routes ambulances to neighboring facilities when capacity breaches 100%.
4.  **Supply Chain Intelligence:** Forecasts Oxygen and PPE usage to prevent stockouts.

---

## ✅ Key Features

| Feature | Description |
| :--- | :--- |
| **📂 SaaS Data Integration** | Any hospital can drag-and-drop their historical CSV. The system's **Retraining Pipeline** instantly builds a custom AI model for them. |
| **🚑 Ambulance Routing** | An intelligent "Air Traffic Control" for ambulances. If ER capacity > 100%, it provides optimal diversion routes to partner hospitals. |
| **📦 Supply Chain Forecast** | Predicts consumption of critical resources (Oxygen Cylinders, N95 Masks) based on predicted patient pathology. |
| **📋 Mathematical Rostering** | Generates the perfect shift schedule (Morning/Evening/Night) to minimize cost while maintaining a 1:5 Nurse-to-Patient ratio. |
| **🚨 Emergency Broadcast** | "One-Click" dispersion system to alert Dept Heads and recall off-duty staff during Mass Casualty events. |

---

## ✅ Setup & Installation Instructions

### Prerequisites
* Python 3.8 or higher installed.

### Step 1: Clone the Repository
```bash
git clone [https://github.com/ByteQuest-2025/GFGBQ-Team-the-validators.git](https://github.com/ByteQuest-2025/GFGBQ-Team-the-validators.git)
cd GFGBQ-Team-the-validators
```
### Step 2: Install Dependencies

```bash
pip install -r requirements.txt

```

### Step 3: Initialize the System

Run the data generator script once to create the privacy-compliant "Digital Twin" dataset:

```bash
python generate_data.py

```

*Output: `Dataset generated successfully.*`

### Step 4: Launch the Dashboard

Start the application:

```bash
python -m streamlit run app.py

```

The application will automatically open in your default web browser at `http://localhost:8501`.

---

## ✅ Usage Instructions

1. **View Live Status**: The top bar shows the system status and **Real-Time Temperature** fetched from the API for your location (Pune HQ).
2. **Set Prediction Parameters**:
* **Target Date**: Select a future date to forecast.
* **Temperature**: If the date is today, it uses live sensors. If it's in the future, use the slider to simulate weather conditions (e.g., a heatwave).
* **Mass Casualty Toggle**: Switch this ON to simulate a major disaster and see how the system handles a sudden 60% surge.


3. **Run Analysis**: Click the **🚀 Analyze & Optimize** button.
4. **Review Intelligence Report**:
* **Predicted Influx**: See the exact number of expected patients.
* **Optimized Roster**: Check the generated table for the exact number of staff needed for Morning, Evening, and Night shifts.
* **Bed Map**: Visual grid showing occupied vs. free beds in ER, ICU, and General Wards.



---

## ✅ Relevant Screenshots

### 1. The Command Center Dashboard

### 2. AI-Optimized Rostering & Bed Map

---

<div align="center">

### 👨‍💻 Developed by Team: The Validators

*Byte Quest Hackathon 2025*

</div>

```


```


