# step3Python.py
# Full pipeline: Load, Clean, Models, Visualizations, Export, Outliers

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------
# STEP 1: Load CSV
# --------------------------
csv_path = "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/bookings.csv"
bookings = pd.read_csv(csv_path)

# Remove spaces in column names
bookings.columns = bookings.columns.str.strip()

print("First 5 rows:")
print(bookings.head())

print("\nColumns:", bookings.columns)
print("\nMissing Values:\n", bookings.isnull().sum())

# --------------------------
# STEP 2: Clean Data
# --------------------------
# Drop unnecessary columns
drop_cols = ['arrival_date', 'Check_In_Date', 'Check_Out_Date']
for col in drop_cols:
    if col in bookings.columns:
        bookings.drop(col, axis=1, inplace=True)

# Fill missing numeric values (future-proof way)
bookings['lead_time'] = bookings['lead_time'].fillna(bookings['lead_time'].median())
bookings['avg_price_per_room'] = bookings['avg_price_per_room'].fillna(bookings['avg_price_per_room'].median())
bookings['Customer_Ratings'] = bookings['Customer_Ratings'].fillna(bookings['Customer_Ratings'].mean())

# --------------------------
# STEP 3: Classification Model (Booking_Status)
# --------------------------
# Features and target
X = bookings[['Hotel_Type', 'room_type_reserved', 'lead_time', 'avg_price_per_room', 'Customer_Ratings']]
y = bookings['booking_status']

# Convert categorical features into numbers
X = pd.get_dummies(X, drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest Classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Predict and accuracy
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("\nBooking Status Prediction Accuracy:", accuracy)

# --------------------------
# STEP 4: Regression Model (Revenue)
# --------------------------
X_reg = bookings[['lead_time', 'avg_price_per_room', 'Customer_Ratings']]
y_reg = bookings['Revenue']  # Replace with Net_Revenue if exists

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

reg = LinearRegression()
reg.fit(X_train_reg, y_train_reg)

y_pred_reg = reg.predict(X_test_reg)
mse = mean_squared_error(y_test_reg, y_pred_reg)
r2 = r2_score(y_test_reg, y_pred_reg)
print("\nRegression MSE:", mse)
print("Regression R2 Score:", r2)

# --------------------------
# STEP 5: Feature Importance (Classification)
# --------------------------
feat_importance = clf.feature_importances_
features = X.columns

plt.figure(figsize=(10,6))
plt.barh(features, feat_importance)
plt.xlabel("Importance")
plt.title("Feature Importance (Booking_Status)")
plt.show()

# --------------------------
# STEP 6: Correlation Heatmap (numeric only)
# --------------------------
numeric_cols = bookings.select_dtypes(include='number')
plt.figure(figsize=(10,8))
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Matrix (Numeric Columns Only)")
plt.show()

# --------------------------
# STEP 7: Export Predictions & Summary Stats
# --------------------------
# Predict booking status
bookings['Predicted_Booking_Status'] = clf.predict(X)

# Predict cancellation probability
bookings['Cancel_Probability'] = clf.predict_proba(X)[:, 1]

bookings['Predicted_Revenue'] = reg.predict(X_reg)

export_path = "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/hotel_predictions.csv"
summary_path = "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/summary_stats.csv"

bookings.to_csv(export_path, index=False)
bookings.describe().to_csv(summary_path)

print("\nPredictions exported to:", export_path)
print("Summary statistics exported to:", summary_path)

# --------------------------
# STEP 8: Flag Outliers in Customer Ratings
# --------------------------
def flag_outliers(series):
    mean = series.mean()
    std = series.std()
    return (series < mean - 2*std) | (series > mean + 2*std)

bookings['Rating_Outlier'] = flag_outliers(bookings['Customer_Ratings'])
print("Number of rating outliers:", bookings['Rating_Outlier'].sum())

