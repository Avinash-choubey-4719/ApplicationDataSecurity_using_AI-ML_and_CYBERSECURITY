import os
import sys
import math
import random
import matplotlib.pyplot as plt
import matplotlib.font_manager
import pandas as pd
import numpy as np
import ujson as json

from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score

from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import IsolationForest

from sklearn import metrics
from sklearn import svm
from sklearn import decomposition
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.covariance import EllipticEnvelope
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import LocalOutlierFactor
from scipy.stats import skew, kurtosis, entropy
from scipy.fftpack import fft,fft2, fftshift
from numpy import quantile, where, random

from metrics import Metrics
from features import Features

# =============================================================================
# Functions
# =============================================================================

# This function extract features with the method sliding window.
def FeatureExtraction(dataset, samples, overlap, output, feautureObject, feature):

    for w in range(0, dataset.shape[0] - samples, overlap):
        end = w + samples 
        #DFT
        discreteFourier = fft(dataset.iloc[w:end, feature])
        # Frequencies
        freq = np.fft.fftfreq(samples)

        # Amplitudes
        idx = (np.absolute(discreteFourier)).argsort()[-2:][::-1]
        amplitude1 = np.absolute(discreteFourier[idx[0]])
        amplitude2 = np.absolute(discreteFourier[idx[1]])
        frequency2 = freq[idx[1]]

        # Frequency features
        mean_frequency = np.mean(freq)
        feautureObject.setAmplitude1(amplitude1)
        feautureObject.setAmplitude2(amplitude2)
        feautureObject.setFrequency2(frequency2)
        feautureObject.setMean_frequency(mean_frequency)

        # Time Based Feautures
        feautureObject.set??ean(np.mean(dataset.iloc[w:end, feature]))
        feautureObject.setSTD(np.std(dataset.iloc[w:end, feature]))
        feautureObject.setMax(np.max(dataset.iloc[w:end, feature]))
        feautureObject.setMin(np.min(dataset.iloc[w:end, feature]))
        feautureObject.setRange(np.ptp(dataset.iloc[w:end, feature]))

        percentile = np.percentile(dataset.iloc[w:end, feature], [25, 50, 75])
        feautureObject.setPercentile25(percentile[0])
        feautureObject.setPercentile50(percentile[1])
        feautureObject.setPercentile75(percentile[2])
        feautureObject.setEntropy(entropy(dataset.iloc[w:end, feature], base = 2))

        feautureObject.setKurtosis(kurtosis(dataset.iloc[w:end, feature]))
        feautureObject.setSkewness(skew(dataset.iloc[w:end, feature]))

        # Output Label
        feautureObject.setY(output)

    return  feautureObject

# This function calculates average metrics per model. (FAR, FRR, Confucion Matrix, Accuracy and F1-Score)
def PerformanceMetrics(users, model, text):

    accuracy_average = 0
    f1score_average = 0
    far_average = 0
    frr_average = 0
    roc_average = 0
    for i in range(0, len(users)):
        accuracy_average = accuracy_average + model.getAccuracy()[i]
        f1score_average = f1score_average +  model.getf1score()[i] 
        far_average = far_average +  model.getFAR()[i]
        frr_average = frr_average +  model.getFRR()[i]

    print()
    print('AVERAGE ONE CLASS SVM PERFORMANCE MODEL: ' + text)
    print('Accuracy: ', accuracy_average / len(users), '\nF1 Score: ', f1score_average / len(users), '\nFAR: ', far_average / len(users), '\nFRR: ', frr_average / len(users))
    sumTest = sum(model.getsizeTest())
    sumFalseAccept = sum(model.getfalseAccept())
    sumFalseReject = sum(model.getfalseReject())
    sumTrueAccept = sum(model.gettrueAccept())
    sumTrueReject = sum(model.gettrueReject())
    print('Confusion Matrix')
    print(sumTrueReject, ' ',  sumFalseAccept)
    print(sumFalseReject, ' ',  sumTrueAccept)

# Local Outlier Factor Algorithm Execution
def LocalOutlierFactorAlgorithm(parameters, X_train, X_test):

    model = LocalOutlierFactor(n_neighbors = parameters[0], novelty = True)
    model.fit(X_train)
    decision = model.decision_function(X_train)
    maxDistance = max(decision) 
    prediction = model.predict(X_test)

    decision = model.decision_function(X_test)
    decision = decision /maxDistance

    return decision, prediction

