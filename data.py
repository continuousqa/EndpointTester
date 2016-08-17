from random import randint

''' Below is example data ONLY.  Replace the data with what your endpoints expect'''
x = randint(101,999)
evil = ''
endpoint1 = {
                     'id': '',
                     'description': evil,  #evil will be replaced with the injections
                     'isCustom=false': 'false',
                     'nextAction': '2',
             }
endpoint2 = {
                  'id': '',
                  'description': evil,
                  'email': evil,
                  'action1': 245,
                  'action2': 245,
                  'action3': 245,
                  'action4': 245,
                  'action5': 245,
                  'action6': 245,
                  'action7': 245,
                  'action8': 245,
                  'action0': 245,
            }

