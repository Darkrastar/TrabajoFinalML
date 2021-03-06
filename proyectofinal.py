# -*- coding: utf-8 -*-
"""ProyectoFinal.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WV5UW1UrTtwdiCV_IT5uJshN1_qrDzQe

#Importaciones

Acontinuación se especifican las diferentes importaciones necesarias para el proceso
"""

# Commented out IPython magic to ensure Python compatibility.
!pip install mglearn
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn
import time
# %matplotlib inline

"""#Carga de datos

El dataset lo obtenemos de un archivo público de nosotros ubicado **en** drive
"""

import pandas as pd
# The file has no headers naming the columns, so we pass header=None
# and provide the column names explicitly in "names"
 
url='https://docs.google.com/uc?export=download&id=1fKWYV2A2uD4jtMvbedwJufAlKjtnl5Q9'


data = pd.read_csv(url,sep=",", header=0, index_col=False,names=['pais', 'codigo_pais', 'oficina_registro', 'grupo_edad',  'edad',
           'area_ocupacion', 'sub_area_ocupacion', 'nivel_academico', 'estado_civil', 'genero',
           'etnia', 'estatura', 'localizacion', 'cantidad_personas'])

# Seleccionamos las columnas a utilizar
data = data[['pais', 'grupo_edad', 'edad','area_ocupacion', 'sub_area_ocupacion', 'nivel_academico', 'estado_civil', 'genero',
           'etnia', 'estatura','cantidad_personas']]

# Hacemos una pequeña visualización de los datos
display(data.head())
data.shape

"""#Eliminación de datos nulos (nan)

En la revisión del dataset, se encontró que existían valores en donde no se encontraba información registrada y por lo tanto venía categorizada con etiquetas específicas, es por esta razón que se decidió reemplazar estas categorías por NaN y posteriormente se hizo su respectiva eliminación.
Los valores según no se nos indico en el dataset que no tenía información fueron:


*   Area_ocupacion, nivel_academico como 'NO INDICA'
*   Estado civil y genero como 'DESCONOCIDO'
*   Etnia como 'SIN ETNIA REGISTRADA'
*   Estatura como '-1'
"""

data = pd.DataFrame(data)
from numpy import nan

#Marcamos los datos indicados como nan en la data principal
data[['area_ocupacion']] = data[['area_ocupacion']].replace('NO INDICA', nan)
data[['nivel_academico']] = data[['nivel_academico']].replace('NO INDICA', nan)
data[['estado_civil']] = data[['estado_civil']].replace('DESCONOCIDO', nan)
data[['genero']] = data[['genero']].replace('DESCONOCIDO', nan)
data[['etnia']] = data[['etnia']].replace('SIN ETNIA REGISTRADA', nan)
data[['estatura']] = data[['estatura']].replace(-1, nan)
data[['etnia']] = data[['etnia']].replace('PALENQUERO DE SAN BASILO', 'PALENQUERO DE SAN BASILIO')
# se borran los datos marcados como NAN
data_remnan=data.copy()
data_remnan.dropna(inplace=True)

# summarize y shape de los datos removidos
print(data.shape)
print(data_remnan.shape)

"""#Modificación de datos anómalos.

Se identificó a través de la grafica de bigotes que existen outliers para este dato



"""

import seaborn as sns
fig=plt.figure(figsize=(30,10))
sns.set_theme(style="whitegrid")
tips = data_remnan
ax = sns.boxplot(x=tips["estatura"])

"""Se calculan los cuartiles, el rango intercuartil y los respectivos bigote superior e inferior.

"""

Q1= data_remnan['estatura'].quantile(0.25)
print("primer cuartil",Q1)

Q3= data_remnan['estatura'].quantile(0.75)
print(" tercer cuartil",Q3)

IQR = Q3 - Q1
print("rango intercuartil",IQR)

mediana = data_remnan['estatura'].median()
print("mediana",mediana)

v_min = data_remnan['estatura'].min()
print("minimo",v_min)

v_max= data_remnan['estatura'].max()
print("maximo",v_max)

BI_calculado = (Q1 - 1.5 * IQR )
print("BI_calculado ",BI_calculado)

BS_calculado = (Q3 + 1.5 * IQR )
print("BS_calculado",BS_calculado)

"""Se crea un dataframe (BS) con la información de los registros cuya estatura fueran mayores al bigote superior y otro dataframe (BI) con la información de los registros menores al bigote inferior.

"""

