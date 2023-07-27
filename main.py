from UIron.utils import prettify

dictionary = {
    'elements': 118,
    'planets': {
        'mercurio': 1,
        'venus': 2,
        'tierra': 3,
        'marte': 4
    },
    'fingers': [
        'thumb',
        'index',
        'middle',
        'anular',
        'pinky'
    ]
}

# print(dictionary)
print(prettify(dictionary))