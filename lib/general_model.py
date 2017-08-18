from sqlalchemy import create_engine
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline



def add_to_or_create_process_list(process, data_dict):
    '''
    This function takes a data dictionary and process and adds it to a list.
    '''

    if 'processes' in data_dict.keys():
        data_dict['processes'].append(process)
    else:
        data_dict['processes'] = [process]
        
    return data_dict


def build_vectorizer(df):
    '''
    This function receives the text portion of a tweet and returns a fit svd transformer.
    '''
    vectorizer = TfidfVectorizer(stop_words='english', decode_error='replace', use_idf=True, max_df=2.0)
    svd = TruncatedSVD(n_components=500,algorithm='randomized',n_iter=10,random_state=42)
    svd_trans = Pipeline([('tfidf', vectorizer), 
                            ('svd', svd)])
    svd_trans.fit(df)
    return svd_trans


def make_data_dict(df, svd_trans): 
    '''
    This function receives a dataframe, perform a test train split and returns an X_test, X_train, y_test, y_train data dictionary.
    '''
    y = df['user']
    X = svd_trans
    
    le = LabelEncoder()
    y = le.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    data_dict = {
                 'X_test' : X_test,
                 'X_train' : X_train,
                 'y_test' : y_test,
                 'y_train' : y_train} 
    
    return data_dict


def general_model(model, data_dict):
    '''
    This function receives a data dictionary, fits on training data, scores on train and test data and returns a data dictionary with model, test score, train score and accuracy percentage.
    '''
    model.fit(data_dict['X_train'], data_dict['y_train'])
    train_score = model.score(data_dict['X_train'], data_dict['y_train'])
    test_score = model.score(data_dict['X_test'], data_dict['y_test'])
    
    add_to_process_list(model, data_dict)
    
    return {'model': model,
            'train_score': train_score,
            'test_score': test_score}
    
