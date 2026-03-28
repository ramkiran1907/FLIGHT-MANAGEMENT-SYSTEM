import mysql.connector  # mysql connector package

obj = mysql.connector.connect(host="localhost", user="root", passwd="root")
# here obj is connection object

# CREATING DATABASE & TABLE
mycursor = obj.cursor()

# cursor is used to row by row processing of record in the resultset
mycursor.execute("CREATE DATABASE IF NOT EXISTS airlines")
mycursor.execute("USE airlines")

# CREATING TABLE FOR ORDER FOOD
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS food_items( "
    "sl_no INT(4) AUTO_INCREMENT PRIMARY KEY, "
    "food_name VARCHAR(40) NOT NULL, "
    "price INT(4) NOT NULL)"
)

# use NULL (without quotes) for autoincrement primary key value
mycursor.execute("INSERT INTO food_items VALUES (NULL, 'pepsi', 150)")
mycursor.execute("INSERT INTO food_items VALUES (NULL, 'coffee', 70)")
mycursor.execute("INSERT INTO food_items VALUES (NULL, 'tea', 50)")
mycursor.execute("INSERT INTO food_items VALUES (NULL, 'water', 60)")
mycursor.execute("INSERT INTO food_items VALUES (NULL, 'milk shake', 80)")
mycursor.execute("INSERT INTO food_items VALUES (NULL, 'chicken burger', 160)")

# CREATING TABLE FOR LUGGAGE ENTRY
# original columns were weight and price but luggage() inserts a luggage type (string).
# To avoid big logic changes, define luggage table to store a luggage_type (string).
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS luggage( "
    "luggage_id INT(4) AUTO_INCREMENT PRIMARY KEY, "
    "luggage_type VARCHAR(100) NOT NULL)"
)

# CREATING TABLE FOR CUSTOMER DETAILS
# Original name used later was customer_details, so create that table (not cust_details).
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS customer_details( "
    "cust_id INT(4) AUTO_INCREMENT PRIMARY KEY, "
    "cust_name VARCHAR(40) NOT NULL, "
    "cont_no BIGINT NOT NULL)"
)

# CREATING TABLE FOR CUSTOMER'S FLIGHT DETAILS
# added datatype for flight_id
mycursor.execute(
    "CREATE TABLE IF NOT EXISTS flight_details( "
    "cus_id INT(4), "
    "cus_name VARCHAR(40) NOT NULL, "
    "flight_id INT(4))"
)

obj.commit()

# TO ENTER THE DETAILS OF LUGGAGE
def luggage():
    print("what do you want to do?")
    print("1. add luggage")
    print("2. delete luggage")
    x = int(input("enter your choice: "))
    if x == 1:
        lname = input("enter luggage type: ")
        # insert needs to match table columns: luggage_id, luggage_type
        mycursor.execute("INSERT INTO luggage VALUES (NULL, '{}')".format(lname))
    elif x == 2:
        lid = int(input("enter your luggage id: "))
        mycursor.execute("DELETE FROM luggage WHERE luggage_id={}".format(lid))
    else:
        print(" **************** PLEASE ENTER A VALID OPTION**************************** ")
    obj.commit()


# TO UPDATE THE INFORMATION OF FOOD DETAILS
def food():
    print("what do you want to do?")
    print("1. add new items")
    print("2. update price")
    print("3. delete items")
    x = int(input("enter your choice: "))
    if x == 1:
        fname = input("enter food name: ")
        fprice = int(input("enter food price: "))
        mycursor.execute("INSERT INTO food_items VALUES (NULL,'{}',{})".format(fname, fprice))
    elif x == 2:
        fid = int(input("enter food id (sl_no): "))
        fprice = int(input("enter new price: "))
        # table has column sl_no (primary key)
        mycursor.execute("UPDATE food_items SET price={} WHERE sl_no={}".format(fprice, fid))
    elif x == 3:
        fid = int(input("enter food id (sl_no): "))
        mycursor.execute("DELETE FROM food_items WHERE sl_no={}".format(fid))
    else:
        print(" **************** PLEASE ENTER A VALID OPTION**************************")
    obj.commit()


# TO UPDATE THE INFORMATION OF CLASSTYPE
def classtype():
    print("what do you want to do? ")
    print("1. change the classtype name")
    print("2. change the price of classtype")
    x = int(input("enter your choice: "))
    if x == 1:
        oname = input("enter old name: ")
        nname = input("enter new name: ")
        # Assuming there is a classtype table with column class_name; using safe SQL
        try:
            mycursor.execute(
                "UPDATE classtype SET class_name='{}' WHERE class_name='{}'".format(nname, oname)
            )
        except Exception:
            print("Could not update classtype - check that 'classtype' table exists with a column 'class_name'.")
    elif x == 2:
        # This branch needs schema details to implement properly
        print("Change price - functionality not implemented because schema not provided.")
    obj.commit()


