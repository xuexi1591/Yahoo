# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".

import scraperwiki
import requests
import lxml.html
import re

def duckint(i):
    try:
        return int(i)
    except ValueError:
        return i

# Blank Python
lookup = ['Name','Team','GP','G','A','Pts','diff','PIM','Hits','BkS','PPG','PPA','SHG','SHA','GW','SOG','Pct']
num =    [0,1,2,4,6,0,9,11,13,15,17,19,21,23,25,27,29]

lstring = ', '.join(lookup)

scraperwiki.sqlite.execute('create table if not exists score (%s)'%lstring)

url='http://sports.yahoo.com/nhl/stats/byposition?pos=D'
#url='http://sports.yahoo.com/nhl/stats/byposition?pos=C,RW,LW,D'
html=requests.get(url).content
root=lxml.html.fromstring(html)

rows=root.xpath('//table[@class="yspcontent"]//tr[@class="ysprow1" or @class="ysprow2"]')
builder=[]
for row in rows:
    data={}
    cells=[cell.text_content().strip() for cell in row.xpath('td[@class="yspscores"]')]
    for i,n in enumerate(num):
        data[lookup[i]]=duckint(cells[n])
    data['Pts']=duckint(row.xpath('descendant-or-self::span[@class="yspscores"]')[0].text_content().strip())
    builder.append(data)
    
scraperwiki.sqlite.save(table_name='score', data=builder, unique_keys=['Name'])
