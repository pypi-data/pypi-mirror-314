import perst


data = {
    'foo': 3,
    'bar': 5,
}
perst.dump(data)
perst.load() == data
