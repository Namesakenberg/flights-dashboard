import mysql.connector


class DB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="hellosql1234",
                auth_plugin='mysql_native_password',
                database='flights'
            )
            if self.conn.is_connected():
                print("Connection established")

            self.mycursor = self.conn.cursor()

        except mysql.connector.Error as err:
            print(f"Connection error: {err}")

    def fetch_city_names(self):
        city = []
        self.mycursor.execute("""
            SELECT distinct(Source) FROM flights.flights
            union 
            SELECT distinct(Destination) FROM flights.flights
            """)
        data = self.mycursor.fetchall()
        city = [item[0] for item in data]
        return city

    def fetch_all_flights(self,source,destination):
        self.mycursor.execute(
            """
            SELECT Airline , Date_of_Journey , Source , Destination ,Route ,Dep_time ,Duration, Total_Stops , Price
            from flights.flights
            where Source = '{}' and Destination = '{}'
            """.format(source,destination)
        )
        results = self.mycursor.fetchall()
        return results

    def fetch_count_flights(self):
        airline=[]
        frequency = []
        self.mycursor.execute(
            """
            select distinct Airline , count(*) from flights.flights
            group by Airline
            """
        )
        data = self.mycursor.fetchall()
        for i in data:
            airline.append(i[0])
            frequency.append(i[1])

        return airline,frequency

    def busy_airports(self):
        airports=[]
        num_flights =[]
        self.mycursor.execute(
            """
            SELECT airport ,sum(num_flights)
            FROM (
            SELECT Source AS airport, COUNT(Airline) AS num_flights 
            FROM flights.flights 
            GROUP BY Source 
            UNION ALL
            SELECT Destination AS airport, COUNT(Airline) AS num_flights 
            FROM flights.flights 
            GROUP BY Destination 
            ) AS flights_small
            GROUP BY airport
            ORDER BY SUM(num_flights) DESC;
            """
        )
        data = self.mycursor.fetchall()
        for i in data:
            airports.append(i[0])
            num_flights.append(i[1])
        return airports,num_flights

    def flights_per_day(self):
        date = []
        count=[]
        self.mycursor.execute(
            """
            select Date_of_Journey , count(*) from flights.flights
            group by Date_of_journey
            order by Date_of_journey asc
            """
        )
        data = self.mycursor.fetchall()
        for i in data:
            date.append(i[0])
            count.append(i[1])
        return date,count