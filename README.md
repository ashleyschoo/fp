My project scrapes and crawls the Petfinder website to collect informaton on pets up for adoption on a national scale. Having a nationwide data distribution will help organzations like the ASPCA distribute resources to areas that demonstrate high need.

A Google API key is required to run this program. Keep this key in a secrets.py file.

The Petfinder website associates shelter names with each pet.
When scraping and crawling Petfinder, follow the link to the shelter information page of each pet and retrieve location and contact information for the shelters.

A database browser (SQLite) that interprets SQL statements is necessary to store the data retrieved from Petfinder.com SQL statements isolate the shelter names into a list.

The google places API will take the name of the shelter and return latitude and longitude values.

The latitude and longitude values will be interpreted by Plotly and plotted on a USA Map.

SQL statements will retrieve information pet breed and age data, which will be displayed on Plotly bar graphs and tables. 

If there is a particular pet you would like more information on, enter the pet name (with correct punctuaton/symbols/numbers assigned by the shelter) into the pet profile search. A webbrowser window will open the pet's profile on Petfinder.com If the pet has beed adopted, the profile page will say the page does not exist. 

For information on adopting a pet, enter "About"
For help on how to interact with the interface, type in "help"


The code begins by establishing the website URL and cache file information. Functions to create_pet_search and create_shelters will get the information from Petfinder and store it in a CSV file. The next set of functions create the database and tables in SQLite. Then there are functions to return specific data. The final set of functions take the data from SQL and visualize it with Plotly based on user commands. 

Plotly documentation can be found here: https://plot.ly/python/
Google Places API documentation can be found here: https://developers.google.com/places/documentation/