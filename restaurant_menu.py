#!/usr/bin/env python3

# importing only std libraries
from urllib.request import urlopen
import json, sys

Url = "https://menu.dckube.scilifelab.se/api/restaurant"

def fetch_json_data(url):
    try:
        response = urlopen(url)
        data_json = json.load(response)
        return data_json 
    except:
        sys.exit("\nSorry, something went wrong with the request, try later or contact support!\n")


def list_restaurants(rst_list):
    print(f"Try one of these resaurants:\n")
    for idx, restaurant in enumerate(rst_list):
        print(f"{idx+1:>5}) {restaurant['name']}")
    print() # new line


def list_food(user_rst):
        url = Url + '/' + user_rst["identifier"]
        user_rst_dct = fetch_json_data(url)["restaurant"]

        # get non-empty dishes
        rst_dishes = [dish for dish in user_rst_dct["menu"] if dish['dish'].strip()]
        
        if len(rst_dishes) > 0:
            print(f"\nNice choice! ({user_rst['name']}) has these dishes:\n")
            
            for idx, dish in enumerate(rst_dishes):
                print(f"{idx+1:>5}) {dish['dish']}")
        
            print(f"    ... find more about their menu: {user_rst['menuUrl']}")
        
        else:      
            print(f"\n No menu found, check their menu on their webpage:")
            print(f"{user_rst['name']} menu:  {user_rst['menuUrl']}")
            
        print(f"\n To check their home page: {user_rst_dct['url']}")
        print(f" To view their location: {user_rst_dct['map_url']}\n")        
        

data_dct = fetch_json_data(Url)
rst_list = data_dct["restaurants"]

# if no argument is given
if len(sys.argv) < 2:
    list_restaurants(rst_list)

# is this better than join in the following "else"?
# quoting works better if multiple restaurants is to be an option
elif len(sys.argv) > 2:
    sys.exit(f"\n\t Sorry, the name may have special characters, try using quotes: e.g. \"restaurant name\" \n")
    
else:
    # To allow spaces in the retstaurant names (Names better be quoted)
    # still fail if restaurant has e.g. * or [ the shell will try to expand on those.
    user_rst = ' '.join(sys.argv[1:]) 

    # Exit the loop once a restaurant is found. This assumes no duplicate names
    # Consider chaning to full search, e.g. should partial input be allowed.
    if (rst_found := next(
        (rst for rst in rst_list if rst["name"] == user_rst), 
        None) ):
        list_food(rst_found)
        
    else:
        print(f"\nSorry, can't find ({user_rst}).\n")
        list_restaurants(rst_list)
        