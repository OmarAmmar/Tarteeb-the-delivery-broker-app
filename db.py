from datetime import date
from datetime import datetime
from datetime import timedelta
import psycopg2
import random

DELIVERY = 0
RESERVATION = 1
PICKUP = 2
DELIVERYFEE = 10

SHOP = 0
RIDER = 1
PRODUCT = 2


# A function to check the availability of connection to a database server
def connect(printmodel=0):
    """ Connect to the PostgreSQL database server """
    conn = None
    cur = None

    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect("dbname=postgres user=postgres password=hictoromar123")

        # create a cursor
        cur = conn.cursor()

        if printmodel:
            # execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn, cur


# A function to view all the shops
def ViewAllShops():
    conn, cur = connect()

    cur.execute('''SELECT S.name, S.location AS RESTAURANTS FROM public."SHOP" S ''')
    result = cur.fetchall()

    conn.close()
    return result


# A function to view all the resturants on the platform
def ViewAllResturants():
    conn, cur = connect()

    cur.execute('''SELECT S.name AS RESTAURANTS FROM public."RESTURANTS" R
                    INNER JOIN 
                    public."SHOP" S 
                    ON R."resturantID" = S."shopID";
                          ''')
    result = cur.fetchall()

    conn.close()
    return result


# A function to view all the grocerry shops on the platform
def ViewAllGrocerry():
    conn, cur = connect()

    cur.execute('''SELECT S.name AS RESTAURANTS FROM public."GROCERRY" G
                    INNER JOIN 
                    public."SHOP" S 
                    ON R."GROCERRY_ID" = S."shopID";
                          ''')
    result = cur.fetchall()

    conn.close()
    return result


# a function to sort the restaurants on the platform
def SortResturants(cuisine=None, area=None):
    conn, cur = connect()

    if cuisine is not None and area is not None:
        cur.execute('''
                SELECT S.name AS RESTAURANTS FROM public."RESTURANTS" R
                INNER JOIN 
                public."SHOP" S 
                ON R."resturantID" = S."shopID" 
                WHERE R."cuisineType" LIKE '{}' AND S."location" LIKE '{}' '''.format("%" + cuisine + "%",
                                                                                      "%" + area + "%"))
    elif cuisine is not None:
        cur.execute('''
                SELECT S.name AS RESTAURANTS FROM public."RESTURANTS" R
                INNER JOIN 
                public."SHOP" S 
                ON R."resturantID" = S."shopID" 
                WHERE R."cuisineType" LIKE '{}' '''.format("%" + cuisine + "%", ))
    elif area is not None:
        cur.execute('''
                SELECT S.name AS RESTAURANTS FROM public."RESTURANTS" R
                INNER JOIN 
                public."SHOP" S 
                ON R."resturantID" = S."shopID" 
                WHERE S."location" LIKE '{}' '''.format("%" + area + "%"))

    result = cur.fetchall()

    conn.close()
    return result


def AddProductToOrder(orderID, ProductID, count=1):
    conn, cur = connect()

    cur.execute('''
    SELECT "productID" FROM public."PRODUCT";''')

    allproducts = []
    result = cur.fetchall()

    for i in range(len(result)):
        allproducts.append(result[i][0])

    if ProductID not in allproducts:
        raise Exception("Product does not exist")
    else:
        cur.execute('''
        INSERT INTO public."PRODUCT_ORDER"(
	    "productID", "orderID", count)
	    VALUES ('{}', '{}', {});'''.format(ProductID, orderID, count))

    conn.commit()
    conn.close()


def getAllProductsFromMenu(shopName, ShopLocation):
    conn, cur = connect()

    # first get the ID of the shop's menu
    cur.execute('''SELECT "menuID"
	FROM public."SHOP" WHERE name = '{}' AND location LIKE '%{}%';'''.format(shopName, ShopLocation))

    ID = cur.fetchone()

    # get all the products from the menu

    cur.execute('''
    SELECT "productID", price, description
	FROM public."PRODUCT" WHERE "menuID" = '{}';'''.format(ID[0]))

    result = cur.fetchall()

    conn.close()
    return result


