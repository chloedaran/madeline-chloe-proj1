# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 16:09:52 2021

@author: ashbu
"""

# Your name: Madeline Trumbauer 
# Your student id: 30608756
# Your email: madzt@umich.edu
# List who you have worked with on this project:Chloe Darancou

import io
import sys
import csv
import unittest
import os
          

def read_csv(file):
    '''
    Function to read in a CSV

    Parameters
    ----------
    file : string
        the name of the file you're reading in

    Returns
    -------
    data_dict : dict
        the double-nested dictionary that holds the data from the csv.

    '''
    
    data_dict = {}
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    with open(path + file, "r") as f:
        #reads in data, separating items as commas and automatically breaks rows at /n
        csv_reader = csv.reader(f, delimiter = ",")
        race_index = 1
        row_count = 0
        #for each row in csv reader
        for row in csv_reader:
            var1 = 0
            #if you're on the 1st row, set info in first row as a list to headers
            if row_count == 0:
                #stores all headers as a list that we can iterate through
                headers = row
                row_count += 1
            else:
                for item in row:
                    #if we're at the first index of our item at our row, set the info to state variable. (one at a time)
                    if var1 == 0:
                        state = item 
                        #bc first item at index 0 is the state
                        data_dict.setdefault(state, {})
                        var1 += 1
                        #access state directly if it isn't already in dictionary
                    else:
                        data_dict[row[0]][headers[var1]] = int(item)
                        #data_dict[row[0]].setdefault(headers[var1], int(item))
                        # for i in headers:
                        #     data_dict[state][i].setdefault(headers[i], int(item))
                        var1 += 1
                       
    return data_dict
                
    # write your code here that does things
    # it should read in the lines of data
    # it should also seperate the first row as header information
    # at the same time, it should grab the first item as the state information
    # the end result of the data should be formated like so
    # ex: (ap_dict) {“Alabama”: {“AMERICAN INDIAN/ALASKA NATIVE”: 1, “ASIAN”: 61,...},...}
                           
    


def pct_calc(data_dict):
    '''
    Function to compute demographic percentages
    Parameters
    ----------
    data_dict : dict
        the dictionary you're passing in. Should be the data dict from the 
        census or AP data. 

    Returns
    -------
    pct_dict: dict
        the dictionary that represents the data in terms of percentage share 
        for each demographic for each state in the data set.
    '''
    
    # declaring dict to hold pct vals
    pct_dict = {}
    for key in data_dict:
        pct_dict.setdefault(key, {})
        #for each key which is the state, it is set to an empty dictionary
        for demo in data_dict[key]:
            if demo != "State Totals" and demo != "NO RESPONSE":
                num = ((data_dict[key][demo])/(data_dict[key]["State Totals"])) * 100
                pct_dict[key][demo] = round(num,2)

    return(pct_dict)
    # write in code here
    # it should take the number for each demographic for each state and divide it by the state total column
    # ex: value = ensus_data["Alabama"]["WHITE]/census_data["Alabama]["State Totals"]
    # ex: round(value * 100, 2))            
   


def pct_dif(data_dict1, data_dict2):
    pct_diff_dict = {}
    for key in data_dict1:
        key2 = key.replace("-", " ")
        pct_diff_dict.setdefault(key, {})
        for value in data_dict1[key]:
            if data_dict1[key] != "State Totals" and data_dict1[key] != "NO RESPONSE":
                if value in data_dict2[key2]:
                    diff = data_dict1[key][value] - data_dict2[key2][value]
                    diff = abs(round(diff, 2))
                    pct_diff_dict[key][value] = diff #Sets value in data_dict1 = diff when it should only set value in pct_diff_dict = diff
    return pct_diff_dict

    
    # creating the dictionary to hold the pct diferences for each "cell"
    # write code here
    # it should subtract the % val of each val in the 2nd dict from the 1st dict
    # it should take the absolute value of that difference and round it to 2 decimal places
    # ex: value = ap_data["Alabama"]["WHITE] - census_data["Alabama"]["WHITE] 
    # ex: abs(round(value, 2))
    # hint: you want to have a way to deal with the difference in naming conventions
    # ex: "North Carolina" vs "North-Carolina" string.replace is your friend
    
def csv_out(data_dict, file_name):
    '''
    Function to write output to a file    

    Parameters
    ----------
    data_dict : dict
        the data dictionary you are writing to the file. In this case, 
        the result from pct_dif_dict
        
    file_name : str
        the name of the file you are writing.

    Returns
    -------
    None. (Doesn't return anything)
    '''
    dir = os.path.dirname(__file__)
    outFile = open(os.path.join(dir, file_name), "w")
    with open(file_name, "w", newline="") as fileout:
        csv_writer = csv.writer(outFile, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)

        for key in data_dict:
            #write the whole row from the dict
            first_row = [key] + list(data_dict[key].values())
            csv_writer.writerow(first_row)

        header = ["State"] + list(data_dict["Alabama"].keys())
        # you'll want to write the rest of the code here
        # you want to write the header info as the first row 
        # you want to then write each subsequent row of data 
        # the rows will look like this
        # ex: Alabama,0.2,18.32,21.16,2.17,0.05,3.58,1.98,1.45
    pass
            
def max_min_mutate(data_dict, col_list):
    # Do not change the code in this function
    '''
    function to mutate the data to simplify sorting

    Parameters
    ----------
    data_dict : dict
        dictionary of data passed in. In this case, it's the 
    col_list : list
        list of columns to mutate to.

    Returns
    -------
    demo_vals: dict
        DESCRIPTION.

    '''
    # Do not change the code in this function
    demo_vals = {}
    
    for demo in col_list:
        demo_vals.setdefault(demo, {})
        
        for state in data_dict:
            demo_vals[demo].setdefault(state, data_dict[state][demo])
    print(demo_vals)   
    return(demo_vals)

def max_min(data_dict):
    '''
    function to find the 5 max and min states & vals for each demographic

    Parameters
    ----------
    data_dict : dict
        the data_dictionary you're passing in. In this case, the mutated dict

    Returns
    -------
    max_min: 
        a triple nested dict with the this basic format
        {"max":{demographic:{"state":value}}}
    '''
    max_min = {"max":{},"min":{}}
    #CORRECT but need to exclude State Totals and NO RESPONSE 
    for demo in data_dict:
        demo = {}
        if demo != "State Totals" or demo != "NO RESPONSE":
            for i in data_dict:
                value = data_dict[i]
                sorted_list = sorted(value.items(), key = lambda x: x[1], reverse = True)
                sorted_list = dict(sorted_list[0:5])
                demo[i] = sorted_list
        max_min["max"] = demo  
        for demo in data_dict:
            demo = {}
            for i in data_dict:
                value = data_dict[i]
                sorted_list = sorted(value.items(), key = lambda x: x[1])
                sorted_list = dict(sorted_list[0:5])
                demo[i] = sorted_list
        max_min["min"] = demo
    return(max_min)
        
    
    # fill out the code in between here
    # you'll want to make code to fill the dictionary
    # the second inner layer will look like {"max":{demographic:{}}
    # the innermost layer will look like {demographic:{"state":value}}
    
    # printing and returning the data
    #print(max_min)

def nat_pct(data_dict, col_list):
    '''
    EXTRA CREDIT
    function to calculate the percentages for each demographic on natl. level    

    Parameters
    ----------
    data_dict : dict
        the data dictionary you are passing in. Either AP or Census data
    col_list : list
        list of the columns to loop through. helps filter out state totals cols

    Returns
    -------
    data_dict_totals
        dictionary of the national demographic percentages

    '''
    data_dict_totals = {}
    
    # fill out code here
    # you'll want to add the demographics as the outerdict keys
    # then you'll want to cycle through the states in the data dict
    # while you're doing that, you'll be accumulating the totals for each demographic
    # you'll then convert each value to a demographic percentage
    # finally, you'll return the dictionary
    pass                                           
    return(data_dict_totals)
        
def nat_dif(data_dict1, data_dict2):
    '''
    EXTRA CREDIT
    function to calculate the difference on the national level

    Parameters
    ----------
    data_dict1 : dict
        the first data dict you are passing in
    data_dict2 : dict
        the 2nd data dict you are passing in.

    Returns
    nat_dif: dict
        the dictionary consisting of the demographic difference on natl. level
    
    '''
    nat_dif = {}
    
    # fill out code here
    # you'll want to remove the state totals 
    # then you'll want to loop through both dicts and find the differences
    # finally, you'll want to return those differences
     
    return(nat_dif)
             
def main():
    # reading in the data
    ap_data = read_csv("ap_cleaned.csv")
    census_data = read_csv("census_cleaned.csv")
    
    # computing demographic percentages
    ap_pct = pct_calc(ap_data)
    print(ap_pct["Alabama"]["ASIAN"])
    census_pct = pct_calc(census_data)
    print(ap_pct["Alabama"]["ASIAN"])
    # computing the difference between test taker and state demographics
    pct_dif_dict = pct_dif(ap_pct, census_pct)
    print(ap_pct["Alabama"]["ASIAN"])
    # outputing the csv
    csv_out(pct_dif_dict, "HW5V1.csv")
        
    # creating a list from the keys of inner dict
    col_list = list(pct_dif_dict["Alabama"].keys())
    
    # mutating the data
    mutated = max_min_mutate(pct_dif_dict, col_list)
    
    # finding the max and min vals
    max_min_vals = max_min(mutated)
        
    # extra credit
    # providing a list of col vals to cycle through
    col_list = census_data["Alabama"].keys()
    
    # computing the national percentages
    ap_nat_pct = nat_pct(ap_data, col_list)
    census_nat_pct = nat_pct(census_data, col_list)    
    
    print(ap_nat_pct)
    print(census_nat_pct)
    
    # computing the difference between them
    dif = nat_dif(ap_nat_pct, census_nat_pct)
        
    print("Difference between AP Comp Sci A and national demographics:\n",
          dif)
        
main()

# unit testing
# Don't touch anything below here
class HWTest(unittest.TestCase):
    
    def setUp(self):
        # surpressing output on unit testing
        suppress_text = io.StringIO()
        sys.stdout = suppress_text 
        
        # setting up the data we'll need here
        # basically, redoing all the stuff we did in the main function
        self.ap_data = read_csv("ap_cleaned.csv")
        self.census_data = read_csv("census_cleaned.csv")
        
        self.ap_pct = pct_calc(self.ap_data)
        self.census_pct = pct_calc(self.census_data)
        
        self.pct_dif_dict = pct_dif(self.ap_pct, self.census_pct)
        
        self.col_list = list(self.pct_dif_dict["Alabama"].keys())

        self.mutated = max_min_mutate(self.pct_dif_dict, self.col_list)
        
        self.max_min_val = max_min(self.mutated)
        
        # extra credit
        # providing a list of col vals to cycle through
        self.col_list = self.census_data["Alabama"].keys()
        
        # computing the national percentages
        self.ap_nat_pct = nat_pct(self.ap_data, self.col_list)
        self.census_nat_pct = nat_pct(self.census_data, self.col_list)    
        
        self.dif = nat_dif(self.ap_nat_pct, self.census_nat_pct)
        
    # testing the csv reading func is working properly
    def test_read_csv(self):
         test = read_csv("ap_cleaned.csv")
         self.assertEqual(test["Alabama"]["ASIAN"], 61)
         
    # testing the pct_calc function
    def test_pct_calc(self):
        self.assertEqual(pct_calc({"state":{"demo":5,"State Totals":10}}), 
                         {"state":{"demo": 50.0}})

    # second test on the pct_calc function
    # fails because my value is wrong (doh!);
    # change it to correct value.
    def test2_pct_calc(self):
        self.assertEqual(
            self.ap_pct["Alabama"]["ASIAN"], 
            19.68)

    # testing the pct_dif function
    def test_pct_dif(self):
        self.assertEqual(
            pct_dif({"state":{"demo":50.0}},{"state":{"demo":50.0}}),
            {'state': {'demo': 0.0}}           
            )
        
    # second test on the pct_dif function
    # needs a valid value though brah
    def test2_pct_dif(self):
        self.assertEqual(
            self.pct_dif_dict["Alabama"]["AMERICAN INDIAN/ALASKA NATIVE"],
            0.2)
    
    # testing the max_min function
    def test_max_min(self):
        self.assertEqual(
            max_min({"demo":{"a":1,"b":2,"c":3,"d":4,"e":5}})
            ,
            {'max': {'demo': {'e': 5, 'd': 4, 'c': 3, 'b': 2, 'a': 1}},
             'min': {'demo': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}}}
            )
        
    # second test on the max_min function
    def test2_max_min(self):
        self.assertEqual(
            self.max_min_val["max"]["BLACK"]["District-of-Columbia"],
            23.92)
    
    # testing the nat_pct extra credit function
    def test_nat_pct(self):
       self.assertEqual(
       nat_pct({"state":{"demo":5,"State Totals":10}},["demo", "State Totals"]),
       {"demo":50.0, "State Totals":10})
        
    # second test for the nat_pct extra credit function
#    def test2_nat_pct(self):
#        self.assertEqual(
#            self.ap_nat_pct["AMERICAN INDIAN/ALASKA NATIVE"], 
#            0.29)
    
    # testing the nat_dif extra credit function
    def test_nat_dif(self):
        self.assertEqual(
            nat_dif({"demo":0.53, "State Totals": 1},{"demo":0.5, "State Totals": 1}),
            {"demo":0.03}
            )
     
    # second test for the nat_dif extra credit function
#    def test2_nat_dif(self):
#       self.assertEqual(
#            self.dif["ASIAN"],
#            27.93)

if __name__ == '__main__':
    unittest.main(verbosity=2)






        

