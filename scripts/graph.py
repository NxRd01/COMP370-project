import pandas as pd
import matplotlib.pyplot as plt

# Let's modify the code to create a 2x2 grid of subplots for the first eight categories provided in the JSON data.
# We will use the 'subplots' functionality of matplotlib to achieve this.

# Function to create 2x2 grid of plots
def create_subplot_grid(tf_idf_data, category_names, grid_number):
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Create a 2x2 grid of subplots
    axs = axs.flatten()  # Flatten the 2x2 grid into a list for easy iteration
    plt.suptitle(f'TF-IDF Score Grid {grid_number}')

    # Loop through the given categories and their corresponding axes
    for ax, category_name in zip(axs, category_names):
        # Extract data for the given category
        category_data = tf_idf_data[category_name]
        
        # Create a DataFrame
        df = pd.DataFrame(category_data, columns=['Word', 'TF-IDF Score'])
        
        # Sort the DataFrame based on TF-IDF score in descending order
        df_sorted = df.sort_values(by='TF-IDF Score', ascending=False)
        
        # Plot the data on the given axes
        ax.bar(df_sorted['Word'], df_sorted['TF-IDF Score'], color='skyblue')
        ax.set_title(category_name)
        ax.set_xlabel('Words')
        ax.set_ylabel('TF-IDF Score')
        ax.tick_params(labelrotation=90)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the layout to make room for the main title

    # Save the plot as a PNG file
    plot_filename = f'images/{grid_number}.png'
    plt.savefig(plot_filename)
    plt.close()  # Close the figure to avoid displaying it in the notebook
    
    return plot_filename

def graph(data):
    # We assume that the categories are ordered and we will take the first eight for the 2x2 grids (4 categories per grid).
    categories = list(data.keys())
    selected_categories = [cat for cat in categories if cat != 'NaN'][:8]  # Exclude 'NaN' and select first eight valid categories
    # Create two 2x2 grids
    grid_1_filename = create_subplot_grid(data, selected_categories[:4], 1)
    grid_2_filename = create_subplot_grid(data, selected_categories[4:8], 2)

    grid_1_filename, grid_2_filename