BI = data_remnan[data_remnan['estatura'] < BI_calculado]
BS = data_remnan[data_remnan['estatura'] > BS_calculado]

"""Se recorre el dataframe (BI) y se modificaron los valores del dataframe principal que cumplieran con que su estatura fuese igual al valor de la estatura de BI como nan.

Se reemplazan los nan de valores inferiores al bigote inferior por la mediana
"""

print(data_remnan.shape)
for indice,fila in BI.iterrows():
  data_remnan['estatura'] = data_remnan['estatura'].replace(fila['estatura'] , nan)
print(data_remnan.shape)

print('Median Values')
data_remnan.fillna(data_remnan['estatura'].median(), inplace=True)
print(data_remnan.shape)

"""Se recorre el dataframe (BS) y se modificaron los valores del dataframe principal que cumplieran con que su estatura fuese igual al valor de la estatura de BS como nan.

Se reemplazan los nan de valores inferiores al bigote inferior por la moda
"""

print(data_remnan.shape)
for indice,fila in BS.iterrows():
  data_remnan['estatura'] = data_remnan['estatura'].replace(fila['estatura'] , nan)
print(data_remnan.shape)

print('Mode Values')
data_remnan.fillna(data_remnan['estatura'].mode(dropna=True).iloc[0], inplace=True)
print(data_remnan.shape)

import seaborn as sns
fig=plt.figure(figsize=(30,10))
sns.set_theme(style="whitegrid")
tips = data_remnan
ax = sns.boxplot(x=tips["estatura"])

"""Grafica antes del tratamiento a la estatura

"""

fig=plt.figure(figsize=(30,15))
sns.set_theme(style="white")
data.groupby('estatura')['cantidad_personas'].sum().plot(kind='bar',width = 0.9)

"""Grafica despues del tratamiento a la estatura"""

fig=plt.figure(figsize=(20,15))
sns.set_theme(style="white")
data_remnan.groupby('estatura')['cantidad_personas'].sum().plot(kind='bar',width = 0.9)

"""#EXPLOSIÓN DE DATOS

Se crean dos dataframe con la información de los datos cuyo campo cantidad_personas es diferente de 1 (data_diferente_1) y otro con los registros de cantidad_personas igual a 1 (data_igual_1)
"""

#Filtramos dataframe para no recorrer los registros iguales a 1
data_diferente_1 = data_remnan[data_remnan['cantidad_personas'] != 1]
data_igual_1 = data_remnan[data_remnan['cantidad_personas'] == 1]

print ("Data original sin nan: ",data_remnan.shape)
print ("Data con cantidad de personas diferente a 1: ", data_diferente_1.shape)
print ("Data con cantidad de personas igual a 1: ",data_igual_1.shape)
print ("La cantidad de registros que se deberan insertar son: ", data_diferente_1['cantidad_personas'].sum())
print ("La nueva data tendrá la siguiente cantidad de registros: ",data_igual_1['cantidad_personas'].sum() + data_diferente_1['cantidad_personas'].sum() )

"""Recorremos el dataframe data_diferente_1 para multiplicar la información, es decir, insertar la cantidad de registros iguales a su información segun indique su campo cantidad_personas, creando un nuevo dataframe llamado data_tem el cúal contendrá estos nuevos registros"""

#inicializamos dataframe temporal
data_tem = pd.DataFrame()

#recorremos el dataframe con los registros de cantidad de personas =! a 1
for indice,fila in data_diferente_1.iterrows():
  #asignamos la cantidad de personas como variable para el recorrido de inserción 
  cant_registros=fila['cantidad_personas']
  count = 0
  while count < cant_registros:
    #creamos un dataframe auxiliar solo con las columnas
    df_aux = pd.DataFrame(columns=['pais', 'grupo_edad', 'edad','area_ocupacion', 'sub_area_ocupacion', 'nivel_academico', 'estado_civil', 'genero',
                               'etnia', 'estatura','cantidad_personas'])
    #agregamos el nuevo registro con cantidad en 1
    df_aux = df_aux.append({'pais': fila['pais'] ,'grupo_edad':fila['grupo_edad'],  'edad':fila['edad'],
                         'area_ocupacion':fila['area_ocupacion'], 'sub_area_ocupacion':fila['sub_area_ocupacion'],
                         'nivel_academico':fila['nivel_academico'], 'estado_civil':fila['estado_civil'], 'genero':fila['genero'],
                         'etnia':fila['etnia'], 'estatura':fila['estatura'],  'cantidad_personas':1},ignore_index=True)
    
    #concatenamos el dataframe auxiliar al dataframe temporal, el cual tendra los registros ya explosionados
    data_tem = pd.concat([data_tem, df_aux])
    #sumamos 1 al contador para agragar la cantidad de registros adecuada
    count = count +1

