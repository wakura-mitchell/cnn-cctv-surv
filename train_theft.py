#!/usr/bin/env python
# coding: utf-8

# Smart City surveillance system (IoT)

# In[1]:


import os
import cv2 as cv
import numpy as np
from imutils import paths


# In[2]:


from keras.applications import ResNet50

from keras.layers import Input, Flatten, Dropout, Dense
from keras.layers import AveragePooling2D

from keras.optimizers import SGD

from keras.models import Model


# In[3]:


from sklearn.preprocessing import LabelBinarizer


# In[4]:


datapath = ('./data')
outputModel = ('./model/theftSurvModel')
outputLB = ('./model/theftSurvLB.pickle')
epoch = 25


# In[15]:


#09/10/2023 test using crime dataset
theft_labels = set(['gun_theft', 'pick_pocketing_theft', 'robbery_theft', 'shoplifting_theft', 'snitching_theft', 'theft'])
print ('Images are being loaded.....')
pathToimages = list(paths.list_images(datapath))
data = []
labels = []

for images in pathToimages:
    label = images.split(os.path.sep)[-2]
    if label not in theft_labels:
        continue
    image = cv.imread(images)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = cv.resize(image, (244,244))
    data.append(image)
    labels.append(label)


# In[16]:


data = np.array(data)
labels = np.array(labels)

#hot encode theft laabes as 0,1,2,3,4
lb = LabelBinarizer()
labels = lb.fit_transform(labels)


# In[17]:


from sklearn.model_selection import train_test_split


# In[18]:


(X_train, x_test, Y_train, y_test) = train_test_split(data, labels, test_size = 0.25, stratify = labels, random_state = 42)


# In[19]:


from keras.preprocessing.image import ImageDataGenerator


# In[20]:


trainingArgumentation = ImageDataGenerator(
    rotation_range = 30,
    zoom_range = 15,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    shear_range = 0.15,
    horizontal_flip = True,
    fill_mode = 'nearest'
)

validationArgumentation = ImageDataGenerator()
mean = np.array([123.68, 116.779, 103.939], dtype = 'float32')

trainingArgumentation.mean = mean

validationArgumentation.mean = mean


# In[21]:


baseModel = ResNet50(
    weights = 'imagenet',
    include_top = False,
    input_tensor = Input(shape = (244,244,3))
)

headModel = baseModel.output
headModel = AveragePooling2D(pool_size = (7,7))(headModel)

headModel = Flatten(name = 'flatten')(headModel)

headModel = Dense(512, activation = 'relu')(headModel)

headModel = Dropout(0.5)(headModel)

headModel = Dense(len(lb.classes_), activation = 'softmax')(headModel)

model = Model(inputs = baseModel.input, outputs = headModel)

for basemodellayers in baseModel.layers:
    basemodellayers.trainable = False


# In[22]:


#since we imported from keras.optimizers import SGD
opt = SGD(learning_rate = 0.0001, momentum = 0.9)


# In[23]:


model.compile(loss = 'categorical_crossentropy', optimizer = opt, metrics = ['accuracy'])


# In[24]:


History = model.fit_generator(
    trainingArgumentation.flow(X_train, Y_train, batch_size = 32),
    steps_per_epoch = len(X_train) // 32,
    validation_data = validationArgumentation.flow(x_test, y_test),
    validation_steps = len(x_test) // 32,
    epochs = epoch
)


# In[25]:


import pickle


# In[26]:


model.save(outputModel)
lbinarizer = open('./model/theftSurvLB.pickle','wb')
lbinarizer.write(pickle.dumps(lb))
lbinarizer.close()

