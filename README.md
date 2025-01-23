In this object oriented python program the user can check different informations. 
It's modelling a schools internal system. The program relies on a PostgreSQL database.

Setup:
1 - clone repository

2 - install dependencies: pip install -r requirements.txt

3 - create a .env file in the root directory:
    DB_HOST=your_db_host
    DB_NAME=your_db_name
    DB_USER=your_db_username
    DB_PASSWORD=your_password

    example for local use:
    DB_HOST=localhost
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=your_password

4 - run main.py

Make sure PostgreSQL is installed and working locally.