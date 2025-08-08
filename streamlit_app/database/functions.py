import sqlite3 as sql

DB_CONNECTION_STRING = "sustainability_data.db"

def testCall():
    """
    Params: None

    Simply a test call to verify relative importing works.

    Returns: 1
    """
    print("You called test!")

    return 1

def getPlants(region_id):
    """
    Params: Region ID
        1 = NA
        2 = LATAM
    Queries the database and returns a list of all the plants that have
    an asset in the `assets` table.

    Returns: A list of strings
    """
    conn = sql.connect(DB_CONNECTION_STRING)
    cur = conn.cursor()

    sqlStatement = '''SELECT DISTINCT site FROM assets WHERE region_id = ?;'''

    result = cur.execute(sqlStatement, (region_id,))
    data = result.fetchall()
    conn.close() # Done with db, should close the connection

    print("Data is a list of tuples: %s" % data)

    index = 0
    plants = []
    for plant in data:
        plants.append(data[index][0])
        index += 1

    return plants

def getTotalPlantFaults(plantName):
    """
    Params: Name of plant as a string

    Queries the database and returns the number of faults that the
    specified plant has in the `alerts` table.

    Returns: An int, will be 0 if the plant was not in the `alerts` table.
    """
    conn = sql.connect(DB_CONNECTION_STRING)
    cur = conn.cursor()

    sqlStatement = '''
        SELECT 
            COUNT(*)
        FROM 
            assets 
        INNER JOIN 
            alerts 
        ON 
            alerts.asset_id = assets.asset_id
        WHERE
            assets.site = ?;
    '''

    result = cur.execute(sqlStatement, (plantName,))
    data = result.fetchall()
    conn.close()

    print("Data is a list of tuples: %s" % data)
    numOfPlantFaults = data[0][0]

    return numOfPlantFaults

def getAvgPlantKWH(plantName):
    """
    Params: Name of plant as a string

    Queries the database and returns the computed avg of total_kwh from
    the 'utility_summary' table.

    Returns: An int, will be None if the plant was not in the `utility_summary` table.
    """
    conn = sql.connect(DB_CONNECTION_STRING)
    cur = conn.cursor()

    sqlStatement = '''
        SELECT 
            site,
            AVG(total_kwh) 
        FROM 
            utility_summary 
        WHERE site = ?;
    '''

    result = cur.execute(sqlStatement, (plantName,))
    data = result.fetchall()
    conn.close()

    print("Data is a list of tuples: %s" % data)
    plantAvgKWH = data[0][1]

    return plantAvgKWH