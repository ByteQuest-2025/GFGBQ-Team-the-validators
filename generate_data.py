import pandas as pd
import numpy as np

def create_dataset():
    print("Generating Hospital Bed History...")
    dates = pd.date_range(start="2023-01-01", end="2024-12-31")
    data = []

    for date in dates:
        volume = 80 
        day_of_year = date.dayofyear
        seasonality = 15 * np.cos((day_of_year - 15) * 2 * np.pi / 365)
        
        weekend_spike = 0
        if date.weekday() >= 4:
            weekend_spike = np.random.randint(10, 20)
            
        noise = np.random.normal(0, 5)
        temp = 20 - (seasonality) + np.random.normal(0, 2)
        
        total_admissions = int(volume + seasonality + weekend_spike + noise)
        
        icu_usage = int(total_admissions * 0.15) + np.random.randint(2, 5)
        general_ward_usage = int(total_admissions * 0.40) + np.random.randint(20, 30)

        data.append([
            date.strftime('%Y-%m-%d'), 
            total_admissions, 
            icu_usage,
            general_ward_usage,
            round(temp, 1), 
            date.weekday() >= 5
        ])

    df = pd.DataFrame(data, columns=['Date', 'Admissions', 'ICU_Usage', 'General_Ward_Usage', 'Temp', 'Is_Weekend'])
    df.to_csv("hospital_training_data.csv", index=False)
    print("Dataset 'hospital_training_data.csv' generated successfully.")

if __name__ == "__main__":
    create_dataset()