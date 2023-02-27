# ApplicationDataSecurity_using_AI-ML_and_CYBERSECURITY

This project deals with the safety of the data that the smarthphone users usually have to take care of. Most of the users want their data to be safe and secure and no one from the external source should use or fetcht their data as the third party attack.
This project work on the concept of machine learning, android applicaton and the cybersecurity which block the every third party or also you can say that the 'THE MAN IN THE MIDDLE' in terms of cybersecurity or ethical hacking.
This will disallow every user apart from the real user to see or modify or delete the data using a proper authectiocation and verification.
These verifications is done using the records of the gestures of the real user and make the model to train itself using these gestures so that, whoever apart from the real user come to fetch the smartphone data the model will make the smartphone lock by identifying some of  the different gestures from the user side who is currently woring on that smartphone.



# MONGODB ISNTALLATION
For the proper and effective way to use the data which we are going to handle with in this project is through the mongodb server which allows us to mange the data's and the collection of data's and to manage the databases.
For proper installation of  the MongoDB, refer the following link:

https://www.geeksforgeeks.org/how-to-install-mongodb-on-windows/

After successful installationg of  the community server edition of the MongoDB, you are now ready to move further............




# PYTHON INSTALLATION

For setting the variables and for the implemenetion of the project, we are using python.
For the proper installation of python, go onto the below url and perform the steps:-

https://www.geeksforgeeks.org/how-to-install-python-on-windows/

After installation of python, go onto the next steps discussed below...............



# Description of the repository

The repository consists of the following 4 files.

- ContinuousImplicitAuthentication.py: This file includes the methodology of applying Novelty Detection Algorithms to recognise users bahaviour through accelerometer and gyroscope data 
- Sensors_and_GesturesContinuousImplicitAuthentication.py: This file includes the methodology of applying Novelty Detection Algorithms to recognise users bahaviour through accelerometer data,gyroscope data and gestures data
- metrics.py: Class that contains the calculated metrics for each model
- features.py: Class that contains the input features from each machine learning model
- dataHandler.py: Handles gestures data from MongoDB.
- MongoDBHandler.py: Used for Gestures Data. Connection to MongoDB.

# Prerequisites

## Dataset 

As we have discussed above in the project description, we are going to handle  the lot of data's including the gestures of  the users, and the data we are achieving using our sensors as the whole recording of the gestures is done by the sensors.

For getting the dataset you can visit the following link, or else I have given the whole dataset in my repo, you can refer that also.
https://zenodo.org/record/2598135#.X4H0qXgzbeo

The proper documentation of the dataset which i'm using here can be found by the below link:
https://res.mdpi.com/data/data-04-00060/article_deploy/data-04-00060.pdf?filename=&attachment=1
 
There are basically 2 types of data set files
1:- sensors data
2:- gestures data

Sensor's data is the data which contains the JSON file containing the records of 2000 users data which has been recorded using the sensors in the terms of key:value pairs



# SYSTEM CONFIGURATION
1:- After the proper installation of the MongoDB and the python, download the dataset form the link or copy from my repo.
2:- Create any folder according to your choice(let xyz).
3:- Now, Inside the xyz folder you have to make some of the some folders by the name of the users
For example,let suppose the user name is 0hz8270, then make a folder using the name of this user and let the user 0hz8270 has 67 JSON files. Move all of them inside folder 0hz8270.
4:- Set the enviroment variables
4.1:- Add the new path
4.2:- Inside that new path add the path of the xyz folder created above.

