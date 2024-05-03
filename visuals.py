from jinja2 import Environment, FileSystemLoader
from IPython.display import display, HTML
import csv
import json

# Load the CSV file
with open('data/players_20.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    data = list(reader)

# Save the data to a JSON file
with open('data/fifa20_players.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile)

def create_circular_treemap(data):
    json.dump('data/fifa20_players.html')
    display(HTML(html))
   


# Call the function to display the circular treemap
create_circular_treemap(data)
