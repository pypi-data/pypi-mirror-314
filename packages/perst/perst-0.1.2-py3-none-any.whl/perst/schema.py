from perst.elems import elems


def schema(spec: list|dict):
    if isinstance(spec, list):
        spec = {'attrs': spec}

    for attr_name, attr_spec in spec['attrs'].items():
        cls_attrs = {}
        match attr_spec['type']:
            case 'elems':
                getter = lambda self: elems(**attr_spec)
        cls_attrs[attr_name] = property(getter)

    return type('Schema', (), cls_attrs)()
