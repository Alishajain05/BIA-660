from random import randrange, choice
import csv
import ast
from math import sqrt
from collections import OrderedDict
from datetime import datetime
from operator import itemgetter
import pprint

class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data = []

            for row in reader:
                data.append(row)

            return cls(list_of_lists=data)

    def __init__(self, list_of_lists, header=True):


        # init the columns as list so we can add according to new objects
        self.int_columns = ['Price', 'Latitude', 'Longitude', 'age', 'salary']
        self.date_columns = ["Transaction_date", "Account_Created", "Last_Login"]
        self.str_columns = ["Product", "Payment_Type", "Name", "City", "State", "Country", 'name']

        # ===== task 2 =====

        # simple method
        # for row in list_of_lists:
        #     for enum, element in enumerate(row):
        #         row[enum] = element.strip()

        # list comprehension
        # for each element of each row on the entire data we run the strip operator
        list_of_lists = [[cell.strip() for cell in row] for row in list_of_lists]

        # ===== task 2 =====
        
        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(list_of_lists[0])]
            self.data = list_of_lists

        # ===== task 1 =====

        # detecting duplicate columns and raising an exception
        # storing all the headers in a list
        header_list = self.header

        # storing the unique headers in a set
        header_set = set(self.header)

        if len(header_list) != len(header_set):
            raise Exception("Duplicate columns detected")
        else:
            self.data = [OrderedDict(zip(self.header, row)) for row in self.data]
            print type(self.data)
        
        # ===== task 1 =====


        self.raw_data = list_of_lists

    def __getitem__(self, item):
        # this is for rows only
        if isinstance(item, (int, slice)):
            # print 'getting row'
            return self.data[item]

        # this is for columns only
        elif isinstance(item, (str, unicode)):
            print "getting column"
            return [row[item] for row in self.data]

        # this is for rows and columns
        elif isinstance(item, tuple):
            # print "getting row and column"
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                    elif all([isinstance(thing, (str, unicode)) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], (str, unicode)):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        # only for lists of column names
        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]


