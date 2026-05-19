import pymysql as pms
import csv
import ast
import prettytable as pt


class DatabaseCreator:
    #method for creating relations in a database
    def create_relation(self, cursor):
        while 1:
            try:
                #create relationship tables for the movie csv such that theyre
                #in atleast 3NF
                cursor.execute('CREATE TABLE genres('
                                +'id INT NOT NULL,'
                                +'name VARCHAR(255) NOT NULL,'
                                +'primary key (id)'
                                +');')
                cursor.execute('CREATE TABLE keywords('
                                +'id INT NOT NULL,'
                                +'name VARCHAR(255) NOT NULL,'
                                +'primary key (id)'
                                +');')
                cursor.execute('CREATE TABLE production_companies('
                                +'id INT NOT NULL,'
                                +'name VARCHAR(255) NOT NULL,'
                                +'primary key (id)'
                                +');')
                cursor.execute('CREATE TABLE production_countries('
                                +'iso_3166_1 VARCHAR(2) NOT NULL,'
                                +'name VARCHAR(255) NOT NULL,'
                                +'primary key (iso_3166_1)'
                                +');')
                cursor.execute('CREATE TABLE spoken_languages('
                                +'iso_639_1 VARCHAR(2) NOT NULL,'
                                +'name VARCHAR(255) NOT NULL,'
                                +'primary key (iso_639_1)'
                                +');')
                cursor.execute('CREATE TABLE movies('
                                +'budget BIGINT NOT NULL,'
                                +'homepage VARCHAR(255) NOT NULL,'
                                +'id INT NOT NULL,'
                                +'original_language VARCHAR(255) NOT NULL,'
                                +'original_title VARCHAR(255) NOT NULL,'
                                +'overview TEXT NOT NULL,'
                                +'popularity DECIMAL NOT NULL,'
                                +'release_date VARCHAR(255) NOT NULL,'
                                +'revenue BIGINT NOT NULL,'
                                +'runtime INT ,'
                                +'status VARCHAR(255) NOT NULL,'
                                +'tagline VARCHAR(255) NOT NULL,'
                                +'title VARCHAR(255) NOT NULL,'
                                +'vote_average FLOAT NOT NULL,'
                                +'vote_count INT NOT NULL,'
                                +'primary key (id)'
                                +');')
                cursor.execute('CREATE TABLE g_movie_relation('
                                +'relation_id INT NOT NULL AUTO_INCREMENT,'
                                +'g_id INT NOT NULL,'
                                +'m_id INT NOT NULL,'
                                +'primary key (relation_id),'
                                +'foreign key (g_id) references genres(id),'
                                +'foreign key (m_id) references movies(id)'
                                +');')
                cursor.execute('CREATE TABLE kw_movie_relation('
                                +'relation_id INT NOT NULL AUTO_INCREMENT,'
                                +'kw_id INT NOT NULL,'
                                +'m_id INT NOT NULL,'
                                +'primary key (relation_id),'
                                +'foreign key (kw_id) references keywords(id),'
                                +'foreign key (m_id) references movies(id)'
                                +');')
                cursor.execute('CREATE TABLE pcompany_movie_relation('
                                +'relation_id INT NOT NULL AUTO_INCREMENT,'
                                +'pcompany_id INT NOT NULL,'
                                +'m_id INT NOT NULL,'
                                +'primary key (relation_id),'
                                +'foreign key (pcompany_id) references production_companies(id),'
                                +'foreign key (m_id) references movies(id)'
                                +');')
                cursor.execute('CREATE TABLE pcountry_movie_relation('
                                +'relation_id INT NOT NULL AUTO_INCREMENT,'
                                +'pcountry_iso VARCHAR(2) NOT NULL,'
                                +'m_id INT NOT NULL,'
                                +'primary key (relation_id),'
                                +'foreign key (pcountry_iso) references production_countries(iso_3166_1),'
                                +'foreign key (m_id) references movies(id)'
                                +');')
                cursor.execute('CREATE TABLE sl_movie_relation('
                                +'relation_id INT NOT NULL AUTO_INCREMENT,'
                                +'sl_iso VARCHAR(2) NOT NULL,'
                                +'m_id INT NOT NULL,'
                                +'primary key (relation_id),'
                                +'foreign key (sl_iso) references spoken_languages(iso_639_1),'
                                +'foreign key (m_id) references movies(id)'
                                +');')
                print('All relations are now present.')
                break
            #if tables existed prompt user to drop the existing table[s]
            except:
                drop_question = input('Database has one or more of the tables'
                                        +' being created would you like to '
                                        +'drop them? (y/n) ')
                if drop_question == 'y':
                    cursor.execute('DROP TABLE IF exists g_movie_relation')
                    cursor.execute('DROP TABLE IF exists kw_movie_relation')
                    cursor.execute('DROP TABLE IF exists pcompany_movie_relation')
                    cursor.execute('DROP TABLE IF exists pcountry_movie_relation')
                    cursor.execute('DROP TABLE IF exists sl_movie_relation')
                    cursor.execute('DROP TABLE IF exists movies')
                    cursor.execute('DROP TABLE IF exists genres')
                    cursor.execute('DROP TABLE IF exists keywords')
                    cursor.execute('DROP TABLE IF exists production_companies')
                    cursor.execute('DROP TABLE IF exists production_countries')
                    cursor.execute('DROP TABLE IF exists spoken_languages')
                    continue
                #if they dont want to drop existing tables all new tables may
                #not be added warn the user
                elif drop_question == 'n':
                    print('Warning: not all relations may have been created.')
                    break
                #loop for none y or n answers
                else:
                    print('Invalid input.')
                    continue
        return

    #method for inserting into a database from a csv
    def insert_from_csv(self, cursor):
        while 1:
            #ask user for the path to the csv files containing the movies information
            csv_path = input('Type the name of the csv file you would like to import'
                            +'into the movies database: ')
            #attempt to open the file
            try:
                with open(csv_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    csv_header = next(csv_reader)
                    for row in csv_reader:
                        if row[13] == '':
                            row13 = None
                        else:
                            row13 = row[13]
                        #this is the insert command for the movies relation
                        cursor.execute('INSERT IGNORE INTO movies(budget,homepage,id,'
                            +'original_language,original_title,overview,popularity,'
                            +'release_date,revenue,runtime,status,tagline,title,'
                            +'vote_average,vote_count)'
                            +'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',
                            (row[0],row[2],row[3],row[5],row[6],row[7],row[8],row[11],
                                row[12],row13,row[15],row[16],row[17],row[18],row[19])
                        )
                        #command for insert into genres
                        genre_array = ast.literal_eval(row[1])
                        for g_dict in genre_array:
                            cursor.execute('INSERT IGNORE INTO genres(id, name)'
                                +'VALUES (%s,%s);',(g_dict['id'],g_dict['name']))
                            cursor.execute('INSERT IGNORE INTO g_movie_relation(g_id,m_id)'
                                +'VALUES (%s,%s);',(g_dict['id'],row[3]))
                        #command for insert into keywords
                        kw_array = ast.literal_eval(row[4])
                        for kw_dict in kw_array:
                            cursor.execute('INSERT IGNORE INTO keywords(id, name)'
                                +'VALUES (%s,%s);',(kw_dict['id'],kw_dict['name']))
                            cursor.execute('INSERT IGNORE INTO kw_movie_relation(kw_id,m_id)'
                                +'VALUES (%s,%s);',(kw_dict['id'],row[3]))
                        #command for insert into production_companies
                        pcompany_array = ast.literal_eval(row[9])
                        for pcompany_dict in pcompany_array:
                            cursor.execute('INSERT IGNORE INTO production_companies(id, name)'
                                +'VALUES (%s,%s);',(pcompany_dict['id'],pcompany_dict['name']))
                            cursor.execute('INSERT IGNORE INTO pcompany_movie_relation(pcompany_id,m_id)'
                                +'VALUES (%s,%s);',(pcompany_dict['id'],row[3]))
                        #command for insert into production_countries
                        pcountry_array = ast.literal_eval(row[10])
                        for pcountry_dict in pcountry_array:
                            cursor.execute('INSERT IGNORE INTO production_countries(iso_3166_1, name)'
                                +'VALUES (%s,%s);',(pcountry_dict['iso_3166_1'],pcountry_dict['name']))
                            cursor.execute('INSERT IGNORE INTO pcountry_movie_relation(pcountry_iso,m_id)'
                                +'VALUES (%s,%s);',(pcountry_dict['iso_3166_1'],row[3]))
                        #command for insert into spoken_lanuages
                        sl_array = ast.literal_eval(row[14])
                        for sl_dict in sl_array:
                            cursor.execute('INSERT IGNORE INTO spoken_languages(iso_639_1, name)'
                                +'VALUES (%s,%s);',(sl_dict['iso_639_1'],sl_dict['name']))
                            cursor.execute('INSERT IGNORE INTO sl_movie_relation(sl_iso,m_id)'
                                +'VALUES (%s,%s);',(sl_dict['iso_639_1'],row[3]))
                #this tells user the import was successful
                print(f'csv file at {csv_path} has been imported.')
                break
            #if file doesnt open then send an error message and ask for another path
            except:
                print(f'Error: file at {csv_path} does not match the correct column format.')
                continue
        return

def query_questions(cursor):
    while 1:
        #present user with the available queries
        query_option = input("""Query options:
[1] Average budget of all movies.
[2] Movies that were produced in the United States.
[3] Top 5 movies that made the most revenue.
[4] Movies with both the genre Science Fiction and Mystery.
[5] Movies that have a popularity greater than the average popularity.
[6] Exit.
What would you like to query for? """)
        #depending on the answer call the query specific function
        if query_option == '1':
            avg_budget(cursor)
            continue
        elif query_option == '2':
            movies_us(cursor)
            continue
        elif query_option == '3':
            top5_revenue(cursor)
            continue
        elif query_option == '4':
            scifi_mystery(cursor)
            continue
        elif query_option == '5':
            above_avg_pop(cursor)
            continue
        elif query_option == '6':
            break
        else:
            print('Please choose from the options presented.')
            continue
        break
    return

def avg_budget(cursor):
    cursor.execute("""SELECT AVG(budget)
FROM movies;""")
    answer = cursor.fetchall()
    answer_table = pt.PrettyTable(['AverageBudget'])
    answer_table.left_padding_width = 0
    answer_table.right_padding_width = 2
    answer_table.align = 'l'
    answer_table.title = 'Average movie budget'
    for row in answer:
        answer_table.add_row(row)
    print(answer_table)

def movies_us(cursor):
    cursor.execute("""SELECT title, GROUP_CONCAT(name SEPARATOR ', ')
FROM
(
    (
    SELECT movies.id, movies.title
    FROM movies JOIN pcountry_movie_relation
    ON movies.id=pcountry_movie_relation.m_id
    WHERE pcountry_movie_relation.pcountry_iso='US'
    ) AS table1
    JOIN
    (
    SELECT pcompany_movie_relation.m_id, production_companies.name
    FROM pcompany_movie_relation JOIN production_companies
    ON pcompany_movie_relation.pcompany_id=production_companies.id
    ) AS table2
    ON table1.id=table2.m_id
)
GROUP BY title;""")
    answer = cursor.fetchall()
    answer_table = pt.PrettyTable(['MovieTitle','ProductionCompany'])
    answer_table.left_padding_width = 0
    answer_table.right_padding_width = 2
    answer_table.align = 'l'
    answer_table.title = 'Movies made in the U.S. & their production companies'
    for row in answer:
        answer_table.add_row(row)
    print(answer_table)

def top5_revenue(cursor):
    cursor.execute("""SELECT title, revenue
FROM movies
ORDER BY revenue DESC
LIMIT 5;""")
    answer = cursor.fetchall()
    answer_table = pt.PrettyTable(['MovieTitle','Revenue'])
    answer_table.left_padding_width = 0
    answer_table.right_padding_width = 2
    answer_table.align = 'l'
    answer_table.title = 'Top 5 movies by revenue'
    for row in answer:
        answer_table.add_row(row)
    print(answer_table)

def scifi_mystery(cursor):
    cursor.execute("""SELECT title, GROUP_CONCAT(name SEPARATOR ', ')
FROM (genres
JOIN
(SELECT title, g_id
FROM movies
JOIN
(SELECT table2.m_id, g_id
FROM g_movie_relation
JOIN
((SELECT m_id
FROM g_movie_relation
JOIN
(SELECT id 
FROM genres
WHERE genres.name='Science Fiction') AS table0
ON g_movie_relation.g_id=table0.id)
INTERSECT
(SELECT m_id
FROM g_movie_relation
JOIN
(SELECT id 
FROM genres
WHERE genres.name='Mystery') AS table1
ON g_movie_relation.g_id=table1.id)) AS table2
ON table2.m_id=g_movie_relation.m_id) AS table3
ON table3.m_id=movies.id) AS table4
ON table4.g_id=genres.id)
GROUP BY title;""")
    answer = cursor.fetchall()
    answer_table = pt.PrettyTable(['MovieTitle','Genre'])
    answer_table.left_padding_width = 0
    answer_table.right_padding_width = 2
    answer_table.align = 'l'
    answer_table.title = 'Movies with both genres Science Fiction and Mystery'
    for row in answer:
        answer_table.add_row(row)
    print(answer_table)

def above_avg_pop(cursor):
    cursor.execute("""SELECT title, popularity
FROM movies
WHERE movies.popularity>(
SELECT AVG(popularity)
FROM movies
)""")
    answer = cursor.fetchall()
    answer_table = pt.PrettyTable(['MovieTitle','Popularity'])
    answer_table.left_padding_width = 0
    answer_table.right_padding_width = 2
    answer_table.align = 'l'
    answer_table.title = 'Movies with above average popularity'
    for row in answer:
        answer_table.add_row(row)
    print(answer_table)

def main():
    my_sql_db = 0
    my_sql_curs = 0
    while 1:
        #ask if user wants to access/create database named HW5 on machine
        db_question = input('Would you like to access/create database \'HW5\' on this'
                            +' machine? (y/n) ')
        if db_question == 'y':
            #prompt user for connect information
            user_host = input('Enter host IP or hostname (if left blank will default'
                                +' to localhost): ')
            if user_host == '':
                user_host = 'localhost'
            user_name = input('Enter your username (if left blank will default to '
                                +'root): ')
            if user_name == '':
                user_name = 'root'
            user_pass = input('Enter your password: ')
            #try to use information gather if it doesnt work try again
            try:
                my_sql_db = pms.connect(host=str(user_host),
                                        user=str(user_name),
                                        password=str(user_pass))
            except:
                print('Invalid information could not connect.')
                continue
            #if connection was successful create a cursor
            print('Connection successful.')
            my_sql_curs = my_sql_db.cursor()
            #since connection is successful we can now instaniate the class that
            #will do the relation building and inserting from a csv
            db_creator = DatabaseCreator()
            while 1:
                #try to create the database
                try:
                    my_sql_curs.execute('CREATE DATABASE HW5')
                    print('New HW5 database created.')
                    break
                #if the database exist ask the user if they would like to drop
                #the existing database
                except:
                    drop_question = input('Database already exist would you like'
                                            +' to drop \'HW5\'? (y/n) ')
                    if drop_question == 'y':
                        my_sql_curs.execute('DROP DATABASE HW5')
                        continue
                    elif drop_question == 'n':
                        break
                    else:
                        print('Invalid input.')
                        continue
            #now select the HW5 database
            my_sql_curs.execute('USE HW5')
            print('HW5 database selected.')
            #call the two methods for creating the relation and inserting from csv 
            db_creator.create_relation(my_sql_curs)
            db_creator.insert_from_csv(my_sql_curs)
            #commit the creation of this database
            my_sql_db.commit()
            #go into a query question function that will loop until the user 
            #decides to exit
            query_questions(my_sql_curs)
            break
        elif db_question == 'n':
            #this will only happen if the user says no they dont want to access
            #the HW5 database
            print('Program ended.')
            break
        else:
            print('Invalid input.')
            continue
    #once program is done close the cursor and connection
    if my_sql_curs:
        my_sql_curs.close()
    if my_sql_db:
        my_sql_db.close()

if __name__ == '__main__':
    main()
