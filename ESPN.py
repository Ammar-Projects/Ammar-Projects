import requests
from bs4 import BeautifulSoup
import pandas as pd

sports = ['nba','nfl','nhl']
d = {}

for x in sports:
    url = 'https://www.espn.com/' + x + '/standings/_/group/league'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup = BeautifulSoup(soup.prettify(),'html.parser')
    nested = soup.find('table',{'class':'Table Table--align-right'})
    df = pd.read_html(str(nested))
    d[x] = pd.DataFrame(df[0])
    nested = soup.find_all('span',{'class':'hide-mobile'})
    list1 = []
    for y in nested:
        list1.append(y.text.strip())
    d[x] = pd.concat([pd.Series(list1),d[x]], axis = 1)
    d[x].rename(columns={ d[x].columns[0]: 'Team' }, inplace = True)