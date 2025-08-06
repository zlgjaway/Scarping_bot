import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pprint
import joblib
from sklearn.pipeline import Pipeline

# Load the dataset
file_path = "/WEB-Scraping Project/clean_data_label.csv"
df = pd.read_csv(file_path, encoding='ISO-8859-1')

print(df['label'].value_counts())

# Drop rows with missing values
df.dropna(subset=['title/description', 'label'], inplace=True)

# Split data
X_train_text, X_test_text, y_train, y_test = train_test_split(
    df['title/description'], df['label'], test_size=0.2, random_state=42)

# Create pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', max_features=1000)),
    ('clf', LogisticRegression(max_iter=1000))
])

# Train pipeline
pipeline.fit(X_train_text, y_train)

# Predict
y_pred = pipeline.predict(X_test_text)

# Evaluate
report = classification_report(y_test, y_pred, output_dict=True)
conf_matrix = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

# Pretty print results
pp = pprint.PrettyPrinter(indent=2)
print("\nClassification Report:")
pp.pprint(report)
print(f"\nAccuracy: {accuracy:.2f}")

# Plot confusion matrix
plt.figure(figsize=(6,4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Pred: Junk', 'Pred: Not Junk'],
            yticklabels=['True: Junk', 'True: Not Junk'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.show()

# Save full pipeline
joblib.dump(pipeline, 'junk_filter_model.pkl')