# A function to add a new order
# type = 0 :: Delivery , 1 :: Reservation , 2:: Pick_up
def AddNewOrder(type=None, orderID=None, totalPrice=None, user_email=None, date=None, shopID=None, no_customers=0):
    currentDate = datetime.today()
    currentTime = datetime.now()
    currentTime = currentTime.strftime("%H:%M:%S")

    conn, cur = connect()

    cur.execute('''
    INSERT INTO public."ORDER"(
	"orderID", "totalPrice", user_email, points, date, "time")
	VALUES ('{}', {}, '{}', {},'{}', '{}');
	'''.format(orderID, totalPrice, user_email, totalPrice / 10, currentDate, currentTime))

    if type == 'DELIVERY':

        # get the list of all available riders
        Riders = getAvailableRiders()

        # get the rider ID ( could be improved later to handle communication instead of this barabaric way)
        riderID = Riders[random.randint(0, len(Riders) - 1)][0]

        cur.execute('''
        INSERT INTO public."ORDER_DELIVERY"(
	    "orderID", "deliveryFee", "riderID", "shopID")
	    VALUES ('{}', {}, '{}', '{}');
        '''.format(orderID, DELIVERYFEE, riderID, shopID))
    elif type == 'RESERVATION':
        cur.execute('''
        INSERT INTO public."ORDER_RESERVATION"(
	    "orderID", no_customers, date, "resturantID")
	    VALUES ('{}', {}, '{}', '{}');'''.format(orderID, no_customers, date, shopID))
    elif type == 'PICKUP':

        EST = random.randint(0, 45)

        cur.execute('''
        INSERT INTO public."ORDER_PICKUP"(
	    "orderID", "EstimatedTime")
	    VALUES ('{}', {});
        '''.format(orderID, EST))
    else:
        # the command was wrongly entered roll back and don't commit changes
        conn.close()
        return

    conn.commit()
    conn.close()


# A function that returns a list of riders
def getAvailableRiders():
    conn, cur = connect()

    cur.execute('''
    select * from 
    public."RIDERS" R
    INNER JOIN public."RIDER_DATA" S ON  S."email" = R."email";   
    ''')
    result = cur.fetchall()
    conn.close()

    return result


# A function to delete the order from the database
def cancelOrder(id):
    conn, cur = connect()

    cur.execute('''
        DELETE FROM public."ORDER" O
        WHERE O."orderID" = '{}';
        '''.format(id))

    conn.commit()
    conn.close()


# a function to add a review to the database
def addReviews(type=0, email=None, review=None, shopID=None, riderID=None, ProductID=None):
    conn, cur = connect()

    if type == PRODUCT:
        cur.execute('''
        INSERT INTO public."PRODUCT_REVIEWS"(
        "productID", user_email, review)
        VALUES ('{}', '{}', '{}');
        '''.format(ProductID, email, review))
    elif type == RIDER:
        cur.execute('''
        INSERT INTO public."RIDER_REVIEWS"(
        "riderID", user_email, review)
        VALUES ('{}', '{}', '{}');
        '''.format(riderID, email, review))
    elif type == SHOP:
        cur.execute('''
        INSERT INTO public."SHOP_REVIEWS"(
	    "shopID", user_email, review)
	    VALUES ('{}', '{}', '{}');
        '''.format(shopID, email, review))
    else:
        return None

    conn.commit()
    conn.close()


# a function to add a new rider to the database
def addRider(ID, email, type, base_salary, name, surname, phone_number, vehicle):
    conn, cur = connect()

    cur.execute('''
                INSERT INTO public."RIDER_DATA"(
    	email, name, surname, phone_number, vehicle)
    	VALUES ('{}', '{}', '{}', '{}','{}');
            '''.format(email, name, surname, phone_number, vehicle))

    cur.execute('''
        INSERT INTO public."RIDERS"(
	"ID", email, type, base_salary)
	VALUES ('{}', '{}', '{}', '{}');
    '''.format(ID, email, type, base_salary))

    conn.commit()
    conn.close()


# a function to remove a rider from the database
def removeRider(riderID):
    conn, cur = connect()

    cur.execute('''
            DELETE FROM public."RIDERS" R WHERE R."ID" = '{}';
            '''.format(riderID))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to update the salary of a rider
def updateSalary(riderID, newSalary):
    conn, cur = connect()

    cur.execute('''
                UPDATE public."RIDERS" base_salary={} WHERE R.ID = '{}';
                '''.format(newSalary, riderID))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to update the menu of a certain shop
def updateMenu(ShopID, newMenu):
    conn, cur = connect()

    cur.execute('''
            UPDATE public."SHOP" S SET "menuID"='{}' WHERE S."shopID" = '{}';
             '''.format(newMenu, ShopID))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to show all the orders on the platform ( Optionally in a certain month)
