import psycopg2

user = "postgres"
password="123456"
host="localhost"
port="5432"
database="colorDetect"

def model(model):
    try:
        connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT * FROM public.mastermodel where model = '+model+' limit 1;'
        cursor.execute(postgreSQL_select_Query)
        authors_records = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
    return authors_records[0]


def maskParam(color):
    try:
        connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)
        cursor = connection.cursor()
        postgreSQL_select_Query = 'SELECT id, color, lh, uh, ls, us, lv, uv, symbol, "timestamp" FROM public.param where color = '+color+' order by id desc limit 1;'
        cursor.execute(postgreSQL_select_Query)
        authors_records = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
    return authors_records[0]

def updateParam(lh,uh,ls,us,lv,uv,color):
    try:
        connection = psycopg2.connect(user=user,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=database)
        cursor = connection.cursor()
        postgreSQL_select_Query = "UPDATE public.param SET  lh="+lh+", uh="+uh+", ls="+ls+", us="+us+", lv="+lv+", uv="+uv+" WHERE color = '"+color+"';"

        cursor.execute(postgreSQL_select_Query)
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while insert data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print(maskParam("'blue'"))
    print(model("'A001'"))