import mysql.connector as Myconn
from mysql.connector import Error

try:
    
    conn = Myconn.connect(host='localhost',user='root',password='Fardin@2121',auth_plugin='mysql_native_password',database='user')
    
    cursor = conn.cursor()
    
    def atm_menu():
        print("\n----Atm Menu----")
        print("Press 1 for Check Balance")
        print("Press 2 for Withdraw Money")
        print("Press 3 for Deposit Money")
        print("Press 4 for Change Password")
        print("Press 5 for Exit")
        choice = int(input("Enter your choice : ")) 
        return choice
    
    def checkBalance(acNumber):
        cursor.execute('select Balance from users where Cno = %s', (acNumber,))
        result = cursor.fetchone()
        return result

    def updateBalance(balance,acNumber):
        cursor.execute('update users set Balance = %s where Cno = %s', (balance, acNumber))
        conn.commit()

    def updatePassword(password,acNumber):    
        cursor.execute('update users set Password = %s where Cno = %s', (password, acNumber))
        conn.commit()


    acNumber = int(input("Enter your atm card number : "))
    password = int(input("Enter your atm card password : "))

    query = 'select Cno,Password from users where Cno=%s and Password=%s'
    data = (acNumber,password)
    cursor.execute(query,data)
    
    results = cursor.fetchone()
     
    if results:
        
        print("Login Successful...\n")

        while True:

            choice = atm_menu() 

            if choice == 1:
                result = checkBalance(acNumber) 
                if result:
                    print(f"Your current balance is ₹{result[0]:.2f}")
                else:
                    print("Unable to fetch balance.")
            elif choice == 2:
                result = checkBalance(acNumber) 
                if result:
                    balance = result[0]
                    amount = int(input("Enter amount to withdraw: ₹"))
                    if  amount <= balance:
                        balance -= amount
                        updateBalance(balance,acNumber)
                        print(f"₹{amount:.2f} withdrawn successfully.")
                    else:
                        print("Insufficient balance or invalid amount.")
                else:
                    print("Account not found.")
            elif choice == 3:
                result = checkBalance(acNumber) 
                if result:
                    balance = result[0]
                    amount = int(input("Enter amount to deposit: ₹"))
                    if amount > 0:
                        balance += amount
                        updateBalance(balance,acNumber)
                        print(f"₹{amount:.2f} deposited successfully.")
                    else:
                        print("Invalid deposit amount.")
                else:
                    print("Account not found.")
            elif choice == 4:
                new_pin = input("Enter new 4-digit PIN: ")
                if len(new_pin) == 4 and new_pin.isdigit():
                    updatePassword(new_pin,acNumber)
                    print("PIN changed successfully.")
                else:
                    print("Invalid PIN format. Must be 4 digits.")
            elif choice == 5:
                print("Thank you for using the ATM.")
                break
            else:
                print("Invalid option. Please try again.")
    else:
        print("Invalid ATM card number or password.")           

except Error as e:
    print(f"Error: {e}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("Connection closed")
