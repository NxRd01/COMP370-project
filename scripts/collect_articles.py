from pathlib import Path
from newsapi import newsapi-python  

def main():
    with open(Path(__file__).parent / 'apikey.txt','r') as f:
        apikey = f.read()
        apikey = apikey.strip()
        
    

if __name__ == '__main__':
    main() 