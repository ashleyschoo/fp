import requests
import json
import csv
import webbrowser
import secrets
import codecs
import sqlite3 as sqlite
import sys
sys.stdout=codecs.getwriter('utf-8')(sys.stdout.buffer)
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go
import sqlite3

import math
math.inf
-math.inf
google_key = secrets.google_places_key

#adopt_a_pet_url
# url = 'https://www.adoptapet.com/dog-adoption/search/50/miles/48105'
# base_url = 'https://www.adoptapet.com/dog-adoption/search/50/miles/48105'

#mich anti cruelty shelter
url = 'https://fpm.petfinder.com/petlist/petlist.cgi?shelter=&status=A&age=&limit=100&offset=0&animal=&title=&style=16&ref=SqJiPpqKc5VIFQk'
base_url = 'https://fpm.petfinder.com/petlist/petlist.cgi?shelter=&status=A&age=&limit=100&offset=0&animal=&title=&style=16&ref=SqJiPpqKc5VIFQk'


CACHE_FNAME = 'fpcache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r', encoding='utf-8')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(base_url):
    return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]
class Pet:
    def __init__(self, name = "Buddy", age_group = "Young" , breed = "Labrador", sheltername = ' ', description = " I just met you and I love yo..SQUIRREL!!", petId = ' '):
        self.name = name
        self.age_group = age_group
        self.breed = breed
        self.gender = gender
        self.sheltername = sheltername
        self.description = description
        self.petId = petId
    def __str__(self):
        str__ = self.name +' ' + self.age_group + ' ' + self.breed + " " + self.sheltername + " " + self.description + ' ' + self.petId
        return str__


pets_list = []
def create_pet_search(url):
    page_text = make_request_using_cache(url)
    soup = BeautifulSoup(page_text, "html.parser")
    content_div = soup.find_all('tr')
    # print(content_div)
    
    for pets in content_div:

        names = pets.find_all('span', role = 'heading')
        for pet in names:
            name = pet.text
            # print(name)

        breeds = pets.find_all('div', class_ = 'breed')
        for pet in breeds:
            breed = pet.text.strip()
            # print(breed)
        agegroups = pets.find_all('div', class_= 'age')
        for pet in agegroups:
            age = pet.text.strip()
            # print(age)
        locations = pets.find_all('div', class_ = 'location')
        for pet in locations:
            location = pet.text.strip()
            # print(location)
        pet_profiles = pets.find_all('a', class_ = 'pflink')
        for pet in pet_profiles:
            pet_profile = pet['href']
            # print(pet_profile)
            try:
                pets_list.append((name, breed, age, location, pet_profile))
            except UnboundLocalError:
                breed = 'unknown'
                age = 'baby'
                location = 'Humane Societ of Huron Valley'
            with open('500pets.csv', 'a', newline = '') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow((name, age, breed, location, pet_profile))




def make_request_using_shelters_cache(shelters_url):
    unique_ident = shelters_url
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = requests.get(shelters_url).text
        CACHE_DICTION[unique_ident] = resp
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]





# shelters_url = 'https://www.petfinder.com/cat/bailey-and-meri-41362267/mi/utica/michigan-anti-cruelty-society-mi112/'
def create_shelters(shelters_url):
    page_text = make_request_using_shelters_cache(shelters_url)
    soup = BeautifulSoup(page_text, "html.parser")
    content_div = soup.find_all('div', class_ = 'card card_org')
    # print(content_div)
    for items in content_div:

        shelter_names = items.find_all('h2', class_ = 'txt txt_h2')
        for item in shelter_names:
            shelterName = item.text.strip()
            # print(shelterName)

        shelter_addresses = items.find_all(itemprop = 'streetAddress')
        for item in shelter_addresses:
            shelterAddress = item.text.strip()


        shelter_city = items.find_all(itemprop = 'addressLocality')
        for item in shelter_city:
            shelterCity = item.text.strip()


        shelter_region = items.find_all(itemprop = 'addressRegion')
        for item in shelter_region:
            shelterRegion = item.text.strip()


        shelter_postalCode = items.find_all(itemprop = 'postalCode')
        for item in shelter_postalCode:
            shelterpostalCode = item.text.strip()

        try:
            shelterLocation = shelterCity + " "  + shelterRegion
            shelterAddresss = shelterAddress + ' ' + shelterLocation + " " + shelterpostalCode
            # print(shelterAddresss)
        except UnboundLocalError:
            shelterAddress = '1059 Sweisford Road'
            shelterCity = 'Perkiomenville,'
            shelterRegion = 'PA'
            shelterpostalCode = '18074'

        shelter_phones = items.find_all('a', class_="txt txt_link m-txt_bold")
        try:
            for item in shelter_phones[2]:
                shelterPhone = item.strip()
                # print(shelterPhone)
        except IndexError:
            shelterPhone = 'NotAvailable'


        shelter_websites = items.find_all('a', class_="btn btn_borderDark m-btn_full")
        for item in shelter_websites:
            shelterWebsite = item['href']
            # print(shelterWebsite)

            with open('shelters.csv', 'a', newline = '') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow((shelterName, shelterAddress, shelterLocation, shelterpostalCode, shelterPhone, shelterWebsite))

