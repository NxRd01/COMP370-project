import numpy as np

def compute_tf_idf(word_counts):
    '''
    Compute tf-idf scores for each word in each category
    '''
    # Initialize TF-IDF
    tf_idf = {}
    # Get ponies
    categories = word_counts.keys()
    # Get total number of ponies
    num_categories = len(categories)
    # Iterate over ponies
    for category in categories:
        if category == 'NaN':
            continue
        # Initialize TF-IDF for pony
        tf_idf[category] = []
        # Get pony words
        category_words = word_counts[category]
        # Get pony words
        category_words = category_words.keys()
        # Iterate over pony words
        for word in category_words:
            # Get pony word count
            pony_word_count = word_counts[category][word]
            # Get number of ponies that use the word
            num_categories_word = sum([1 for pony in categories if word in word_counts[pony]])
            # Compute TF-IDF
            tf_idf_score = pony_word_count * np.log(num_categories / num_categories_word)
            # Add TF-IDF score to TF-IDF
            tf_idf[category].append((word, tf_idf_score))
        # Sort TF-IDF
        tf_idf[category].sort(key=lambda x: x[1], reverse=True)
    # Return TF-IDF
    return tf_idf