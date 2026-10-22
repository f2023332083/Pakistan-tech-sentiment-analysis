import pandas as pd
import os

def load_data():
    file_path = os.path.join("data", "pakistan_mobile_brands_analyzed.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"Error: {file_path} file nahi mili!")
        return None

def ask_dataset_agent(query, df):
    if df is None or df.empty:
        print("Dataset available nahi hai.")
        return

    query_lower = query.lower()
    filtered_df = df.copy()
    
    # 1. Brand Filter
    target_brand = None
    for brand in ['infinix', 'oppo', 'vivo']:
        if brand in query_lower:
            target_brand = brand.capitalize()
            break
            
    if target_brand:
        filtered_df = filtered_df[filtered_df['brand'] == target_brand]

    # 2. Sentiment Filter
    if any(w in query_lower for w in ['positive', 'tareef', 'good', 'best']):
        filtered_df = filtered_df[filtered_df['sentiment'] == 'Positive']
    elif any(w in query_lower for w in ['negative', 'kharab', 'bad', 'complaint', 'issue']):
        filtered_df = filtered_df[filtered_df['sentiment'] == 'Negative']
    elif any(w in query_lower for w in ['neutral', 'price', 'keemat']):
        filtered_df = filtered_df[filtered_df['sentiment'] == 'Neutral']

    # 3. Keyword Filter
    keywords = ['camera', 'battery', 'price', 'heating', 'lag', 'pubg', 'gaming', 'screen', 'display', 'charging']
    matched_keyword = None
    for kw in keywords:
        if kw in query_lower:
            matched_keyword = kw
            filtered_df = filtered_df[filtered_df['cleaned_text'].str.contains(kw, case=False, na=False)]
            break

    # 4. Output Summary
    total_matches = len(filtered_df)
    
    print("\n" + "="*50)
    print(f"QUERY RESULT FOR: '{query}'")
    print("="*50)
    print(f"Total Relevant Comments Found: {total_matches}")
    
    if target_brand:
        print(f"Target Brand: {target_brand}")
    if matched_keyword:
        print(f"Topic Filter: {matched_keyword.upper()}")
        
    if total_matches > 0:
        avg_likes = filtered_df['likes'].mean()
        print(f"Average Likes per Comment: {round(avg_likes, 2)}")
        
        print("\nSample Comments from Users:")
        sample_size = min(3, total_matches)
        samples = filtered_df.sort_values(by='likes', ascending=False).head(sample_size)
        
        for idx, row in samples.iterrows():
            print(f" - [{row['brand']}] ({row['sentiment']}): \"{row['post_text']}\" (Likes: {row['likes']})")
    else:
        print("No direct comments matched this criteria. Try another question.")
    print("="*50 + "\n")
