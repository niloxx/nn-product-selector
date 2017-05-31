from keras.models import Sequential
from keras.layers import Dense

import numpy
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# load pima indians dataset
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]

# create model
model = Sequential()
model.add(Dense(100, input_dim=8, init='normal', activation='relu')) #Dense = Fully Connected ; uniform = 0 - 0.05
model.add(Dense(50, init='normal', activation='relu'))
model.add(Dense(1, init='normal', activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy']) #Adam = efficient gradient descent

# Fit the model
model.fit(X, Y, nb_epoch=300, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print(("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100)))

 
