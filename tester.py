import shelve

s = shelve.open('test_shelf')

s['key1'] = 'oneone'
s['key2'] = 'twotwo'

for key in s.keys():
    print(s[key])

print('-----------------')

print(s[key] for key in s.keys())

s.close()