# Elliptic Envelope Algorithm Execution
def EllipticEnvelopeAlgorithm(parameters, X_train, X_test):

    model = EllipticEnvelope(contamination = parameters[0]).fit(X_train)
    decision = model.decision_function(X_train)
    maxDistance = max(decision) 
    prediction = model.predict(X_test)

    decision = model.decision_function(X_test)
    decision = decision /maxDistance

    return decision, prediction

# Isolation Forest Algorithm Execution
def IsolationForestAlgorithm(parameters, X_train, X_test):

    model = IsolationForest(n_jobs = -1, n_estimators = parameters[0], contamination = parameters[1], bootstrap = False).fit(X_train)
    decision = model.decision_function(X_train)
    maxDistance = max(decision) 
    prediction = model.predict(X_test)

    decision = model.decision_function(X_test)
    decision = decision /maxDistance

    return decision, prediction

# One Class SVM Algorithm Execution
def OneClassSVMAlgorithm(parameters, X_train, X_test):

    model = svm.OneClassSVM(gamma = parameters[0], kernel = 'rbf', nu = parameters[1], cache_size = 500)
    model.fit(X_train)
    decision = model.decision_function(X_train)
    maxDistance = max(decision) 
    prediction = model.predict(X_test)

    decision = model.decision_function(X_test)
    decision = decision /maxDistance

    return decision, prediction

# This function executed the Machine Learning Algorithm
def AlgorithmExecution(trainData, testData, algorithm, parameters, text, model):

    # Split Dataset in a random way 
    percent = int(math.ceil(0.2 * trainData.shape[0]))
    sampling = trainData.sample(n = percent)
        
    indecies = []
    for ii in range(0, percent):
        indecies.append(sampling.iloc[ii,:].name)

    test = pd.concat([testData, sampling])
    train = trainData.drop(trainData.index[indecies])

    X_train = train.iloc[:,0:test.shape[1]-2]
    y_train = train.iloc[:,test.shape[1]-1 ]

    X_test = test.iloc[:,0:test.shape[1]-2]
    y_test = test.iloc[:,test.shape[1]-1]

    print('After Split Sizes:')
    print('Train Size One Class: ', X_train.shape[0], 'Test Size Two Class: ', y_test.shape[0])

    # MinMaxScaler Normalized to [0,1]
    scaler = MinMaxScaler().fit(X_train)
    X_train_norm = scaler.transform(X_train)
    X_test_norm = scaler.transform(X_test)

    # Call the appropriate algorithm, loop throught the functions, find the desired algorithm and execute it
    functions = (LocalOutlierFactorAlgorithm, EllipticEnvelopeAlgorithm, IsolationForestAlgorithm, OneClassSVMAlgorithm)
    for func in functions:
        functionName = func.__name__
        if algorithm in functionName:
            decision, prediction = func(parameters, X_train_norm, X_test_norm)
        
    print("******************************* Model " + text + " *******************************")
    score = f1_score(y_test, prediction, pos_label = 1)
    #print('F1 Score: %.3f' % score)
    acc = accuracy_score(y_test, prediction)
    #print(f'SVM accuracy is {acc}')
    cfm = confusion_matrix(y_test, prediction, labels = [-1, 1])
    print(cfm)
    np.sum(y_test == -1)
    far = cfm[0,1]/ np.sum(y_test == -1)
    frr = cfm[1,0]/ np.sum(y_test == 1)
    print('FAR: ', far, ' FFR: ', frr)
    
    model.setFAR(far)
    model.setFRR(frr)
    model.setAccuracy(acc)
    model.setf1score(score)
    model.setfalseAccept(cfm[0,1])
    model.setfalseReject(cfm[1,0])
    model.settrueAccept(cfm[1,1])
    model.settrueReject(cfm[0,0])
    model.setsizeTest(y_test.shape[0])

    # AUC represents the probability that a random positive (green) example is positioned to the right of a random negative (red) example.
    roc = roc_auc_score(y_test, prediction)
    #print('ROC AUC Score: ',roc)

    return decision, model, y_test

