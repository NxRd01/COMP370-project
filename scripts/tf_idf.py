import argparse
import json
import compile_word_counts
import compute_lang
import graph
import pandas as pd

def main():
    '''
    '''
    # Parse arguments
    parser = argparse.ArgumentParser(description='Compile word counts and compute tf-idf scores')
    parser.add_argument('-d', '--data', type=str, help='Path to data directory')
    args = parser.parse_args()
    # Get data directory
    data_dir = args.data
    # Load data
    data = pd.read_csv(data_dir)
    # Compile word counts
    dialog = compile_word_counts.clean_data(data)
    word_count = compile_word_counts.compile_word_counts(dialog)
    # Compute tf-idf scores
    tf_idf = compute_lang.compute_tf_idf(word_count)
    # get top 10 words for each category with their tf-idf scores
    top_words = {}
    for category in tf_idf.keys():
        top_words[category] = tf_idf[category][:10]
    # Save tf-idf scores
    with open('data/tf_idf.json', 'w') as f:
        json.dump(top_words, f, indent=4)
    # Create graph
    graph.graph(top_words)

if __name__ == '__main__':
    main()