"""
# Magic methods - Comparison (Assignment 3)

 

# return_list[]
# return_list.append[]


            def __lt__(self, other):
                return_list[]
                for item in list:
                    if self.data < other.data:
                        return True
                    if self.data !< other.data:
                        return False 
                return_list.append[]
                # return (self.data, other.data) < 0
            def __gt__(self, other):
                for item in list:
                    if self.data > other.data:
                        return True
                    if self.data !> other.data:
                        return False 
                return_list.append[]
                # return (self.data, other.data) > 0
            def __eq__(self, other):
                for item in list:
                    if self.data == other.data:
                        return True
                    if self.data != other.data:
                        return False
                return_list.append[]
            # return (self.data, other.data) == 0
            def __le__(self, other):
                for item in list:
                    if self.data <= other.data:
                        return True
                    if self.data !<= other.data:
                        return False 
                return_list.append[]
            # return (self.data, other.data) <= 0
            def __ge__(self, other):
                for item in list:
                    if self.data >= other.data:
                        return True
                    if self.data !>= other.data:
                        return False 
                return_list.append[]
            # return (self.data, other.data) >= 0
            def __ne__(self, other):
                for item in list:
                    if self.data != other.data:
                        return True
                    if self.data == other.data:
                        return False 
                return_list.append[]
            # return (self.data, other.data) != 0
"""

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

    def df_data(self):
        """
        custom function for console testing purposes
        returns a dataframe
        """
        return self.raw_data
    
    # ===== task 3 =====

    def datatype_convertor(self, column_name):
        """
        Master function for converting the string values in the dataset to particular datatype
        By defining the column data type in the init function, we can implement conversion of newer columns
        (task 4 and 5) to be considered while performing the opertions
        """
        
        # converting the headers list into a string for printing in exception block
        all_columns = ' '.join(self.header)
    
        # using the __getitem__ implement in class D-R-Y principle (google it)
        all_values = self.__getitem__(column_name)

        if column_name in self.int_columns:
            all_values = map(convert_to_float, all_values)
        elif column_name in self.date_columns:
            all_values = map(convert_to_datetime, all_values)
        elif column_name in self.str_columns:
            raise Exception("Cannot perform mathematical operation on string datatype column")
        else:
            raise Exception("Invalid column. Please enter valid column",all_columns)

        return all_values
        
    def min(self, column_name):
        """
        pass the column name to the datatype convertor
        and find the min value from the returning list
        """
        all_values = self.datatype_convertor(column_name)
        min_value = min(all_values)

        if column_name in self.int_columns:
            return min_value
        elif column_name in self.date_columns:
            # converting the python datetime object back into a human readable string format
            return datetime.strftime(min_value, "%m/%d/%y %H:%M")
        else:
            # pass the block if the column name in not in the above conditions
            # can add more conditions in the future
            pass

    def max(self, column_name):
        """
        Same as min(). finds the max value
        """
        all_values = self.datatype_convertor(column_name)
        max_value = max(all_values)

        if column_name in self.int_columns:
            return max_value
        elif column_name in self.date_columns:
            return datetime.strftime(max_value, "%m/%d/%y %H:%M")
        else:
            pass

    def median(self, column_name):
        """
        finds the median value in the column eg [1,2,3,4,5] = 3
        """
        if column_name in self.int_columns:
            all_values = self.datatype_convertor(column_name)        
            sorted_values = sorted(all_values)
            center = len(sorted_values) / 2
            if len(sorted_values) % 2 == 0:
                return sum(sorted_values[center - 1:center + 1]) / 2.0
            else:
                return sorted_values[center]
        else:
            raise Exception("no median for date time columns")

    def sum(self, column_name):
        """
        finds the sum of the column eg[1,2,3,4] = 10
        """
        values_sum = 0

        if column_name in self.int_columns:
            all_values = self.datatype_convertor(column_name)
            values_sum = sum(all_values)

            # or
            # for i in all_values:
                # values_sum += i

            return values_sum
        else:
            raise Exception("no Sum for date time columns")

    def mean(self, column_name):
        """
        finds the mean of the column eg[1,2,3,4] = 2.5 
        """
        if column_name in self.int_columns:
            all_values = self.datatype_convertor(column_name)
            mean = sum(all_values)/len(all_values)
            return mean
        else:
            raise Exception("no Mean for date time columns")

    def std(self, column_name):
        """
        finds the standard deviation of the column. (google the formula and add it to the doc strings.)
        """
        if column_name in self.int_columns:        
            all_values = self.datatype_convertor(column_name)
            variance = 0
            values_mean = sum(all_values)/len(all_values)
            
            for element in all_values:
                variance += (element - values_mean) ** 2
            
            variance = variance/len(all_values)
            std = sqrt(variance)
            return std
        else:
            raise Exception("No median for date time columns")

    # ===== task 3 =====
    
    # ===== task 4 =====
    
    def add_rows(self, list_of_rows):
        """
        Input Takes in a list of rows
        Matches the row element lenght with the instance header lenght
        if the lenght is not equal, raises an exception
        else created an ordered dict by zipping the column headers and saves 
        it to the dataframe object
        """

        for row in list_of_rows:
            if len(row) == len(self.header):
                new_row = OrderedDict(zip(self.header, row))
                self.data.append(new_row)
            else:
                raise Exception("New row do not match the existing header count. Please reenter. Existing headers are: ", ' '.join(self.header))
    
    # ===== task 4 =====

    # ===== task 5 =====

    def add_column(self, list_of_values, column_name):
        """
        Function is used to add a new column
        """

        dataframe_count = len(self.data)
        if len(list_of_values) == dataframe_count:

            data_type = None
            while data_type not in ["1","2"]:
                data_type = raw_input("What is the datatype of the new column? Please type 1 or 2\n1.Integer or Float\n2.String\n>> ")
            if data_type == "1":
                self.int_columns.append(column_name)
            else:
                self.str_columns.append(column_name)

            # adding the new column to the headers
            self.header.append(column_name)

            for i, row in enumerate(self.data):
                row.update({column_name: list_of_values[i]})
            

        else:
            raise Exception("New rows do not match the existing row count. Please reenter.")

    # ===== task 5 =====

