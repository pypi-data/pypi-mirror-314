def ml1():
    return """
from sklearn.datasets import fetch_openml
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
from sklearn.model_selection import train_test_split

#1
dataset = fetch_openml(name='vertebra-column', as_frame=True)
X = dataset.data
y = dataset.target

print("Описание датасета:\n", dataset.DESCR)

#2
print("\nКоличество строк (объектов):", X.shape[0])
print("Количество столбцов (признаков):", X.shape[1])
print("\nОсновная статистика по признакам:\n", X.describe())

unique_classes = np.unique(y)
print("\nКоличество классов:", len(unique_classes))
print("Список классов:", unique_classes)



#3
print(f"количество пропущенных значений в каждом столбце:\n{X.isnull().sum()}")
print(f"\nколичество пропущенных значений во всех столбцах: {X.isnull().sum().sum()}") #X = pd.get_dummies(X)

X = X.select_dtypes(include=['float64','int64'])
X.fillna(X.mean(), inplace=True)
print(f"\nТипы данных после преобразования:\n{X.dtypes}")

class_counts = Counter(y)

RARE_THRESHOLD = 2

y = ['other' if class_counts[label] < RARE_THRESHOLD else label for label in y]
class_counts_after = Counter(y)


#4
import time
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

start_time = time.time()
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(X_train_scaled, y_train)
lr_train_time = time.time() - start_time

y_pred_lr = lr.predict(X_test_scaled)
lr_accuracy = accuracy_score(y_test, y_pred_lr)
print("\nЛогистическая регрессия:")
print("Accuracy:", lr_accuracy)
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred_lr))
print("Classification report:\n", classification_report(y_test, y_pred_lr))

#5
from sklearn.preprocessing import PolynomialFeatures

best_poly_degree = None
best_poly_accuracy = 0
best_poly_model = None
best_poly_y_pred = None
poly_train_time = None

for degree in [2, 3, 4]:
    start_time = time.time()
    poly = PolynomialFeatures(degree=degree)
    X_train_poly = poly.fit_transform(X_train_scaled)
    X_test_poly = poly.transform(X_test_scaled)

    lr_poly = LogisticRegression(max_iter=1000, random_state=42)
    lr_poly.fit(X_train_poly, y_train)
    current_train_time = time.time() - start_time

    y_pred_poly = lr_poly.predict(X_test_poly)
    current_accuracy = accuracy_score(y_test, y_pred_poly)

    if current_accuracy > best_poly_accuracy:
        best_poly_accuracy = current_accuracy
        best_poly_degree = degree
        best_poly_model = lr_poly
        best_poly_y_pred = y_pred_poly
        poly_train_time = current_train_time

print("\nПолиномиальная модель (Лучшая степень полинома = {}):".format(best_poly_degree))
print("Accuracy:", best_poly_accuracy)
print("Confusion matrix:\n", confusion_matrix(y_test, best_poly_y_pred))


print("Classification report:\n", classification_report(y_test, best_poly_y_pred))

#6
from sklearn.svm import SVC

kernels = ['linear', 'rbf', 'poly', 'sigmoid']
best_svm_kernel = None
best_svm_accuracy = 0
best_svm_model = None
best_svm_y_pred = None
svm_train_time = None

for kernel in kernels:
    start_time = time.time()
    svm = SVC(kernel=kernel, random_state=42)
    svm.fit(X_train_scaled, y_train)
    current_train_time = time.time() - start_time

    y_pred_svm = svm.predict(X_test_scaled)
    current_accuracy = accuracy_score(y_test, y_pred_svm)

    if current_accuracy > best_svm_accuracy:
        best_svm_accuracy = current_accuracy
        best_svm_kernel = kernel
        best_svm_model = svm
        best_svm_y_pred = y_pred_svm
        svm_train_time = current_train_time

print("\nSVM (Лучшее ядро = {}):".format(best_svm_kernel))
print("Accuracy:", best_svm_accuracy)
print("Confusion matrix:\n", confusion_matrix(y_test, best_svm_y_pred))
print("Classification report:\n", classification_report(y_test, best_svm_y_pred))


#7
from sklearn.linear_model import Perceptron

start_time = time.time()
perc = Perceptron(random_state=42)
perc.fit(X_train_scaled, y_train)
perc_train_time = time.time() - start_time

y_pred_perc = perc.predict(X_test_scaled)
perc_accuracy = accuracy_score(y_test, y_pred_perc)
print("\nПерцептрон:")
print("Accuracy:", perc_accuracy)
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred_perc))
print("Classification report:\n", classification_report(y_test, y_pred_perc))


#8
import pandas as pd

results = pd.DataFrame({
    'Model': ['Logistic Regression', 'Polynomial LR', 'SVM', 'Perceptron'],
    'Accuracy': [lr_accuracy, best_poly_accuracy, best_svm_accuracy, perc_accuracy],
    'Training Time (sec)': [lr_train_time, poly_train_time, svm_train_time, perc_train_time]
})

print("\nИтоговая таблица сравнения моделей:")
print(results)

Логистическая регрессия показала достаточно высокую точность (80,65%) и относительно быстрое время обучения. Это делает ее пригодной для использования в задачах классификации, особенно если требуется баланс между точностью и скоростью. Полиномиальная логистическая регрессия показала чуть более низкую точность (78,49%) по сравнению с обычной логистической регрессией, при этом время обучения немного увеличилось. Это может быть связано с более сложной структурой модели, что не всегда приводит к улучшению точности. SVM показал самую высокую точность (83,87%) среди всех рассмотренных моделей, при этом время обучения было одним из самых низких. Это делает SVM наиболее эффективным и быстрым методом для данной задачи классификации. Перцептрон показал самую низкую точность (76,34%) среди всех моделей, хотя время обучения было одним из самых низких. Это говорит о том, что перцептрон может быть менее пригодным для данной задачи, так как его точность недостаточно высока.

Наиболее эффективной моделью для классификации объектов в данной задаче является SVM, так как она показала самую высокую точность (83,87%) при одном из самых низких времен обучения (0,004630 секунды).

Логистическая регрессия также является хорошим выбором, особенно если требуется баланс между точностью и скоростью.

Полиномиальная логистическая регрессия и перцептрон могут быть менее предпочтительными из-за более низкой точности.

"""


