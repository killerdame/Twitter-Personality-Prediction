def prediction_prob(model, tweet_num):    
    pred_prob = model.predict_proba(X_test[tweet_num]).argmax()
    print "The predicted twitter user is:"
    print twitionary[pred_prob]
    print ''
    print "The real twitter user is:"
    print twitionary[y_test[tweet_num]]