# Python Cookbook, 3rd Ed.
#
# Chapter: Functional Programming Features
# Recipe: Writing recursive generator functions with the yield from statement


def find_value_sketch1(value, node, path=None):
    path = path or []
    match node:
        case dict() as dnode:
            for key in dnode.keys():
                pass  # find_value(value, node[key], path+[key])
            # This may yield multiple values
        case list() as lnode:
            for index in range(len(lnode)):
                pass  # find_value(value, node[index], path+[index])
            # This may yield multiple values
        case _ as pnode:
            # a primitive type
            if pnode == value:
                yield path

def some_client(value, node, key, path):
    for match in find_value_sketch1(value, node[key], path+[key]):
        yield match
