import json

class Element:
    def __init__(self):
        self.locator = ''
        self.name = ''

def load_json(filename):
    with open(filename, 'r') as f:
        distros_dict = json.load(f)
        return distros_dict

    # try:
    #     dict2 = load_json(distros_dict["import"])
    # finally:


def get_elements(locator):
    return 0

# =========

content = load_json("file1.json")

#print(content["Element1"])
#print(content["import"])
dictEle = {}
doctFind = {}
for k, v in content.items():
    print("current key")
    print(k)
    print("current value")
    print(v)
    try:
        if "import" in k:
            print(v[0])
            print(v[2])
        if "import" not in k:
            print(v)
            dictEle[k] = v

    finally:
        print("=")
print("last dict")
print(dictEle)