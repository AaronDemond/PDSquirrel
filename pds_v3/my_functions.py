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
    day = int(date[8:10])
    month = int(date[5:7])
    year = int(date[:4])
    return datetime.date(year,month,day)
