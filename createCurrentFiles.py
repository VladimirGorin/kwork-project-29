import os
from config.data import catalog_pages
import json


for key, page in catalog_pages.items():
    
    CurrentId = page['id']
    CurrentPage = page['url']
    CurrentFile = page['fileName']   

    with open(f"./info/{CurrentFile}.json", "w") as file:
        file.write("{}")

    with open(f"./info/Links{CurrentFile}.json", "w") as file:
        file.write("{}")
        
    with open(f"./info/Error.json", "w") as file:
        file.write("{}")
