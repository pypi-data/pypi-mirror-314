def lr():
  s="""
# 5
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error, mean_absolute_error 
import seaborn as sns

df=pd.read_csv('')
df.head()
X=df['Head Size(cm^3)'].values 
Y=df['Brain Weight(grams)'].values
X=X.reshape(-1,1)
Y=Y.reshape(-1,1)
xtrain,xtest,ytrain,ytest=train_test_split(X,Y,test_size=0.2,random_state=42)

lr=LinearRegression()
lr.fit(xtrain,ytrain)
ypred=lr.predict(xtest)

plt.scatter(xtrain,ytrain,color='red')
plt.plot(xtrain,lr.predict(xtrain),color='blue')
plt.title('Training Data')

print(mean_squared_error(ytest,ypred))
print(mean_absolute_error(ytest,ypred))
print(mean_squared_error(ytest,ypred)**0.5)
"""
  print(s)

def dt():
  s="""
# 6
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split as tts
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

x, y = make_classification(n_samples=1000, n_classes=2, n_features=5, n_redundant=0, random_state=1)
xtrain,xtest,ytrain,ytest=tts(x,y,test_size=0.25, shuffle=True)
models=[]
models.append((DecisionTreeClassifier()))
models.append((LinearRegression()))
models.append((KNeighborsClassifier()))
models.append((LinearDiscriminantAnalysis()))
models.append((GaussianNB()))
models.append((SVC()))
names=['DTC','LR','KNN','LDA','NB','SVC']
scores=[]
for i in models:
  i.fit(xtrain,ytrain)
  scores.append(i.score(xtest,ytest))
  print(names[models.index(i)],scores[-1])

plt.bar(names,scores)
"""
  print(s)

def kms():
  s="""
# 7
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df=pd.read_csv('')
x=df[['Annual Income (k$)','Spending Score (1-100)']]
x=StandardScaler().fit_transform(x)

el=[]
for i in range(1,11):
  model=KMeans(n_clusters=i)
  model.fit(x)
  el.append(model.inertia_)

# plt.plot(range(1,11),el)

km=KMeans(n_clusters=5)
y=km.fit_predict(x)

plt.scatter(x[:,0],x[:,1],c = y,alpha=0.5)
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],c='red')
plt.plot()
"""
  print(s)

def ann():
  s="""
# 8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

df=pd.read_excel('')

le=LabelEncoder()

#label encode req cols
df['Gender']=le.fit_transform(df['Gender'])
df['Geography']=le.fit_transform(df['Geography'])

xtrain,xtest,ytrain,ytest=train_test_split(df.drop(['RowNumber','CustomerId','Surname','Exited'],axis=1),df['Exited'],test_size=0.2,random_state=42)

sc=StandardScaler()
xtrain=sc.fit_transform(xtrain)
xtest=sc.transform(xtest)

model=Sequential()
model.add(Dense(units=6,activation='relu',input_dim=10))
model.add(Dense(units=6,activation='relu'))
model.add(Dense(units=1,activation='sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

model.fit(xtrain,ytrain,batch_size=10,epochs=100)

loss,accuracy=model.evaluate(xtest,ytest)
print(accuracy)
"""
  print(s)

def cnn():
  s="""
# 9
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np

(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=10,
                    validation_data=(test_images, test_labels))

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend()
plt.show()

probability_model = tf.keras.Sequential([model,
                                        tf.keras.layers.Softmax()])
predictions = probability_model.predict(test_images)

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
              'dog', 'frog', 'horse', 'ship', 'truck']
num_images_to_display = 5
plt.figure(figsize=(10, 5))
for i in range(num_images_to_display):
  plt.subplot(1, num_images_to_display, i + 1)
  plt.imshow(test_images[i])
  plt.title(class_names[np.argmax(predictions[i])])
  plt.axis('off')
plt.show()
"""
  print(s)

def mnist():
  s="""
# 10
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy Curves')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

predictions = model.predict(x_test)

predicted_labels = np.argmax(predictions, axis=1)

actual_labels = np.argmax(y_test, axis=1)

num_images_to_display = 5
plt.figure(figsize=(10, 5))
for i in range(num_images_to_display):
  plt.subplot(1, num_images_to_display, i + 1)
  plt.imshow(x_test[i])
  plt.title(predicted_labels[i])
plt.show()
"""
  print(s)

def nlp():
  s="""
# 11
!pip install python-Levenshtein
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

import nltk
from nltk import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords, wordnet
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import Levenshtein

text=open('').read()
sentences=sent_tokenize(text)
words=word_tokenize(text)
# print(sentences)
# print(words)

fd=FreqDist(words)
# fd.most_common(5)

non_punc_words=[]
for word in words:
  if word.isalpha():
    non_punc_words.append(word)

stopwords=stopwords.words('english')
clean_words=[]
for word in non_punc_words:
  if word not in stopwords:
    clean_words.append(word)
fd1=FreqDist(clean_words)
# fd1.most_common(5)

fd1.plot(10)

text=" ".join(clean_words)
wc=WordCloud().generate(text)
plt.imshow(wc)
plt.axis("off")

cv=CountVectorizer()
bow=cv.fit_transform(sentences)
# print(bow.toarray())
# print(cv.vocabulary_)

# jaccard-----> score
def jaccard_score(a,b):
  a=set(a)
  b=set(b)
  return float(len(a.intersection(b)) / len(a.union(b)))
# print(jaccard_score(clean_words,non_punc_words))

def phonetic_sim(w1,w2):
  dist=Levenshtein.distance(w1,w2)
  max_len=max(len(w1),len(w2))
  if 1-(dist/max_len) >0:
    return 1.0-(dist/max_len)
  else:
    return 1.0
# print(phonetic_sim('hello','hallo'))

# for words in wordnet.synsets("Fun"):
#   for lemma in words.lemmas():
#     print(lemma)
word1=wordnet.synsets("Fun","n")[0]
word2=wordnet.synsets("champ","n")[0]
print(word1.wup_similarity(word2))
"""
  print(s)

def imgseg():
  s ="""
# 12
!pip install pixellib
!curl -LO https://github.com/ayoolaolafenwa/PixelLib/releases/download/0.2.0/pointrend_resnet50.pkl
!pip install pillow==9.5.0

import pixellib
from pixellib.torchbackend.instance import instanceSegmentation
import cv2
from google.colab.patches import cv2_imshow

segment_image = instanceSegmentation()

segment_image.load_model("")

image_path = ""

results, output = segment_image.segmentImage(image_path)

cv2_imshow(output)
"""
  print(s)

def ocr():
  s="""
# 13
!pip install pytesseract
!sudo apt install tesseract-ocr

import pytesseract
import cv2
from google.colab.patches import cv2_imshow

img = cv2.imread('')

text = pytesseract.image_to_string(img)

print(text)
"""
  print(s)

def fd():
  s=""" 
# 14
!pip install opencv-python

import cv2
from google.colab.patches import cv2_imshow

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

img = cv2.imread('')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.1, 4)
smile=smile_cascade.detectMultiScale(gray, 1.1, 4)
eyes=eyes_cascade.detectMultiScale(gray, 1.1, 4)

for (x, y, w, h) in faces:
  cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
  for (a, b, c, d) in smile:
    if (x < a < x + w) and (y < b < y + h):
      cv2.rectangle(img, (a, b), (a + c, b + d), (255, 0, 0), 2)
  for (e, f, g, i) in eyes:
    if (x < e < x + w) and (y < f < y + h):
      cv2.rectangle(img, (e, f), (e + g, f + i), (255, 0, 0), 2)

cv2_imshow(img)
"""
  print(s)