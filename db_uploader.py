# manage.py 경로에 db_uploader.py
import os
import django
import csv
import bcrypt
# import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE','hangover.settings')
django.setup()
#

from products.models import *
from users.models import Friend, User, Cart
from reviews.models import Review, Comment, ReviewLike, Rating


###no_dependency(have no foreignkey)
#users : User
CSV_PATH_PRODUCTS='./db_csv/users_User_i.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if User.objects.filter(pk=row[0]).exists():
            pass
        else:
            encrypted_password = bcrypt.hashpw(row[4].encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            User.objects.create(pk=row[0],firstname=row[1],lastname=row[2],email=row[3],password=encrypted_password
            )

#products:Category, Country, FoodPairing
CSV_PATH_PRODUCTS='./db_csv/products_Category_i.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if Category.objects.filter(pk=row[0]).exists():
            pass
        else:
            Category.objects.create(pk=row[0],name=row[1])

CSV_PATH_PRODUCTS='./db_csv/products_Country_i.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if Country.objects.filter(pk=row[0]).exists():
            pass
        else:
            Country.objects.create(pk=row[0],country=row[1])

CSV_PATH_PRODUCTS='./db_csv/products_FoodPairing_i.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if FoodPairing.objects.filter(pk=row[0]).exists():
            pass
        else:
            FoodPairing.objects.create(pk=row[0],food_category=row[1])

#reviews : Review
CSV_PATH_PRODUCTS='./db_csv/reviews_Rating_i.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if Rating.objects.filter(pk=row[0]).exists():
            pass
        else:
            Rating.objects.create(pk=row[0],score=row[1])

###have_dependency(have_foreignkey)
#users : Friend
CSV_PATH_PRODUCTS='./db_csv/users_Friend_d.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if Friend.objects.filter(pk=row[0]).exists():
            pass
        else:
            Friend.objects.create(pk=row[0],friend_from_id=row[1],friend_to_id=row[2])
            #그냥 friend_from으로 하면 객체를 넣어줘야 함!!

#products : Product
CSV_PATH_PRODUCTS='./db_csv/products_Product_d.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if Product.objects.filter(pk=row[0]).exists():
            pass
        else:
            property = {
                'sweetness':row[6],
                'sparkling':row[7],
                'bitterness':row[8]
            }

            Product.objects.create(pk=row[0],name=row[1],category_id=row[2],country_id=row[3],alcohol_percentage=row[4],price=row[5],property=property)
            #그냥 friend_from으로 하면 객체를 넣어줘야 함!!


#have_deep_dependency(have_foreignkey)
#users : Cart
CSV_PATH_PRODUCTS='./db_csv/users_Cart_dd.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if Cart.objects.filter(pk=row[0]).exists():
            pass
        else:
            Cart.objects.create(pk=row[0],user_id=row[1],product_id=row[2],count=row[3])
            #그냥 friend_from으로 하면 객체를 넣어줘야 함!!

#products : ImageURL, ProductFoodPairing
CSV_PATH_PRODUCTS='./db_csv/products_ImageUrl_dd.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if ImageUrl.objects.filter(pk=row[0]).exists():
            pass
        else:
            ImageUrl.objects.create(pk=row[0],image_url=row[1],product_id=row[2])
            #그냥 friend_from으로 하면 객체를 넣어줘야 함!!

CSV_PATH_PRODUCTS='./db_csv/products_ProductFoodPairing_dd.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if ProductFoodPairing.objects.filter(pk=row[0]).exists():
            pass
        else:
            ProductFoodPairing.objects.create(pk=row[0],product_id=row[1],foodpairing_id=row[2])


#reviews : Review, Comment,ReviewLike
CSV_PATH_PRODUCTS='./db_csv/reviews_Review_dd.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if Review.objects.filter(pk=row[0]).exists():
            pass
        else:
            Review.objects.create(pk=row[0],user_id=row[1],product_id=row[2],rating_id=row[3], content = row[4])


CSV_PATH_PRODUCTS='./db_csv/reviews_ReviewLike_dd.csv'
with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader,None)
    for row in data_reader:
        if ReviewLike.objects.filter(pk=row[0]).exists():
            pass
        else:
            ReviewLike.objects.create(pk=row[0],review_id=row[1],user_id=row[2])