# Load Dataset and save it in Dataframes
def loadDataset(path, screenName):

    users = [ f.path for f in os.scandir(path) if f.is_dir() ]
    info = pd.DataFrame(columns= ['accelometer_size', 'gyroscope_size', 'timestamp'])

    accelerometer = pd.DataFrame(columns=['x', 'y', 'z', 'screen', 'user', 'magnitude','combine_angle', 'timestamp'])
    gyroscope = pd.DataFrame(columns=['x_gyroscope', 'y_gyroscope', 'z_gyroscope', 'screen_gyroscope', 'user_gyroscope', 'magnitude_gyroscope', 'combine_angle_gyroscope', 'timestamp_gyroscope'])

    # Read sensors data from json file and save them in Dataframes
    for i in range(0, len(users)):

        json_files = [pos_json for pos_json in os.listdir(users[i]) if pos_json.endswith('.json')]

        for index, js in enumerate(json_files):
            with open(os.path.join(users[i], js)) as json_file:
                json_text = json.load(json_file)
                accSize = 0
                gyrSize = 0
                js = js.replace('.json','')
                arr = js.split('_')

                for j in json_text['accelerometer']:
                    if screenName in j['screen']:
                        x = j['x']
                        y = j['y']
                        z = j['z']
                        if x == 0 and y == 0:
                            continue
                        screen = j['screen']
                        user = arr[0]
                        m = x**2 + y**2 + z**2
                        m = np.sqrt(m)
                        ca = np.sqrt(y**2 + z**2)
                        timestamp = arr[1]
                        accSize = accSize + 1
                        df = {'x': x, 'y': y, 'z' : z, 'screen' : screen, 'user': user, 'magnitude' : m, 'combine_angle': ca, 'timestamp': timestamp}
                        accelerometer = accelerometer.append(df, ignore_index=True)
                        
                for j in json_text['gyroscope']:
                    if screenName in j['screen']:
                        x = j['x']
                        y = j['y']
                        z = j['z']
                        if x == 0 and y == 0:
                            continue
                        screen = j['screen']
                        user = arr[0]
                        m = x**2 + y**2 + z**2
                        m = np.sqrt(m)
                        ca = np.sqrt(y**2 + z**2)
                        timestamp = arr[1]
                        gyrSize =  gyrSize + 1
                        df = {'x_gyroscope': x, 'y_gyroscope': y, 'z_gyroscope' : z, 'screen_gyroscope' : screen, 'user_gyroscope': user, 'magnitude_gyroscope' : m, 'combine_angle_gyroscope': ca, 'timestamp_gyroscope': timestamp}
                        gyroscope = gyroscope.append(df, ignore_index=True)
                    
                dframe = {'accelometer_size': accSize, 'gyroscope_size': gyrSize, 'timestamp': arr[1]}
                info = info.append(dframe, ignore_index=True)

    return accelerometer, gyroscope, info, users

# This function calculates average performace of each user from 10-Fold
def averagePerformance_KFold(userModel, modelObject, K):

    far = 0
    frr = 0
    accu = 0  
    fscore = 0
    FA = 0
    FalseR = 0
    TrueA = 0
    TrueR = 0
    testS = 0

    for index in range(0, K):

        far = far + userModel.getFAR()[index]  
        frr = frr + userModel.getFRR()[index]  
        accu = accu + userModel.getAccuracy()[index]  
        fscore = fscore + userModel.getf1score()[index]
        FA = FA + userModel.getfalseAccept()[index]
        FalseR = FalseR + userModel.getfalseReject()[index]
        TrueA = TrueA + userModel.gettrueAccept()[index]
        TrueR = TrueR + userModel.gettrueReject()[index]
        testS = testS + userModel.getsizeTest()[index]
    
    modelObject.setAccuracy(accu/K)
    modelObject.setf1score(fscore/K)
    modelObject.setFAR(far/K)
    modelObject.setFRR(frr/K)
    modelObject.setfalseAccept(FA/K)
    modelObject.setfalseReject(FalseR/K)
    modelObject.settrueAccept(TrueA/K)
    modelObject.settrueReject(TrueR/K)
    modelObject.setsizeTest(abs(testS/K))

    return modelObject

