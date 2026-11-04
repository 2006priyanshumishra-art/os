# # Principal Component Analysis(PCA)

# #### IMPORTING LIBRARIES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix

# #### LOADING DATASET

df=pd.read_csv("Wine.csv")

print("Number of samples:", df.shape[0])
print("Number of features:", df.shape[1])
df.head(5)

df["Customer_Segment"].unique()

# #### DATA ANALYSIS

print("Missing values:")
print(df.isnull().sum())

if(df.duplicated().sum()==0):
  print("\nNo duplicate rows present.")
else:
  print("\nDuplicate rows:", df.duplicated().sum())

# #### DEPENDENT AND INDEPENDENT FEATURES

X = df.drop("Customer_Segment",axis=1)
y = df["Customer_Segment"]

print("Input features shape:", X.shape)
print("Output variable shape:", y.shape)

# #### SCALING

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)
print("Shape after standardization:", X_scaled.shape)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

model = KNeighborsClassifier()
model.fit(X_train, y_train)

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print("Training Accuracy:", accuracy_score(y_train, y_train_pred))
print("Testing Accuracy:", accuracy_score(y_test, y_test_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_test_pred))

cm = confusion_matrix(y_test, y_test_pred)

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")
plt.title("KNN Confusion Matrix")
plt.show()

# #### PRINCIPAL COMPONENT ANALYSIS

pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)

pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
pca_df["Customer_Segment"] = y.values

pca_df.head()

X = pca_df[["PC1", "PC2"]]
y = pca_df["Customer_Segment"]

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2,random_state=42,stratify=y)

print("Training shape:", X_train.shape)
print("Testing shape:", X_test.shape)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Before PCA
axes[0].scatter(
    X_scaled[:, 0],
    X_scaled[:, 1],
    color='green',
    alpha=0.6
)
axes[0].set_title("Before PCA: Original Features")
axes[0].set_xlabel("Original Feature 1")
axes[0].set_ylabel("Original Feature 2")
axes[0].grid(True)

# After PCA
axes[1].scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    color='orange',
    alpha=0.6
)
axes[1].set_title("After PCA: Principal Components")
axes[1].set_xlabel("PC1")
axes[1].set_ylabel("PC2")
axes[1].grid(True)

plt.tight_layout()
plt.show()

variance_df = pd.DataFrame({
    "Principal Component": ["PC1", "PC2"],
    "Explained Variance Ratio": pca.explained_variance_ratio_
})

print(variance_df)

# Fit PCA on all components
pca_full = PCA()
pca_full.fit(X_scaled)

# Plot explained variance
plt.figure(figsize=(8, 5))
plt.plot(
    range(1, len(pca_full.explained_variance_ratio_) + 1),
    pca_full.explained_variance_ratio_,
    marker='o'
)

plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("PCA - Explained Variance")
plt.xticks(range(1, len(pca_full.explained_variance_ratio_) + 1))
plt.grid(True)
plt.show()

model = KNeighborsClassifier()
model.fit(X_train, y_train)

y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

print("Training Accuracy:", accuracy_score(y_train, y_train_pred))
print("Testing Accuracy:", accuracy_score(y_test, y_test_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_test_pred))

print("Predicted classes:", np.unique(y_test_pred))
print("Actual classes:", np.unique(y_test))

print("Actual test class distribution:")
print(y_test.value_counts().sort_index())

print("\nPredicted class distribution:")
print(pd.Series(y_test_pred).value_counts().sort_index())

plt.figure(figsize=(8, 5))

plt.scatter(X_test["PC1"],X_test["PC2"],c=y_test_pred,cmap="viridis",alpha=0.7)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("KNN Predictions on PCA-Reduced Wine Dataset")
plt.colorbar(label="Customer_Segment")
plt.show()
