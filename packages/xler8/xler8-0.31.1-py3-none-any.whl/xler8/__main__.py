import xler8

xler8.out(
    "test1.xlsx",
    sheets={
        'blatt1': {
            'data': [['A', 'B', 'C'],['120', '121', '122'],['8', '8', '8']],
            'cw':{'A': 50}
        }
    }
)

xler8.out(
    "test2.xlsx",
    sheets={
        'blatt1': {
            'data': [['A', 'B', 'C'],['12', '12', '12'],['8', '8', '8']],
            'cw':{'A': 50}
        }
    }
)
