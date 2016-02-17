__author__ = 'Aaron'

def threeIsFive(x):
    return x + 1

def test_answer():
    #it should be 5
    assert threeIsFive(3) == 5


from django.test.client import Client

