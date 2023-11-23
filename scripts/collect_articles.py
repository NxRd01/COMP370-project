from newsapi import NewsApiClient
import json     
from pathlib import Path
from datetime import datetime,timedelta
from time import sleep as wait
import argparse


def main(): 
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--query',type=str,default='Taylor+AND+Swift',help='The query to search for')
    parser.add_argument('output',type=str,default='articles.json',help='The name of the output file')
    args = parser.parse_args()

    with open(Path(__file__).parent.parent / 'data' / 'apikey.txt','r') as f:
        apikey = f.read()
        apikey = apikey.strip()
        
    with open(Path(__file__).parent.parent / 'data' / 'sources_id.txt','r') as f:
        sources = f.read()
        sources = sources.strip()
         
    #Initialise newsapi with the api key 
    newsapi = NewsApiClient(api_key=apikey)
    
    #Get the articles from the sources for each day 
    current_date = datetime.today() - timedelta(days=30)
    day_after = current_date + timedelta(days=1)
    articles_list = []
    query = args.query
    output = args.output
    
    while current_date < datetime.today() - timedelta(days=1):
        articles = newsapi.get_everything(q=query,
                                          sources=sources,
                                          language='en',
                                          sort_by='relevancy',
                                          from_param=current_date,
                                          to=day_after,
                                          page_size=100)
        articles_list.append(articles)
        current_date = day_after
        day_after = current_date + timedelta(days=1)
        wait(1)

    with open(Path(__file__).parent.parent / 'data' / output,'w') as f:
        json.dump(articles_list,f,indent=4)
        
if __name__ == '__main__':
    main()