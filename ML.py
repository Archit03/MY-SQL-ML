import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the CSV file
csv_file_path = 'query_logs_df.csv'
df = pd.read_csv(csv_file_path)

'''
missing_values = df.isnull().sum()
print(missing_values)
'''

# Feature Engineering and Normalization
vectorizer = CountVectorizer()
X_text = vectorizer.fit_transform(df['Queries']).toarray()
X_numerical = df[['Execution Time', 'QueryType']].values

# Use LabelEncoder for 'QueryType'
label_encoder = LabelEncoder()
X_numerical[:, 1] = label_encoder.fit_transform(X_numerical[:, 1])

scaler = StandardScaler()
X_numerical = scaler.fit_transform(X_numerical)
X = np.concatenate([X_text, X_numerical], axis=1)


np.random.seed(1)
# Adding a random binary 'SuccessLabel' column to the DataFrame (0 or 1)
df['SuccessLabel'] = np.random.choice([0, 1], size=len(df))

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, df['SuccessLabel'], test_size=0.2, random_state=1)

# Train the model (assuming RandomForestClassifier, you can use your own model)
model = RandomForestClassifier(random_state=1, n_estimators=65)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Display evaluation metrics
print("Accuracy:", accuracy)
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(class_report)

# Feature Engineering and Normalization for New Queries
X_text_new_queries = vectorizer.transform(df['Queries']).toarray()
X_numerical_new_queries = df[['Execution Time', 'QueryType']].values

# Use LabelEncoder for 'QueryType' in new queries
X_numerical_new_queries[:, 1] = label_encoder.transform(X_numerical_new_queries[:, 1])

X_numerical_new_queries = scaler.transform(X_numerical_new_queries)
X_new_queries = np.concatenate([X_text_new_queries, X_numerical_new_queries], axis=1)

# Predict outcomes for new queries
predictions = model.predict(X_new_queries)

# Update DataFrame with Predicted Outcomes
df['PredictedOutcome'] = predictions

# Save the DataFrame with Predicted Outcomes to a new CSV file
predicted_outcomes_file = 'predicted_outcomes.csv'  
df.to_csv(predicted_outcomes_file, index=False)

# Display Predicted Outcomes
print("Predicted Outcomes:")
print(df[['Queries', 'PredictedOutcome']])
