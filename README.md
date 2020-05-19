# password_manager
This is a password manager that runs in console, and stores passwords on a local DB.

Password Manager allows you to store passwords safely on an encrypted db stored locally on your pc. Select store to enter a
service (i.e. Netflix, Amazon,etc.) and select whether or not you already have a password for that service. If you don't, a 
password will be generated for you. The password will be 12 characters with letters,numbers,and a special character. After you
have stored passwords, you can access them by typing 'get'. Once you type in the name of the service you would like to retrieve,
the password will be provided to you. Once you are finished you can type quit and the program will end.

It uses the sqlite3, hashlib, base64, os, sys, and random libraries which should all be standard.
