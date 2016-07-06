import csv
import requests
from bs4 import BeautifulSoup

# sample search
search_base = "http://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&type=totals&year_min=2016&year_max=2016&age_min=0&age_max=99&height_min=0&height_max=99&order_by=ws"

# salary page
salary_base = "http://www.basketball-reference.com/contracts/"
salary_ext  = ".html"

# Adapted from code by github user @andrewgiessel
def getSoupFromURL(url, suppressOutput=True):
    """
    This function grabs the url and returns and returns the BeautifulSoup object
    """
    if not suppressOutput:
        print "Querying: " + url + "."

    try:
        r = requests.get(url)
        if not suppressOutput:
          print "Query succesful."

    except:
        return None

    return BeautifulSoup(r.text, "html.parser")

# Load statistics for all players on a team, sorted by total win shares
def load_team_data(TEAM_ID):
  search_query = search_base + '&franch_id=' + TEAM_ID
  soup = getSoupFromURL( search_query, False )
  if soup == None:
    print "Error."
    return
  # Get table
  table = soup.find('table', attrs={ "class" : "sortable"})
  # Get headers
  headers = [header.text for header in table.find_all('th')]
  # Remove top headers
  del headers[:4]
  # Fill rows with data
  rows = []
  for row in table.find_all('tr'):
    data = [val.text.encode('utf8') for val in row.find_all('td')]
    if len( data ) > 0:
      rows.append(data)
  table = [ headers ] 
  table . extend ( rows )
  return table

# Load all salaries for players on a team who played in the 2015-2016 season
def load_team_salaries(TEAM_ID):
  salary_url = salary_base + TEAM_ID + salary_ext
  soup = getSoupFromURL( salary_url, False )
  # Get table
  table = soup.find('table', attrs={ "id" : "payroll"})
  # Populate players
  players = []
  for row in table.find_all('tr'):
    data = [val.text.encode('utf8') for val in row.find_all('td')]
    if len( data ) < 2:
      continue
    name = data[0]
    salary = data[2]
    salary = salary.replace("$", "") # Remove $
    salary = salary.replace(",", "") # Remove ,
    if not (name == None or salary == None):
      player = {}
      player["name"]   = name
      player["salary"] = float( salary )
      player["team"]   = TEAM_ID
      players.append( player )
  # Return
  return players

def process_team(team_data, team_salaries):
  # Create array to store player data
  players = []
  # Load data from arrays into objects
  keys = team_data [ 0 ] # headers
  for j in xrange( 1,len(team_data) ):
    row = team_data[j]
    player_name = row[1]
    # Find player in salaries array
    s_i = -1
    for s_j in xrange( len( team_salaries) ):
      player_obj = team_salaries[s_j]
      if player_obj["name"] == player_name:
        s_i = s_j
        break
    # Ensure player found
    if s_i == -1:
      # No salary found - player probably got traded midseason
      print "No salary found for", row[1], "on", team_salaries[0]["team"] + "."
      # Skip to next player
      continue
    # Store all data
    for i in xrange( len( row ) ):
      datum = row [i]
      key  = keys[i]
      team_salaries[s_i][key] = datum
    # Store in players
    players . append ( team_salaries[s_i] )
  # Calculate total salary and win shares
  TOTAL_TEAM_SALARY = 0.0
  TOTAL_WIN_SHARES  = 0.0
  for player in players:
    TOTAL_TEAM_SALARY += float(player["salary"])
    TOTAL_WIN_SHARES  += float(player["WS"])
  # Calculate WS%
  for player in players:
    WS = float(player["WS"])
    player["WS%"] = WS / TOTAL_WIN_SHARES
  # Calculate expected salary based on WS% - and difference between that and actual salary
  for player in players:
    player["expected_salary"] = float( player["WS%"] ) * TOTAL_TEAM_SALARY
    player["salary_diff"] = float ( player["expected_salary"] ) - float( player["salary"] )
  # Return
  return players

def main(OUTPUT_FILE):
  for team in teams:
    # Load team data
    data = load_team_data( team )
    # Load salaries
    salaries = load_team_salaries( team )
    # Combine and parse
    players = process_team( data, salaries )
    # Export to CSV
    headers = data[0]
    headers.extend(["WS%", "expected_salary", "salary_diff"])
    print "Writing to ", OUTPUT_FILE + "."
    with open(OUTPUT_FILE, 'wb') as csvfile:
      csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      # Write headers
      csvwriter.writerow( headers )
      # Write all player dicts
      for player in players:
        print "Player:",player
        print
        player_list = []
        for key in headers:
          player_list.append( player[key] )
        csvwriter.writerow(player_list)
      # Finished
      print "Successfully wrote to ", OUTPUT_FILE + "."


#
# Call main function
#
teams = [ 'CLE' ]
main('players.csv')
