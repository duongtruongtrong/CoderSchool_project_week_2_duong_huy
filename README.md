# OBJECTIVE: build a web crawler that crawl all pages from each category in Tiki and store the data in the SQLite.

## 1. Files:
- **duong_crawl_category.py**: Get all categories.
- **duong_crawl_items.py**: Get all items in all crawled categories.
- **tiki_db.rar**: Contain tiki.db because GitHub does not allow pushing file with >100MB on repository.
- **tiki_cat.xlsx**: Categories table as an excel file.
- **tiki_products.xlsx**: Sample records from tiki_products table.
- duong_analysis.ipynb: Some charts.

## 2. Results:
- 3,191 categories.
- 708,133 products: All products that can be crawled from Tiki website.

## 3. Steps to achieve the target:

* **Step 1:** Create a SQLite database 
    - **Create table "categories" in the database**
    
    Columns:
    - id
    - name
    - url
    - **level**: Level of the category in the category tree. Level 1 = the main categories. 
    - **total_sub_category**: Total of sub categories that the category contain. **Purpose:** 0 = the category does not have any sub category.
    - parent_id
    - created_at
    
    ![image](https://user-images.githubusercontent.com/71629218/95008136-48442b00-0641-11eb-8b29-53b4a0ddb9e9.png)

    - **Use OOP to temporarily store, create save_to_db method using "INSERT" and update_total_sub_category using "UPDATE"**
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

    Similar to Week 1 project with some updates:
    - Use class "Product" (OOP) to temporily save product values from HTML, instead of a dictionary.
    - Save items to SQLite database, instead of a dataframe and a excel file.
    - **Extra features**: Continue crawling where the script left when interupted by using SQLite database (catgories and tiki_products tables) as backup source, instead of a excel file.
        - Continue to crawl the next item in a page;
        - Or continue the next page;
        - Or continue the next category.

## 4. Data Analysis:
### A. Categories:
It took more than **4 hours** to finish crawling all categories urls.

**Total sub categories in each main categories**

"Homes for Life" (Nhà Cửa Đời Sống) has the biggest number of sub categories: 600 sub categories.
![image](https://user-images.githubusercontent.com/71629218/95008402-db7e6000-0643-11eb-8164-b2cb97d5259c.png)

**Total products in each main categories**

Big number of sub categories of "Homes for Life" (Nhà Cửa Đời Sống) is due to the big number of products.
![image](https://user-images.githubusercontent.com/71629218/95012554-bef22000-0663-11eb-8a14-ac77b8be3795.png)

### Interesting findings
**Top 10 sub categories with highest number of products**

Number of products of each category usually reachs the **maximum of 1000**. Tiki database contains more than that, but not showing on the website.

However, there are **3 categories breaks the rule**: "Bộ chăn ga, ra, drap" (Blankets, sheets), "Tranh canvas" (Canvas pictures), "Đồ chơi" (Toys) have **over 4000 products** and **up to 200 pages**. 

**Not sure** how the script can scrawl such data because with UI on the webpage, pages above 21 can not be accessed. 

All products in those 3 categories are **only duplicated** because Tiki place the **same product in different places** with the product links are also different.

![image](https://user-images.githubusercontent.com/71629218/95008927-0a96d080-0648-11eb-8f03-e4edaede13a6.png) ![image](https://user-images.githubusercontent.com/71629218/95009341-847c8900-064b-11eb-8c60-77734cb2fb3a.png)

### B. Products:
It took more than **19 hours**  to finish crawling all products in all categories.

**Average current price of each main categories**

Unit: 10,000,000 VND (10 million VND)

Price after discount.

Electronics (Điện tử - điện lạnh) has the highest average price, over 10 million VND.
![image](https://user-images.githubusercontent.com/71629218/95033177-72502880-06e7-11eb-8ac2-1f204e5a99eb.png)

**Highest price**: Harley Davidson FXDRS 2019 (Xe Mô Tô Harley Davidson FXDRS - 2019) - 799,500,000 VND

**A sample of 0 VND price**: Box of 10 Volluto Coffee Capsule Capsules - Nespresso (Hộp 10 Viên Nén Capsule Cà Phê Volluto - Nespresso) **due to out of stock**

**Lowest price**: Zinc Branches (Kẽm Cành) - 1,920 VND

### Intersting Findings
**Product position on a page vs Discount rate** (only considering products having discount rate > 0%)

Position number **7, 17, 27, 37, 47** usually do not have **discount range of 40-60%**. Popular discount percentage: 10, 20, 30, 40, 50.

![image](https://user-images.githubusercontent.com/71629218/95015867-a7be2d00-0679-11eb-80b4-23a3369acd80.png)

**Product page number vs Discount rate** (only consiering products having discount rate > 0%)

Discounted products are mostly placed on **page 1 to page 6**. After page 6, the number of discounted products starts decreasing.
![image](https://user-images.githubusercontent.com/71629218/95015923-f10e7c80-0679-11eb-8914-4a9eb2dcaeab.png)
