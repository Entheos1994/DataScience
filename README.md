# DataScience
COMP6235 Group Project

## Running locally
The application uses MongoDB as its database.  The proper json files must be stored in the correct collections for the application to work.  To enter the proper json files, run the following commands at the mongo shell.

`mongoimport --db test --collection bbc --file bbc_database.json`<br >
`mongoimport --db test --collection bbcHealthy --file bbc_Healthy.json`<br >
`mongoimport --db test --collection Rank --file ingredients_ranking_overall.json`

To start the application, run the run.py file
