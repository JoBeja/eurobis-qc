import sys
import os
import pyodbc
import atexit
import configparser
import logging

this = sys.modules[__name__]

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'resources/config.ini'))

this.conn = None
this.database = None
this.driver = None
this.username = None
this.password = None

this.logger = logging.getLogger(__name__)

if "SQLSERVERDB" in config:
    try:
        this.driver = config['SQLSERVERDB']['driver']
        this.server = config['SQLSERVERDB']['server']
        this.port = config['SQLSERVERDB']['port']
        this.database = config['SQLSERVERDB']['database']
        this.username = config['SQLSERVERDB']['username']
        this.password = config['SQLSERVERDB']['password']
    except KeyError:
        # Some Parameters cannot be loaded or are missing - Should find clean exit strategy
        pass
else:
    # Parameters cannot be loaded - Should find clean exit strategy
    pass

# Build a connection string
this.connection_string = f'DRIVER={this.driver};' \
                         f'PORT={this.port};' \
                         f'SERVER={this.server};' \
                         f'DATABASE={this.database};' \
                         f'UID={this.username};' \
                         f'PWD={this.password}'

def open_db():
    """ Opens a DB, the parameters are already loaded from the configuration file
        upon importing the module
        """
    try:
        this.conn = pyodbc.connect(this.connection_string)
        return this.conn
    except pyodbc.Error as ex:
        # The connection is not initialized, log the exception message
        sqlstate = ex.args[1]
        this.logger.error(sqlstate)
        this.conn = None
        return None



def close_db():
    """ Closes the DB after use, automatically called upon module exit """

    this.conn.close()
    this.conn = None


@atexit.register
def close_down():
    """ Upon unloading the module close the DB connection """

    if this.conn is not None:
        close_db()
