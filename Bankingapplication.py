import pyodbc 
from datetime import date 
conn=pyodbc.connect(
    Trusted_Connection="Yes",
    Driver='{SQL Server Native Client 11.0}',
    Server='DESKTOP-SMB2HR8\SQLEXPRESS',
    Database='Bank'
)

#choose options

def menu():
    print('''
                    1.open new account
                    2.deposit amount
                    3.withdraw amount
                    4.balance enquiry
                    5.show customer details
                    6.close an account
                    7.money transfer
                    8.menu'''
        )


# Create a cursor object
cursor = conn.cursor()

#deposit
def  deposit():
    account_number=int(input("enter your account number "))
    #check the account number is valid for money deposit
    cursor.execute("{CALL check_the_account_id_for_deposit(?)}", (account_number))
    result = cursor.fetchone()


    if result and result[0] == 1 :
        cursor.execute("{CALL password_checking(?)}", (account_number))
        password_check=cursor.fetchone()
        password=input("enter your password ")
        if password_check and password_check[0]==password:
            deposit_amount=int(input("entrer your deposit amount "))
            #insert the deposit money  in the deposit table 
            deposit_date=date.today()

            cursor.execute("{CALL only_money_deposit(?, ?,?)}", (account_number, deposit_amount,deposit_date))

            #update the money
            cursor.execute("{CALL update_runnig_balance(?, ?)}", (account_number, deposit_amount))
            conn.commit()
        else:
            print("the password is invalid please enter valid password number ")
    else:
        print("invalid account number")

#withdraw

def  withdraw():
    account_number=int(input("enter your id "))
    cursor.execute("{CALL check_the_account_id_for_withdraw(?)}", (account_number))
    result = cursor.fetchone()
    cursor.execute("{CALL password_checking(?)}", (account_number))
    password_check=cursor.fetchone()
    password=input("enter your password ")

    if result and result[0] == 1:
        if password_check and password_check[0]==password:
            cursor.execute("{CALL check_balance(?)}", (account_number))
            checkbalance=cursor.fetchone()
            if checkbalance and checkbalance[1]>=100:

                wamount=int(input("entrer your withdraw amount "))
                if checkbalance[1]>=wamount:
                    withdraw_date=date.today()
                    cursor.execute("{CALL  withdrawmoney(?, ?,?)}", (account_number, wamount,withdraw_date))
                    cursor.execute("{CALL  update_withdrawmoney_in_runningbalance(?, ?)}", (account_number, wamount))
                    conn.commit()
                    print('amount withdraw successfully ')
                else:
                    print("Insufficient Balance")
            else:
                print('Insufficient Balance')
        else:
            print("the password is invalid please enter valid password number ")
    else:
        print("invalid account number")

#balance enquiry

def balanceEnquiry():
    id_number=int(input("enter your id "))
    cursor.execute("{CALL check_the_account_id_for_deposit(?)}", (id_number))
    result = cursor.fetchone()

    if result and result[0] == 1:
        cursor.execute("{CALL password_checking(?)}", (id_number))
        password_check=cursor.fetchone()
        password=input("enter your password ")
        if password_check and password_check[0]==password:
            cursor.execute("{CALL balance_enquiry(?)}", (id_number))
            checkbalance=cursor.fetchone()
            conn.commit()
            for i in checkbalance:
                print("Your Account Balance is ",i)
        else:
            print("the password is invalid please give the correct password ")
    else:
        print("The Account Id Is Invalid ")

        
#show customer details
def customerDetails():
        
    id_number=int(input("enter your id "))
    cursor.execute("{CALL check_the_account_id_for_deposit(?)}", (id_number))
    result = cursor.fetchone()

    if result and result[0] == 1:
        cursor.execute("{CALL password_checking(?)}", (id_number))
        password_check=cursor.fetchone()
        password=input("enter your password ")
        if password_check and password_check[0]==password:
            cursor.execute("{CALL account_details(?)}", (id_number))
            details=cursor.fetchall()
            conn.commit()
            for i in details:
                print(i)
        else:
           print("the password is invalid please give the correct password ") 
    else:
        print("The Account Id Is Invalid ")
#customerDetails()
        
#close an account
        
def deleteAccount():
        
    id_number=int(input("enter your id "))
    cursor.execute("{CALL check_the_account_id_for_deposit(?)}", (id_number))
    result = cursor.fetchone()
    #it is not working because it contains the referense key so create a one more duplicate table with same columns 
    #and new account open data insert into both tables

    if result and result[0] == 1:
        cursor.execute("{CALL password_checking(?)}", (id_number))
        password_check=cursor.fetchone()
        password=input("enter your password ")
        if password_check and password_check[0]==password:

            cursor.execute("{CALL delete_account(?)}", (id_number))
            account_closing_date=date.today()
            cursor.execute("{CALL insert_delete_details(?,?)}", (id_number,account_closing_date))

            conn.commit()
            print(" The Acoound Id  ",id_number,"is deleted")
        else:
            print("the password is invalid please give the correct password ") 
    else:
        print("The Account Id Is Invalid ")

#new account opening
        
