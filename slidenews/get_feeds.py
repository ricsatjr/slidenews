import feedparser
import pandas as pd
import hashlib

# source: https://rss.feedspot.com/philippines_news_rss_feeds/
feed_urls={'manilaTimes':'https://www.manilatimes.net/?utm_source=feedspot',
           'inquirer':'https://www.inquirer.net/fullfeed/',
               'interaksyon-philStar':'https://interaksyon.philstar.com/feed/',
               'gmanews':'https://data.gmanetwork.com/gno/rss/news/feed.xml',
               'sunstar':'https://www.sunstar.com.ph/rssFeed/0'}

# initialize hash
h = hashlib.new('sha256')

# get saved local feeds
try:
  feeds_df=pd.read_csv("feeds.csv").drop(columns=['Unnamed: 0'])
except:
  feeds_df=pd.DataFrame(columns=['hash','feed','published','title','link'])

# append downloaded feeds to saved local feeds
for feed_source in feed_urls.keys():
  feed = feedparser.parse(feed_urls[feed_source])
  if feed['entries']:
    hash=[]
    feedname=[]
    published=[]
    title=[]
    link=[]
    for a in range(len(feed['entries'])):
      h.update(feed['entries'][a]['link'].encode())
      hash.append(h.hexdigest())
      feedname.append(feed['feed']['title'])
      published.append(feed['entries'][a]['published'])
      title.append(feed['entries'][a]['title'])
      link.append(feed['entries'][a]['link'])
    downloads=[[hash[a],feedname[a],published[a],title[a],link[a]] for a in range(len(feed['entries']))]
    feeds_df=pd.concat([feeds_df,pd.DataFrame(downloads,columns=feeds_df.columns)],ignore_index=True,axis=0)

# remove duplicates
feeds_df.drop_duplicates(subset=['hash'],inplace=True, ignore_index=True)
# update saved local feeds
feeds_df.to_csv('feeds.csv')

feeds_df