#retrieves all pet profile website urls and scrapes all of them for shelter info



PETSCSV = '500pets.csv'
SHELTERSCSV = 'shelters.csv'
DBNAME = '500Pets.db'

def create_pets_db():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except sqlite3.OperationalError as e:
        print(e)

    statement = '''
        DROP TABLE IF EXISTS 'Pets';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Shelters';
    '''
    cur.execute(statement)

    create_table_statement = '''
                CREATE TABLE "Pets"(
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'PetName' TEXT,
                'AgeGroup' TEXT,
                'Breed' TEXT,
                'ShelterLocation' TEXT,
                'peturl' TEXT,
                'ShelterId' INTEGER,
                    FOREIGN KEY (ShelterId) REFERENCES Shelters(Id)
                );
            '''
    cur.execute(create_table_statement)

    create_table_statement = '''
                CREATE TABLE "Shelters"(
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'shelterName' TEXT,
                'shelterAddress' TEXT,
                'shelterLocation' TEXT,
                'shelterpostalCode' TEXT,
                'shelterPhone' TEXT,
                'shelterWebsite' TEXT
                 );
            '''
    cur.execute(create_table_statement)
    conn.close()

def put_data_into_table():

    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except OperationalError as e:
        print(e)

    f = open(PETSCSV)
    f.close()
    
    with open(PETSCSV) as Pets_File:
        data = csv.reader(Pets_File)
        for row in data:
            statement = '''
            INSERT INTO Pets(Id, PetName, AgeGroup, Breed, 
            ShelterLocation, peturl, ShelterId) 
            VALUES(?,?,?,?,?,?,?); '''
            values = (None, row[0].strip('" ! # "'), row[1], row[2], row[3], row[4], None)
            cur.execute(statement, values)
            conn.commit()


def put_shelter_into_table():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except OperationalError as e:
        print(e)

    f = open(SHELTERSCSV)
    f.close()
    region_city_list = []
    with open(SHELTERSCSV) as Shelters_File:
        data = csv.reader(Shelters_File)
        for row in data:
            tag = row[3]
            region_city_list.append(row)
            #check for duplicates
            if tag not in region_city_list: 
                statement = '''
                INSERT INTO Shelters(Id, shelterName, shelterAddress, shelterLocation, 
                shelterpostalCode, shelterPhone, shelterWebsite) 
                VALUES(?,?,?,?,?,?,?); '''
                values = (None, row[0], row[1], row[2], row[3], row[4], row[5])
                cur.execute(statement, values)
                conn.commit()
                region_city_list.append(tag)

def update_foreign_keys():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except OperationalError as e:
        print(e)
    statement = 'UPDATE Pets SET ShelterId = (SELECT Id FROM Shelters WHERE Pets.ShelterLocation = Shelters.shelterLocation ) '
    cur.execute(statement)



#################### DATA PROCESSING STATEMENTS TO PREP FOR PLOTLY  ##########################

#MAP list  of shelters
shelterstr = []

def get_list_of_shelters_for_google_api():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except OperationalError as e:
        print(e)
    statement = 'SELECT S.shelterName FROM Shelters AS S'
    cur.execute(statement)
    for row in cur:
        shelterstr.append(row[0])

### DONE ###
#pets by breed (50 breeds...)
breed_search_N_data = []
breed_search_B_data = []
breed_search_A_data = []

