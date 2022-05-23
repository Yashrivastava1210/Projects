INTRODUCTION
------------

This folder includes all the Data Science Projects developed by me.

* Basic CNN Model
* SPAM classification
* Emotion Recognition using Audio Files
* Emotion Recognition using Video Files


BASIC CNN MODEL
---------------

Starting out as a Data Science student, the first step towards Machine Learning Modeling is always a basic Convolutional Neural Network or CNN. This project is a small step to the realm of Deep Learning and how image classification takes place. I used the readily available MNIST dataset to train my model for digit recognition and got back a good accuracy when tested on unseen data.

SPAM CLASSIFICATION
-------------------

This is the first major project undertaken by me which required all the steps for a basic data science project. The dataset that I used was readily available on Kaggle for free download. The first step was loading the data and performing EDA on it which gave some interesting results. I used multiple machine learning models to train my data and test their accuracies in order to find the model which best suited my dataset.
This project was undertaken as a group project with Kiran Rangwani (kirarang@iu.edu) and my part of the project included Modeling of all the ML algorithms.


EMOTION RECOGNITION
-------------------

Emotion recognition falls under the wide umbrella of classification problem in terms of Data science. For emotion recognition I used the RAVDESS dataset which is a collection of Audio, Video and Audio-video files. This project helped me to increase my knowledge on handling different types of files and design Deep Learning models, also to understand how they perform better than machine learning models for some cases.
 
 > Emotion Recognition in Audio Files:
    For loading and handling Audio Files I used Librosa Library. The model created for the predictions is a multi layer Recurrent Neural Network or RNN with various techniques applied to avoid overfitting and still get good results since the size of dataset was quite small.
 
 
 > Emotion Recognition in Video Files:
    Understanding emotions in video files is a bit tricky as human emotions have a wde range and keep on changing from time to time. To load video files I used open cv library which provides a great number of features for image and video file extraction and handling. I divided the video into each frame like an image and then trained the RNN model over it. The tests results on unseen data were quite good and it could be regenerated into a video which showed emotion being predicted by the system for each instance.
