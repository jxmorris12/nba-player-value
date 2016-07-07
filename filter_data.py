# Jack Morris 07/07/16

import csv

INPUT_FILE  = 'players.csv'
OUTPUT_FILE = 'filtered-players.csv'
HEADERS     = ["Player", "Tm", "G", "GS", "WS", "WS%", "salary", "WS%", "expected_salary", "salary_diff"]

FILTER_KEY       = "G"
FILTER_THRESHOLD = 58 # Minimum number of games to qualify for NBA scoring title

def main():
  # read lines
  file         = open(INPUT_FILE, 'r')
  lines_data   = file.readlines()
  orig_headers = lines_data[0].split(",")
  headers      = HEADERS
  lines        = lines_data[1:]
  # output to csv
  with open(OUTPUT_FILE,'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # Write headers
    csvwriter.writerow( headers )
    # Write line
    for line in lines:
      row = []
      vals = line.split(",")
      for i in xrange ( len ( vals ) ):
        key = orig_headers[i]
        val = vals[i]
        if key == FILTER_KEY: 
          if float ( val ) < FILTER_THRESHOLD:
            # filter out player
            continue
          #
        #
        if key in headers:
          row.append( val )
        #
      #
      csvwriter.writerow(row)
      #
    #
  #
#


main()