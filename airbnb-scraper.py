# importing all the required libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


offset_values = list(range(0, 300, 20))
all_url_links = []

for value in offset_values:
    url_link = f'https://www.airbnb.com/s/Mombasa/homes?items_offset={value}'
    all_url_links.append(url_link)
    print(url_link)
    
    


# function to parse each page and get data
def get_page(url):
    response = requests.get('https://www.airbnb.com/s/Mombasa/homes?items_offset=0')
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    number_of_listings = soup.find('span', attrs={'class':'to8eev7'})
    
    listings = soup.find_all('div', attrs={'class':'c4mnd7m'})
    
    page_listing_details = []
    
    for listing in listings:
        listing_type = listing.find('div', attrs={'class':'t1jojoys'}).text
        listing_title = listing.find('span', attrs={'class':'t19nnqvo'}).text
        quick_features = listing.find_all('div', attrs={'class':'f15liw5s s1cjsi4j dir dir-ltr'})
        bed_type = quick_features[0].text
        availability = quick_features[1].text
        
        # superhost or not?
        host_tier = listing.find('div', attrs={'class':'t1mwk1n0 dir dir-ltr'})
        if not host_tier:
            host_tier = 'Starter / Mid'
        else:
            host_tier = host_tier.text
            
        # link to the listing page 
        listing_url = listing.find('meta', attrs={'itemprop':'url'})
        listing_url = listing_url['content']
        
        # price
        price_wrap = listing.find('div', attrs={'class':'p1v28t5c'})
        price = price_wrap.find('span', attrs={'class':'_tyxjp1'}).text
        
        # rating
        rating = listing.find('span', attrs={'class':'t5eq1io'}).text
        rating_split = rating.split(' ')
        if len(rating_split) > 1:
            rating = rating_split[0]
            number_of_reviews = rating_split[1]
            number_of_reviews = number_of_reviews.strip('()')
        else:
            rating = 'New'
            number_of_reviews = 0
        
        # creating a list of dictionary with details
        listing_details = [{'listing_type':listing_type,'listing_title':listing_title, 
                            'Host Level':host_tier,'bed_type':bed_type, 'availability':availability,
                            'price':price,'rating':rating,'reviews':number_of_reviews, 
                            'Link': listing_url}]
        
        page_listing_details.append(listing_details)
    
    # waiting five seconds before making another request
    
    print('Waiting....')
    # creating a random time in seconds for sleep
    sleep_time = range(5, 13)
    random_time = random.choice(sleep_time)
    time.sleep(random_time)
    print(f'Waited {random_time} seconds!') 
    
    return page_listing_details

# parsing through the web data we obtained to a dataframe
def data_to_df(all_listings):
    global all_listings_df
    z_index = 0
    for page in range(len(all_listings)):
        print(len(all_listings[page]))
        for listing in range(len(all_listings[page])):
            details = list(all_listings[page][listing][0].values())
            
            # isolating each detail
            listing_type = details[0]
            listing_title = details[1]
            host_tier = details[2]
            bed_type = details[3]
            availability = details[4]
            price = details[5]
            rating = details[6]
            number_of_ratings = details[7]
            listing_url = details[8]
            
            # creating the row data dataframe
            row_data = pd.DataFrame({'listing_type': listing_type, 'listing_title': listing_title,
                                     'Host Level':host_tier,'bed_type': bed_type, 'availability': availability, 
                                     'price': price, 'rating': rating, 'number_of_ratings': number_of_ratings, 'Link': listing_url},
                                    index=[z_index])
            z_index += 1
            # concatenating to the dataframe
            all_listings_df = pd.concat([all_listings_df, row_data])
            
    return all_listings_df
    
if __name__ == '__main__':
    print('We are going to get the details of AirBnBs in Mombasa')
    
    # passing in the links to the different pages
    all_listings = [get_page(url) for url in all_url_links]
    
    # converting the results to a dataframe
    # creating an empty dataframe
    all_listings_df = pd.DataFrame()
    
    # calling the function to put data into a dataframe
    listings_to_df = data_to_df(all_listings)

            
    
    
    
    