"""Se tomá el dataframe data_tem el cual contiene los registros explosionados y lo unimos al dataframe data_igual_1, el cual contiene el resto de registros de nuestro dataset y finalmente regeneramos indices"""

#visualizamos la data temporal explosionada
print(data_tem)
#unimos los dos dataframes
print(data_igual_1.shape)
print(data_tem.shape)
data_expl= pd.concat([data_igual_1,data_tem])
#regeneramos indices
data_expl.reset_index(drop=True, inplace=True)
print(data_expl)

"""Para aplicar el metodo de balanceo, fue necesario eliminar los registros que fueran inferiores a 6, ya que se generaba un error al ejecutar"""

registros_menores_6= data_expl.groupby(['pais']).size().reset_index(name='cantidad_reg')
registros_menores_6 = registros_menores_6[registros_menores_6['cantidad_reg'] <= 6]
registros_menores_6.reset_index(drop=True, inplace=True)
print(registros_menores_6)

"""Se procede a eliminar estos registros."""

print(data_expl.shape)
for indice,fila in registros_menores_6.iterrows():
  #asignamos la cantidad de personas como variable para el recorrido de inserción
  pais_r=fila['pais'] 
  #print (pais_r)
  data_expl = data_expl.drop(data_expl[data_expl['pais']==pais_r].index)
  #print(fila['pais'])
print(data_expl.shape)

"""#Categorización de los datos 
Dado que algunos de los algoritmos solo permitian datos numéricos y por lo tanto fue necesario la realización de una categorización de las características cualitativas, para la realización de este proceso convertimos a category cada una de las características cualitativas como género, etnia, estado_civil, etc.

"""

data_expl.pais=data_expl.pais.astype("category").cat.codes
data_expl.grupo_edad = data_expl.grupo_edad.astype("category").cat.codes
data_expl.area_ocupacion=data_expl.area_ocupacion.astype("category").cat.codes
data_expl.sub_area_ocupacion=data_expl.sub_area_ocupacion.astype("category").cat.codes
data_expl.nivel_academico=data_expl.nivel_academico.astype("category").cat.codes
data_expl.estado_civil=data_expl.estado_civil.astype("category").cat.codes
data_expl.genero=data_expl.genero.astype("category").cat.codes
data_expl.etnia=data_expl.etnia.astype("category").cat.codes

"""Definimos los datos"""

X = data_expl[['grupo_edad', 'edad','area_ocupacion', 'sub_area_ocupacion', 'nivel_academico', 'estado_civil', 'genero',
           'etnia', 'estatura']]
        
y = data_expl.pais

"""#Balanceo de datos

"""

from imblearn.combine import SMOTETomek
oversample = SMOTETomek("all")
X_over, y_over = oversample.fit_resample(X, y)

"""Dividimos los datos de prueba y entrenamiento"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_over, y_over,
                                                    random_state=0)

"""#Aplicamos los modelos de ML

#RNA
"""

inicio = time.time()
# Código a medir
time.sleep(1)
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(solver='adam', random_state=0, max_iter=300, learning_rate= 'adaptive',activation = 'logistic').fit(X_train, y_train)

print("RNA Test set score: {:.2f}".format(mlp.score(X_test, y_test)))
print("RNA Train set score: {:.2f}".format(mlp.score(X_train, y_train)))

fin = time.time()
print("Tiempo total de ejecución en segundos:" , fin-inicio)

"""Por incompatibilidad de versiones y para poder hacer uso de las metricas fue necesario subir la versión, sin embargo, el algoritmo de RNA nos generaba conflicto por eso procuramos ejecutarlo antes"""

!pip uninstall scikit-learn -y
!pip install -U scikit-learn==0.24.2

from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
import time

inicio = time.time()
# Código a medir
time.sleep(1)
y_pred=mlp.predict(X_test)

print("Test mean_squared_error: {:.3f}".format(mean_squared_error(y_test, y_pred)))
print("Test accuracy_score: {:.3f}".format(accuracy_score(y_test,y_pred)))
print("Test precision_score: {:.3f}".format(precision_score(y_test,y_pred, average='weighted')))
print("Test recall_score: {:.3f}".format(recall_score(y_test,y_pred, average='weighted')))
print("Test f1_score: {:.3f}".format(f1_score(y_test,y_pred, average='weighted')))
fin = time.time()
print("Tiempo total de ejecución en segundos:" , fin-inicio)

"""#KNN"""

