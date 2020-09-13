import sqlite3
from sqlite3 import Error
from ..sector_and_region.sector_and_region import TreeNavigator

class InvestorsDB:
    def __init__(self, db_dir, sectors_dir, regions_dir, sep="|"):
        self.db_dir = db_dir

        # initiate the sectors and regions tree
        self.sectors = TreeNavigator(sectors_dir)
        self.regions = TreeNavigator(regions_dir)

        # seperator for items in each col
        self.sep = sep

        # create investor database if not already
        sql_create_investors_table = """ CREATE TABLE IF NOT EXISTS investors (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL UNIQUE,
                                                regions text,
                                                sectors text,
                                                website text,
                                                description text
                                            ); """
        self._create_connection()
        try:
            self._cursor.execute(sql_create_investors_table)
        except Error as e:
            print(e)

        # colomn data
        self.col_names = ("name", "regions", "sectors", "website", "description")

        # collect all names of investors
        self._cursor.execute("SELECT name FROM investors")
        self.investor_names = [name[0] for name in self._cursor.fetchall()]

    def del_investor(self, investor_name):
        """ delete an investor """
        if investor_name not in self.investor_names:
            raise ValueError("Investor name does not exist!")

        # delete the investor with specified name
        sql_cmd = 'DELETE FROM investors WHERE name=?'
        self._cursor.execute(sql_cmd, investor_name)
        self._conn.commit()

    # def add_investors_from_csv(self, csv_dir):
    #     """ add investors from csv file """
    #

    def add_investor(self, investor_name, investor_regions, investor_sectors, investor_website, investor_description):
        """ add a new investor into the database"""
        # make sure investor_name was not mentioned before
        if investor_name in self.investor_names:
            raise ValueError("Investor name already exists!")

        # make sure regions and sectors mentioned are valid
        self._allowed_args("regions", investor_regions)
        self._allowed_args("sectors", investor_sectors)

        # prepare each arguments in the query
        investor_regions = self._list2str(investor_regions)
        investor_sectors = self._list2str(investor_sectors)
        investor_website = investor_website
        investor_description = investor_description

        # prepare sql query
        investor_args = (investor_name, investor_regions, investor_sectors, investor_website, investor_description)
        sql_cmd = ''' INSERT INTO investors(name, regions, sectors, website, description)
                      VALUES(?,?,?,?,?) '''
        self._cursor.execute(sql_cmd, investor_args)
        self._conn.commit()

        # add name to name list
        self.investor_names.append(investor_name)

    def update_investor(self, investor_name, col_name, args):
        """ update element """
        if investor_name not in self.investor_names:
            raise ValueError("Unknown investor name!")

        self._allowed_args(col_name, args)

        # update element
        sql_cmd = "UPDATE investors SET {} = ? WHERE name = ?".format(col_name)
        if type(args) is str:
            self._cursor.execute(sql_cmd, (args, investor_name))
        else:
            self._cursor.execute(sql_cmd, (self._list2str(args), investor_name))
        self._conn.commit()

        if col_name == "name": # if we are changing the name of an investor
            i = self.investor_names.index(investor_name)
            self.investor_names[i] = args

    def acquire_element(self, investor_name, col_name):
        """ acquire element in the table: name is not allowed here """
        if investor_name not in self.investor_names:
            raise ValueError("Unknown investor name!")

        if col_name not in self.col_names:
            raise ValueError("Unknown column name!")
        elif col_name == "name":
            raise ValueError("Why would you try to acquire name when you know the name???")

        return self._str2list(self._cursor.execute("SELECT {} FROM investors WHERE name=?".format(col_name), (investor_name,)).fetchall()[0][0])

    def search(self, col_name, args):
        """ search for args in specified cols, return rows that satisfies """
        # check if args are valid
        self._allowed_args(col_name, args)

        # augment search query for sectors and regions
        args = self._augment_search_query(col_name, args)

        # do the searching
        if type(args) is set:
            args = ["%" + self.sep + arg + self.sep + "%" for arg in set(args)]
            sql_query = "SELECT * FROM investors WHERE {} LIKE ?".format(col_name)
            for i in range(len(args) - 1):
                sql_query += " OR {} LIKE ?".format(col_name)
        elif type(args) is str:
            sql_query = "SELECT * FROM investors WHERE {} LIKE ?".format(col_name)
            args = (args, )
        self._cursor.execute(sql_query, args)
        return self._cursor.fetchall()

    def _list2str(self, l):
        return self.sep + (self.sep + self.sep).join(set(l)) + self.sep

    def _str2list(self, s):
        results = s.split(self.sep + self.sep)
        if len(results) > 1:
            results[0] = results[0][1:]
            results[-1] = results[-1][:-1]
        else:
            results[0] = results[0][1:-1]
        return results

    def _allowed_args(self, col_name, args):
        """ check if the args are allowed under specified col_name"""
        if col_name not in self.col_names:
            raise ValueError("Unknown column name!")
        else:
            if col_name in ("sectors", "regions"): # if col is regions or sectors, check if every element is valid
                assert(type(args) is list or type(args) is set)
                invalid_args = []
                valid_args = []
                if col_name == "regions":
                    for region in set(args):
                        if self.regions.has_node(region):
                            valid_args.append(region)
                        else:
                            invalid_args.append(region)
                elif col_name == "sectors":
                    for sector in set(args):
                        if self.sectors.has_node(sector):
                            valid_args.append(sector)
                        else:
                            invalid_args.append(sector)
                if len(invalid_args) > 0:
                    print("invalid args are: ", ", ".join(invalid_args))
                    args = valid_args
            elif col_name in ("name", "website", "description"):
                assert(type(args) is str)

    def _augment_search_query(self, col_name, args):
        """ for sectors and regions, augment search query """
        augmented_args = []
        if col_name == "sectors":
            for arg in args:
                augmented_args += self.sectors.find_node(arg)
        elif col_name == "regions":
            for arg in args:
                augmented_args += self.regions.find_node(arg)
        else:
            augmented_args = args
        return set(augmented_args)

    def _create_connection(self):
        """ create a database connection to a SQLite database """
        self._conn = None
        try:
            self._conn = sqlite3.connect(self.db_dir)
            self._cursor = self._conn.cursor()
        except Error as e:
            print(e)