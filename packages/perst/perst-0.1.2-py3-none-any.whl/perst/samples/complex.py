import perst


hosts = perst.elems('./hosts.json', key='name')
hosts.add({'name': 'foo', 'age': 3})
hosts.add({'name': 'bar', 'age': 5})
for host in hosts:
    print(host)
hosts.update('foo', {'age': 8})
for host in hosts:
    print(host)
