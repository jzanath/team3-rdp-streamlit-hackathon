import sqlite3 as sql
from datetime import datetime
from datetime import timedelta

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

def getPlantAssets(plantName):
    """
    Params: Name of plant as a string

    Queries the database and returns assetId and assetName pairs from
    the `assets` table for the given site.

    Returns: A list of python dictionaries.
        Keys:
            Asset ID
            Name
    """
    conn = sql.connect(DB_CONNECTION_STRING)
    cur = conn.cursor()

    sqlStatement = '''
        SELECT asset_id, name FROM ASSETS WHERE site = ?;
    '''

    result = cur.execute(sqlStatement, (plantName,))
    data = result.fetchall()
    conn.close()

    print("Data is a list of tuples: %s" % data)

    returnList = []
    for asset in data:
        tempDict = {"Asset ID": asset[0], "Name": asset[1]}
        returnList.append(tempDict)

    print(returnList)
    return returnList

def getAssetAlertTypes(assetId):
    """
    Params:
        Int: assetId

    Queries the database and returns all alert instances for that asset
    that appear in 'alerts'.

    Returns: A list of strings that are the alert_types
    """
    conn = sql.connect(DB_CONNECTION_STRING)
    cur = conn.cursor()

    sqlStatement = '''
        SELECT alert_type FROM ALERTS WHERE asset_id = ?;
    '''

    result = cur.execute(sqlStatement, (assetId,))
    data = result.fetchall()
    conn.close()

    print("Data is a list of tuples: %s" % data)

    index = 0
    alertTypes = []
    for alert in data:
        alertTypes.append(data[index][0])
        index += 1

    return alertTypes

def getTotalAssetAlerts(assetId):
    """
    Params:
        Int: assetId

    Queries the database and returns a count of alerts for that asset
    that appear in 'alerts'.

    Returns: An Int
    """
    conn = sql.connect(DB_CONNECTION_STRING)
    cur = conn.cursor()
    sqlStatement = '''
        SELECT COUNT(*) FROM ALERTS WHERE asset_id = ?;
    '''

    result = cur.execute(sqlStatement, (assetId,))
    data = result.fetchall()
    conn.close()

    print("Data is a list of tuples: %s" % data)
    numOfAssetAlerts = data[0][0]

    return numOfAssetAlerts

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

def getTotalPlantFaultsFromDate(plantName, date):
    """
    Params:
        Name of plant as a string
        Date you want to search starting from (Format YYYY-MM-DD)

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
            assets.site = ? AND alerts.timestamp >= ?;
    '''

    result = cur.execute(sqlStatement, (plantName, date))
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

def getPlantAvgBatchTime(plantName):
    """
    Params: Name of plant as a string

    Queries the database and returns the average batch time
    from the 'batches' table for that site.

    Returns: A string
    """
    conn = sql.connect(DB_CONNECTION_STRING)
    cur = conn.cursor()

    sqlStatement = '''
        SELECT 
            batches.start_time,
            batches.end_time
        FROM 
            assets 
        INNER JOIN 
            batches 
        ON 
            batches.asset_id = assets.asset_id
        WHERE
            assets.site = ?
        ORDER BY
            start_time;
    '''

    result = cur.execute(sqlStatement, (plantName,))
    data = result.fetchall()
    conn.close()

    batchTimes = []
    numOfBatches = len(data)

    if numOfBatches > 0:
        for timeframe in data:
            startTime = timeframe[0]
            endTime = timeframe[1]

            startDT = datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
            endDT = datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

            batchTimes.append(endDT - startDT)

        averageBatchTime = sum(batchTimes, timedelta()) / numOfBatches
        print("Average Batch Time: %s" % averageBatchTime)
    else:
        averageBatchTime = timedelta(0)

    return int(averageBatchTime.total_seconds() / 60)