def table_data_breed_search():
    # while input_breed != 'quit':
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except OperationalError as e:
        print(e)
    input_breed = input("Enter a breed: ")
    statement = 'SELECT Pets.PetName, Pets.Breed, Pets.AgeGroup FROM Pets WHERE Pets.Breed LIKE "%' + input_breed + '"'
    cur.execute(statement)
    for row in cur:
        breed_search_N_data.append(row[0])
        breed_search_B_data.append(row[1])
        breed_search_A_data.append(row[2])


### DONE ###
#BAR GRAPH number of pets in 4 age groups
bar_graph_x_values = []
bar_graph_y_values = []

def make_bar_graph_data():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except OperationalError as e:
        print(e)
    statement = "SELECT COUNT(Pets.AgeGroup), Pets.AgeGroup FROM Pets GROUP BY Pets.AgeGroup"
    cur.execute(statement)
    for row in cur:
        bar_graph_x_values.append(row[1])
        bar_graph_y_values.append(row[0])



### DONE ###
#TABLE finds pets based on user input age
table_N_values = []
table_B_values = []
def input_find_pets_by_age():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except OperationalError as e:
        print(e)
    input_age = input("Enter one: 'Baby', 'Young', 'Adult', 'Senior': ")
    statement = "SELECT Pets.PetName, Pets.Breed FROM Pets WHERE Pets.AgeGroup = '" + input_age + "'"
    cur.execute(statement)
    for row in cur:
        table_N_values.append(row[0])
        table_B_values.append(row[1])


##Google places API uses location text string to return lat/long location
def params_unique_combo(g_url, params_diction):
    alphabetized_keys = sorted(params_diction.keys())
    results = []
    for k in alphabetized_keys:
        results.append("{}={}".format(k, params_diction[k]))
    return g_url + "&".join(results)

lat_vals = []
lon_vals = []
text_vals =[]

def get_shelter_location(shelterstr):
    g_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    params_diction = {}
    params_diction['key'] = google_key
    params_diction['query'] = shelterstr
    response = params_unique_combo(g_url, params_diction)
    # print(response)

    if response in CACHE_DICTION:
        print("Getting cached data...")

    else:
        print("Making a request for new data...")
        resp = requests.get(g_url, params=params_diction)
        loaded_resp = json.loads(resp.text)
        CACHE_DICTION[response] = loaded_resp
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, 'w', encoding='utf-8')
        fw.write(dumped_json_cache)
        fw.close()

    for item in CACHE_DICTION[response]['results']:
        if CACHE_DICTION[response]["status"] == "OK":
            #print(response) gives website url
            #print(CACHE_DICTION[response]['results'])

            for lat in CACHE_DICTION[response]['results']:
                latit = lat['geometry']['location']['lat']
                lat_vals.append(latit)
                #print(latit)
                lon = lat['geometry']['location']['lng']
                lon_vals.append(lon)
                #print(lon)
                location = (str(latit) + "," + str(lon))
                text_vals.append(shelterstr)


#### DONE ####
pet_profile_url = []

def find_pet_profile_urls():
    try:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
    except OperationalError as e:
        print(e)
    input_name = input("Please enter a pet's name to view their profile: ")
    statement = '''SELECT Pets.peturl FROM Pets WHERE Pets.PetName LIKE '%''' + input_name + "'"
    cur.execute(statement)
    for row in cur:
        pet_profile_url.append(row[0])
    # print(pet_profile_url)


######################### PLOTLY CODES ##########################################


