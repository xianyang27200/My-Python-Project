import mysql.connector as mc
from datetime import datetime
import string
from email_validator import validate_email, EmailNotValidError
from phonenumbers import (
    parse,
    is_valid_number,
    is_possible_number,
    format_number,
    PhoneNumberFormat,
    phonenumberutil,
)

mydb = mc.connect(
    user="sql12350647",
    host="sql12.freemysqlhosting.net",
    password="5rfZpZldba",
    database="sql12350647",
)
curs = mydb.cursor()


def manage_contact():
    print(
        "1:register new contact,2:list the contacts, 3:delete contacts, 4:update contact, 5:exit "
    )
    choic = input("your choice: ")
    choice = int(choic)
    if choice == 1:
        # declaration of variables and validatoin of them
        name = input("Please enter your name: ")
        try:
            all(c in string.ascii_letters + " " for c in name)

            # return true
        except NameError:
            raise Exception("invalid name")

        today_date = datetime.today()

        email = input("Please enter your email: ")
        try:
            # validate
            valid = validate_email(email)

            # update with the normalized form
            email = valid.email
        except EmailNotValidError:
            raise Exception("invalid email")

        phone = parse(input("Please type your phone number: "), None)
        try:
            if is_valid_number(phone) and is_possible_number(phone):
                global phone_in_formatted
                phone_in_formatted = format_number(
                    phone, PhoneNumberFormat.INTERNATIONAL
                )

        except phonenumberutil.NumberParseException:
            raise Exception("Not Valid Phone number")

        address = input("City of your locatio: ")
        try:
            all(c in string.ascii_letters + " " + "123456789" for c in address)
        except NameError:
            raise Exception("invalid address")

        sql = "INSERT INTO contact_details(Name,Phone,Address,Email,Date) VALUES (%s, %s, %s, %s, %s)"
        val = (name, phone_in_formatted, address, email, today_date)
        curs.execute(sql, val)
        mydb.commit()
        print("Inserted ", curs.rowcount, " Row. ")

    elif choice == 2:
        print("1:Alphabetic order,2:Date of of creation")
        inside_choice = int(input("Your choice: "))
        if inside_choice == 1:
            curs.execute("SELECT * FROM contact_details order by Name")
            show = curs.fetchall()
            for i in show:
                print(i)
        elif inside_choice == 2:
            curs.execute("SELECT * FROM contact_details order by Date")
            show = curs.fetchall()
            for i in show:
                print(i)
        else:
            print("Not in range(1,2)")
    elif choice == 3:
        curs.execute("SELECT Name FROM contact_details")
        curss = curs.fetchall()
        name_to_delete = input("Which name to delete: ")
        for name in curss:
            if name_to_delete in name:
                sql = "DELETE FROM contact_details WHERE Name = %s"
                val = (str(name_to_delete),)
                curs.execute(sql, val)
                mydb.commit()
                print(curs.rowcount, " affected")

    elif choice == 4:
        print("1:Update phone,2:Update name,3:Update address,4:Update email")
        inside_choice = int(input("Enter your choice: "))
        if inside_choice == 1:
            new_phone = parse(input("New Phone Number: "), None)
            try:
                if is_possible_number(new_phone) and is_valid_number(new_phone):
                    inter_format = format_number(
                        new_phone, PhoneNumberFormat.INTERNATIONAL
                    )
                    name_choosen = input("Name to refer to: ")
                    curs.execute("SELECT Name FROM contact_details")
                    curss = curs.fetchall()
                    for name in curss:
                        if name_choosen in name:
                            sql = (
                                "UPDATE contact_details SET Phone = %s where Name = %s"
                            )
                            val = (inter_format, name_choosen)
                            curs.execute(sql, val)
                            mydb.commit()
                            print(curs.rowcount, "changed")
            except phonenumberutil.NumberParseException:
                raise Exception("Invalid format")

        elif inside_choice == 2:
            new_name = input("New Name Number: ")
            try:
                if all(c in string.ascii_letters + " " for c in new_name) == True:
                    name_choosen = input("Name to refer to: ")
                    curs.execute("SELECT Name FROM contact_details")
                    curss = curs.fetchall()
                    for name in curss:
                        if name_choosen in name:
                            sql = "UPDATE contact_details SET Name = %s where Name = %s"
                            val = (new_name, name_choosen)
                            curs.execute(sql, val)
                            mydb.commit()
                            print(curs.rowcount, " changed")
            except NameError:
                raise Exception("Invalid format")

        elif inside_choice == 3:
            new_address = input("New address: ")
            try:
                if (
                    all(
                        c in string.ascii_letters + " " + "0123456789"
                        for c in new_address
                    )
                    == True
                ):
                    name_choosen = input("Name to refer to: ")
                    curs.execute("SELECT Name FROM contact_details")
                    curss = curs.fetchall()
                    for name in curss:
                        if name_choosen in name:
                            sql = "UPDATE contact_details SET Address = %s where Name = %s"
                            val = (new_address, name_choosen)
                            curs.execute(sql, val)
                            mydb.commit()
                            print(curs.rowcount, " changed")
            except NameError:
                raise Exception("Invalid format")
        elif inside_choice == 4:
            new_email = input("New email: ")
            try:
                valid = validate_email(new_email)

                new_email = valid.email
                name_choosen = input("Name to refer to: ")
                curs.execute("SELECT Name FROM contact_details")
                curss = curs.fetchall()
                for name in curss:
                    if name_choosen in name:
                        sql = "UPDATE contact_details SET Email = %s where Name = %s"
                        val = (new_email, name_choosen)
                        curs.execute(sql, val)
                        mydb.commit()
                        print(curs.rowcount, " changed")
            except EmailNotValidError:
                raise Exception("Invalid format")
        else:
            print("Not in range(1,4) or not integer")
    elif choice == 5:
        exit()
    else:
        print("not a digit or not in range(1,3)")

