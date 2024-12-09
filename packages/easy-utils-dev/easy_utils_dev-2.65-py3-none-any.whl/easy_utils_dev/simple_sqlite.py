from datetime import datetime
import sqlite3 , os
from .debugger import DEBUGGER
from .utils import getRandomKey
from .custom_env import custom_env , setupEnvironment 
from .utils import fixTupleForSql

env = custom_env()

def getLoggerFromMemory( id ) :
    '''
    When Logger/Debugger is called or initialized it automatically is stored in memory with certain id.
    you can call this event from memory by passing that id to this function which will return the event if found.
    if not.. it will return None
    '''
    ev = env.get('simple_sqlite' , {} )
    return ev.get( id , None )


class initDB :
    def __init__(self, db=None , logger=None,useDefaultLogger=False,enable_log=True,id=getRandomKey(n=5)) :
        self.db_file = db
        self.disableLog = False
        self.logger = logger
        self.enable_log = enable_log
        self.lastCur = None
        self.lastCon=None
        self.id = id
        self.applyDatabaseParams=True
        setupEnvironment('simple_sqlite')
        env['simple_sqlite'][id] = self
        if not logger : 
            self.logger = DEBUGGER(name='simple-sqlite')

    def config_database_path(self,path) :
        self.logger.debug(f'Database path set to {path}')
        self.db_file = path
        
    def fixTupleForSql(self , list:list ):
        if len(list) <= 1 :
            execlude = str(list).replace('[' , '(' ).replace(']' , ')')
        else :
            execlude = tuple(list)
        return execlude

    def db_connect(self, timeout: int =5):
        self.logger.debug(f'connecting to {self.db_file}')
        self.con = sqlite3.connect(self.db_file , check_same_thread=False,timeout= timeout)
        self.cur = self.con.cursor()
        return  self.cur , self.con 

    def execute_dict(self,cli:str) :
        self.logger.debug(f"execute_dict: {cli}")
        cur , conn = self.db_connect()
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        c = conn.cursor()
        h = c.execute(cli).fetchall()
        if not 'select' in cli.lower() :
            conn.commit()
        conn.close()
        return h

    def vacuum(self) :
        try :
            cur , conn = self.db_connect()
            cur.execute('VACUUM')
            conn.commit()
            conn.close()
        except :
            pass


    def createTable(self , tableName ,data=[] , autoId=True) :
        self.logger.debug(f'Creating table : {data}')
        cur,con = self.db_connect()
        cli = f"""CREATE TABLE IF NOT EXISTS {tableName} ( \n"""
        if autoId : 
            data.insert(0,{
                'column' : 'id' ,
                'params' : 'INTEGER PRIMARY KEY AUTOINCREMENT'
            })
        for elem in data :
            cli += f""" {elem['column']} {elem['params']} , \n"""
        cli = cli.rstrip(', \n') + ' \n)'
        cur.execute(cli)
        con.commit()
        con.close()

    def execute(self,cli) :
        self.logger.debug(f'Executing : {cli}')
        cur,con = self.db_connect()
        h = cur.execute(cli).fetchall()
        if not 'select' in cli.lower() :
            con.commit()
        con.close()
        return h

    def insert_to_table(self,table_name , table_headers , table_values , autocommit= True) :
        cur , con = self.db_connect()
        self.logger.debug(f'Inserting data into {table_name}'.format(table_name=table_name))
        table_headers = tuple(table_headers)
        table_values = tuple(table_values)
        cli = f"INSERT INTO {table_name} {table_headers} VALUES{table_values}"
        self.logger.debug('INFO DB EXECUTION: '+cli)
        cur.execute(cli)
        if autocommit == True :
            con.commit()
        con.close()
        return cur.lastrowid
    
    def insert_to_table_from_dict(self , table_name , dict : dict , autocommit= True ) :
        headers = list(dict.keys())
        values = list(dict.values())
        self.logger.debug(f'headers= {headers}')
        self.logger.debug(f'values= {values}')
        return self.insert_to_table(table_name , headers , values , autocommit= autocommit)
            
    def insert_to_table_bulk(self, tableName, values={} , autoCommit=True):
        cur , con = self.db_connect()
        self.logger.debug(f'Inserting data into {tableName}')
        headers = fixTupleForSql(list(values[0].keys()))
        rowIdStart= cur.rowcount
        cli = f"INSERT INTO {tableName} {headers} values "
        for key , elem  in enumerate(values) :
            values = elem.values()
            cli +=  f'{fixTupleForSql(values)} ,'
        cli = cli.rstrip(',')
        cur.execute(cli)
        if autoCommit :
            con.commit()
        con.close()
        rowEnd= cur.rowcount
        return [x + 1 for x in range(rowIdStart + 1 , rowEnd)] , cur.lastrowid
        
    def dump_database(self,outputPath , export_rows=True ,fileName=None) :
        cur , conn = self.db_connect()           
        if not fileName :
            fileName = os.path.basename(outputPath)
        outputPath= os.path.dirname(outputPath)
        fullPath = os.path.join(outputPath, fileName)
        if not os.path.exists(outputPath) :
                os.makedirs(outputPath)
        if os.path.exists(fullPath) :
            os.remove(fullPath)
        with open(fullPath, 'a+') as f:
            for line in conn.iterdump():
                if not export_rows :
                    if line.lower().startswith('insert into') :
                        continue
                f.write(line + '\n')
        
    def reset(self , exclude: list=[]) :
        '''
        This function will reset all the database tables. to skip some tables, add their names to exclude array.
        '''
        cli = f'select name from sqlite_sequence'
        results= self.execute_dict(cli)
        exclude = [str(x).lower() for x in exclude]
        cur , conn = self.db_connect()
        for elem in results :
            tableName = elem['name']
            if tableName.lower() in exclude :
                continue
            self.logger.debug(f'Resetting table : {tableName}')
            cli = f'DELETE FROM {tableName}'
            cur.execute(cli)
        cli = f'DELETE FROM sqlite_sequence'
        cur.execute(cli)
        cli = f'VACUUM'
        conn.commit()
        cur.execute(cli)
        conn.commit()
        conn.close()

    def execute_script(self, scriptPath) :
        if not os.path.exists(scriptPath) :
            raise Exception(f'SQL script not found: {scriptPath}')
        cur , conn = self.db_connect()
        with open(scriptPath, 'r') as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        conn.close()
        
if __name__ == '__main__' :
    pass