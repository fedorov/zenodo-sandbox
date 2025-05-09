import requests
import json
from html_to_markdown import convert_to_markdown

def get_zenodo_metadata(deposition_id, access_token=None):
    """
    Retrieve metadata for a Zenodo deposition given the deposition ID.
    If the deposition is private, supply a valid access_token.
    """
    url = f"https://zenodo.org/api/deposit/depositions/{deposition_id}"
    params = {}
    if access_token:
        params['access_token'] = access_token
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# get environment variable TOKEN
import os
TOKEN = os.getenv('ZENODO_API_TOKEN')

# read deposition_id from command line argument
import sys
if len(sys.argv) > 1:
    deposition_id = sys.argv[1]
else:
    # default is one of the IDC depostions
    deposition_id = '14041167'
metadata = get_zenodo_metadata(deposition_id, access_token=TOKEN)
print(json.dumps(metadata,indent=2))

# transform metadata["metadata"]["description"] from HTML to markdown
md = convert_to_markdown(metadata["metadata"]["description"])
print(" ===== MARKDOWN ===== \n\n\n")
print(md)


# go back from markdown to HTML
import markdown
html = markdown.markdown(md)
print(" ===== HTML ===== \n\n\n")
# print the HTML
print(html)