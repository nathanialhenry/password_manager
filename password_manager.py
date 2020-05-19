# TODO create replace functionality for already created services, date/time of when password was accessed, more robust account creation, GUI?
import sqlite3, hashlib, base64, os, sys, random

# referenced below, is first function called
def startup():
    # checks for db
    if os.path.isfile('password_manager.db'):
        conn = sqlite3.connect('password_manager.db')
        input_password = input("Password database exists. What is your password?:\n")
        admin_password = get_password(input_password,service='asdflkanvoie124lakvn')

        while input_password != admin_password:
            input_password = input("Incorrect password was entered. \nPlease enter Password: \n")
            admin_password = get_password(input_password,service='asdflkanvoie124lakvn')
    # this is only ran if it is the first time the program is run on the machine or the db doesn't exist
    else:
        conn = sqlite3.connect('password_manager.db')
        c = conn.cursor()
        # creates table of two columns, key(specific to service requested) and password
        c.execute('''CREATE TABLE passwordmanager
            (key TEXT PRIMARY KEY NOT NULL, password); ''')
        admin_password = input("A Password database does not exist yet. Create a password for a new database.\nEnter New Admin Password:")
        while True:
            if len(admin_password) >= 8:
                storeadmin(admin_password,service='asdflkanvoie124lakvn')
                input_password = admin_password
                return
            else:
                admin_password = input("Password must be at least 8 characters in length \nEnter New Admin Password:")

def storeadmin(admin_password,service='asdflkanvoie124lakvn'):
    print("\nAdmin Password is set as:{}".format(admin_password))
    secret = get_hex_key(admin_password, service)
    # encrypts password with base64 encryption
    bytes_password = admin_password.encode('utf-8')
    existing_pass = base64.b64encode(bytes_password)
    conn = sqlite3.connect('password_manager.db')
    # inserts key and password for admin into table
    conn.execute('INSERT OR IGNORE INTO passwordmanager (key,password) VALUES (\"{0}\", \"{1}\");'.format(secret,existing_pass))
    conn.commit()

def create_generated_password(service, admin_password):
    # creates a 12 character password (11 generated from password and service, and one special character tacked on), then encrypts password with b64
    gen_hash_pass = hashlib.sha256(admin_password.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()[:11]
    ran_char = ['!','@','$','%','&']
    gen_pass = gen_hash_pass + random.choice(ran_char)
    bytes_password = gen_pass.encode('utf-8')
    enc_gen_pass = base64.b64encode(bytes_password)
    return enc_gen_pass

def get_hex_key(admin_password, service):
    # creates a key for the table using password and service
    return hashlib.sha256(admin_password.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()

def get_password(admin_password, service):
    conn = sqlite3.connect('password_manager.db')
    secret = get_hex_key(admin_password, service)
    # selects corresponding password in the row with the key (secret variable)
    cursor = conn.execute("SELECT (password) FROM passwordmanager WHERE key= \"{0}\"".format(secret)) 
    # the encrypted password is stored in the encr_pass variable
    encr_pass = ''
    for i in cursor:
        encr_pass = i[0]
    if encr_pass == "":
        return "There is no service or password by that name in DB"
    else:
        # removes first two and last characters from encrypted password and then decodes it
        encr_pass_strip = encr_pass[2:-1]
        user_pass_bytes = base64.b64decode(encr_pass_strip)
        user_password = user_pass_bytes.decode('utf-8')
        return user_password

def add_generated_password(service, admin_password):
    secret = get_hex_key(admin_password, service)
    conn.execute('INSERT OR IGNORE INTO passwordmanager (key,password) VALUES (\"{0}\", \"{1}\");'.format(secret,create_generated_password(service,admin_password)))
    conn.commit()
    return create_generated_password(service, admin_password)

def add_existing_password(service, admin_password, user_password):
    secret = get_hex_key(admin_password, service)
    bytes_password = user_password.encode('utf-8')
    existing_pass = base64.b64encode(bytes_password)
    conn.execute('INSERT OR IGNORE INTO passwordmanager (key,password) VALUES (\"{0}\", \"{1}\");'.format(secret,existing_pass))
    conn.commit()
    return user_password

# Script starts here
input_password = ''
admin_password = ''
startup()
if input_password != None and input_password == admin_password:
    conn = sqlite3.connect('password_manager.db')

    while True:
        print('='*30)
        print('enter \"store\" to store a password')
        print('enter \"get\" to get a password')
        print('enter \"help\" for help')
        print('enter \"quit\" to quit')
        print('='*30)
        input_ = input(':')

        if input_ == 'store':
            service = input ('For what service would you like to store the password? \n')
            does_password_exist = input('Does a password already exist for {0}? \nEnter yes or no:'.format(service.capitalize()))
            
            if does_password_exist.lower() == 'yes':
                user_password = input('Please enter password for {0}:\n'.format(service.capitalize()))
                add_existing_password(service, admin_password, user_password)
                print("\n {0} password has been added for {1}".format(user_password ,service.capitalize()))

            elif does_password_exist.lower() == 'no':
                add_generated_password(service, admin_password)
                print("\n {0} password has been created: {1}".format(service.capitalize(), get_password(admin_password, service)))
                
            else:
                does_password_exist = print('please re enter commands and state yes or no for whether or not you already have a password:')

        if input_ == 'get':
            service = input("\nFor what service would you like to get the password from? \n")
            print("{0} Password: {1}".format(service.capitalize(), get_password(admin_password, service)))
        
        if input_ == 'help':
            print('Password Manager allows you to store passwords safely on an encrypted db stored locally on your pc. Select store to enter a\n'
            +'service (i.e. Netflix, Amazon,etc.) and select whether or not you already have a password for that service. If you don\'t, fret not\n'
            +'for a password will be generated for you. The password will be 12 characters with letters,numbers,and a special character. After you \n'
            +'have stored passwords to your heart\'s content, you can access them by typing \'get\'. Once you type in the name of the service you \n'
            +'would like to retrieve, the password will be provided to you. Once you are finished you can type quit and the program will end.'
            )

        if input_ == 'quit':
            break