# Creating a new sort_column function (Assignment 3)

    def sort_column(self, col_name, reverse_order=True):

        print "Sorting for the column name %s \n" % col_name

        if reverse_order:
            print "Sorting in the reverse order"
        else:
            print "Sorting in asc order"

        print '\n'

        if col_name in self.header:
            if col_name in self.str_columns:
                self.data = sorted(self.data, key=lambda x: str(x[col_name]), reverse=reverse_order)
            elif col_name in self.date_columns:
                self.data = sorted(self.data, key=lambda x: convert_to_datetime(x[col_name]), reverse=reverse_order)                
            elif col_name in self.int_columns:
                print "it is a date column"
                self.data = sorted(self.data, key=lambda x: convert_to_float(x[col_name]), reverse=reverse_order)
            pprint.pprint(self.data, indent=4)
        else:
            raise Exception("Header not present")

# Creating a group_by function (Assignment 3)
    def group_by(self, grouping_col, aggr_col, aggr_func):

        print """
                The grouping col is %s and we are running the aggr by %s
            """ % (grouping_col, aggr_col)
        
        if aggr_col not in self.int_columns:
            raise Exception("Aggregate functions are used to compute against a numeric data")
        
        # converting the OrderedDict into a list of dictionaries
        data_dict = [dict(ordered_dict) for ordered_dict in self.data]
        
        # unique grouping columns will be stored in a dictionary
        new_data = {}
        

        for row in data_dict:
            uniq_val = row.get(grouping_col, None)
            agg_val = convert_to_float(row.get(aggr_col, 0))
            
            # if the uniq data dict contains the key,
            # we will append the value to the value array of that key
            # else we will create the key and a value array
            # eg {"Mastercard":[1200], "Visa":[1200, 1300]}
            
            if not new_data.get(uniq_val):
                new_data[uniq_val] = [agg_val]
            else:
                new_data[uniq_val].append(agg_val)

        return_data = []

        for uniq_val, agg_val in new_data.items():
            return_dict = {}
            return_dict[grouping_col] = uniq_val
            return_dict[aggr_col] = aggr_func(agg_val)

            return_data.append(OrderedDict(return_dict))
        
        # print return_data
        return return_data

#helper functions
def mypandas_avg(vals):
    """
    mypandas prefix to avoid default function overriding 
    """
    print "running the AVG aggregate function"
    return sum(vals)/len(vals)

def mypandas_count(vals):
    """
    mypandas prefix to avoid default function overriding 
    """
    print "running the COUNT aggregate function"
    return len(vals)

def mypandas_sum(vals):
    """
    mypandas prefix to avoid default function overriding 
    """
    print "running the SUM aggregate function"
    return sum(vals)

def mypandas_min(vals):
    """
    mypandas prefix to avoid default function overriding 
    """
    print "running the MIN aggregate function"
    return min(vals)

def mypandas_max(vals):
    """
    mypandas prefix to avoid default function overriding 
    """
    print "running the MAX aggregate function"
    return max(vals)



def convert_to_float(value):
    """
    helper function to convert the str into float for numeric columns
    """
    try:
        return float(value.replace(',','').replace('"',''))
    except Exception as e:
        print value
        print "Program broke while converting to int"
        print e

def convert_to_datetime(value):
    """
    helper function to convert the str into datetime object for numeric columns
    """
    try:
        datetime_value = datetime.strptime(value, "%m/%d/%y %H:%M")
        return datetime_value
    except TypeError:
        print "Program broke while converting to int"    

if __name__ == '__main__':
    my_csv = "SalesJan2009.csv"
    # my_csv = 'test2.csv'
    # my_csv = 'test.csv'
    df = DataFrame.from_csv(my_csv)

    # randomly choice the sorting direction
    sorting_direction = choice([True, False])

    pprint.pprint(df.sort_column('Longitude', sorting_direction),indent=4)
    pprint.pprint(df.sort_column('City', sorting_direction),indent=4)
    pprint.pprint(df.sort_column('Transaction_date', sorting_direction),indent=4)

    pprint.pprint(df.group_by('Payment_Type','Price', mypandas_avg), indent=4)
    pprint.pprint(df.group_by('Payment_Type','Price', mypandas_min), indent=4)
    pprint.pprint(df.group_by('Payment_Type','Price', mypandas_max), indent=4)
    pprint.pprint(df.group_by('Payment_Type','Price', mypandas_sum), indent=4)
    pprint.pprint(df.group_by('Payment_Type','Price', mypandas_count), indent=4)
    pprint.pprint(df.group_by('City','Price', mypandas_max), indent=4)
