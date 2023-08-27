import trafilatura
import spacy
from geopy.geocoders import Nominatim


def load_model(model="en_core_web_lg",model_folder="./models/"):
  """
  Load spacy's english model
  """
  try:
    nlp("a")
  except:
    try:
      nlp = spacy.load(model_folder+model)
    except:
        spacy.cli.download(model)
        nlp = spacy.load(model)
        nlp.to_disk(model_folder+model)
  return nlp

def parse_report_from_url(url):
  """
  Generate parsed report from url using trafilatura

  Return
  report    dict containing parsed report
  """
  report=trafilatura.bare_extraction(trafilatura.fetch_url(url),
                                     with_metadata=True,
                                     url=url,
                                     date_extraction_params={"extensive_search": True,"original_date":True})
  return report

def keys_in_report(report,searchkey_list):
  """
  Return True if report contains target search keys. False if otherwise
  """
  search_in=(report['title']+report['description']+report['text']).replace(" ","")
  if any(searchkey in search_in for searchkey in searchkey_list):
    return True
  else:
    return False


def add_date_locs(report,country_code='ph',report_id=0):
  """
  Extract inferred dates and locations in report, and append these information to report

  report    dict, from article parsed by Trafilatura

  Return
  report    dict, with new key-value pairs for report_id, inferred dates and inferred locations
  """

  # Extract location names and dates from report
  text=report['title']+" "+report['description']+" "+report['text']
  doc = nlp(text)
  location_names = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
  dates=[ent.text for ent in doc.ents if ent.label_ == "DATE"]
  
  if location_names:
    # get unique location names, and their frequencies and geocoded addresses
    uniq_locs=list(set(location_names))
    uniq_locs_freq=[location_names.count(a) for a in uniq_locs]
    uniq_locs_address=[geolocator.geocode(uniq_locs[l],addressdetails=True,country_codes=country_code) for l in range(len(uniq_locs))]
    inferred_locs = [[uniq_locs[l], uniq_locs_freq[l],uniq_locs_address[l]] for l in range(len(uniq_locs))]
    inferred_locs = sorted(inferred_locs, key=lambda x: x[1], reverse=True)
    inferred_locs_id=[i for i in range(len(inferred_locs))]
    # append inferred locs to dict
    report["inferred_location"]={inferred_locs_id[l]:inferred_locs[l] for l in range(len(inferred_locs))}

  if dates:
    # get unique dates, and their frequencies
    uniq_dates=list(set(dates))
    uniq_dates_freq=[dates.count(a) for a in uniq_dates]
    inferred_dates=[[uniq_dates[d], uniq_dates_freq[d]] for d in range(len(uniq_dates))]
    inferred_dates = sorted(inferred_dates, key=lambda x: x[1], reverse=True)
    inferred_dates_id=[i for i in range(len(inferred_dates))]
    # append inferred dates to dict
    report["inferred_dates"]={inferred_dates_id[d]:inferred_dates[d] for d in range(len(inferred_dates))}

  # add report_id to dict
  report["report_id"]=report_id
  return report


# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="geo_inference_app")

# Load model
nlp=load_model()


# define search keys
searchkeys=[s.replace(" ","") for s in ['landslide','rockfall','roadslip',
                                        'soil erosion','soil collapse',
                                        'mudslide','mudflow']]


# set url
url='https://www.gmanetwork.com/news/topstories/regions/828201/at-least-22-killed-in-landslide-in-baybay-leyte/story/'


# parse report from url
report=parse_report_from_url(url)
# check if search key is in report
if keys_in_report(report,searchkeys):
  # add inferred dates and locations
  report=add_date_locs(report)

for key in report.keys():
  if 'inferred' in key:
    print(key)
    for key2 in report[key].keys():
      print(key2,":",report[key][key2])
  else:
    print(key,":",report[key])


