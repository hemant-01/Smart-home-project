# latest

#Libraries
import getpass
import tkinter as tk
import tkinter.messagebox as tkmbox
import sqlite3
import random
from functools import partial
import requests
import os

#global variables

# dictionary used to store user credentials in the form:< user_name, password >
users_credentials_db = {}
iot_devices_db = {}

# used for controlling login attempts
verf_count = 0
verf_count_max = 5

secret_key = 112233

###########################################################################################################################


# function that reads user credential SQL database "credentials.db" and writes values to local database "users_credentials_db"
# and prints the user data that is currently present in the database

def update_credentials_db():
    credential_cursor.execute('SELECT * FROM sql_users_credentials_db')
    data = credential_cursor.fetchall()

    print("\n The User Credentials database Entries : ")

    for (val1,val2) in data:
        users_credentials_db[val1] = val2
        print("------------------------")
        print("User Name is : ",val1)
        if( val1 == "root"):
            print("Password is : ", val2)
        else :
            print("Password is ****")
        print("------------------------\n")



# Initial setup of SQL server which is used to store username and passwords 
credential_connect = sqlite3.connect('credentials.sqlite')
credential_cursor = credential_connect.cursor()

# code to create and connect to credentials database
# The below 2 commented commands must be executed only once as re-initialising the database throws error. Please comment after
# initialising the database

#credential_cursor.execute('CREATE TABLE sql_users_credentials_db (username VARCHAR, password VARCHAR)')
#credential_cursor.execute('INSERT INTO sql_users_credentials_db (username, password) values ("root", "root123")')
credential_connect.commit()
update_credentials_db()


###########################################################################################################################

#code to control user login. Rest of the code is self-readable


username = input("Enter Your Username : ")
userfound = 0

for user in users_credentials_db.keys():
    if (username == user):
        userfound = 1
        password = getpass.getpass("Enter Your Password : ")
        while (password != users_credentials_db.get(user)):
            verf_count = verf_count + 1

            if ( verf_count == verf_count_max):
                print("You have run out of login attempts. Notifying root user.")
                # We have attached the script "sender.py" that can be used to send the email to the configured recepient
                # We have not initialised that script here as it requires authentication to send a mail, which in practical
                # scenarios would be implemented in some secure manner. We just print error message and exit.
                exit(0)

            print("You have %d tries left" % (verf_count_max - verf_count))
            password = getpass.getpass("Enter Your Password Again : ")
        
        break


if( userfound ):
    print("User Verified : " + username)
else :
    print("Invalid username entered! Exiting...")
    exit(0)





################################################################################################################################



# function used to update newly added user to both local dictionary and credential SQL server
def submit():
    print("Adding new user >>> ")
    name=name_var.get()
    passw=passw_var.get()
    print("New user name is : " + name)
    credential_cursor.execute('INSERT INTO sql_users_credentials_db (username, password) values (?,?)',(name,passw))
    credential_connect.commit()
    update_credentials_db()
    print("\n")


# function used to update removed user to both local dictionary and credential SQL server
def delete():
    
    print("Deleting user >>>")
    userfound = 0
    del_name = name_var_1.get()
    
    for u1 in users_credentials_db.keys():
        if( u1 == del_name ):
            userfound = 1
    
    if( userfound ):
        print("User deleted: " + del_name)
        del users_credentials_db[del_name]
    else:
        print("Invalid username")
        exit(0)

    credential_cursor.execute("""DELETE FROM sql_users_credentials_db where username=?""",(del_name,))
    credential_connect.commit()
    update_credentials_db()
    print("\n")


# function used to add new user. 
def add_new_user() :

    name_label = tk.Label( text = 'Username', font=('calibre',10, 'bold'))
    name_entry = tk.Entry( textvariable = name_var, font=('calibre',10,'normal'))
    passw_label = tk.Label( text = 'Password', font = ('calibre',10,'bold'))
    passw_entry = tk.Entry( textvariable = passw_var, font = ('calibre',10,'normal'), show = '*')
    sub_btn = tk.Button( text = 'Submit',command = submit)

    name_label.pack()
    name_entry.pack()
    passw_label.pack()
    passw_entry.pack()
    sub_btn.pack()


