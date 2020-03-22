
from twitterscraper.query import query_user_info
from twitterscraper.query import query_tweets_from_user
import pandas as pd
from multiprocessing import Pool
import time
from IPython.display import display
import json
import collections
from datetime import datetime
import openpyxl

'''
что бы вручную не переписывать твиты
'''
a=[]

wb = openpyxl.load_workbook('123.xlsx')

sheet = wb.active

for cell in sheet['B']:
	a.append(cell.value)

del a[0]


global twitter_user_info
twitter_user_info = []


def get_user_info(twitter_user):
    """
    An example of using the query_user_info method
    :param twitter_user: the twitter user to capture user data
    :return: twitter_user_data: returns a dictionary of twitter user data
    """
    user_info = query_user_info(user=twitter_user)
    twitter_user_data = {}
    twitter_user_data["user"] = user_info.user
    twitter_user_data["fullname"] = user_info.full_name
    twitter_user_data["location"] = user_info.location
    twitter_user_data["blog"] = user_info.blog
    twitter_user_data["date_joined"] = user_info.date_joined
    twitter_user_data["id"] = user_info.id
    twitter_user_data["num_tweets"] = user_info.tweets
    twitter_user_data["following"] = user_info.following
    twitter_user_data["followers"] = user_info.followers
    twitter_user_data["likes"] = user_info.likes
    twitter_user_data["lists"] = user_info.lists

    return twitter_user_data


def main():
    '''
    start = time.time()
    users = ['realDonaldTrump']

    pool = Pool(8)    
    for user in pool.map(get_user_info,users):
        twitter_user_info.append(user)

    cols=['id','fullname','date_joined','location','blog', 'num_tweets','following','followers','likes','lists']
    data_frame = pd.DataFrame(twitter_user_info, index=users, columns=cols)
    data_frame.index.name = "Users"
    data_frame.sort_values(by="followers", ascending=False, inplace=True, kind='quicksort', na_position='last')
    elapsed = time.time() - start
    print("Elapsed time: ")
    print(elapsed)
    display(data_frame)
'''
    with open("data.json", "w") as f:
        f.write("Current time {} START!!!\n".format(datetime.now().ctime()))
    users = list(a)
    json_object_array = []
    data = {}
    tweet_count_old = 0    
    for user in users:
        for tweet in query_tweets_from_user(user, limit=10):
            data['screen_name'] = tweet.screen_name.encode('utf-8')
            data['timestamp'] = tweet.timestamp.ctime()
            data['text'] = tweet.text.encode('utf-8')
            json_dump = json.dumps(data)
            json_object_array.append(json.loads(json_dump))
        with open("data.json", "a") as f:
            f.write("Got {} tweets from username {}\n".format(len(json_object_array) - tweet_count_old,user))
        tweet_count_old = len(json_object_array)
    with open('data.json', 'a') as f:
        json.dump(json_object_array, f,  indent=2)    


print("Done!")

if __name__ == '__main__':
    main()
