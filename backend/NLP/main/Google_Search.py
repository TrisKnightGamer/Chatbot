# Import the api module for the results class
import search_google.api
from search_google.cli import run

# Define buildargs for cse api
buildargs = {
  'serviceName': 'customsearch',
  'version': 'v1',
  'developerKey': 'AIzaSyDoi7PUkRbzJ0ggoQ25FJ-3-fTLRTEAuEs'
}

# Define cseargs for search
cseargs = {
  'q': 'keyword query',
  'cx': 'your_cse_id',
  'num': 3
}

# Create a results object
results = search_google.api.results(buildargs, cseargs)

# Download the search results to a directory
results.download_links('downloads')

# Preview the search results
results.preview()

# Obtain the url links from the search
# Links are inside results['items'] list
links = results.get_values('items', 'link')

# Obtain the url links from the search
links = results.links

# Save the search result links to a text file
results.save_links('links.txt')