import numpy as np
# import cv2
from cnn import CNN
from keras.utils import np_utils
from keras import optimizers
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.nan)

class CNN1(object):
	def __init__(self, train_img=None, train_labels=None, test_img=None, test_labels=None,b_size=None,num_epoch=None):
		self.train_img = train_img
		self.train_labels = train_labels
		self.test_img = test_img
		self.test_labels = test_labels

		self.b_size=b_size
		self.num_epoch=num_epoch

	def train(self):

		#Change data to required format
		img_rows,img_columns = 45,45
		train_data = self.train_img.reshape((self.train_img.shape[0], img_rows,img_columns))
		train_data = train_data[:, np.newaxis, :, :]
		test_data = self.test_img.reshape((self.test_img.shape[0], img_rows,img_columns))
		test_data = test_data[:, np.newaxis, :, :]
		label_map={}
		count = 0
		for folder in os.listdir("../src/data"):
			label_map[folder]=count
			count+=1
		for i in range(len(self.train_labels)):
			self.train_labels[i]=label_map[self.train_labels[i]]
		for j in range(len(self.test_labels)):
			self.test_labels[j]=label_map[self.test_labels[j]]

		# Transform training and testing data to 10 classes in range [0,classes] ; num. of classes = 0 to 9 = 10 classes
		total_classes = count
		train_labels = np_utils.to_categorical(self.train_labels, total_classes)
		test_labels = np_utils.to_categorical(self.test_labels,total_classes)


		# Defing and compile the SGD optimizer and CNN model
		print('\n Compiling model...')
		sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
		clf = CNN().build(img_rows,img_columns,1,total_classes)
		clf.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

		# Initially train and test the model; If weight saved already, load the weights using arguments.
		num_epoch = self.num_epoch		# Number of epochs
		verb = 1			# Verbose
		print('\nTraining the Model...')
		model_info=clf.fit(train_data, train_labels, batch_size=self.b_size, nb_epoch=num_epoch,verbose=verb)

		# Evaluate accuracy and loss function of test data
		print('Evaluating Accuracy and Loss Function...')
		loss, accuracy = clf.evaluate(test_data, test_labels, batch_size=self.b_size, verbose=1)
		print('Accuracy of Model',(accuracy * 100))
		clf.save_weights('model.h5', overwrite=True)
		print(model_info.history)
		self.plot_model_history(model_info)
		return accuracy
	def test(self):
		'''

		use self.clf to get score/accuracy
		prints accuracy
		draws plot
		'''
		img_rows,img_columns = 45,45
		test_data = self.test_img.reshape((self.test_img.shape[0], img_rows,img_columns))
		test_data = test_data[:, np.newaxis, :, :]
		label_map={}
		count = 0
		for folder in os.listdir("../src/data"):
			label_map[folder]=count
			count+=1
		for j in range(len(self.test_labels)):
			self.test_labels[j]=label_map[self.test_labels[j]]
		total_classes = count
		test_labels = np_utils.to_categorical(self.test_labels,total_classes)
		sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
		clf = CNN().build(img_rows,img_columns,1,total_classes,'model.h5')
		clf.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
		loss, accuracy = clf.evaluate(test_data, test_labels, batch_size=self.b_size, verbose=1)
		print('Accuracy of Model: {:.2f}%'.format(accuracy * 100))
		return accuracy
	def predict(self,test_img):
		img_rows,img_columns = 45,45
		count = 0
		label_map={}
		for folder in os.listdir("../src/data"):
			label_map[folder]=count
			count+=1
		total_classes = count
		clf = CNN().build(img_rows,img_columns,1,total_classes,'model.h5')
		probs = clf.predict(test_img)
		print(probs)
		prediction = probs.argmax(axis=1)
		return prediction


	def get_probs_cnn(self,img):
		img_rows,img_columns = 45,45
		count = 0
		label_map={}
		for folder in os.listdir("../src/data"):
			label_map[folder]=count
			count+=1
		total_classes = count
		clf = CNN().build(img_rows,img_columns,1,total_classes,'../src/model.h5')
		probs = clf.predict(img)
		return probs
	def plot_model_history(self,model_history):
	    fig, axs = plt.subplots(1,2,figsize=(15,5))
	    # summarize history for accuracy
	    axs[0].plot(range(1,len(model_history.history['acc'])+1),model_history.history['acc'])
	    # axs[0].plot(range(1,len(model_history.history['val_acc'])+1),model_history.history['val_acc'])
	    axs[0].set_title('Model Accuracy')
	    axs[0].set_ylabel('Accuracy')
	    axs[0].set_xlabel('Epoch')
	    axs[0].set_xticks(np.arange(1,len(model_history.history['acc'])+1),len(model_history.history['acc'])/10)
	    axs[0].legend(['train', 'val'], loc='best')
	    # summarize history for loss
	    axs[1].plot(range(1,len(model_history.history['loss'])+1),model_history.history['loss'])
	    # axs[1].plot(range(1,len(model_history.history['val_loss'])+1),model_history.history['val_loss'])
	    axs[1].set_title('Model Loss')
	    axs[1].set_ylabel('Loss')
	    axs[1].set_xlabel('Epoch')
	    axs[1].set_xticks(np.arange(1,len(model_history.history['loss'])+1),len(model_history.history['loss'])/10)
	    axs[1].legend(['train', 'val'], loc='best')
	    plt.savefig("cnn_"+str(self.b_size)+"_"+str(self.num_epoch)+".png")
