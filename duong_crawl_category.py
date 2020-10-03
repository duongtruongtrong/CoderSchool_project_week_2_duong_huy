from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd
import re
from time import sleep
from random import uniform


TIKI_URL = 'https://tiki.vn'

conn = sqlite3.connect('tiki.db')
cur = conn.cursor()

# Create table categories in the database using a function
def create_categories_table():
    query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            level INTEGER,
            total_sub_category INTEGER,
            parent_id INTEGER,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        cur.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

def get_html(link):
    """From URL return HTML code in the website.

    get_html(link)
    link: URL of the website, type: string
    """
    try:
        # get website data
        r = requests.get(link)

        # turn website data text to HTML
        soup = BeautifulSoup(r.text, 'html.parser')

        return soup

    except Exception as err:
        print('ERROR BY REQUEST:', err)

class Category:
    """ Instead of using a function to do CRUD on database,
        creating a class Category is preferred
        attributes: name, url, parent_id
        instance method: save_into_db()
    """
    def __init__(self, name, url, cat_id=None, level=None, total_sub_category=None, parent_id=None):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.level = level
        self.total_sub_category = total_sub_category
        self.parent_id = parent_id

    def __repr__(self):
        return f"ID: {self.cat_id}, Name: {self.name}, URL: {self.url}, Level: {self.level}, Total sub-category: {self.total_sub_category}, Parent: {self.parent_id}"

    def save_into_db(self):
        query = """
            INSERT INTO categories (name, url, level, total_sub_category, parent_id)
            VALUES (?, ?, ?, ?, ?);
        """
        val = (self.name, self.url, self.level, self.total_sub_category, self.parent_id)
        try:
            cur.execute(query, val)
            self.cat_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)
    
    def update_total_sub_category(self):
        query = """
            UPDATE categories
            SET total_sub_category = ?
            WHERE id = ?;
        """
        val = (self.total_sub_category, self.cat_id)
        try:
            cur.execute(query, val)
            conn.commit()
        except Exception as err:
            print('ERROR BY UPDATE:', err)

def get_main_categories(save_db=False):
    """
    Get main categories from Tiki home page: https://tiki.vn
    Save to table "categories" in tiki.db is optional
    """

    soup = get_html(TIKI_URL)

    result = []
    for a in soup.find_all('a', {'class': 'MenuItem__MenuLink-sc-181aa19-1 fKvTQu'}):
        url = a['href']

        name = a.find('span', {'class': 'text'}).text
        main_cat = Category(name, url, level=1)

        if save_db == True:
            main_cat.save_into_db()
        result.append(main_cat)
    return result

# get_sub_categories() given a parent category
def get_sub_categories(parent_category, save_db=False):
    parent_url = parent_category.url
    result = []

    sub_level = parent_category.level + 1
    parent_id = parent_category.cat_id

    try:
        soup = get_html(parent_url)
        div_containers = soup.find_all('div', {'class':'list-group-item is-child'})

        # update total_sub_category of parent_category
        parent_category.total_sub_category = len(div_containers)

        parent_category.update_total_sub_category()

        # crawl data of sub_categories
        for div in div_containers:
            sub_url = TIKI_URL + div.a['href']

            name = div.a.text

            # remove newline, spaces that appear > 2 times and numbers with parenthesis
            name = re.sub(r'(\s{2,}|\n+|\(\d+\))', '', name)

            cat = Category(name=name, url=sub_url, level=sub_level, parent_id=parent_id) # we now have parent_id, which is cat_id of parent category

            # skip crawled categories, so the data in the DB won't be duplicated
            if save_db == True:
                cat.save_into_db()
            result.append(cat)

        # random sleep to ease Tiki server load -> pretend not to be a bot
        sleep(uniform(1, 3))

    except Exception as err:
        f = open('error_sub_cat.txt', 'w')
        print(parent_url, end='\n==============\n', file=f)
        print('ERROR BY GET SUB CATEGORIES:', err)
        f.close()
    return result

# get_all_categories() given a list of main categories (This is a recursion function)
def get_all_categories(categories,save_db=False):
    if len(categories) == 0:
        return
    for cat in categories:
        sub_categories = get_sub_categories(cat, save_db=save_db)
        print(f'{cat.name} has {len(sub_categories)} sub-categories')

        get_all_categories(sub_categories, save_db=save_db)

create_categories_table()
# cur.execute('DROP TABLE categories;')
# conn.commit()

main_categories = get_main_categories(save_db=True)

get_all_categories(main_categories,save_db=True)

# import os
# os.system('shutdown /p /f')

# df = pd.read_sql_query('''
# select * from categories
# ''', conn)
# df.to_excel('tiki_cat.xlsx', index=False)