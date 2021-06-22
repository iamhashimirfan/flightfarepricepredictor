import streamlit as st
import datetime
import pandas as pd
import tweepy
from textblob import TextBlob
import re
import string
import pandas as pd
from datetime import date
from Flight_Price_Predict import predict

st.set_page_config(page_title="Flight Price Predictor App",page_icon="✈️")

#Twitter Access and API keys
consumerKey = "xeY9xjMdDA9lnnRy5zIdLxMht"
consumerSecret = "IMp0MCua7ZtVAybo0y0KHIKIwekBFuKNmRa4w9G6E5UdYo0z8n"
accessToken = "1018529541126434817-RH6kmB6rzDIBDB3mfSRkexOTNDCWt2"
accessTokenSecret = "464EYAbFHP9IVte71L6it8CndYhsa1DmKFughK6vJBXAr"

authenicate = tweepy.OAuthHandler(consumerKey, consumerSecret)
authenicate.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(authenicate, wait_on_rate_limit=True)

def TwitterApi(city_entity):
    search_term = '#' + city_entity + ' -filter:retweets'
    #fetching current date and format it to retrive latest tweets
    today=date.today()
    today_format=today.strftime("%Y-%m-%d")
    tweets = tweepy.Cursor(api.search, q=search_term, lang='en', since=today_format, tweet_mode='extended').items(10)
    all_tweets = [tweet.full_text for tweet in tweets]
    return all_tweets

#Preprocessing
def pre_process(twt):
    if twt == 0:
        return '0'
    else:
        #Removing cases,newlines,urls,numbers and punctuations from tweets
        replacements=[
            ('#[A-Za-z0]+',''),
            ('\\n',''),
            ('https?:\/\/\S+','')
        ]
        for old,new in replacements:
            twt=re.sub(old,new,twt)
        twt = "".join([char for char in twt if char not in string.punctuation])
        twt = re.sub('[0-9]+','',twt) 
        return twt

'''
# Flight Price Prediction
Fill the necessary details and get approx price. 
'''
airline = ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia', 'Vistara Premium economy', 'Jet Airways Business',
           'Multiple carriers Premium economy', 'Trujet']
source = ['Kolkata', 'Delhi', 'Chennai', 'Mumbai', 'Banglore']
destination = ['Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad']
stop = [0, 1, 2, 3, 4]

airline = st.selectbox("Select Airline", airline)
source = st.selectbox("Select Source", source)
destination = st.selectbox("Select Destination", destination)
total_stop = st.selectbox('Select Number of Stop', stop)

date_of_journey = st.date_input('Select Date of Journey')
journey_time = st.time_input("Journey time is", datetime.time())

date_of_arrival = st.date_input('Select Date of Arrival')
arrival_time = st.time_input('Arrival Time', datetime.time())
startTime = datetime.datetime.combine(date_of_journey, journey_time)
arrivalTime = datetime.datetime.combine(date_of_arrival, arrival_time)
total_difference = (arrivalTime - startTime).total_seconds()
print('total_difference : ', total_difference)
duration = str(int(total_difference / 3600)) + 'h ' + str(int((total_difference % 3600)%60)) + 'm'

def Conv_2_Percentage(remark_score):
    remark_score_percentage = remark_score / 100
    return remark_score_percentage

def time_difference_check():
    flag = True
    if total_difference / 60 <= 30:
        st.error('Arrival and Start datetime should have atleast 30 minute gap')
        flag = False
    elif date_of_arrival < date_of_journey:
        st.error('Please select a proper date range')
        flag = False
    return flag
    return flag

def Sentiment_Menatality(remark_score):
    if remark_score < 0:
        return 'negative'
    elif remark_score == 0:
        return 'neutral'
    else:
        return 'positive'

def sentiment_subject(twt):
    return TextBlob(twt).sentiment.subjectivity

def sentiment_polar(twt):
    return TextBlob(twt).sentiment.polarity

