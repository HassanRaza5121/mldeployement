import os
import sys
from src.mlproject.exception import CustomExceptiom
from src.mlproject.logger import logging
import pandas as pd
import pymysql
from dotenv import load_dotenv
import pickle
import numpy as np
from sklearn.model_selection import GridSearchCV
load_dotenv()
host=os.getenv('host')
user=os.getenv('user')
password=os.getenv('password')
db = os.getenv('db')
def read_sql_data():
    logging.info('Reading database started')
    try:
        mydb=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        
        )
        logging.info("connection has started",mydb)
        df = pd.read_sql_query('select * from churn_modelling',mydb)
        print(df.head())
        return df
    except Exception as ex:
        raise CustomExceptiom(ex)
def save_obj(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomExceptiom(e,sys)
def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report={}

        for i in range(len(list(models))):

            model = list(models.values())[i]

            para = params[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            
            gs.fit(X_train,y_train)
            
            model.set_params(**gs.best_params_)
            
            model.fit(X_train,y_train)
            
            y_test_pred = model.predict(X_test)
            
            y_train_pred = model.predict(X_train)
            
            model_train_score = model.score(X_train,y_train)
            
            model_test_score = model.score(X_test,y_test)
            
            report[list(models.keys())[i]] = model_test_score
        
        return report




    except Exception as e:
        raise CustomExceptiom(e,sys)
    