def map_shelter(key=google_key):
    trace1 = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = lon_vals,
        lat = lat_vals,
        text = text_vals,
        mode = 'markers',
        marker = dict(
        size = 15,
        symbol = 'star',
        color = 'magenta'
        ))
    min_lat = 10000
    max_lat = -10000
    min_lon = 10000
    max_lon = -10000

    for str_v in lat_vals:
        v = float(str_v)
        if v < min_lat:
            min_lat = v
        if v > max_lat:
            max_lat = v
    for str_v in lon_vals:
        v = float(str_v)
        if v < min_lon:
            min_lon = v
        if v > max_lon:
            max_lon = v

    center_lat = (max_lat+min_lat) / 2
    center_lon = (max_lon+min_lon) / 2

    max_range = max(abs(max_lat - min_lat), abs(max_lon - min_lon))
    padding = max_range * 0.1
    lat_axis = [min_lat - padding, max_lat + padding]
    lon_axis = [min_lon - padding, max_lon + padding]

    layout = dict(
        title = 'Your New Best Friend is Waiting for you Here: <br>(Hover for Shelter Names)',
        geo = dict(
        scope='usa',
        projection=dict( type='albers usa' ),
        showland = True,
        landcolor = "rgb(250, 250, 250)",
        subunitcolor = "rgb(100, 217, 217)",
        countrycolor = "rgb(217, 100, 217)",
        lataxis = {'range': lat_axis},
        lonaxis = {'range': lon_axis},
        center = {'lat': center_lat, 'lon': center_lon },
        countrywidth = 3,
        subunitwidth = 3
        ),
    )
    fig = dict(data=[trace1], layout=layout )
    py.plot(fig, validate=False) 


### DONE ###
def bar_graph_ages():
    data = [go.Bar(
                x=["Adult", "Baby", "Senior", "Young"],
                y=bar_graph_y_values
        )]
    py.plot(data, filename='pets-bar')

### DONE ###
def table_pets_by_age():
    trace = go.Table(
    header=dict(values=['Pet Names', 'Pet Breeds'],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values = [table_N_values, table_B_values],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

    layout = dict(width=500, height=300)
    data = [trace]
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'pets_table')

### DONE ###
def make_table_breed_search():
    trace = go.Table(
    header=dict(values=['Pet Names', 'Pet Breed', 'Pet Age Group'],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values = [breed_search_N_data, breed_search_B_data, breed_search_A_data],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

    layout = dict(width=500, height=300)
    data = [trace]
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'pet_breeds_table')

### DONE ###
def launch_pet_profile_page():
    for profile in pet_profile_url:
        webbrowser.open(profile)


################ INTERACTIVITY ########################################################
def get_adoption_info():
        help_url = "https://theshelterpetproject.org/why-adopt/"
        webbrowser.open(help_url)

def load_help_text():
    with open('help.txt') as f:
        return f.read()

def interactive_prompt():
    help_text = load_help_text()

    response = ''
    while response != 'exit':
        response = input('Please Enter shelters, ages data, pets by age, breed search, pet profile, about, help, or exit: ')
        if response == 'exit':
            print('Bye!')
            break 
        if response == 'quit':
            print('Bye!')
            break
        if response == 'help':
            print(help_text)
            continue
        if response == 'about':
            get_adoption_info()
            continue
        try:
            if response == 'shelters':
                a = get_list_of_shelters_for_google_api()
                for shelter in shelterstr:
                    b = get_shelter_location(shelterstr = shelter)
                c = map_shelter()
                a 
                b 
                c 
                continue 

            if response == 'ages data':
                a = make_bar_graph_data()
                b = bar_graph_ages()
                a
                b
                continue


            if response == 'pets by age':
                a = input_find_pets_by_age() 
                b = table_pets_by_age()
                a 
                b 
                continue

            if response == 'breed search':

                a = table_data_breed_search()
                b = make_table_breed_search()
                a 
                b 
                continue


            if response == 'pet profile':
                a = find_pet_profile_urls()
                b = launch_pet_profile_page()
                a 
                b 
                continue


        except TypeError:
            print("Invalid entry, Please enter 'help' for approved inputs")
            continue
        except IndexError:
            print("Invalid entry, Please enter 'help' for approved inputs")
            continue
        except UnboundLocalError:
            print("Something went wrong, please try again")
            continue
        except sqlite3.OperationalError:
            print("Invalid entry, Please enter 'help' for approved inputs")
            continue
        except PlotlyRequestError:
            print("Please delete some of your plotly files to make room for new ones")
            continue

################ CALLING FUNCTIONS HERE ############################

# p = create_pet_search(url)

# shelters_urls = []
# for pet in pets_list:
#     shelters_url = (pet[4])
#     shelters_urls.append(shelters_url)

# for shelterinfo in shelters_urls:
#     S = create_shelters(shelterinfo)

# a = create_pets_db()
# b = put_data_into_table()
# c = put_shelter_into_table()
# d = update_foreign_keys()

interactive_prompt()

############## UNCOMMENT TO RUN TEST FILE ##############################################
# # Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