def openNewAccount():
    name=input("enter your name: ")
    DOB=input("enter your age ")
    adress=input("enter your adress ")
    contact=input("enter your phone number ")
    password=input("set your password ")
    accountopeningdate=date.today()
    cursor.execute("{CALL account_number}")
    result=cursor.fetchone()
    new=result[0]+1
    print("your account number is ",new)
    accountnumber=int(input("enter your valid account number "))
    
    if accountnumber==new:
        print(name)
        name_check=input("enter yes or no ")
        if name_check=="NO" or name_check=="no" or name_check=="No":

            menu()
            

        elif name_check=="YES" or name_check=="yes" or name_check=="Yes":
            balance=int(input("deposit the money for account opening minimum deposit is 500"))
            password1=input("enter your password ")
            if balance>=500 and password==password1:
                cursor.execute("{CALL insert_data_into_account_opening(?,?,?,?,?,?,?,?)}", (new,name,DOB,adress,contact,balance,accountopeningdate,password))
                cursor.execute("{CALL account_opening_money_deposit(?,?,?)}", (new,balance,accountopeningdate))
                cursor.execute("{CALL running_balance(?,?)}", (new,balance))
                conn.commit()

                print("account opening successfully")
                print("")
                print("THANK YOU FOR ACCOUNT OPENING ")
    else:
        print("the account number is invalid")


def moneytransfer():
    depositer_phone_number=input("enter your phone number  ")
    money_receiver=input("enter the money receiving phone number  ")
    cursor.execute("{CALL sender_exit_or_not(?)}", (depositer_phone_number))
    sender_result=cursor.fetchone()
    cursor.execute("{CALL receiver_exit_or_not(?)}", (money_receiver))
    reseiver_result=cursor.fetchone()
    conn.commit()
    if sender_result and sender_result[0]==1:
        if reseiver_result and reseiver_result[0]==1:
            #money_transfer=int(input("enter how much money transfer "))
            cursor.execute("{CALL find_accountnumber_by_using_the_sender_phone_number(?)}", (depositer_phone_number))
            d_result=cursor.fetchone()
            d_result_accountnumber=d_result[0]
            send_money=int(input("enter the amount "))
            cursor.execute("{CALL check_money_transfer(?)}",(d_result_accountnumber))
            amount=cursor.fetchone()
            check_amount=amount[0]
            money_transfer_date=date.today()
            if check_amount>1:
                if check_amount>=send_money:
                    #insert the sender details data into withdraw table 
                    cursor.execute("{CALL insert_data_inwithdarw_for_amount_transfer_method(?,?,?)}",(d_result_accountnumber,send_money,money_transfer_date))
                    cursor.execute("{CALL  update_withdrawmoney_in_runningbalance(?, ?)}", (d_result_accountnumber, send_money))
                    cursor.execute("{CALL find_accountnumber_by_using_the_receiver_phone_number(?)}", (money_receiver))
                    r_result=cursor.fetchone()
                    r_result_accountnumber=r_result[0]
                    cursor.execute("{CALL insert_data_indeposit_for_amount_transfer_method(?,?,?)}",(r_result_accountnumber,send_money,money_transfer_date))
                    cursor.execute("{CALL update_runnig_balance(?, ?)}", (r_result_accountnumber, send_money))
                    conn.commit()
                else:
                    print("insufficient balance ")
            else:
                print("insufficient balance ")
        else:
            print(" do not the accept the money for this number ",money_receiver)
    else:
        print(" do not the accept the money transfer  for this number ",depositer_phone_number)


def password():
    contactNumber=input("enter your phone number +91  ")

    cursor.execute("{CALL contact_number_verification_for_password_conformation(?)}",(contactNumber))
    contact=cursor.fetchone()
    if contact and contact[0]==1:


        password_check=input("enter your password ")
        cursor.execute("{ CALL  password_conformation (?)}",(contactNumber))
        result=cursor.fetchone()

        if result and result[0]==password_check:
            menu()
            perform=int(input("select  your option "))

            if perform ==1:
                openNewAccount()
            elif perform ==2:
                deposit()
            elif perform==3:
                withdraw()
            elif perform==4:
                balanceEnquiry()
            elif perform==5:
                customerDetails()
            elif perform==6:
                deleteAccount()
            elif perform==7:
                moneytransfer()
            elif perform==8:
                menu()
        else:
            print("invalid password ")
            forgat_password=input(" you want  change your  password  yes or no ")
            if forgat_password=="yes" or forgat_password=="YES" or forgat_password=="Yes":
                newpassword=input(" set your new password  ")
                cursor.execute("{CALL forgat_and_update_password(?,?)}",(contactNumber,newpassword))
                conn.commit()
                print("New  Password Set Sucessfully ")
            
    else:
        print("invalid contact number")
        menu()
        perform=int(input("select  your option "))

        if perform ==1:
            openNewAccount()
        elif perform ==2:
            deposit()
        elif perform==3:
            withdraw()
        elif perform==4:
            balanceEnquiry()
        elif perform==5:
            customerDetails()
        elif perform==6:
            deleteAccount()
        elif perform==7:
            moneytransfer()
        elif perform==8:
            menu()

password()


   


    











        








