# project_week_2_duong_huy
# OBJECTIVE: build a web crawler that crawl 10 pages from each category in Tiki and store the data in the SQLITE
## 3 steps to achieve the target:
###
* **Step 1:** Create a SQLite database 
    - **Create table categories in the database using a function**
        - ![image](https://scontent.fvca1-1.fna.fbcdn.net/v/t1.15752-9/120374473_802224490580735_9180431419013507570_n.png?_nc_cat=106&_nc_sid=ae9488&_nc_ohc=J0FEA3AKGOQAX-_iDQ7&_nc_ht=scontent.fvca1-1.fna&oh=558e8baf9266c660c73c45462738e702&oe=5F9F91ED)
    - **Create tables to store your data (using OOP).**
        - ![image](https://scontent.fvca1-1.fna.fbcdn.net/v/t1.15752-9/120408810_368931617481902_4783010203367506995_n.png?_nc_cat=106&_nc_sid=ae9488&_nc_ohc=gwM9fynXJWsAX-Jolho&_nc_oc=AQnp9DHYz0cbXGNaXBXtGyhTNP5ezlpqttsTszSIy9X9gKeRL13W1L86L44wT8XJPDU&_nc_ht=scontent.fvca1-1.fna&oh=502808f7680033a54c6d5cc1778743e8&oe=5F9F978E)
* **Step 2:** Make a function to crawl the link of the categories and return a list of category URLs.
    - **Get main categories**
        - ![image](https://scontent.fvca1-2.fna.fbcdn.net/v/t1.15752-9/120467874_3392052234220383_4456734011941116404_n.png?_nc_cat=100&_nc_sid=ae9488&_nc_ohc=B3djkERTWToAX9S0OP2&_nc_ht=scontent.fvca1-2.fna&oh=37bc7821e286bb514b9fd677fc7305fb&oe=5F9FEACA)
    - **Get sub categories**
        - ![image](https://scontent.fvca1-1.fna.fbcdn.net/v/t1.15752-9/120746264_627959471215965_8530475285572795709_n.png?_nc_cat=103&_nc_sid=ae9488&_nc_ohc=6LZXAz-Htm8AX_4bW3x&_nc_ht=scontent.fvca1-1.fna&oh=c40fd488d0e6a59006a9806aca7bf18c&oe=5F9CE0C8)
    - **Get all categories**
        - ![image](https://scontent.fvca1-1.fna.fbcdn.net/v/t1.15752-9/120553800_702208290374701_4086598671036702406_n.png?_nc_cat=106&_nc_sid=ae9488&_nc_ohc=Ow_MkPjDneYAX-9WnvA&_nc_ht=scontent.fvca1-1.fna&oh=e8fc396b7fb6eb71ffa9ea51eac1dea1&oe=5F9C7F28)
* **Step 3:** Use the data from your database to make analysis about Tiki
## Extra steps:
