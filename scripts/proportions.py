import pandas as pd
import json
import matplotlib.pyplot as plt

def graph_data(data):
    '''
    Keep only category and category2 columns
    - replacing punctuation with spaces
    - remove non-alphabetical words
    - change categories to lowercase
    '''
    # Replace punctuation with spaces
    data['category2'] = data['category2'].str.replace('[\(\)\[\],\-\.\?\!\:\;\#\&]', ' ',regex=True)
    # Remove non-alphabetical words
    data['category2'] = data['category2'].str.replace('[^a-zA-Z\s]', '',regex=True)
    # Change everything to lowercase
    data['category'] = data['category'].str.lower()
    data['category2'] = data['category2'].str.lower()
    return data
    
def get_proportions(data):
    '''
    Graph the proportion of category2 within category
    '''
    data = graph_data(data)
    # Get categories
    categories = data['category'].unique()
    # Initialize proportions
    proportions = {}
    # Iterate over categories
    for category in categories:
        # Get category2 counts
        category2_counts = data[data['category'] == category]['category2'].value_counts()
        # Get total number of category2
        total_category2 = category2_counts.sum()
        # Get proportions
        proportions[category] = {k: v / total_category2 for k, v in category2_counts.items()}
    # Get rid of NaN
    proportions.pop('NaN', None)
    # Save proportions to json file
    with open('data/proportions.json', 'w') as f:
        json.dump(proportions, f, indent=4)
    return proportions
    
def graph_proportions(data):
    '''
    Graph the proportion of category2 within category
    '''
    proportions = get_proportions(data)
    filtered_data = {k: v for k, v in proportions.items() if k != 'NaN'}

    # Divide the data into two sets for two 1x4 grids
    data_sets = list(filtered_data.items())
    first_half = data_sets[:len(data_sets)//2]
    second_half = data_sets[len(data_sets)//2:]

    # Function to create a single 1x4 grid
    def create_single_grid(data_set, row_number):
        fig, axs = plt.subplots(1, 4, figsize=(24, 6))
        for (category, values), ax in zip(data_set, axs):
            # Sort the data to ensure consistent color assignment
            sorted_values = {k: values[k] for k in sorted(values, key=lambda x: x.lower())}

            # Data to plot
            labels = sorted_values.keys()
            sizes = sorted_values.values()
            # Assign colors: gold for positive, pink for negative, lightskyblue for neutral
            colors = ['gold' if label == 'p' else 'pink' if label == 'n' else 'lightskyblue' for label in labels]

            # Explode the slice with the highest proportion
            explode = [0.1 if label == max(labels) else 0 for label in labels]

            # Plot each pie chart in its respective subplot
            ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
            if category == 'social interactionsrelations':
                category = 'social interactions/relations'
            elif category == 'musicachievements':
                category = 'music/achievements'
            ax.set_title(f'Proportion of "p", "n", and "ne" in {category}')

        plt.tight_layout()
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.05, right=0.95, hspace=0.25, wspace=0.35)
        plt.savefig(f'images/proportions_{row_number}.png')
        plt.close()
    # Create two 1x4 grids
    create_single_grid(first_half, 1)
    create_single_grid(second_half, 2)