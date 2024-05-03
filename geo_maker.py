"""from bokeh.plotting import figure, show, output_file
from bokeh.models import GeoJSONDataSource, HoverTool, ColumnDataSource
import json
import pandas as pd
from bokeh.sampledata import download
import pprint as pp
import os 

#download()
from bokeh.sampledata.population import data as population_data

players_data = pd.read_csv('data/players_20.csv')
player_data_w_dropped_cols = players_data.drop(columns=['player_url', 'long_name', 'real_face'])
players_data = players_data[['short_name', 'club', 'nationality']]
# Create a dictionary with nationality as keys and list of player-club pairs as values
nationality_data = {}
for index, row in players_data.iterrows():
    nationality = row['nationality']
    short_name = str(row['short_name'])
    player_club = {'short_name': short_name, 'club': row['club']}
    if nationality in nationality_data:
        nationality_data[nationality].append(player_club)
    else:
        nationality_data[nationality] = [player_club]

    
# Write the data to a JSON file
file_path = 'data/players.json'
if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        json.dump(nationality_data, f, indent=4)
    print(f"JSON file '{file_path}' created.")
else:
    print(f"JSON file '{file_path}' already exists.")
# Load the country GeoJSON data from the Bokeh sample data

# Read the JSON file
with open('data/players.json', 'r') as f:
    json_data = json.load(f)



countries = list(json_data.keys())
# Create the GeoJSONDataSource
geo_source = GeoJSONDataSource(tags=countries)

# Load the player data (assuming it's in a Pandas DataFrame called 'players_data')
player_source = ColumnDataSource(dict(players_data))

# Create a list of unique countries from the player data
countries = players_data['nationality'].unique()

# Create the Bokeh plot
p = figure(title="Players by Country", toolbar_location=None)
p.patches('xs', 'ys', source=geo_source, fill_color='lightgrey', line_color='black', line_width=0.5)

# Add interactivity with hover tooltips
hover = HoverTool(tooltips=[
    ("Country", "@name"),
    ("Players", "@players")
])
p.add_tools(hover)

# Create a callback function to update the hover tooltips
callback = 
var data = source.data;
var f = cb_obj.data['name'];
var players = data['player_names'][data['country'] == f].join(', ');
tooltips.properties.tooltips[1][1] = 'Players: ' + players;
source.change.emit();

geo_source.add_field('players', callback)

# Show the plot
show(p)
"""
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, GeoJSONDataSource, CustomJS
from bokeh.sampledata.population import data as population
from countryinfo import CountryInfo as c_info
import pandas as pd
import json
import pprint as pp

# Load players data
players_data = pd.read_csv('data/players_20.csv')
players_data = players_data[['short_name', 'club', 'nationality']]

# Create a dictionary with nationality as keys and list of player-club pairs as values
nationality_data = {}
for index, row in players_data.iterrows():
    nationality = row['nationality']
    short_name = row['short_name']
    club = row['club']
    if nationality in nationality_data:
        nationality_data[nationality].append((short_name, club))
    else:
        nationality_data[nationality] = [(short_name, club)]

# Extract country names from world_cities
countries = set()
print(population)
for name in population['Location']:
    countries.add(name)
for country in countries:
    country = c_info('Iran')
    pp.pprint(country.geo_json())
    break

# Create GeoJSON data for player countries
features = []
for country in countries:
    feature = {
        'type': 'Feature',
        'properties': {
            'name': country,
            'players': ', '.join([player[0] for player in nationality_data.get(country, [])]),
            'clubs': ', '.join([player[1] for player in nationality_data.get(country, [])])
        },
        'geometry': {
            'type': 'Point',
            'coordinates': [0, 0]  # Coordinates not used for this approach
        }
    }
    features.append(feature)

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

# Create a GeoJSONDataSource for the data
geo_source = GeoJSONDataSource(geojson=json.dumps(geojson))

# Create the Bokeh plot
p = figure(title="Players by Country", tools=[HoverTool()], tooltips=[
    ("Country", "@name"),
    ("Players", "@players"),
    ("Clubs", "@clubs")
])
p.circle(x='x', y='y', size=10, fill_alpha=0.3, source=geo_source)

# Add interactivity with tap tool
callback = CustomJS(args=dict(source=geo_source), code="""
    var selected_indices = cb_obj['source'].selected.indices;
    var data = cb_obj['source'].data;
    var selected_country = data['name'][selected_indices[0]];
    var players = data['players'][selected_indices[0]];
    var clubs = data['clubs'][selected_indices[0]];
    console.log(selected_country, players, clubs);
""")
p.js_on_event('tap', callback)

# Show the plot
show(p)
