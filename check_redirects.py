import os
import re
import yaml
import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

internal_link = re.compile('^[^(#|http|\/)]([^#\s]*)')

try:
    with open(os.path.join(os.path.dirname(__file__), 'docs-italia-documents.yml')) as documents_list:
        documents = documents_list.read()
        documents = yaml.safe_load(documents)
except:
    documents = {}

for document in documents:
    broken_redirects = []
    
    for version in document['versions']:
        req = Request(document['url'] + version)
        
        try:
            html_page = urlopen(req)
        except:
            print('Unable to open url: ' + document['url'] + version)
            sys.exit('Check your docs-italia-documents.yml file for errors')
        
        soup = BeautifulSoup(html_page, "lxml")
        
        links = []
        
        for link in soup.findAll('a'):
            link_url = link.get('href')
            if link_url:
                try:
                    doc_url = internal_link.search(link_url).group(0)
                except AttributeError:
                    doc_url = None
            if doc_url and doc_url not in links:
                links.append(link_url)
        
        print('Checking redirect links from document: ' + document['url'])
        print('Redirect document is: ' + document['redirect_url'])
        print('Vesion: ' + version)
        for link in links:            
            req = Request(document['redirect_url'] + version + '/' + link)
        
            try:
                html_page = urlopen(req)
            except:
                print('[ ' + u'\u2718' + ' ]\t\t' + link)
                broken_redirects.append({
                    'original_url': document['url'] + version + '/' + link,
                    'redirect_url': document['redirect_url'] + version + '/' + link,
                    'reason': '404'
                })
                continue
        
            soup = BeautifulSoup(html_page, "lxml")
        
            if len(soup.findAll(id='redirect')) == 0:
                print('[ ' + u'\u2718' + ' ]\t\t', end='')
                broken_redirects.append({
                    'original_url': document['url'] + version + '/' + link,
                    'redirect_url': document['redirect_url'] + version + '/' + link,
                    'reason': 'redirect not in page'
                })
            else:
                print('[ ' + u'\u2714' + ' ]\t\t', end='')
        
            print(link)
        
        print('\n')
        
    print('\n')
    
    if len(broken_redirects):
        print ('The following redirects are broken:\n')
        for broken_redirect in broken_redirects:
            print('Original url: ' + broken_redirect['original_url'])
            print('Test url: ' + broken_redirect['redirect_url'])
            print('Reason: ' + broken_redirect['reason'])
            print('\n-----------------------\n')
