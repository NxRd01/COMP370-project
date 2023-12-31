import json
import pandas as pd

def clean_data(data):
    '''
    Clean data by:
    - replacing punctuation with spaces
    - remove non-alphabetical words
    - change categories to lowercase
    - remove stop words
    '''
    # Replace punctuation with spaces
    data['title'] = data['title'].str.replace('[\(\)\[\],\-\.\?\!\:\;\#\&]', ' ',regex=True)
    data['description'] = data['description'].str.replace('[\(\)\[\],\-\.\?\!\:\;\#\&]', ' ',regex=True)
    data['category'] = data['category'].str.replace('[\(\)\[\],\-\.\?\!\:\;\#\&]', ' ',regex=True)
    # Remove non-alphabetical words
    data['title'] = data['title'].str.replace('[^a-zA-Z\s]', '',regex=True)
    data['description'] = data['description'].str.replace('[^a-zA-Z\s]', '',regex=True)
    data['category'] = data['category'].str.replace('[^a-zA-Z\s]', '',regex=True)
    # Change everything to lowercase
    data['category'] = data['category'].str.lower()
    data['title'] = data['title'].str.lower()
    data['description'] = data['description'].str.lower()
    # Remove stop words
    with open('data/stopwords.txt', 'r') as f:
        stop_words = f.read().splitlines()
    data['title'] = data['title'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    data['description'] = data['description'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))
    return data

def compile_word_counts(data):
    '''
    Compile word counts for each category by keeping words with more than 5 appearances
    '''
    # Compile word counts for each category
    # Combine word counts for titles and descriptions
    word_counts = {}
    for category in data['category'].unique():
        word_counts[category] = {}
        # Compile word counts for titles
        title = data[data['category'] == category]['title'].str.split(expand=True).stack().value_counts()
        # Compile word counts for descriptions
        description = data[data['category'] == category]['description'].str.split(expand=True).stack().value_counts()
        # Convert dictionaries to Series
        title_series = pd.Series(title)
        description_series = pd.Series(description)
        # Add Series together
        combined = title_series.add(description_series, fill_value=0)
        # Sort Series in descending order
        sorted_combined = combined.sort_values(ascending=False)
        # Convert sorted Series back to dictionary
        sorted_dict = sorted_combined.to_dict()
        # Convert values in dictionary to integers
        word_counts[category] = {k: int(v) for k, v in sorted_dict.items()}
        # Remove "Taylor" and "Swift" from word counts
        word_counts[category].pop('taylor', None)
        word_counts[category].pop('swift', None)
        # Only keep top 10 words for each category
        # If words have same count as 10th word, keep them
        if len(word_counts[category]) > 10:
            # Get 10th word count
            tenth_word_count = list(word_counts[category].values())[9]
            # Keep words with same count as 10th word
            word_counts[category] = {k: v for k, v in word_counts[category].items() if v >= tenth_word_count}
        
    # Save word counts to json file
    with open('data/word_counts.json', 'w') as f:
        json.dump(word_counts, f, indent=4)
    return word_counts