# function used to remove user
def del_user() :
    name_label_1 = tk.Label( text = 'Username', font=('calibre',10, 'bold'))
    name_entry_1 = tk.Entry( textvariable = name_var_1, font=('calibre',10,'normal'))

    del_btn = tk.Button( text='Delete', command = delete )

    name_label_1.pack()
    name_entry_1.pack()
    del_btn.pack()



# main function used to manage users. 2 functions are supported currently. Adding a new user and removing registered user
def user_management() : 

    local_button1 = tk.Button(root, text="Add New User",height="1",width="25",command=add_new_user)
    local_button1.pack()

    local_button2 = tk.Button(root, text="Delete Registered User",height="1",width="25",command=del_user)
    local_button2.pack()



################################################################################################################################


# function that reads IOT device SQL database "all_devices_db" and writes values to local database "iot_devices_db"
# and prints the devices and their status that are currently present in the database

def update_iot_devices_db():

    devicedb_cursor.execute('SELECT * FROM iot_device_db')
    data = devicedb_cursor.fetchall()

    print("Device Database current entries:: ")

    for (val1,val2,val3,val4,val5) in data:
        iot_devices_db[val1] = [val2,val3,val4,val5]
        print("----------------")
        
        print("Device Name    : %s"%(val1))
        print("Device Type    : %s"%(val2))
        print("Device ID      : %d"%(val3))
        print("Device State   : %d"%(val4))
        print("Device Value   : %f"%(val5))
        
        print("----------------")

    print("\n")




# Creating a database to store device parameters
devicedb_connect = sqlite3.connect('all_devices_db.sqlite')
devicedb_cursor = devicedb_connect.cursor()
#devicedb_cursor.execute('CREATE TABLE iot_device_db (name VARCHAR, type VARCHAR, device_ID INT, state INT, effect_value REAL)')
#devicedb_cursor.execute('INSERT INTO iot_device_db (name, type, device_ID, state, effect_value) values ("dining_bulb", "BULB", 10, 0, 0)')
#devicedb_cursor.execute('CREATE UNIQUE INDEX dnames on iot_device_db(name)')




# function to add the gathered new device data to the SQL server
def general_device_submit( type1, device_ID1 ):

    name1 = general_name_var.get()
    state1 = int(general_state_var.get())

    if( state1 == 1):
        effect_value1 = int(general_eff_var.get())
    else:
        effect_value1 = 0
    
    devicedb_cursor.execute('INSERT INTO iot_device_db (name, type, device_ID, state, effect_value) values (?,?,?,?,?)',\
                (name1, type1, device_ID1, state1, effect_value1))
    devicedb_connect.commit()

    print("Device Suucessfully Added \n")
    update_iot_devices_db()



# function to get device data from the GUI provided
def general_add(general_type):

    general_device_ID = random.randint(0,1000)
    print("Adding new %s"%(general_type),"\n")

    if(general_type == "BULB"):
        general_device_type = "BULB"
    elif( general_type == "FAN"):
        general_device_type = "FAN"
    elif( general_type == "AC"):
        general_device_type = "AC"
    elif( general_type == "TV"):
        general_device_type = "TV"
    else:
        print("Invalid device Type value passed. Exiting!")
        exit(0)

    general_name_label = tk.Label( text = 'Device Name', font=('calibre',10, 'bold'))
    general_name_entry = tk.Entry( textvariable = general_name_var, font=('calibre',10,'normal'))

    general_state_label = tk.Label( text = 'State Value', font=('calibre',10, 'bold'))
    general_state_entry = tk.Entry( textvariable = general_state_var, font=('calibre',10,'normal'))

    general_name_label_1 = tk.Label( text = 'Device Intensity value', font=('calibre',10, 'bold'))
    general_eff_entry = tk.Entry( textvariable = general_eff_var, font=('calibre',10,'normal') )
    
    sub_btn = tk.Button( text = 'Submit',command = partial(general_device_submit, general_device_type, general_device_ID))

    general_name_label.pack()
    general_name_entry.pack()
    general_state_label.pack()
    general_state_entry.pack()
    general_name_label_1.pack()
    general_eff_entry.pack()

    sub_btn.pack()




