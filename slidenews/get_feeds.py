import feedparser
import pandas as pd


# source: https://rss.feedspot.com/philippines_news_rss_feeds/
feed_urls={'manilaTimes':'https://www.manilatimes.net/?utm_source=feedspot',
           'inquirer':'https://www.inquirer.net/fullfeed/',
           'interaksyon-philStar':'https://interaksyon.philstar.com/feed/',
           'gmanews':'https://data.gmanetwork.com/gno/rss/news/feed.xml',
           'sunstar':'https://www.sunstar.com.ph/rssFeed/0'}

# get saved local feeds
try:
  feeds_df=pd.read_csv("downloads/feeds.csv").drop(columns=['Unnamed: 0'])
except:
  feeds_df=pd.DataFrame(columns=['feed','published','title','link'])

# append downloaded feeds to saved local feeds
for feed_source in feed_urls.keys():
  print(feed_source)
  feed = feedparser.parse(feed_urls[feed_source])
  downloads=[[feed['feed']['title'],
              feed['entries'][a]['published'],
              feed['entries'][a]['title'],
              feed['entries'][a]['link']] for a in range(len(feed['entries']))]
  feeds_df=pd.concat([feeds_df,pd.DataFrame(downloads,columns=feeds_df.columns)],ignore_index=True,axis=0)

# remove duplicates
feeds_df.drop_duplicates(inplace=True, ignore_index=True)
# update saved local feeds
feeds_df.to_csv("downloads/feeds.csv")

feeds_df