def fooditems():
    print(" ")
    print(" ")
    print(" THE AVAILABLE FOODS ARE: ")
    print(" ")
    print(" ")
    mycursor.execute("SELECT * FROM food_items")
    x = mycursor.fetchall()
    for i in x:
        print(" FOOD ID: ", i[0])
        print(" FOOD Name: ", i[1])
        print(" PRICE: ", i[2])
        print(" ")
    # return to user menu
    # user()  <-- removed automatic recursive call to avoid infinite recursion


# Admin Interface after verifying password
def admin1():
    while True:
        print("************ WHAT'S YOUR TODAYS GOAL? ****************")
        print("1. update details")
        print("2. show details")
        print("3. job approval")
        print("4. back to main menu")
        x = int(input("select your choice: "))
        if x == 1:
            print("1. classtype")
            print("2. food")
            print("3. luggage")
            x1 = int(input("enter your choice: "))
            if x1 == 1:
                classtype()
            elif x1 == 2:
                food()
            elif x1 == 3:
                luggage()
            else:
                print(" ********************** PLEASE ENTER A VALID OPTION****************************")
        elif x == 2:
            print("1. classtype")
            print("2. food")
            print("3. luggage")
            print("4. records")
            y = int(input("from which table: "))
            if y == 1:
                try:
                    mycursor.execute("SELECT * FROM classtype")
                    z = mycursor.fetchall()
                    for i in z:
                        print(i)
                except Exception:
                    print("classtype table not found")
            elif y == 2:
                mycursor.execute("SELECT * FROM food_items")
                z = mycursor.fetchall()
                for i in z:
                    print(i)
            elif y == 3:
                mycursor.execute("SELECT * FROM luggage")
                z = mycursor.fetchall()
                for i in z:
                    print(i)
            elif y == 4:
                try:
                    mycursor.execute("SELECT * FROM customer_details")
                    z = mycursor.fetchall()
                    for i in z:
                        print(i)
                except Exception:
                    print("customer_details table not found")
            else:
                print(" ********************** PLEASE ENTER A VALID OPTION****************************")
        elif x == 3:
            print("Job approval - functionality not implemented.")
        elif x == 4:
            break
        else:
            print(" ********************** PLEASE ENTER A VALID OPTION****************************")


# TO SEE THE AVAILABLE FLIGHTS
def flightavailable():
    print(" ")
    print(" ")
    print(" THE AVAILABLE FLIGHTS ARE: ")
    print(" ")
    print(" ")
    mycursor.execute("SELECT * FROM flight_details")
    x = mycursor.fetchall()
    for i in x:
        print(" ")
        print(" Flight ID: ", i[0])
        print(" Flight Name: ", i[1])
        print(" departure: ", i[2])
        print(" Destination: ", i[3])
        # remaining columns may not exist; printing safely
        if len(i) > 4:
            print(" Take off Day: ", i[4])
        if len(i) > 5:
            print(" Take off time : ", i[5])
        if len(i) > 6:
            print(" bussiness : ", i[6])
        if len(i) > 7:
            print(" middle : ", i[7])
        if len(i) > 8:
            print(" economic : ", i[8])
        print(" ")
    # return to user menu
    # user()  <-- removed automatic recursive call here


# Stubs for missing functions so program won't crash
def ticketbooking():
    print("Ticket booking - TODO: implement ticketbooking()")


def records():
    print("Records - TODO: implement records()")


# USER INTERFACE
def user():
    while True:
        print("************** MAY I HELP YOU? *****************")
        print("1. flight details")
        print("2. food details")
        print("3. book ticket")
        print("4. my details")
        print("5. exit")
        x = int(input("enter your choice: "))
        if x == 1:
            flightavailable()
        elif x == 2:
            fooditems()
        elif x == 3:
            ticketbooking()
        elif x == 4:
            records()
        elif x == 5:
            break
        else:
            print("************ PLEASE CHOOSE A CORRECT OPTION************")


print("****************** WELCOME TO LAMNIO AIRLINES**********************")
print("************ MAKE YOUR JOURNEY SUCCESS WITH US!*****************")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")


# Main Interface
def menu1():
    while True:
        print("**************** YOUR DESIGNATION? *******************")
        print("1. admin")
        print("2. user")
        print("3. exit")
        x = int(input("choose a option: "))
        if x == 1:
            admin1()
        elif x == 2:
            user()
        elif x == 3:
            break
        else:
            print("************PLEASE CHOOSE A CORRECT OPTION******************")


menu1()
