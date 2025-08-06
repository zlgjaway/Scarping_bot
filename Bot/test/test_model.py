import joblib

# Load the full pipeline
model = joblib.load("D:/WEB-Scraping Project/junk_filter_model.pkl") 

# User input
title = input("Title: ")

text = f"{title}"

# Predict
if model.predict([text])[0] == 1:  # 0 = junk
    print("Not junk")
else:
    print("junk")
