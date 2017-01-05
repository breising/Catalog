###Catalog App

A basic catalog app built with Flask, sqlalchemy, sqlite. Dependencies can be found in the requirements.txt file. Dependencies can be installed via `pip install -r requirements.txt`. 

###Functionality
Users can optionally create an account via Google+ signin to have access for creating items and categories. Unauthenticated users can still browse the catalog by selecting a category which then shows the items in that category. Clicking on an item will show details about that item. Authenticated users can create items with various data fields like, price, description, title, sku, image url etc. Authenticated users can also create new categories. Users can edit the items and categories that they create. 


### How to run:

To run the app, you must have python installed.
1. navigate to the catalog root dir.
2. Create the database by running the setup: `python database_setup.py`
3. Optional. To populate the db with a bulk list of items you can modify the `catalog_items.py` file and then run it: `python catalog_items.py`
4. Finally, to run the app: `python catalog.py` 
5. In your browser, navigate to localhost at port 8000