inicio = time.time()
# Código a medir
time.sleep(1)
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

print("Test set score: {:.2f}".format(knn.score(X_test, y_test)))
print("Train set score: {:.2f}".format(knn.score(X_train, y_train)))

y_pred=knn.predict(X_test)

print("Test mean_squared_error: {:.3f}".format(mean_squared_error(y_test, y_pred)))
print("Test accuracy_score: {:.3f}".format(accuracy_score(y_test,y_pred)))
print("Test precision_score: {:.3f}".format(precision_score(y_test,y_pred, average='weighted')))
print("Test recall_score: {:.3f}".format(recall_score(y_test,y_pred, average='weighted')))
print("Test f1_score: {:.3f}".format(f1_score(y_test,y_pred, average='weighted')))
fin = time.time()
print("Tiempo total de ejecución en segundos:" , fin-inicio)

"""#SVM"""

inicio = time.time()
# Código a medir
time.sleep(1)
from sklearn import svm
rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo',max_iter =-1).fit(X_train, y_train)
print("rbf Test set score: {:.2f}".format(rbf.score(X_test, y_test)))
print("rbf Train set score: {:.2f}".format(rbf.score(X_train, y_train)))

y_pred=rbf.predict(X_test)

print("Test mean_squared_error: {:.3f}".format(mean_squared_error(y_test, y_pred)))
print("Test accuracy_score: {:.3f}".format(accuracy_score(y_test,y_pred)))
print("Test precision_score: {:.3f}".format(precision_score(y_test,y_pred, average='weighted')))
print("Test recall_score: {:.3f}".format(recall_score(y_test,y_pred, average='weighted')))
print("Test f1_score: {:.3f}".format(f1_score(y_test,y_pred, average='weighted')))
fin = time.time()
print("Tiempo total de ejecución en segundos:" , fin-inicio)

"""#RF"""

inicio = time.time()
# Código a medir
time.sleep(1)
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators=5, random_state=2)
forest.fit(X_train, y_train)
print("Test set score: {:.3f}".format(forest.score(X_test, y_test)))
print("Train set score: {:.3f}".format(forest.score(X_train, y_train)))

y_pred=forest.predict(X_test)

print("Test mean_squared_error: {:.3f}".format(mean_squared_error(y_test, y_pred)))
print("Test accuracy_score: {:.3f}".format(accuracy_score(y_test,y_pred)))
print("Test precision_score: {:.3f}".format(precision_score(y_test,y_pred, average='weighted')))
print("Test recall_score: {:.3f}".format(recall_score(y_test,y_pred, average='weighted')))
print("Test f1_score: {:.3f}".format(f1_score(y_test,y_pred, average='weighted')))
fin = time.time()
print("Tiempo total de ejecución en segundos:" , fin-inicio)

"""#XGBoost"""

inicio = time.time()
# Código a medir
time.sleep(1)
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# fit model no training data
xgbc = XGBClassifier(objective= 'multi:softmax',num_class= 99,gamma= 0.1,max_depth= 12,reg_lambda=2,subsample= 1,colsample_bytree=0.7,min_child_weight=3).fit(X_train, y_train)
print("Test set score: {:.3f}".format(xgbc.score(X_test, y_test)))
print("Train set score: {:.3f}".format(xgbc.score(X_train, y_train)))

y_pred=xgbc.predict(X_test)

print("Test mean_squared_error: {:.3f}".format(mean_squared_error(y_test, y_pred)))
print("Test accuracy_score: {:.3f}".format(accuracy_score(y_test,y_pred)))
print("Test precision_score: {:.3f}".format(precision_score(y_test,y_pred, average='weighted')))
print("Test recall_score: {:.3f}".format(recall_score(y_test,y_pred, average='weighted')))
print("Test f1_score: {:.3f}".format(f1_score(y_test,y_pred, average='weighted')))
fin = time.time()
print("Tiempo total de ejecución en segundos:" , fin-inicio)