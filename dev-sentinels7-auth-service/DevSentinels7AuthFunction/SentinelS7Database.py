###########################################################################
#
## @file SentinelS7Database.py
#
###########################################################################

import psycopg2
import os

###########################################################################
#
##   A wrapper around the psycopg2 python library.
#
#    The Database class is a high-level wrapper around the psycopg2
#    library. It allows users to create a postgresql database connection and
#    write to or fetch data from the selected database.
#
###########################################################################

#######################################################################
#
## The constructor of the Database class
#
#  The constructor can either be passed the name of the database to open
#  or not, it is optional.
#
#  @param url Optionally, the url of the database to open.
#
#
#######################################################################
    
class SentinelS7Database:
    def __init__(self, client):
        self.client = client
    
    def get_select_query_all_results(self, query):
        SENTINELS7DBCONNECTIONSTRING = os.environ['SENTINELS7DBCONNECTIONSTRING']
        conn = psycopg2.connect(SENTINELS7DBCONNECTIONSTRING)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