def showAllOrders():
    conn, cur = connect()

    cur.execute('''
            SELECT * FROM public."ORDER";
             ''')

    result = cur.fetchall()
    conn.close()

    return result


# a function to calculate the platform's profit
def calculateProfit():
    conn, cur = connect()

    cur.execute('''
                SELECT (SUM(O."totalPrice") -SUM(R."base_salary") ) AS Profit 
                FROM public."ORDER" O
                INNER JOIN public."ORDER_DELIVERY" D ON O."orderID" = D."orderID"
                INNER JOIN public."RIDERS" R ON R."ID" = D."riderID";
    ''')

    result = cur.fetchone()
    conn.close()

    return result


# a function to add a new shop
def addNewShop(shopID, location, name, menuID, mgr_phone, cuisine, desc=None):
    conn, cur = connect()

    if desc == ' ':
        cur.execute('''
        INSERT INTO public."SHOP"(
        "shopID", location, name, "menuID", mgr_phone)
        VALUES ('{}','{}', '{}', '{}', '{}');
        '''.format(shopID, location, name, menuID, mgr_phone))
    else:
        addNewMenu(menuID, desc)
        addNewShop(shopID, location, name, menuID, mgr_phone, cuisine, desc=' ')

    if cuisine != ' ' and cuisine:
        cur.execute('''
        INSERT INTO public."RESTURANTS"(
        "resturantID", "cuisineType")
        VALUES ('{}', '{}');'''.format(shopID, cuisine))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to add a new menu
def addNewMenu(menu, desc):
    conn, cur = connect()
    cur.execute('''
            INSERT INTO public."MENU"(
	        "menuID", description)
	        VALUES ('{}', '{}');
            '''.format(menu, desc))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to add a new product to a certain menu
def addNewProduct(productID, price, description, menuID):
    conn, cur = connect()
    cur.execute('''
            INSERT INTO public."PRODUCT"(
	        "productID", price, description, "menuID")
	        VALUES ('{}', '{}', '{}', '{}');
                '''.format(productID, price, description, menuID))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to delete the account of a user
def deleteAccount(email):
    conn, cur = connect()

    cur.execute('''
            DELETE FROM public."USER" U WHERE P."email" = '{}';
            '''.format(email))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to delete a certain product from a menu
def deleteProduct(id):
    conn, cur = connect()

    cur.execute('''
            DELETE FROM public."PRODUCT" P WHERE P."productID" = '{}';
            '''.format(id))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to update the product price in a menu
def updateProductPrice(id, newprice):
    conn, cur = connect()

    cur.execute('''
            UPDATE public."PRODUCT" P SET price={} WHERE P."productID" = '{}';
            '''.format(newprice, id))

    conn.commit()  # commit the changes to the database
    conn.close()


# a function to create another user account
def createNewUser(email, uname, surname, pwd, accountType, phone):
    conn, cur = connect()

    cur.execute('''
        INSERT INTO public."USER"(
        email, uname, surname, pwd, "accountType", phone)
        VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
    '''.format(email, uname, surname, pwd, accountType, phone))

    conn.commit()
    conn.close()


# a function to list the most popular order on the platform
def listMostPopularOrder():
    conn, cur = connect()

    cur.execute('''
                SELECT
    	O."productID",
    	description
    FROM
    	"PRODUCT_ORDER" O
    INNER JOIN "PRODUCT" P
    		 ON   P."productID" = O."productID" 
    GROUP BY O."productID" ,description
    HAVING COUNT(O."productID") = (SELECT MAX("countitems") FROM (
    								(SELECT pd."productID",COUNT(*) AS COUNTitems 
    								 FROM "PRODUCT_ORDER" pd 
    								 GROUP BY(pd."productID"))) AS ItemsOrderCount);

                ''')

    result = cur.fetchone()
    conn.commit()  # commit the changes to the database
    conn.close()

    return result


# a function to list the top 10 users of the platform
def listTop10Users():
    conn, cur = connect()
    result = []
    cur.execute('''
    SELECT U."uname" , U."surname" , SUM(O."points") AS POINTS 
    FROM public."ORDER"  O
    INNER JOIN
    public."USER" U ON U."email" = O."user_email" 
    GROUP BY U."uname" ,U."surname",O."user_email" ORDER BY POINTS DESC;
    ''')

    for i in range(10):
        result.append(cur.fetchone())

    conn.close()
    return result