# function to provide user the options of the devices available that the user can select via GUI
def add_device():
        
    bulb_button = tk.Button( text="Bulb",height="1",width="25",command=partial(general_add,"BULB"))
    bulb_button.pack()

    fan_button = tk.Button( text="Fan",height="1",width="25",command=partial(general_add,"FAN"))
    fan_button.pack()

    AC_button = tk.Button( text="AC",height="1",width="25",command=partial(general_add,"AC"))
    AC_button.pack()

    TV_button = tk.Button( text="TV",height="1",width="25",command=partial(general_add,"TV"))
    TV_button.pack()

    slashn = tk.Label(root, text="%s%s"%("\n","\n"), height="2", width="20")
    slashn.pack()




# function used to update removed device to both local database and SQL device database
def delete_dev():
    
    devicefound = 0
    del_name = name_var_2.get()

    devicedb_cursor.execute('SELECT * FROM iot_device_db')
    data = devicedb_cursor.fetchall()

    for (a,b,c,d,e) in data:
        if( a == del_name ):
            devicefound = 1
    
    if( devicefound ):
        del iot_devices_db[del_name]
        print("Device deleted: " + del_name)
    else:
        print("Invalid Device name")
        exit(0)

    devicedb_cursor.execute("""DELETE FROM iot_device_db where name=?""",(del_name,))
    devicedb_connect.commit()
    
    update_iot_devices_db()
    slashn = tk.Label(root, text="%s%s"%("\n","\n"), height="2", width="20")
    slashn.pack()




# function used to remove device after gathering device name to be deleted from GUI
def delete_device():

    print("Deleting Device >>> \n")
    name_label_1 = tk.Label( text = 'Device Name', font=('calibre',10, 'bold'))
    name_entry_1 = tk.Entry( textvariable = name_var_2, font=('calibre',10,'normal'))

    del_btn = tk.Button( text='Delete Device', command = delete_dev )

    name_label_1.pack()
    name_entry_1.pack()
    del_btn.pack()




def dev_ON(name,type1,device_ID,state,effect_value):

    lambda_input={"device":type1,"id":device_ID,"action":1,"curr_state":effect_value,"send_secret":secret_key}
    r = requests.get('https://6u15wdv8ok.execute-api.us-east-2.amazonaws.com/samsung_project', params=lambda_input)
    lambda_output=r.json()

    print("ONN")
    print("L_INPUT  :: ",lambda_input)
    print("L_OUTPUT :: ",lambda_output)

    result = lambda_output["result_status"]
    
    if(result == 1):
        devicedb_cursor.execute('REPLACE INTO iot_device_db (name,type,device_ID,state,effect_value) values (?,?,?,?,?)',\
                    ( name, type1, device_ID, 1, lambda_output["result_state"]))
        devicedb_connect.commit()
        update_iot_devices_db()



def dev_OFF(name,type1,device_ID,state,effect_value):

    lambda_input={"device":type1,"id":device_ID,"action":0,"curr_state":effect_value,"send_secret":secret_key}
    r = requests.get('https://6u15wdv8ok.execute-api.us-east-2.amazonaws.com/samsung_project', params=lambda_input)
    lambda_output=r.json()

    print("OFFF")
    print("L_INPUT  :: ",lambda_input)
    print("L_OUTPUT :: ",lambda_output)

    result = lambda_output["result_status"]

    if(result):
        devicedb_cursor.execute('REPLACE INTO iot_device_db (name,type,device_ID,state,effect_value) values (?,?,?,?,?)',\
                    ( name, type1, device_ID, 0, lambda_output["result_state"]))
        devicedb_connect.commit()
        update_iot_devices_db()



