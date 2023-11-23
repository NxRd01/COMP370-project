import argparse
import json
import random
from pathlib import Path

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', type=str, required=True) #json file in data folder
    parser.add_argument('-o','--output', type=str, required=True) #tsv file in data folder
    parser.add_argument('-n','--num', type=int, required=True) #number of articles to sample
    args = parser.parse_args()
    
    with open(Path(__file__).parent.parent / 'data' / args.input, 'r') as f:
        requests = json.load(f)
    
    articles_new = []
   
    #only keep the title description source and url
    keep = ['title','description','source']
    for request in requests:
        articles = request['articles']
        for article in articles:
            articles_new.append({key: article[key] for key in keep})
    
    for i in range(len(articles_new)):
        articles_new[i]['source'] = articles_new[i]['source']['name']

    #sample articles
    sampled_articles = random.sample(articles_new, args.num)
    
    #turn into tsv file
    with open(Path(__file__).parent.parent / 'data' / args.output, 'w',encoding='utf-8') as f:
        for article in sampled_articles:
            f.write(article['title'] + '\t' + article['description'] + '\t' + article['source'] + '\n')
    
    

if __name__ == '__main__':
    main()
    