import os

def lcog(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        lines = [line.strip().rstrip(';') for line in f if line.strip()]
        return {k.strip(): v.strip().strip("'") for k, v in (line.split(':', 1) for line in lines)}

def scog(path, data):
    with open(path, 'w') as f:
        for k, v in data.items():
            f.write(f"{k}: '{v}';\n")


def acog(path, k, v):
    data = lcog(path)
    data[k] = v
    scog(path, data)

def ecog(path, k, v):
    data = lcog(path)
    if k in data:
        data[k] = v
    scog(path, data)

def rcog(path, k):
    data = lcog(path)
    if k in data:
        del data[k]
    scog(path, data)

def fcog(path, k):
    return lcog(path).get(k)