def dev_increase(name,type1,device_ID,state,effect_value):

    lambda_input={"device":type1,"id":device_ID,"action":2,"curr_state":effect_value,"send_secret":secret_key}
    r = requests.get('https://6u15wdv8ok.execute-api.us-east-2.amazonaws.com/samsung_project', params=lambda_input)
    lambda_output=r.json()

    print("INCR")
    print("L_INPUT  :: ",lambda_input)
    print("L_OUTPUT :: ",lambda_output)

    result = lambda_output["result_status"]

    if(result):
        devicedb_cursor.execute('REPLACE INTO iot_device_db (name,type,device_ID,state,effect_value) values (?,?,?,?,?)',\
                    ( name, type1, device_ID, 1, lambda_output["result_state"] ))
        devicedb_connect.commit()
        update_iot_devices_db()



def dev_decrease(name,type1,device_ID,state,effect_value):

    lambda_input={"device":type1,"id":device_ID,"action":3,"curr_state":effect_value,"send_secret":secret_key}

    print("INput :" , lambda_input)
    r = requests.get('https://6u15wdv8ok.execute-api.us-east-2.amazonaws.com/samsung_project', params=lambda_input)
    lambda_output=r.json()

    print("DECRRR")
    print("L_INPUT  :: ",lambda_input)
    print("L_OUTPUT :: ",lambda_output)

    result = lambda_output["result_status"]

    if(result):
        devicedb_cursor.execute('REPLACE INTO iot_device_db (name,type,device_ID,state,effect_value) values (?,?,?,?,?)',\
                    ( name, type1, device_ID, 1, lambda_output["result_state"] ))
        devicedb_connect.commit()
        update_iot_devices_db()



def operate_device():

    devicedb_cursor.execute('SELECT * FROM iot_device_db')
    data = devicedb_cursor.fetchall()

    for (name,type1,device_ID,state,effect_value) in data:

        devicedb_cursor.execute('SELECT * FROM iot_device_db')
        data = devicedb_cursor.fetchall()

        iot_devices_db[name]=[type1,device_ID,state,effect_value]
        dev_name_label = tk.Label( text = '%s'%(name), font=('calibre',10, 'bold'))
        dev_name_label.pack()
        
        dev_on_button = tk.Button( text='Turn ON',command=partial(dev_ON,name,type1,device_ID,state,effect_value))
        dev_on_button.pack()

        dev_off_button = tk.Button( text='Turn OFF',command=partial(dev_OFF,name,type1,device_ID,state,effect_value))
        dev_off_button.pack()

        dev_increase_button = tk.Button( text='Increase Effect', command=partial(dev_increase,name,type1,device_ID,state,effect_value))
        dev_increase_button.pack()

        dev_decrease_button = tk.Button( text='Decrease Effect', command=partial(dev_decrease,name,type1,device_ID,state,effect_value))
        dev_decrease_button.pack()





# main function to manage IOT devices, currently we can add,delete and operate on already added device
def iot_device_management() :

    local_button1 = tk.Button(root, text="Add New Device",height="1",width="25", command=add_device)
    local_button1.pack()

    local_button3 = tk.Button(root, text="Delete device",height="1",width="24", command=delete_device)
    local_button3.pack()

    local_button4 = tk.Button(root, text="Operate on device",height="1",width="25", command=operate_device)
    local_button4.pack()

    slashn = tk.Label(root, text="%s%s"%("\n","\n"), height="2", width="20")
    slashn.pack()

    

################################################################################################################################

# main window configuration
root = tk.Tk()
root.geometry("800x600")

# button input variables
name_var=tk.StringVar()
name_var_1=tk.StringVar()
name_var_2=tk.StringVar()
passw_var=tk.StringVar()
general_name_var=tk.StringVar()
general_eff_var=tk.StringVar()
general_state_var=tk.StringVar()
bulb_name_var=tk.StringVar()
bulb_state_var=tk.StringVar()
bulb_brightness_var=tk.StringVar()
bulb_ID_var=tk.StringVar()


# main window display variables
main_console = tk.Label(root, text="Welcome", foreground="white", background="blue", height="1", width="20")
main_console.pack()

umbutton = tk.Button(root, text="User Management Console",height="1",width="25", command= user_management)
umbutton.pack()

iotbutton = tk.Button(root, text="Device Management Console",height="1",width="25",command= iot_device_management)
iotbutton.pack()

slashn = tk.Label(root, text="%s%s"%("\n","\n"), height="1", width="20")
slashn.pack()


root.mainloop()


################################################################################################################################





