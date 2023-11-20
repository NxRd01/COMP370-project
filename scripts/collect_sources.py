from pathlib import Path
from newsapi import NewsApiClient
import json 
import argparse

def main():
    
    args = argparse.ArgumentParser()
    args.add_argument('--keyword',type=str,default='entertainment')
    args = args.parse_args()
    
    keyword = args.keyword.lower()
    
    with open(Path(__file__).parent.parent / 'data' / 'apikey.txt','r') as f:
        apikey = f.read()
        apikey = apikey.strip()
        
    newsapi = NewsApiClient(api_key=apikey)
    sources = newsapi.get_sources()
    
    #keep only the sources that are from the us or canada
    sources = [source for source in sources['sources'] if source['country'] == 'us' or source['country'] == 'ca']
    #Keep only the sources that have 'entertainment' in their description
    sources = [source for source in sources if keyword in source['description'].lower()]
    
    with open(Path(__file__).parent.parent / 'data' / 'sources.json','w') as f:
        json.dump(sources,f,indent=4)
    
    

if __name__ == '__main__':
    main() 