# This function contains the methodology of Continious Implicit Authentication
def continuousImplicitAuthentication(users, accelerometer, gyroscope, info):

    # feauture variable gets values 0, 1, 5, 6
    # where 0 is X, 1 is Y, 5 is magnitude and 6 is combined angle
    feauture = 5
    samples = 500
    overlap = 50
    print('Feature: ', feauture)

    # Objects with metrics for each model
    accelerometerModel = Metrics()
    gyroscopeModel = Metrics()
    ensembleModel = Metrics()

    for user in users:
        
        # Objects with features for each model
        accelerometerFeatures = Features()
        gyroscopeFeatures = Features()

        # Dataset dataframe
        df = pd.DataFrame() 
        df_gyroscope = pd.DataFrame() 

        train = []
        test = []
        train_gyroscope = []
        test_gyroscope  = []
        arr = user.rsplit('/', 1)
        user = arr[1]
        print('User: ', user)

        # Create accelerometer and gyroscope Dataframes where each instance in accelerometer Dataframe 
        # has an instance in gyroscope Dataframe at the same timestamp. 
        for ind in info.index: 

            if info['accelometer_size'][ind] == 0 & info['gyroscope_size'][ind] == 0:
                continue
            else:

                if info['gyroscope_size'][ind] < info['accelometer_size'][ind]:
                    info['accelometer_size'][ind] = info['gyroscope_size'][ind]   
            
                if info['accelometer_size'][ind] < info['gyroscope_size'][ind]:
                    info['gyroscope_size'][ind] = info['accelometer_size'][ind]

                # Indecies where each timestamp contains accelometer and gyroscope measures
                idxAccelometer = accelerometer.index[accelerometer['timestamp'] == info['timestamp'][ind]]
                idxGyroscope = gyroscope.index[gyroscope['timestamp_gyroscope'] == info['timestamp'][ind]]

                for i in range(0, info['gyroscope_size'][ind]):

                    # Original user
                    if accelerometer.iloc[idxAccelometer[i],4] == user: 
                        frame = {'x': accelerometer.iloc[idxAccelometer[i],0], 'y' : accelerometer.iloc[idxAccelometer[i],1], 'z' : accelerometer.iloc[idxAccelometer[i],2], 
                        'screen' : accelerometer.iloc[idxAccelometer[i],3], 'user' : accelerometer.iloc[idxAccelometer[i],4], 'magnitude' : accelerometer.iloc[idxAccelometer[i],5],
                        'combine_angle' : accelerometer.iloc[idxAccelometer[i],6], 'timestamp': accelerometer.iloc[idxAccelometer[i],7]}
                        frame2 = {  'x_gyroscope' : gyroscope.iloc[idxGyroscope[i],0], 'y_gyroscope': gyroscope.iloc[idxGyroscope[i],1], 
                        'z_gyroscope': gyroscope.iloc[idxGyroscope[i],2], 'screen_gyroscope': gyroscope.iloc[idxGyroscope[i],3], 'user_gyroscope' : gyroscope.iloc[idxGyroscope[i],4], 
                        'magnitude_gyroscope': gyroscope.iloc[idxGyroscope[i],5], 'combine_angle_gyroscope': gyroscope.iloc[idxGyroscope[i],6], 'timestamp_gyroscope': gyroscope.iloc[idxGyroscope[i],7]}
                        train.append(frame)
                        train_gyroscope.append(frame2)
                    # Attackers    
                    else:
                        frame = {'x': accelerometer.iloc[idxAccelometer[i],0], 'y' : accelerometer.iloc[idxAccelometer[i],1], 'z' : accelerometer.iloc[idxAccelometer[i],2], 
                        'screen' : accelerometer.iloc[idxAccelometer[i],3], 'user' : accelerometer.iloc[idxAccelometer[i],4], 'magnitude' : accelerometer.iloc[idxAccelometer[i],5],
                        'combine_angle' : accelerometer.iloc[idxAccelometer[i],6], 'timestamp': accelerometer.iloc[idxAccelometer[i],7]}
                        frame2 = {  'x_gyroscope' : gyroscope.iloc[idxGyroscope[i],0], 'y_gyroscope': gyroscope.iloc[idxGyroscope[i],1], 
                        'z_gyroscope': gyroscope.iloc[idxGyroscope[i],2], 'screen_gyroscope': gyroscope.iloc[idxGyroscope[i],3], 'user_gyroscope' : gyroscope.iloc[idxGyroscope[i],4], 
                        'magnitude_gyroscope': gyroscope.iloc[idxGyroscope[i],5], 'combine_angle_gyroscope': gyroscope.iloc[idxGyroscope[i],6], 'timestamp_gyroscope': gyroscope.iloc[idxGyroscope[i],7]}
                        test.append(frame)
                        test_gyroscope.append(frame2)
                        
        print('Accelometer Data Sizes:\n', 'Train Size One Class: ', len(train), ' Test Size Two Class: ', len(test))
        train = pd.DataFrame(train)
        test = pd.DataFrame(test)

        train_gyroscope = pd.DataFrame(train_gyroscope)
        test_gyroscope = pd.DataFrame(test_gyroscope)

        # =============================================================================
        # Feature Extraction
        # =============================================================================     

        accelerometerFeatures = FeatureExtraction(train, samples, overlap, 1, accelerometerFeatures, feauture)
        gyroscopeFeatures = FeatureExtraction(train_gyroscope, samples, overlap, 1, gyroscopeFeatures, feauture)

        accelerometerFeatures = FeatureExtraction(test, samples, overlap, -1, accelerometerFeatures, feauture)
        gyroscopeFeatures = FeatureExtraction(test_gyroscope, samples, overlap, -1, gyroscopeFeatures, feauture)

        # =============================================================================
        # Machine Learning Models
        # ============================================================================= 

        # Add features to dataframe
        df['Mean'] = accelerometerFeatures.getMean() 
        df['Std'] = accelerometerFeatures.getSTD()
        df['Skew'] = accelerometerFeatures.getSkewness()
        df['Kurtosis'] = accelerometerFeatures.getKurtosis()
        df['Max'] = accelerometerFeatures.getMax()
        df['Min'] = accelerometerFeatures.getMin()
        #df['Range'] = Range
        df['Percentile25'] = accelerometerFeatures.getPercentile25()
        df['Percentile50'] = accelerometerFeatures.getPercentile50()
        df['Percentile75'] = accelerometerFeatures.getPercentile75()
        #df['Entropy'] = Entropy

        df['Amplitude1'] = accelerometerFeatures.getAmplitude1()
        df['Amplitude2'] = accelerometerFeatures.getAmplitude2()
        df['Frequency'] = accelerometerFeatures.getFrequency2()
        df['MeanFrequency'] = accelerometerFeatures.getMean_frequency()

        df_gyroscope['Mean_Gyroscope'] = gyroscopeFeatures.getMean()
        df_gyroscope['Std_Gyroscope'] = gyroscopeFeatures.getSTD()
        df_gyroscope['Skew_Gyroscope'] = gyroscopeFeatures.getSkewness()
        df_gyroscope['Kurtosis_Gyroscope'] = gyroscopeFeatures.getKurtosis()
        df_gyroscope['Max_Gyroscope'] = gyroscopeFeatures.getMax()
        df_gyroscope['Min_Gyroscope'] = gyroscopeFeatures.getMin()
        #df_gyroscope['Range_Gyroscope'] = Range_Gyroscope
        df_gyroscope['Percentile25_Gyroscope'] = gyroscopeFeatures.getPercentile25()
        df_gyroscope['Percentile50_Gyroscope'] = gyroscopeFeatures.getPercentile50()
        df_gyroscope['Percentile75_Gyroscope'] = gyroscopeFeatures.getPercentile75()
        #df_gyroscope['Entropy_Gyroscope'] = Entropy_Gyroscope

        df_gyroscope['Amplitude1_Gyroscope'] = gyroscopeFeatures.getAmplitude1()
        df_gyroscope['Amplitude2_Gyroscope'] = gyroscopeFeatures.getAmplitude2()
        df_gyroscope['Frequency_Gyroscope'] = gyroscopeFeatures.getFrequency2()
        df_gyroscope['MeanFrequency_Gyroscope'] = gyroscopeFeatures.getMean_frequency()

        df['y'] = accelerometerFeatures.getY()
        df_gyroscope['y_gyroscope'] = gyroscopeFeatures.getY()

        train =  pd.DataFrame(df[df['y'] == 1])
        test =  pd.DataFrame(df[df['y'] == -1])
        
        train_gyroscope =  pd.DataFrame(df_gyroscope[df_gyroscope['y_gyroscope'] == 1])
        test_gyroscope =  pd.DataFrame(df_gyroscope[df_gyroscope['y_gyroscope'] == -1])

        print('After Sampling Sizes\n','Train Size One Class: ', train.shape[0], 'Test Size Two Class: ', test.shape[0])
        
        trainStarter = train
        testStarter = test
            
        trainStarter_gyroscope = train_gyroscope
        testStarter_gyroscope = test_gyroscope

        accelerometerModelUser = Metrics()
        gyroscopeModelUser = Metrics()
        ensembleModelUser = Metrics()
        
        # 10 Executions per original user
        for fold in range(0,10):

            # =============================================================================
            # Best Hyper-Parameters values for Model 1 - Accelerometer
            # ============================================================================= 
            '''
            LocalOutlierFactor(n_neighbors = 3, novelty = True)
            EllipticEnvelope(contamination = 0)
            IsolationForest(n_jobs = -1, n_estimators = 100, contamination = 0, bootstrap = False)
            svm.OneClassSVM(gamma = 0.1, kernel="rbf", nu = 0.01, cache_size = 500)
            '''

            # =============================================================================
            # Best Hyper-Parameters values for Model 2 - Gyroscope
            # ============================================================================= 
            '''
            LocalOutlierFactor(n_neighbors = 5, novelty = True)
            EllipticEnvelope(contamination = 0)
            IsolationForest(n_jobs = -1, n_estimators = 100, max_features = 1, contamination = 0, bootstrap = False)
            svm.OneClassSVM(gamma = 0.001, kernel="rbf", nu = 0.1, cache_size = 500)
            '''
            decision1 = []  
            decision2 = []
            decision1, accelerometerModelUser, y_test= AlgorithmExecution(trainStarter, testStarter, "LocalOutlierFactor", [3], "Accelerometer", accelerometerModelUser)
            decision2, gyroscopeModelUser, y_test = AlgorithmExecution(trainStarter_gyroscope, testStarter_gyroscope, "LocalOutlierFactor", [5], "Gyroscope", gyroscopeModelUser)

            # =============================================================================
            # Enseble Models
            # ============================================================================= 
            TP = 0
            TN = 0
            FP = 0
            FN = 0
            sumPred = 0
            predictions = []
            for i in range(0, len(decision1)):

                sumPred = (decision1[i] + decision2[i]) 
                if sumPred >= 0:
                    predictions.append(1)
                    if y_test.iloc[i] == 1:
                        TP = TP + 1
                    else:
                        FP = FP + 1
                else:
                    predictions.append(-1)
                    if y_test.iloc[i] == -1:
                        TN = TN + 1
                    else:
                        FN = FN + 1
            print('------------- Ensemle Results ---------------')
            print(TN, " ", FP)
            print(FN, " ", TP)  
            print() 

            score = f1_score(y_test, predictions, pos_label= 1)
            #print('F1 Score: %.3f' % score)
            acc = accuracy_score(y_test, predictions)
            cfm = confusion_matrix(y_test, predictions, labels = [-1, 1])

            far = FP/ np.sum(y_test == -1)
            frr = FN/ np.sum(y_test == 1)           
            print('FAR: ', far, ' FFR: ', frr)

            ensembleModelUser.setfalseAccept(cfm[0,1])
            ensembleModelUser.setfalseReject(cfm[1,0])
            ensembleModelUser.settrueAccept(cfm[1,1])
            ensembleModelUser.settrueReject(cfm[0,0])
            ensembleModelUser.setsizeTest(y_test.shape[0])
            ensembleModelUser.setAccuracy(acc)
            ensembleModelUser.setFAR(far)
            ensembleModelUser.setFRR(frr)
            ensembleModelUser.setf1score(score)

        # =============================================================================
        # Average Performance per user (10-FOLD)
        # =============================================================================     
        ensembleModel = averagePerformance_KFold(ensembleModelUser, ensembleModel, 10)
        accelerometerModel = averagePerformance_KFold(accelerometerModelUser, accelerometerModel, 10)
        gyroscopeModel = averagePerformance_KFold(gyroscopeModelUser, gyroscopeModel, 10)

    return  accelerometerModel, gyroscopeModel, ensembleModel

# Main Controller Function
def main(): 

    # =============================================================================
    # Load Dataset and Create Panda Dataframes
    # =============================================================================
    # Set the absolute path in which the json files are saved.
    path = ''
    screen = 'MathisisGame'
    accelerometer, gyroscope, info, users = loadDataset(path, screen)

    # =============================================================================
    # Dataset Pre-process, Sampling, Feature Extraction and 
    # Continuous Implicit Authentication Methodology 
    # =============================================================================
    accelerometerModel, gyroscopeModel, ensembleModel = continuousImplicitAuthentication(users, accelerometer, gyroscope, info)

    # =============================================================================
    # Performance Evaluation
    # ============================================================================= 
    PerformanceMetrics(users, accelerometerModel, "ACCELEROMETER")
    PerformanceMetrics(users, gyroscopeModel, "GYROSCOPE")
    PerformanceMetrics(users, ensembleModel, "ENSEMLBE")

# Calling main function 
if __name__=="__main__": 
    main()