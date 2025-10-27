import pandas as pd

# Create sample data
data = {
    'text': [
        "I feel extremely stressed about my upcoming exams and deadlines. The pressure is overwhelming.",
        "I'm so happy today! Everything is going great and I feel blessed.",
        "I feel worthless and alone. Nothing seems to matter anymore.",
        "Work is getting intense but I'm managing it well with breaks.",
        "I'm excited about my new project! Can't wait to see the results.",
        "Feeling anxious about the presentation tomorrow. Hope it goes well.",
        "Life feels empty and meaningless. I don't see the point anymore.",
        "Had an amazing day with friends! Feeling grateful and loved.",
        "The constant pressure is making me exhausted and burnt out.",
        "Just feeling okay today, nothing special happening."
    ],
    'timestamp': [
        '2025-10-27 09:00',
        '2025-10-27 09:15',
        '2025-10-27 09:30',
        '2025-10-27 09:45',
        '2025-10-27 10:00',
        '2025-10-27 10:15',
        '2025-10-27 10:30',
        '2025-10-27 10:45',
        '2025-10-27 11:00',
        '2025-10-27 11:15'
    ],
    'user_id': [f'user{str(i).zfill(3)}' for i in range(1, 11)]
}

df = pd.DataFrame(data)

# Save as Excel
df.to_excel('sample_data.xlsx', index=False)
print("Sample Excel file created: sample_data.xlsx")

# Also save as CSV
df.to_csv('sample_data.csv', index=False)
print("Sample CSV file created: sample_data.csv")

# Create TXT file
with open('sample_data.txt', 'w') as f:
    for text in data['text']:
        f.write(text + '\n')
print("Sample TXT file created: sample_data.txt")

print("\nAll sample files created successfully!")
