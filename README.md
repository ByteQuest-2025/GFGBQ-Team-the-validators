I apologize. I see the issue—the previous response rendered the text as "formatted" blocks, which makes it annoying to copy everything at once into a file.

Here is the **Raw Source Code** for the `README.md` file. You can click "Copy" on this single block and paste it directly into your `README.md` file.

```markdown
# 🏥 Hospital Command Center (MediForecast Pro)

### 🚀 PS 06: Predictive Hospital Resource & Emergency Load Intelligence System
**Byte Quest Hackathon Submission**

---

## 📖 Project Overview
The **Hospital Command Center** is an intelligent decision-support system designed to transition hospital operations from **Reactive** to **Predictive**. 

Currently, hospitals struggle with sudden patient surges, leading to staff burnout and resource shortages. Our solution utilizes **Machine Learning (Random Forest)** to forecast emergency admissions and **Linear Programming (PuLP)** to mathematically optimize staff allocation, ensuring hospitals are prepared *before* a crisis hits.

---

## 💡 Key Features
* **🧠 AI-Driven Forecasting**: Predicts daily emergency patient volume with high accuracy using historical trends, seasonality, and weekend patterns.
* **☀️ Live Weather Integration**: Connects to the **Open-Meteo API** to fetch real-time local temperature, adjusting predictions dynamically (e.g., detecting cold snaps that trigger flu surges).
* **📋 Optimized Staff Rostering**: Uses **Linear Programming (Optimization)** to generate the mathematically perfect shift schedule (Morning/Evening/Night) that minimizes cost while maintaining safe nurse-to-patient ratios.
* **🚨 Smart Surge Alerts**: Automatically flags critical days where demand exceeds capacity, triggering "Overflow Protocols" for administrators.

---

## 🛠️ Tech Stack
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | `Streamlit` | Interactive Web Dashboard for Hospital Admins |
| **ML Core** | `Scikit-Learn` | Random Forest Regressor for Patient Volume Prediction |
| **Optimization** | `PuLP` | Linear Programming for Staff Scheduling |
| **Data Processing** | `Pandas` & `NumPy` | Data Manipulation and Synthetic Data Generation |
| **Live Data** | `Requests` (Open-Meteo API) | Real-time Weather Data Fetching |
| **Visualization** | `Plotly` | Interactive Charts and Trend Analysis |

---

## ⚙️ Installation & Setup

### Prerequisites
* Python 3.8 or higher installed.

### Step 1: Clone or Download
Download the project folder `Hospital_Command_Center` to your local machine.

### Step 2: Install Dependencies
Open your terminal/command prompt, navigate to the project folder, and run:
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

## 🖥️ How to Use

1. **View Live Status**: The top bar shows the system status and **Real-Time Temperature** fetched from the API for your location (Pune HQ).
2. **Set Prediction Parameters**:
* **Target Date**: Select a future date to forecast.
* **Temperature**: If the date is today, it uses live sensors. If it's in the future, use the slider to simulate weather conditions (e.g., a heatwave).


3. **Run Analysis**: Click the **🚀 Analyze & Optimize** button.
4. **Review Intelligence Report**:
* **Predicted Influx**: See the exact number of expected patients.
* **Resource Needs**: View the required ICU beds and total nursing staff.
* **Optimized Roster**: Check the generated table for the exact number of staff needed for Morning, Evening, and Night shifts.



---

## 🧠 Methodology

### 1. Data Generation (Digital Twin)

Since real hospital data is protected (HIPAA/DISHA), we generate a mathematically accurate synthetic dataset (`hospital_training_data.csv`) that mimics real-world healthcare patterns:

* **Seasonality**: Sine wave functions simulate winter flu peaks.
* **Weekly Cycles**: Weighted probabilities simulate weekend trauma spikes.

### 2. Predictive Modeling

We train a **Random Forest Regressor** on 2 years of this historical data. The model learns non-linear relationships between:

* `Temperature` vs. `Admissions` (Inverse correlation).
* `Day_of_Week` vs. `Trauma Cases`.

### 3. Resource Optimization

We solve a **Minimization Problem** using Linear Programming:

* **Objective**: Minimize Total Staff ().
* **Constraint 1 (Day)**: 1 Nurse per 5 Patients.
* **Constraint 2 (Night)**: 1 Nurse per 8 Patients.

---

## 🔮 Future Scope

* **Bed Management Module**: Integration with IoT sensors to track real-time bed occupancy.
* **Ambulance Routing**: AI to redirect incoming ambulances to less crowded hospitals during surges.
* **SMS Alerts**: Twilio integration to automatically text off-duty staff during "Critical Surge" events.

---

### 👨‍💻 Developed for Byte Quest Hackathon

```

```