# OBJECTIVE: build a web crawler that crawl all pages from each category in Tiki and store the data in the SQLite.

## 1. Files:
- duong_crawl_category.py: Get all categories.
- duong_crawl_items.py: Get all items in all crawled categories.
- tiki.db
- tiki_cat.xlsx
- tiki_products.xlsx

## 2. Steps to achieve the target:

* **Step 1:** Create a SQLite database 
    - **Create table "categories" in the database**
    
    Columns:
    - id
    - name
    - url
    - **level**: Level of the category in the category tree. Level 1 = the main categories.
    - **total_sub_category**: Total of sub categories that the category contain. 0 = the category does not have any sub category.
    - parent_id
    - created_at
    
    ![image](https://user-images.githubusercontent.com/71629218/95008136-48442b00-0641-11eb-8b29-53b4a0ddb9e9.png)

    - **Use ODP to temporauily store, create save_to_db method using "INSERT" and update_total_sub_category using "UPDATE"**
        - **save_to_db**: Save every category to table categories as 1 row.
        - **update_total_sub_category**: Update total_sub_category of every parent category in table categories.
    
    ![image](https://user-images.githubusercontent.com/71629218/95008161-79246000-0641-11eb-925a-76c28361276b.png)

* **Step 2:** Crawl the link of the sub categories and return a list of last sub-categories.
    - **Get main categories:** The categories on tiki.vn homepage
    
    ![image](https://user-images.githubusercontent.com/71629218/95008206-fd76e300-0641-11eb-9eae-61fab8263cd8.png)

    - **Get sub categories:** Assign level of the sub category (= parent_level + 1) and update total_sub_category of the direct parent category.
    
    ![image](https://user-images.githubusercontent.com/71629218/95008228-25664680-0642-11eb-936d-32c2af0a68ad.png)
        
    - **Get all categories:** Only the last sub-categories (category with total_sub_category = 0) are used for crawling items.
    
    ![image](https://user-images.githubusercontent.com/71629218/95008235-4038bb00-0642-11eb-9c22-530efd3d32a2.png)

* **Step 3:** Crawl all items in each last sub-categories (category with total_sub_category = 0) and save each item to table **tiki_products** in SQLite database.

**Extra features**: Continue where the script left when interupted:
- Continue to crawl the next item in a page;
- Or continue the next page;
- Or continue the next category.

## 3. Data Analysis:
### A. Categories:
**Total Sub Categories in each Main Categories**
Homes for Life (Nhà Cửa Đời Sống) has the most number of sub categories: 600 sub categories.
![image](https://user-images.githubusercontent.com/71629218/95008402-db7e6000-0643-11eb-8164-b2cb97d5259c.png)

### B. Products:

