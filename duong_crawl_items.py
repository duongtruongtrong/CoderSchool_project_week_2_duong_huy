from bs4 import BeautifulSoup
import requests
import sqlite3
import re
import pandas as pd
from time import sleep
from random import uniform

conn = sqlite3.connect('tiki.db')
cur = conn.cursor()

def create_products_table():
    query = """
        CREATE TABLE IF NOT EXISTS tiki_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            product_sku INTEGER,
            product_name VARCHAR(255),
            current_price INTEGER,
            data_id INTEGER,
            product_brand VARCHAR(255),
            category_id INTEGER,
            product_link TEXT,
            product_image_link TEXT,
            original_price INTEGER,
            discount_pct FLOAT,
            rating_pct FLOAT,
            number_of_reviews INTEGER,
            page INTEGER,
            item_position INTEGER,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        cur.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

def update_total_pages_products_categories(cat_id, total_pages, total_products):
    query = """
        UPDATE categories
        SET total_pages = ?,
            total_products = ?

        WHERE id = ?;
    """
    val = (total_pages, total_products, cat_id)
    try:
        cur.execute(query, val)
        conn.commit()
    except Exception as err:
        print('ERROR BY UPDATE CATEGORIES:', err)

# use dictionary for renaming the column in output excel file
data_col = {'data-seller-product-id':'product_id',
'product-sku':'product_sku',
'data-title':'product_name',
'data-price':'current_price',
'data-id':'data_id',
'data-brand':'product_brand',
'category_id':'category_id',
'product_link':'product_link',
'product_image':'product_image_link',
'price-regular':'original_price',
'sale-tag sale-tag-square':'discount_pct',
'rating_percentage':'rating_pct',
'number_of_reviews':'number_of_reviews'}

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

class Product:
    """ Use to store and save to DB all product items in 1 category.
    """
    def __init__(self, product_id, product_sku, product_name, current_price, data_id, product_brand, product_link, product_image_link, original_price, discount_pct, rating_pct, number_of_reviews, page=None, item_position=None, item_id=None, category_id=None):
        self.item_id = item_id
        self.product_id = product_id
        self.product_sku = product_sku
        self.product_name = product_name
        self.current_price = current_price
        self.data_id = data_id
        self.product_brand = product_brand
        self.category_id = category_id
        self.product_link = product_link
        self.product_image_link = product_image_link
        self.original_price = original_price
        self.discount_pct = discount_pct
        self.rating_pct = rating_pct
        self.number_of_reviews = number_of_reviews
        self.page = page
        self.item_position = item_position
        
    def save_into_db(self):
        query = """
            INSERT INTO tiki_products (product_id, product_sku, product_name, current_price, data_id, product_brand, category_id, product_link, product_image_link, original_price, discount_pct, rating_pct, number_of_reviews, page, item_position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        val = (self.product_id,
                self.product_sku,
                self.product_name,
                self.current_price,
                self.data_id,
                self.product_brand,
                self.category_id,
                self.product_link,
                self.product_image_link,
                self.original_price,
                self.discount_pct,
                self.rating_pct,
                self.number_of_reviews,
                self.page,
                self.item_position)
        try:
            cur.execute(query, val)
            self.cat_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

def get_item_list(full_webpage_html):
    """From HTML string return HTML string containing item list section on Tiki website.
    Then, get all items in the section as a list
    Only tested on Tiki TV category webpage.

    get_item_list(full_webpage_html)
    full_webpage_html: HTML of a full Tiki website page, type: string
    """
    
    # crawl class='product-box-list' section
    item_list = full_webpage_html.find_all('div', {"class":"product-item"})

    return item_list

def get_data(item_html, crawled_url_list):
    """Get data from item_list HTML for selected data_col list.
    Return Product class object -> easier to insert to tables

    If error when crawling, skip it.

    get_data(item_html)
    item_html: HTML of each item in item_list, type: string
    """

    product_link = 'https://tiki.vn/' + item_html.a['href']

    # check if this item was crawled before or not
    if len(crawled_url_list) == 0 or product_link not in crawled_url_list:

        # get general_info
        product_id = int(item_html['data-seller-product-id'])
        product_sku = int(item_html['product-sku'])
        product_name = item_html['data-title']
        current_price = int(item_html['data-price'])
        data_id = int(item_html['data-id'])
        product_brand = item_html['data-brand']

        # get links
        product_link = 'https://tiki.vn/' + item_html.a['href']
        product_image_link = item_html.a.img['src']

        # get price
        try:
            original_price = item_html.find('span', {'class':'price-regular'}).text
            original_price = int(re.sub(r'\.|đ', '', original_price))

            discount_pct = item_html.find('span', {'class':'sale-tag sale-tag-square'}).text
            discount_pct = float(re.sub(r'-|%', '', discount_pct))
        except:
            original_price = current_price
            discount_pct = 0

        # get number_of_reviews
        try:
            rating_section = item_html.find('div', {'class':'review-wrap'})
        
            number_of_reviews = rating_section.find('p', {'class':'review'}).text
            number_of_reviews = int(re.sub(r'\(| nhận xét\)', '', number_of_reviews))
        except:
            number_of_reviews = 0

        # getting to rating_pct
        try:
            p_rating = rating_section.find('p', {'class':'rating'})
            span_rating = p_rating.find('span', {'class':'rating-content'})
            
            rating_pct = span_rating.span['style']
            rating_pct = float(re.sub(r'width:|%', '', rating_pct))
        except:
            rating_pct = 0

        result = Product(product_id, product_sku, product_name, current_price, data_id, product_brand, product_link, product_image_link, original_price, discount_pct, rating_pct, number_of_reviews)

    else:
        # if this item was crawled before, return 'crawled' to stop next steps.
        result = 'crawled'

    return result

# ======================================
create_products_table()
# cur.execute('DROP TABLE tiki_products;')
# conn.commit()

# get all uncrawled category
df_category = pd.read_sql_query('''
select * from categories
where total_sub_category = 0
and total_pages is null
''', conn)

# get the last category was crawled
df_category_crawled = pd.read_sql_query('''
select * from categories
where total_sub_category = 0
and total_pages is not null
order by id desc
limit 1
''', conn)

df_category = pd.concat([df_category_crawled, df_category], sort=False)

df_category_url_list = df_category['url'].tolist()
df_category_id_list = df_category['id'].tolist()
df_category_total_pages_list = df_category['total_pages'].tolist()
df_category_total_products_list = df_category['total_products'].tolist()

for cat_link, cat_id, cat_pages, cat_products in zip(df_category_url_list, df_category_id_list, df_category_total_pages_list, df_category_total_products_list):

    number_of_product = 1

    # continue the last page to check if all product was crawled or not
    if cat_pages == None or cat_pages == 0:
        page_number = 1
    else:
        page_number = cat_pages

    # tiki link without page number
    tiki_link = cat_link + '&page='

    while number_of_product > 0:
        
        # get HTML from tiki_link + page_number
        # f'https://tiki.vn/tivi/c5015?src=c.5015.hamburger_menu_fly_out_banner&page={page_number}'
        full_html = get_html(tiki_link + str(page_number))

        # get item list from full_html
        item_list = get_item_list(full_html)
        number_of_product = len(item_list)

        # if there is not produc in item list, it means it reach the last page.
        if number_of_product > 0:

            # product count
            cat_products = 0

            # get all uncrawled category
            df_product = pd.read_sql_query(f'''
            select product_link from tiki_products
            where category_id = {cat_id}
            ''', conn)

            crawled_url_list = df_product['product_link'].tolist()

            # get all the data
            for item_html in item_list:
                output_object = get_data(item_html, crawled_url_list)
                
                if output_object != 'crawled':

                    output_object.category_id = cat_id
                    output_object.page = page_number
                    output_object.item_position = n+1
                    
                    output_object.save_into_db()
                    n+=1

            print(f'Category ID: {cat_id}. Finish crawling page {page_number} with {n} products')
            if n != 0:
                if cat_products == None:
                    cat_products = 0
                # continue adding number of products
                cat_products+=n
                update_total_pages_products_categories(cat_id, page_number, cat_products)

        page_number+=1

        sleep(uniform(1, 2))

print('Finish crawling!')