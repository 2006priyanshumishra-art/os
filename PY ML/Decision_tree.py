# # Graduate Admission Classification — Decision Tree & Naive Bayes

student_name='\u0906\u092F\u0941\u0937\u0020\u0915\u0941\u092E\u093E\u0930'
print("STUDENT NAME: ",student_name)

submited_to='\u0935\u0948\u0936\u093E\u0932\u0940\u0020\u0907\u0902\u0917\u0933\u0947'
print("SUBMITED TO: ",submited_to)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report


import warnings
warnings.filterwarnings("ignore")


RANDOM_STATE = 42
TEST_SIZE = 0.20

df = pd.read_csv('Admission_Predict.csv')

df.head(5)

print("Number of samples:", df.shape[0])
print("Number of features:", df.shape[1])

df.columns = df.columns.str.strip()
print("Columns:", df.columns.tolist())

df.describe()

print("Number of duplicates:", df.duplicated().sum())

print(df.dtypes)

print("\nMissing values :", df.isna().sum())

df = df.drop(columns=["Serial No."])

# # Convert continuous Chance of Admit into classes
#
# - Chance of Admit < Q1 → **Low**
# - Chance of Admit >= Q1 → **High**

target_threshold = df["Chance of Admit"].quantile(0.75)

df["Chance of Admit"] = (df["Chance of Admit"] >= target_threshold).astype(int)

class_names = ["Low", "High"]

print(f"25th-percentile target threshold = {target_threshold:.4f}")

df.head(5)

df["Chance of Admit"].value_counts()

X = df.drop("Chance of Admit", axis=1)
y = df["Chance of Admit"]

# # Train/test split

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
print("Training rows:", len(X_train))
print("Testing rows :", len(X_test))

print("\nTraining class distribution:")
display(y_train.value_counts().rename(index={0: "Low", 1: "High"}).to_frame("Count"))

print("\nTesting class distribution:")
display(y_test.value_counts().rename(index={0: "Low", 1: "High"}).to_frame("Count"))

# # Decision Tree — Entropy / Gini

def train_tree(criterion):

    model = DecisionTreeClassifier(criterion=criterion,max_depth=4,min_samples_split=10,min_samples_leaf=5,random_state=RANDOM_STATE)

    model.fit(X_train, y_train)

    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Training metrics
    train_metrics = {
        "Accuracy": accuracy_score(y_train, y_train_pred),
        "Precision": precision_score(y_train, y_train_pred, zero_division=0),
        "Recall": recall_score(y_train, y_train_pred, zero_division=0),
        "F1 Score": f1_score(y_train, y_train_pred, zero_division=0)
    }

    # Testing metrics
    test_metrics = {
        "Accuracy": accuracy_score(y_test, y_test_pred),
        "Precision": precision_score(y_test, y_test_pred, zero_division=0),
        "Recall": recall_score(y_test, y_test_pred, zero_division=0),
        "F1 Score": f1_score(y_test, y_test_pred, zero_division=0)
    }

    print(criterion.upper(), "Decision Tree")

    print("\nTraining Metrics")
    display(pd.DataFrame([train_metrics],index=["Training"]).round(2))

    print("Testing Metrics")
    display(pd.DataFrame([test_metrics],index=["Testing"]).round(2))

    return model, train_metrics, test_metrics, y_train_pred, y_test_pred

# # Entropy

dt_entropy, entropy_train, entropy_test, y_train_pred_entropy, y_test_pred_entropy = train_tree("entropy")
cm_entropy = confusion_matrix(y_test, y_test_pred_entropy)

plt.figure(figsize=(5, 4))
sns.heatmap(cm_entropy,annot=True,fmt="d",cmap="Blues",xticklabels=class_names,yticklabels=class_names)

plt.title("Entropy")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 10))

plot_tree(dt_entropy,feature_names=X_train.columns,class_names=class_names,filled=True)

plt.title("Decision Tree - Entropy")
plt.show()

# # Gini

dt_gini, gini_train, gini_test, y_train_pred_gini, y_test_pred_gini = train_tree("gini")
cm_gini = confusion_matrix(y_test, y_test_pred_gini)

plt.figure(figsize=(5, 4))
sns.heatmap(cm_gini,annot=True,fmt="d",cmap="Blues",xticklabels=class_names,yticklabels=class_names)

plt.title("Gini")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 10))

plot_tree(dt_gini,feature_names=X_train.columns,class_names=class_names,filled=True)

plt.title("Decision Tree - Gini")
plt.show()

# # Naive Bayes

nb = GaussianNB(priors=None,var_smoothing=1e-9)

nb.fit(X_train, y_train)

features = ["GRE Score","TOEFL Score","University Rating","SOP","LOR","CGPA","Research"]

X_high_low = X.copy()

