__author__ = 'Aaron'
import datetime

def foo(a_list, idx):
    return a_list[idx]

class Node:
    def __init__(self, cargo=None, next=None):
        self.cargo = cargo
        self.next = next

    def __str__(self):
        return str(self.cargo)

    def print_list(node):
        while node:
            print node
            node = node.next
        return True

    def print_backwards(list):
        if list == None: return

def print_backwards(node):
    if node == None : return
    print_backwards(node.next)
    print node

def date_from_input(user_input,return_dict=False):
    date = str(user_input)
    date_dict = {}
    try:
        day = int(date[8:10])
        month = int(date[5:7])
        year = int(date[:4])
        if day < 10:
            date_dict['day'] = '0' + str(day)
        else:
            date_dict['day'] = str(day)
        if month < 10:
            date_dict['month'] = '0' + str(month)
        else:
            date_dict['month'] =  str(month)

        date_dict['year'] = str(year)

    except ValueError:
        return False

    try:
        d = datetime.date(year,month,day)
    except:
        return False

    if return_dict == True:
        return date_dict
    else:
        return datetime.date(year,month,day)
