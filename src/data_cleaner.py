import pandas as pd
import re

def clean_text(text):
    if pd.isna(text):
        return ""
    
    text = str(text)
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Remove user mentions (@username)
    text = re.sub(r'@\w+', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def clean_dataset(df, text_column='post_text'):
    """
    Takes a dataframe and cleans the specified text column.
    """
    if text_column in df.columns:
        df['cleaned_text'] = df[text_column].apply(clean_text)
    else:
        # Fallback if column name is different
        df['cleaned_text'] = df.iloc[:, 0].apply(clean_text)
        
    return df