for feature in features:
    X_high_low[feature] = np.where(X_high_low[feature] >= X_high_low[feature].median(),"High","Low")

X_high_low["Output"] = y.values


likelihood_tables = {}

for feature in features:

    table = pd.crosstab(
        X_high_low[feature],
        X_high_low["Output"],
        normalize="columns"
    )

    likelihood_tables[feature] = table

    print(f"\n{feature}")
    display(table.round(4))


output_probability = y.value_counts(normalize=True)

output_df = pd.DataFrame({
    "Output": output_probability.index,
    "Probability": output_probability.values,
    "Percentage (%)": output_probability.values * 100
})

output_df["Probability"] = output_df["Probability"].round(4)
output_df["Percentage (%)"] = output_df["Percentage (%)"].round(2)

display(output_df.style.hide(axis="index"))

# Predictions
y_train_pred_nb = nb.predict(X_train)
y_test_pred_nb = nb.predict(X_test)

# Training metrics
nb_train_metrics = {
    "Accuracy": accuracy_score(y_train, y_train_pred_nb),
    "Precision": precision_score(y_train, y_train_pred_nb, zero_division=0),
    "Recall": recall_score(y_train, y_train_pred_nb, zero_division=0),
    "F1 Score": f1_score(y_train, y_train_pred_nb, zero_division=0)
}

# Testing metrics
nb_test_metrics = {
    "Accuracy": accuracy_score(y_test, y_test_pred_nb),
    "Precision": precision_score(y_test, y_test_pred_nb, zero_division=0),
    "Recall": recall_score(y_test, y_test_pred_nb, zero_division=0),
    "F1 Score": f1_score(y_test, y_test_pred_nb, zero_division=0)
}

cm_nb = confusion_matrix(y_test, y_test_pred_nb)

plt.figure(figsize=(5, 4))
sns.heatmap(cm_nb,annot=True,fmt="d",cmap="Blues",xticklabels=class_names,yticklabels=class_names)

plt.title("Naive Bayes")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()


print("Categorical Naive Bayes")

print("\nTraining Metrics")
display(pd.DataFrame([nb_train_metrics],index=["Training"]).round(2))

print("Testing Metrics")
display(pd.DataFrame([nb_test_metrics],index=["Testing"]).round(2))

# # Compare Accuracy, Precision, Recall and F1

results = pd.DataFrame(
    [entropy_test, gini_test, nb_test_metrics],
    index=["Entropy", "Gini", "Naive Bayes"]
)

metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]

ax = results[metrics].plot(
    kind="bar",
    figsize=(12, 6),
    color=["#4F81BD", "#F28E2B", "#70AD47", "#A64D79"]
)

# Add values on top of bars
for container in ax.containers:
    ax.bar_label(container, fmt="%.2f", padding=3)

plt.title("Model Performance Comparison")
plt.xlabel("Models")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.legend(title="Metrics")
plt.tight_layout()
plt.show()

# # user input

def predict_student():

    print("Enter Student Details")
    print("-" * 40)
    print("Please enter values within the given ranges:\n")

    gre = float(input("Enter GRE Score (290-340): "))
    toefl = float(input("Enter TOEFL Score (92-120): "))
    university_rating = float(input("Enter University Rating (1-5): "))
    sop = float(input("Enter SOP (1-5): "))
    lor = float(input("Enter LOR (1-5): "))
    cgpa = float(input("Enter CGPA (6.8-9.92): "))
    research = int(input("Enter Research (0 = No, 1 = Yes): "))

    # Validate input ranges
    ranges = {
        "GRE Score": (gre, 290, 340),
        "TOEFL Score": (toefl, 92, 120),
        "University Rating": (university_rating, 1, 5),
        "SOP": (sop, 1, 5),
        "LOR": (lor, 1, 5),
        "CGPA": (cgpa, 6.8, 9.92),
        "Research": (research, 0, 1)
    }

    for name, (value, minimum, maximum) in ranges.items():
        if not minimum <= value <= maximum:
            print(
                f"Error: {name} must be between "
                f"{minimum} and {maximum}."
            )
            return

    if research not in [0, 1]:
        print("Error: Research must be 0 or 1.")
        return

    student = pd.DataFrame([{"GRE Score": gre,"TOEFL Score": toefl,"University Rating": university_rating,"SOP": sop,"LOR": lor,"CGPA": cgpa,"Research": research}])


    result = pd.DataFrame({
        "Model": ["Decision Tree (Entropy)","Decision Tree (Gini)","Naive Bayes"],
        "Prediction": [class_names[dt_entropy.predict(student)[0]],class_names[dt_gini.predict(student)[0]],class_names[nb.predict(student)[0]]]
    })

    return result


result = predict_student()

if result is not None:
    display(result)
