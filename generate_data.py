import pandas as pd
import numpy as np

def create_dataset():
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
        
        data.append([
            date.strftime('%Y-%m-%d'), 
            total_admissions, 
            round(temp, 1), 
            date.weekday() >= 5
        ])

    df = pd.DataFrame(data, columns=['Date', 'Admissions', 'Temp', 'Is_Weekend'])
    df.to_csv("hospital_training_data.csv", index=False)
    print("Dataset generated successfully.")

if __name__ == "__main__":
    create_dataset()