import json 
from pathlib import Path
import argparse

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', type=str, default='articles.json', help='The name of the input file')
    parser.add_argument('-k','--keyword',type=str,default='Taylor Swift', help='The keyword to search for')
    parser.add_argument('-o','--output', type=str, default='articlesv2.json', help='The name of the output file')
    args = parser.parse_args()
    
    
    json_input = args.input
    json_output = args.output
    
    with open(Path(__file__).parent.parent / 'data' / json_input,'r') as f:
        queries = json.load(f)
    
    keyword = args.keyword.lower()

    total_articles = 0
    
    for query in queries:
        total_articles += len(query['articles'])
        query['articles'] = [article for article in query['articles'] if 
                             (article['title'] and keyword in article['title'].lower()) or
                             (article['description'] and keyword in article['description'].lower())]
        
        query['totalResults'] = len(query['articles'])
    
    def remove_duplicates(data):
        unique_titles = set()
        unique_data = []
        total_articles =0 
        for entry in data:
            articles = entry.get("articles", [])
            unique_articles = []

            for article in articles:
                title = article["title"]
                if title not in unique_titles:
                    unique_titles.add(title)
                    unique_articles.append(article)
                    total_articles += 1

            if unique_articles:
                entry["articles"] = unique_articles
                unique_data.append(entry)

        return unique_data,total_articles
    
    queries,filtered = remove_duplicates(queries)
            
        
    with open(Path(__file__).parent.parent / 'data' / json_output,'w') as r:
        json.dump(queries,r,indent=4)
        
    
            
    print(f"Done, found {filtered}/{total_articles} articles containing the keyword {keyword} in the title or description \n results saved to /data/{json_output}")

if __name__ == '__main__':
    main()  
    