def ml2():
    return """
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from sklearn.datasets import fetch_openml


№1
data_dict = fetch_openml('LEV')
print(data_dict.DESCR)

data = pd.DataFrame(data_dict.data, columns = data_dict.feature_names)
data['Target'] = data_dict.target
data.head()

y = data['Target']
X = data.drop('Target', axis=1)
X, y

№2
X.shape, y.shape

data.describe()

y.unique()

№3

data.info()

№4
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

model_lr = LogisticRegression(max_iter=10000)
model_lr.fit(X, y)

y_pred = model_lr.predict(X)
y_pred

accuracy_score(y, y_pred)

print(classification_report(y, y_pred))

№5

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from warnings import simplefilter
simplefilter(action='ignore')

best_accuracy = 0
best_degree = 0
best_plr_model = None

for degree in [1, 2, 3, 4, 5]:
    model_poly = make_pipeline(PolynomialFeatures(degree), LogisticRegression(max_iter=10000))
    model_poly.fit(X, y)

    y_pred = model_poly.predict(X)

    accuracy_poly = accuracy_score(y, y_pred)
    print(f'Accuracy для полинома степени {degree}: {accuracy_poly}')

    if accuracy_poly > best_accuracy:
        best_accuracy = accuracy_poly
        best_degree = degree
        best_plr_model = model_poly

print(f'Лучшая степень полинома: {best_degree} с accuracy: {best_accuracy}')


y_pred_best_poly = best_plr_model.predict(X)
print(f"Classification Report для полинома степени {best_degree}:")
print(classification_report(y, y_pred_best_poly))

№6
from sklearn.svm import SVC

best_accuracy_svc = 0
best_kernel = None
best_svc_model = None

for kernel in ['linear', 'poly', 'rbf', 'sigmoid']:
    model_svc = SVC(kernel=kernel, max_iter=10000)
    model_svc.fit(X, y)

    y_pred_svc = model_svc.predict(X)

    accuracy_svc = accuracy_score(y, y_pred_svc)
    print(f'Accuracy для ядра {kernel}: {accuracy_svc}')

    if accuracy_svc > best_accuracy_svc:
        best_accuracy_svc = accuracy_svc
        best_kernel = kernel
        best_svc_model = model_svc

print(f'Лучшее ядро: {best_kernel} с accuracy: {best_accuracy_svc}')

y_pred_best_svc = best_svc_model.predict(X)
print(f"Classification Report для SVC с ядром {best_kernel}:")
print(classification_report(y, y_pred_best_svc))

№7
from sklearn.linear_model import Perceptron

model_ppn = Perceptron(max_iter=10000)
model_ppn.fit(X, y)

y_pred_ppn = model_ppn.predict(X)

accuracy_ppn = accuracy_score(y, y_pred_ppn)
print(f'Accuracy Перцептрона: {accuracy_ppn}')

y_pred_ppn = model_ppn.predict(X)

print("Classification Report для Перцептрона:")
print(classification_report(y, y_pred_ppn))

№8

import time

results = []
full_reports = {}
models = {
    'Logistic Regression': LogisticRegression(max_iter=10000),
    'Best Polynomial Logistic Regression': make_pipeline(PolynomialFeatures(best_degree), LogisticRegression(max_iter=10000)),
    'Best SVC': SVC(kernel=best_kernel, max_iter=10000),
    'Perceptron': Perceptron(max_iter=10000)
}

for name, model in models.items():
    start_time = time.time()
    model.fit(X, y)
    fit_time = time.time() - start_time

    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)

    report = classification_report(y, y_pred, output_dict=True)
    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'Time (s)': fit_time,
    })
    full_reports[name]=report

pd.DataFrame(results)

pd.DataFrame(full_reports['Logistic Regression'])

pd.DataFrame(full_reports['Best Polynomial Logistic Regression'])

pd.DataFrame(full_reports['Best SVC'])

pd.DataFrame(full_reports['Perceptron'])

"""