# a function to upgrade an account to premium or student
def upgradeAccount(updateTo="PREMIUM", email=None, student_no=None, school_name=None):
    currentDate = date.today()
    conn, cur = connect()
    # first check if the account ID is in db
    cur.execute('''
    SELECT * FROM public."USER" WHERE email = '{}' ;
    '''.format(email))

    result = cur.fetchone()

    if result is not None and updateTo == "PREMIUM":
        cur.execute('''
        UPDATE public."USER" SET "accountType"= 'PREMIUM' WHERE email = '{}';
        '''.format(email))

        cur.execute('''
        INSERT INTO public."PREMIUM"(
	    user_email, sub_start_date, sub_end_date)
	    VALUES ('{}', '{}', '{}');
        '''.format(email, currentDate, currentDate + timedelta(days=30)))

    elif result is not None and updateTo == "STUDENT":
        cur.execute('''
                UPDATE public."USER" SET "accountType"='STUDENT' WHERE email = '{}';
                '''.format(email))

        cur.execute('''
            INSERT INTO public."STUDENT"(
	        user_email, student_no, school_name)
	        VALUES ('{}', '{}', '{}');
                '''.format(email, student_no, school_name))

    conn.commit()
    conn.close()


# A function to calculate the points of a certain account
def calculatePoints(email):
    conn, cur = connect()

    cur.execute('''
    SELECT U."uname" , U."surname" , SUM(O."points") AS POINTS 
    FROM public."ORDER"  O
    INNER JOIN
    public."USER" U ON U."email" = O."user_email" 
    WHERE U."email" = '{}'
    GROUP BY U."uname" ,U."surname",O."user_email" ORDER BY POINTS DESC;
    '''.format(email))

    conn.close()


# A function to add a new address to an account
def addNewAddress(email, address):
    conn, cur = connect()

    cur.execute('''
    INSERT INTO public."USER_ADDRESSES"(
	user_email, "Adress")
	VALUES ('{}', '{}');
    '''.format(email, address))

    conn.commit()
    conn.close()


# A function to add new cc info to an account
def addCCInfo(email, ccinfo):
    conn, cur = connect()

    cur.execute('''
    INSERT INTO public."USER_CC_INFO"(
	user_email, cc_info)
	VALUES ('{}','{}');
    '''.format(email, ccinfo))

    conn.commit()
    conn.close()


def showMenu(shopID):
    conn, cur = connect()

    cur.execute('''
    SELECT P."productID", P.price, P.description
	FROM public."PRODUCT" P
	INNER JOIN public."MENU" M ON P."menuID" = M."menuID" 
	INNER JOIN public."SHOP" S on S."menuID" = P."menuID"
	WHERE S."shopID" = '{}';

        '''.format(shopID))

    result = cur.fetchall()
    conn.commit()
    conn.close()

    return result


def getShopIdfromNameLocation(name, location):
    conn, cur = connect()

    cur.execute('''SELECT "shopID"
	FROM public."SHOP" WHERE name LIKE '%{}%' and location LIKE '%{}%' ;'''.format(name, location))

    result = cur.fetchone()
    conn.close()
    return result


def getOrdersByEmail(email):
    conn, cur = connect()

    cur.execute('''SELECT "orderID", "totalPrice", user_email, points, date, "time"
	FROM public."ORDER" WHERE user_email = '{}';'''.format(email))

    result = cur.fetchall()
    conn.close()
    return result


def getAllShopOrders(shopID):
    result = []

    conn, cur = connect()

    cur.execute('''
    SELECT O."orderID", "totalPrice", user_email, points, date, "time"
	FROM public."ORDER" O 
	INNER JOIN "ORDER_DELIVERY" OD ON O."orderID" = OD."orderID"
	WHERE OD."shopID" = '{}';'''.format(shopID))

    result.append(cur.fetchall())

    cur.execute('''
        SELECT O."orderID", "totalPrice", user_email, points, O.date, "time"
    	FROM public."ORDER" O 
    	INNER JOIN "ORDER_RESERVATION" OD ON O."orderID" = OD."orderID"
    	WHERE OD."resturantID" = '{}';'''.format(shopID))

    result.append(cur.fetchall())

    cur.execute('''
        SELECT O."orderID", "totalPrice", user_email, points, date, "time"
    	FROM public."ORDER" O 
    	INNER JOIN "ORDER_PICKUP" OD ON O."orderID" = OD."orderID";
    	''')

    result.append(cur.fetchall())

    conn.close()
    return result


if __name__ == '__main__':
    connect(printmodel=1)
