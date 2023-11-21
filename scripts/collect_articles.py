from newsapi import NewsApiClient
import json     
from pathlib import Path
from datetime import datetime,timedelta
from time import sleep as wait


def main(): 
    with open(Path(__file__).parent.parent / 'data' / 'apikey.txt','r') as f:
        apikey = f.read()
        apikey = apikey.strip()
        
    with open(Path(__file__).parent.parent / 'data' / 'sources_id.txt','r') as f:
        sources = f.read()
        sources = sources.strip()
         
    #Initialise newsapi with the api key 
    newsapi = NewsApiClient(api_key=apikey)
    
    #Get the articles from the sources for each day 
    current_date = datetime(2023,10,20)
    day_after = current_date + timedelta(days=1)
    articles_list = []
    
    while current_date < datetime(2023,11,19):
        articles = newsapi.get_everything(q="Taylor Swift",
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

    with open(Path(__file__).parent.parent / 'data' / 'articles.json','w') as f:
        json.dump(articles_list,f)
        
if __name__ == '__main__':
    main()