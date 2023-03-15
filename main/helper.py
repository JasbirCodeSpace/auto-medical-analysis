import os
import pickle
import numpy as np

def predict(values, dic):

    test_type = None
    pred= None
    # diabetes
    if len(values) == 8:
        test_type = "diabetes"
        dic2 = {'NewBMI_Obesity 1': 0, 'NewBMI_Obesity 2': 0, 'NewBMI_Obesity 3': 0, 'NewBMI_Overweight': 0,
                'NewBMI_Underweight': 0, 'NewInsulinScore_Normal': 0, 'NewGlucose_Low': 0,
                'NewGlucose_Normal': 0, 'NewGlucose_Overweight': 0, 'NewGlucose_Secret': 0}

        if dic['BMI'] <= 18.5:
            dic2['NewBMI_Underweight'] = 1
        elif 18.5 < dic['BMI'] <= 24.9:
            pass
        elif 24.9 < dic['BMI'] <= 29.9:
            dic2['NewBMI_Overweight'] = 1
        elif 29.9 < dic['BMI'] <= 34.9:
            dic2['NewBMI_Obesity 1'] = 1
        elif 34.9 < dic['BMI'] <= 39.9:
            dic2['NewBMI_Obesity 2'] = 1
        elif dic['BMI'] > 39.9:
            dic2['NewBMI_Obesity 3'] = 1

        if 16 <= dic['Insulin'] <= 166:
            dic2['NewInsulinScore_Normal'] = 1

        if dic['Glucose'] <= 70:
            dic2['NewGlucose_Low'] = 1
        elif 70 < dic['Glucose'] <= 99:
            dic2['NewGlucose_Normal'] = 1
        elif 99 < dic['Glucose'] <= 126:
            dic2['NewGlucose_Overweight'] = 1
        elif dic['Glucose'] > 126:
            dic2['NewGlucose_Secret'] = 1

        dic.update(dic2)
        values2 = list(map(float, list(dic.values())))

        model = pickle.load(open(os.path.join(os.path.dirname(__file__), 'ml_models', 'diabetes.pkl'),'rb'))
        values = np.asarray(values2)
        pred = model.predict(values.reshape(1, -1))[0]

    # breast_cancer
    elif len(values) == 22:
        test_type = "breast_cancer"
        model = pickle.load(open(os.path.join(os.path.dirname(__file__), 'ml_models', 'breast_cancer.pkl'),'rb'))
        values = np.asarray(values)
        pred =  model.predict(values.reshape(1, -1))[0]

    # heart disease
    elif len(values) == 13:
        test_type = "heart"
        model = pickle.load(open(os.path.join(os.path.dirname(__file__), 'ml_models', 'heart.pkl'),'rb'))
        values = np.asarray(values)
        pred =  model.predict(values.reshape(1, -1))[0]

    # kidney disease
    elif len(values) == 24:
        test_type = "kidney"
        model = pickle.load(open(os.path.join(os.path.dirname(__file__), 'ml_models', 'kidney.pkl'),'rb'))
        values = np.asarray(values)
        pred =  model.predict(values.reshape(1, -1))[0]

    # liver disease
    elif len(values) == 10:
        test_type = "liver"
        model = pickle.load(open(os.path.join(os.path.dirname(__file__), 'ml_models', 'liver.pkl'),'rb'))
        values = np.asarray(values)
        pred =  model.predict(values.reshape(1, -1))[0]

    return test_type, pred