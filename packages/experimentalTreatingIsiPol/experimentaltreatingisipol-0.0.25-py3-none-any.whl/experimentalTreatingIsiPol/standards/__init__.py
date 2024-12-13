__standards = [

    'standard-ASTM-D7078'
    ,'standard-ASTM-D7264' 
    ,'standard-ASTM-D3039'
    ,'standard-ASTM-D638'

]


def print_standards():
    '''
    Prints the avaliable standards: 
    '''
    for each_s in __standards:
        print(f'''
=======================================
STANDARD_NAME : {each_s}
=======================================
''')