import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def initialize_vader():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(df, text_column='cleaned_text'):
    """
    Applies custom VADER sentiment analysis on the dataframe.
    """
    initialize_vader()
    sia = SentimentIntensityAnalyzer()
    
    # Custom Roman Urdu and Tech slang lexicon tuning
    custom_lexicon = {
        'zabardast': 2.0,
        'behtareen': 2.5,
        'kamal': 2.0,
        'sasta': 1.0,
        'op': 1.5,
        'value': 1.5,
        'bakwas': -2.5,
        'ghatiya': -2.5,
        'kharab': -2.0,
        'bekar': -2.0,
        'overpriced': -1.5,
        'heating': -1.5,
        'lag': -1.5,
        'slow': -1.0
    }
    sia.lexicon.update(custom_lexicon)
    
    scores = []
    sentiments = []
    
    for text in df[text_column]:
        if pd.isna(text) or str(text).strip() == "":
            scores.append(0.0)
            sentiments.append('Neutral')
            continue
            
        score = sia.polarity_scores(str(text))['compound']
        scores.append(score)
        
        if score >= 0.05:
            sentiments.append('Positive')
        elif score <= -0.05:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
            
    df['sentiment_score'] = scores
    df['sentiment'] = sentiments
    
    return df