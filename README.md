# nba-player-value

Scripts to download data for all NBA players for the current season, filter, and calculate their "Expected Salary" based on their Total Win Share production.

Check out the description in my Reddit post [here](https://www.reddit.com/r/nba/comments/4rmvjx/oc_valuing_the_expected_salaries_of_nba_players/). I used [this cool tool](http://truben.no/table/) to make the tables.

**collect_data.py**: save all data from http://basketball-reference.com to `players.csv`

**filter_data.py**: filter data from `players.csv` to `filtered-players.csv`
