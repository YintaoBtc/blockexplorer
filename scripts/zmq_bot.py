import psycopg2
import random
import string  

try:
    guid =''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20)) #Generate gui

    connection = psycopg2.connect(user="postgres",
                                    password="postgres",
                                    host="db",
                                    port="5432",
                                    database="postgres")
    cursor = connection.cursor()


    postgres_insert_query = """ INSERT INTO block (ID, hash_block, confirmations, datetime, height, number_txs, difficulty, bits, weight, nonce) VALUES (%s,%s,%s)"""
    record_to_insert = (str(guid),"kinadsajkbreasdsajda321893u21932ndka", '5', "950", "680876", "1345", "12312321321312213", "56", "123213adwqdwq", "00000000001321321")
    print(record_to_insert)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print (count, "Record inserted successfully into block table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into block table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")