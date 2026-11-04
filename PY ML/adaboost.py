import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split,GridSearchCV, cross_val_score
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier,RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix

columns=['buying_price','Mantainance','No. of doors','No. of People','BootSpace','Safety','Decision']

df= pd.read_csv("car_evaluation.csv",header=None,names=columns)
df.head()

df.shape

df.isnull().sum()

df.duplicated().sum()

X=df.drop(columns=['Decision'])
y=df['Decision']

y.unique()

# onehot encoding
X= pd.get_dummies(X,dtype=int)
encoder= LabelEncoder()
y=encoder.fit_transform(y)

X.head()

X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

models={
    "SVM" : SVC(),
    "Random Forest" : RandomForestClassifier(random_state=42),
    "AdaBoost" : AdaBoostClassifier(algorithm='SAMME', random_state=42)
}

for name, model in models.items():
    model.fit(X_train,y_train)
    print(name," is trained successfully.")

for name,model in models.items():
    y_train_pred= model.predict(X_train)
    y_test_pred= model.predict(X_test)

    print("\n",name)
    print("Training Accuracy:", round(accuracy_score(y_train,y_train_pred)*100,2),'%')
    print("Testing Accuracy:", round(accuracy_score(y_test,y_test_pred)*100,2),'%')
    print("Classifiction Report:")
    print(classification_report(y_test,y_test_pred))

cv_results=[]

for name,model in models.items():
    score= cross_val_score(model,X_train,y_train,cv=10,scoring="accuracy")
    cv_results.append({
        'Model' : name,
        'CV Accuracy' : score.mean(),
        'CV Standard Deviation': score.std()
    })

    print("\n",name)
    print("Fold accuracies:", score.round(4))
    print("Mean CV Accuracy", round(score.mean()*100,2))

cv_df=pd.DataFrame(cv_results)
display(cv_df)

# hyperparameter tuning

param_grids={
    'SVM' : {
        'C': [0.1,1,10],
        'kernel': ['linear','rbf'],
        'gamma': ['scale','auto']
    },
    'Random Forest' : {
        'n_estimators': [50,100,200],
        'max_depth': [None,10,20],
        'min_samples_split': [2,5]
    },
    'AdaBoost' : {
        'n_estimators': [50,100,200],
        'learning_rate': [0.01,0.1,1]
    }
}

optimized_models={}
best_cv_score={}
results={}

for name,model in models.items():
    grid=GridSearchCV(model,param_grids[name],cv=10,scoring="accuracy",n_jobs=-1)
    grid.fit(X_train,y_train)

    optimized_models[name]=grid.best_estimator_
    best_cv_score[name]=grid.best_score_

    print('\n',name)
    print("Best Parameters:",grid.best_params_)
    print("Best score:",round(grid.best_score_*100,2))

# Accuracy before optimization (default models on Test Data)
before_accuracy = {}
for name, model in models.items():
    y_test_pred = model.predict(X_test)
    before_accuracy[name] = accuracy_score(y_test, y_test_pred)

# Accuracy after optimization (optimized models on Test Data)
after_accuracy = {}
for name, model in optimized_models.items():
    y_test_pred = model.predict(X_test)
    after_accuracy[name] = accuracy_score(y_test, y_test_pred)

df_plot = pd.DataFrame({"Before": before_accuracy, "After": after_accuracy})
ax = df_plot.plot(kind="bar", figsize=(7, 4))

display(df_plot)