5:- For gestures data visualization, we use the MongoDB which we have previously installed on our system(be sure you have installed  the MongoDB in your system)
6:- Import the gestures data in MongoDB server(refer page No 12 of :-  https://res.mdpi.com/data/data-04-00060/article_deploy/data-04-00060.pdf?filename=&attachment=1)
7:- Now you are ready to start MongoDB.
8:- Go to terminal or powershell, and write Mongo
9:- Type dbs(to list of all the databases), and use the database or create a new database for further work.
10:- For creating or using the database(command :- use db_name)............


# EXECUTING OF THE PROGRAM

1:- Be sure of that it this point, you have python installed in your system.
2:- Now, we have to set some of the variables required for our project execution.
  2.1:- set the path variable previously told.
  2.2:- set some name for the database using 'use' command (eg :- use mydatabase).
3:- Now you can able to run the project from the terminal or powershell or from any ide.(command to run from the terminal :- python3 ContinuousImplicitAuthentication.py)

# Methodology

Within the context of this study, the accelerometer and gyroscope sensors were selected to model the way a user interacts with its smartphone. The measurements were collected in an uncontrolled environment from an application downloaded from the Store. Two machine learning models were trained, one for each sensor and then, the results were combined to produce the final system’s performance. The performance of the final system exceeded the performance of the literature.

## Dataset Description

The dataset used is called BrainRun and is a set of biometric data for use in continuous implicit user authentication. A mobile application called BrainRun for Android and iOS mobile phones was developed for data collection. The application includes a list of brain training games through which data is collected from the sensors. BrainRun includes five different game-types, which are called “Focus”, “Mathisis”, “Memoria”, “Reacton”, and “Speedy”, and their main goal is the collection of users’ information. Each game-type is specifically designed to collect different kind of hand gestures, such as taps, horizontal swipes, vertical swipes, swipes and taps combined, etc. In addition, sensors measurements are collected from accelerometer, gyroscope kai magnetometer sensor.

## Data Preprocessing

The data received from the motion sensors are of the form (x, y, z, screen), where x, y, z is the position of the mobile according to the 3 axes and screen is the game that was recorded e.g. SpeedyGame. The accelerometer detects changes in the orientation of the mobile phone (rate of change of speed) in relation to the x, y and z axes, while the gyroscope helps the accelerometer to understand how the mobile phone is oriented, adding an extra level of accuracy.

The dataset, for each user, consists of an unknown number of JSON files. Each JSON file is also a timestamp, during which the data was collected. In addition to the values x, y, z, their derivatives are also calculated, such as the magnitude and the combined angle.

To select the appropriate variable, experiments were performed with each variable (x, y, z, combined angle, magnitude) and at the end, the performance of the algorithms was compared. From the experiments, it emerged that the variable **magnitude** was the one with which, the models achieved the best performance.

Formulae:-
(x^2 + y^2 + z^2)^05
(y^2 + z^2)^0.5

## ERROR CHECKING AND CORRECTION DURING THE RECORDING OF THE GESTURES USING THE SENSORS

Using the sensors, whatever the data we are downloading from, it is of sure it is not correct. It should have some of the outliers or the wrong values, which in this case we are using by checking the previous value and the currenct value.
we are making record of the previou value and the current value, and while making the note of it, if in case we are getting some irrelevant data(like odd one out), then we are simply making that data correct or else simply remove it accoring to your choice.

## FEATURE EXTRACTION

Feature extraction is the feature selection process, which is considered important, in the sense that they provide valuable knowledge for drawing conclusions and correlations. Choosing the right features is a key factor in the performance of a model. The need to export key signal characteristics to enable advanced processing algorithms to discover useful information has led to the development of a wide range of algorithmic approaches. These approaches are based on converting input signals to and from different areas of representation. 

For this project, the final features that were chosen are shown below. From the time domain, I choose 9 features and from the frequency domain, I choose 4. I used correlation for dimensional reduction.

| Feature       | Description   | Domain        |
| ------------- | ------------- | ------------- |
| Mean  | Mean value  | Time  |
| STD  | Standard deviation  | Time  |
| Max  | Maximum value  | Time  |
| Min  | Minimum value  | Time  |
| Percentile25  | 25% quartiles  | Time  |
| Percentile50  | 50% quartiles  | Time  |
| Percentile75  | 75% quartiles  | Time  |
| Kurtosis  | Width of peak  | Time  |
| Skewness  | Orientation of peak | Time  |
| P1  | Amplitude of the first highest peak | Frequency  |
| F1  | Frequency of the second highest peak | Frequency  |
| P2  | Amplitude of the second highest peak  | Frequency  |
| Mean Frequency  | Mean value of frequencies  | Frequency  |

Once the feature vector is finished, I used normalization to transform data into [0,1]. Normalization is a rescaling of the data from the original range so that all values are within the new range of 0 and 1. Normalization is very important when we use machine learning algorithms based on distance. The scale of the data matters and data that are on a higher scale than others may contribute to the result more due to their larger value. So we normalize the data to bring all the variables to the same range.

## Training Algorithms

I used 4 Novelty Detection Algorithms:
- Local Outlier Factor 
- One Class SVM
- Isolation Forest
- Elliptic Envelope - Robust Covariance

For Hyperparameter Tuning, the Cross-Validation technique was applied in combination with the Grid Search technique. The purpose of cross-validation is to determine the learning parameters that generalize well. The right choice of hyper-parameters is extremely important to achieve a good performance of a model. The process of finding the right hyper-parameters is a process of Try and Error, as there is no mathematical way to show the appropriate value for each problem or there is no mathematical formula, which through the training data, can extract the appropriate prices.

The Hyperparameter Tuning procedure is shown below.
![image](https://user-images.githubusercontent.com/104202659/221658234-242f9817-e3c8-40a7-9e78-22da9e22da7a.png)


The following steps were applied:
- For each user
- - 5 repetitions
- - 1. Split dataset into 3 sub-sets, training, validation and test with a random way
- - 2. K old(here k can be any numeric value, for example k=20 or k = 10)
- - 3. Test in the training set
- -  Choose the best hyper-parameters
- - Test on the validation set
- Test in the test set
- Final values of hyper-parameters

## Ensemble Learning

Ensemble learning improves the overall accuracy of the system by combining 2 or more models. The combination of models is achieved either by combining 2 or more models of different algorithms or by combining models of the same algorithms but with some differences.

Ensemble Learning is shown below.
![image](https://user-images.githubusercontent.com/104202659/221658173-72cee8d1-49c0-4f8e-a20a-03e55e7ba009.png)

Initially, the data of the 2 sensors (gyroscope and accelerometer) must be identical in time, ie each recording of the accelerometer must correspond to one recording of the gyroscope at the same time. Unidentified samples were discarded. The result of the above processing is 2 different datasets, which consist of the same set of data with measurements from the 2 sensors (one contains measurements from the accelerometer, while the other from the gyroscope) at the same time. 

The next step is the training of the 2 models. Each is trained separately with the corresponding dataset. The results are combined using the decision_function function. The decision_function function predicts the confidence (probability) scores for each sample. The confidence score for a sample is the distance of that sample from the separation surface. When its value for a sample is positive, it means that this sample belongs to the class of the real user, ie the positive class, while when its value for a sample is negative, it means that this sample is an extreme value, therefore it is classified as a malicious or unauthorized user. During the training process, the distance of each sample from the separation surface is calculated and the maximum distance for each model is found. 

Then, after completing the prediction process, divide the distance of each sample by the maximum distance calculated in the training and what emerges is a good estimate of the probability that the investigated sample belongs to the class of the actual user or to the class of the malicious user. Once the execution of the 2 models is completed, the process of combining the results of the models follows. During the combination, for each sample, the above estimate from the 2 models is added and if the sum value is positive the sample is categorized as a real user otherwise as a malicious user.

# EVALUTIONG METRICS
Evaluation is always good in any field right! In the case of machine learning, it is best the practice. In this post, I will almost cover all the popular as well as common metrics used for machine learning.

Confusion Matrix
Classification Accuracy.
Logarithmic loss.
Area under Curve.
F1 score.
Mean Absolute Error.
Mean Squared Error.

Using the above evalution metrics, we are able to get the performance of our model and better accuracy.



# Conclusions

- Motion sensor measurements (accelerometer, gyroscope) provide valuable information related to user behavior, capable of user identification only with navigation data.
- Proper data processing was considered vital. The correct selection of the sampling and overlap window significantly improved the performance of the algorithms. The appropriate selection of features, which are the independent variables, improved the performance of the models as they were the features, based on which the algorithms learned the distribution of the authorized user's behavior. The combination of data in the domain of time and frequency gave the best results.
- The behavior and performance fluctuations of the algorithms were kept constant in all experiments. This leads to the conclusion that the models that were trained, the algorithms that were selected, and the data processing that followed, led to strong and robust models that can be used in the real world.
- One Class SVM and Local Outlier Factor algorithms efficiently solve the problem of continuous implicit authentication. Their performance surpassed that of the literature.
- For applications that require a low acceptance rate of malicious or unauthorized users (<0.7%), the Local Outlier Factor algorithm is more appropriate.
- For applications that require a low actual user rejection rate (<5.7%) combined with a low malicious user acceptance rate (1.1%), the One Class SVM algorithm is considered appropriate.
- The One Class SVM and Local Outlier Factor algorithms achieved the best percentages of metric FAR compared to all literature studies, even those using the same dataset. The percentages of metric FRR were particularly low (4-6%) and comparable to the literature, but in some cases slightly higher.
- This study was applied to uncontrolled environmental data. Most of the literature studies were done in a controlled environment.
- **The results show that the proposed approach provides an additional level of security and privacy and can ensure that 99% of unauthorised users will be denied access to the device and the users' personal data.**
