import cx_Oracle
from DatabaseConnectionUtility import Oracle 
from DatabaseConnectionUtility import Dremio
from DatabaseConnectionUtility import InMemory 
from DatabaseConnectionUtility import Oracle
from DatabaseConnectionUtility import MySql
from DatabaseConnectionUtility import MSSQLServer 
from DatabaseConnectionUtility import SAPHANA
from DatabaseConnectionUtility import Postgress
import json
from .UserRights import UserRights
import loggerutility as logger
from flask import request
import commonutility as common
import requests, json, traceback
from .ApplMst import ApplMst
from .Itm2Menu import Itm2Menu

class Generate_Application:

    connection           = None
    dbDetails            = ''
    menu_model           = ''
    token_id           = ''
    
    def get_database_connection(self, dbDetails):
        if dbDetails is not None:
            klass = globals()[dbDetails['DB_VENDORE']]
            dbObject = klass()
            connection_obj = dbObject.getConnection(dbDetails)
        return connection_obj

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
                logger.log("Transaction committed successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during commit: {error}")
        else:
            logger.log("No active connection to commit.")

    def rollback(self):
        if self.connection:
            try:
                self.connection.rollback()
                logger.log("Transaction rolled back successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during rollback: {error}")
        else:
            logger.log("No active connection to rollback.")

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                logger.log("Connection closed successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during close: {error}")
        else:
            logger.log("No active connection to close.")

    def genearate_application_with_model(self):
        jsondata = request.get_data('jsonData', None)
        jsondata = json.loads(jsondata[9:])
        logger.log(f"\nJsondata inside Manage_Menu class:::\t{jsondata} \t{type(jsondata)}")

        if "menu_model" in jsondata and jsondata["menu_model"] is not None:
            self.menu_model = jsondata["menu_model"]
            logger.log(f"\nInside menu_model value:::\t{self.menu_model}")

        if "dbDetails" in jsondata and jsondata["dbDetails"] is not None:
            self.dbDetails = jsondata["dbDetails"]
            logger.log(f"\nInside dbDetails value:::\t{self.dbDetails}")

        if "token_id" in jsondata and jsondata["token_id"] is not None:
            self.token_id = jsondata["token_id"]
            logger.log(f"\nInside token_id value:::\t{self.token_id}")

        self.connection = self.get_database_connection(self.dbDetails)

        if self.connection:
            try:

                token_status = common.validate_token(self.connection, self.token_id)

                if token_status == "active":

                    appl_mst = ApplMst()
                    appl_mst.process_data(self.connection, self.menu_model)

                    user_rights = UserRights()
                    user_rights.process_data(self.connection, self.menu_model)

                    itm2menu = Itm2Menu()
                    itm2menu.process_data(self.connection, self.menu_model)

                    self.commit()

                    trace = traceback.format_exc()
                    descr = str("Application and Menus Deployed Successfully.")
                    returnErr = common.getErrorXml(descr, trace)
                    logger.log(f'\n Exception ::: {returnErr}', "0")
                    return str(returnErr)
                elif token_status == "inactive":
                    trace = traceback.format_exc()
                    descr = str("Token Id is not Active.")
                    returnErr = common.getErrorXml(descr, trace)
                    logger.log(f'\n Exception ::: {returnErr}', "0")
                    return str(returnErr)
                else:
                    trace = traceback.format_exc()
                    descr = str("Invalid Token Id.")
                    returnErr = common.getErrorXml(descr, trace)
                    logger.log(f'\n Exception ::: {returnErr}', "0")
                    return str(returnErr)
                
            except Exception as e:
                logger.log(f"Rollback due to error: {e}")
                self.rollback()
                trace = traceback.format_exc()
                descr = str(e)
                returnErr = common.getErrorXml(descr, trace)
                logger.log(f'\n Exception ::: {returnErr}', "0")
                return str(returnErr)
                
            finally:
                logger.log('Closed connection successfully.')
                self.close_connection()
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Connection fail")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)