if st.button('Predict Price'):
    # print('Airline : ',airline)
        print('Source :',source)
        print('Destination : ',destination)
    # print('total stop : ',total_stop)
    # print('date of journey : ',date_of_journey)
    # print(date_of_journey.day)
    # print('journey time : ',type(journey_time))
    # print('date of arrival : ',date_of_arrival)
    # print('arrival time : ',arrival_time)
        route_names=["Kolkata","Hyderabad","Chennai","Mumbai","Cochin","Banglore","Delhi"]
        routes =route_names
        collected_route_tweets = pd.DataFrame()
        processed_route_tweets = pd.DataFrame()
        collected_route_polarity= pd.DataFrame()
        collected_route_subjectivity= pd.DataFrame()
        final_sentiment = pd.DataFrame()
        all_sentiment_scores_df = pd.DataFrame()
        dataframe_to_export = pd.DataFrame()
        filler = 0
        for t in routes:
            single_route = TwitterApi(t)
            collected_route_tweets [t] = single_route + [filler]*(len(collected_route_tweets .index) - len(single_route))
        
        for each_route in routes:
            processed_route_tweets[each_route] = collected_route_tweets [each_route].apply(pre_process)
       
        for each_route in routes:
            collected_route_polarity[each_route] = processed_route_tweets[each_route].apply(sentiment_polar)
            collected_route_subjectivity[each_route] = processed_route_tweets[each_route].apply(sentiment_subject)
        
        for each_route in routes:
            final_sentiment[each_route] =collected_route_polarity[each_route].apply(Sentiment_Menatality)
        
        for each_route in routes:
            all_sentiment_scores_df[each_route] = final_sentiment[each_route].value_counts()
        
        all_sentiment_scores_df = all_sentiment_scores_df.fillna(0)
        
        for each_route in routes:
            dataframe_to_export[each_route] = all_sentiment_scores_df[each_route].apply(Conv_2_Percentage)
            
        positive_score = []
        for each_route in routes:
            positive_score.append(dataframe_to_export[each_route][1])
            
        #Storing sentiment scores of destination
        result=dataframe_to_export[[destination]].T
        # result=result.set_index(pd.Index([destination]))
        result=result.sort_values(by=destination,ascending=False,axis=1)
        destination_sentiment=result.iloc[0].index.values
        
        #sentiment mentality and sentiment value
        destination_sentiment_mentality=str(destination_sentiment[0])
        destination_sentiment_value=(result.iloc[0,0])
        
        #Storing sentiment scores of destination
        result1=dataframe_to_export[[source]].T
        # result=result.set_index(pd.Index([destination]))
        result1=result1.sort_values(by=source,ascending=False,axis=1)
        source_sentiment=result1.iloc[0].index.values
        
        #sentiment mentality and sentiment value
        source_sentiment_mentality=str(source_sentiment[0])
        source_sentiment_value=(result1.iloc[0,0])
        
        flag = time_difference_check()
        if flag == True:
            
            predicted_value = predict(airline, date_of_journey, source, destination, journey_time, arrival_time, duration, total_stop)
            
            predicted_value=int(predicted_value)
            #Discounting System
            if source_sentiment_mentality == "positive" or source_sentiment_mentality == "neutral":
            
                if destination_sentiment_mentality == "positive" or destination_sentiment_mentality == "neutral":
                
                    predicted_value=predicted_value-(source_sentiment_value+destination_sentiment_value)*1000
            
                else:
               
                    predicted_value=predicted_value+(source_sentiment_value+destination_sentiment_value)*1000
    
            elif source_sentiment_mentality == "negative":
        
            
                 if destination_sentiment_mentality == "negative" or destination_sentiment_mentality == "neutral":
                
                     predicted_value=predicted_value+(source_sentiment_value+destination_sentiment_value)*1000
            
                 else:
               
                     predicted_value=predicted_value-(source_sentiment_value+destination_sentiment_value)*1000
            
            st.write('Predicted Price is ', predicted_value)
