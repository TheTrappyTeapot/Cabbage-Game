import sqlite3

con = sqlite3.connect('CGDB.db')
cur = con.cursor()

#cur.execute('''CREATE TABLE Plant
#            (PlantID INT PRIMARY KEY,
#            PlantPotID           INT,
#            CropID               INT,
#            GrowthStartTick      INT);''')


#cur.execute('''CREATE TABLE Inventory
#         (EntryID                INT,
#         ItemID                  INT,
#         TableName       VARCHAR(20),
 #        Type            VARCHAR(20),
#         Quantity                INT);''')

poo = (cur.execute('''

SELECT Planter.PlanterID, Light.Name, GrowthMedia.Name
FROM Planter, Light, GrowthMedia
WHERE Planter.LightID = Light.LightID AND Planter.GrowthMediaID = GrowthMedia.GrowthMediaID

''')).fetchall()

res = (cur.execute(f'SELECT Name FROM Light WHERE LightID = {1}')).fetchall()

for line in res:
    for item in line:
        print(f'{item:20}',end=' | ')
    print()

def fillVeg():
    cur.execute(f'''
    UPDATE Inventory
    SET Quantity = 30
    WHERE entryID = 17 ''')
    con.commit()
    
def eraseData(table):
    cur.execute(f'''
    TRUNCATE TABLE {table}
    ''')
    con.commit()

def eraseSpefData(table, where, what):
    cur.execute(f'''
    DELETE FROM {table}
    WHERE {where} == {what}
    ''')
    con.commit()

def eraseTable(table):
    cur.execute(f'''
    DROP TABLE {table}
    ''')
    con.commit()

def eraseColumn(table,column):
    cur.execute(f'''
    ALTER TABLE {table}
    DROP COLUMN {column}; ''')
    con.commit()

def renameColumn(table,column):
    cur.execute(f'''
    ALTER TABLE {table}
    RENAME COLUMN {column}; ''')
    con.commit()

def editValues(table,setto,where):
    cur.execute(f'''
    UPDATE {table}
    SET {setto}
    WHERE {where} ''')
    con.commit()

def insertValues(table,data):
    cur.executemany(f'INSERT INTO {table} VALUES(?,?,?,?)', data)
    con.commit()

def readTable(table):
    res = (cur.execute(f'SELECT * FROM {table}')).fetchall()
    for line in res:
        for item in line:
            print(f'{item:10}',end=' | ')
        print()

def rQ(what, fromWhere, where):
    return (cur.execute(f'SELECT {what} FROM {fromWhere} WHERE {where}')).fetchall()



while True:
    inp = input('>>>:')

    if inp == 'endtt':
        data = []
        table = input('which table:')
        print('enter blank to stop loop, sepperate data by \' \'')
        run = True
        while run:
            databit = input('')
            if databit == '':
                run = False
            else:
                databit = databit.split(' ')
                data.append(databit)
        insertValues(table, data)

    elif inp == 'rq':
        rQ(input(''), input(''), input(''))

    elif inp == 'ev':
        print('enter table name and new data')
        editValues(input(''), input(''), input(''))
        
    elif inp == 'dt':
        print('enter table name')
        eraseTable(input(''))

    elif inp == 'dc':
        print('enter table name and column name')
        eraseColumn(input(''), input(''))
        
    elif inp == 'dd':
        print('enter table name')
        eraseData(input(''))

    elif inp == 'dsd':
        print('enter table name, where and what')
        eraseSpefData(input(''), input(''), input(''))

    elif inp == 'fillC':
        fillVeg()
        print('full')

    elif inp == 'rc':
        print('enter table name and column info')
        renameColumn(input(''), input(''))
        
    elif inp == 'rt':
        readTable(input('which table:'))
        
    else:
        print('invalid')

