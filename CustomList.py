import numpy as np

class CustomList:
    def __init__(self, file_name):
        self.readFile(file_name)
        self.display_list()

    def readFile(self, file_name):
        self.data = np.loadtxt(file_name, dtype=str) #, delimiter="\n")
        self.data = np.char.lower(self.data)

    def in_list(self, site):
        index = np.array( np.where(self.data == np.char.lower(site)) )
        return index.size > 0

    def display_list(self):
        for i, l in enumerate(self.data):
            print(i, ": ", l)
        
    def __str__(self):
        item_str = ""
        for l in self.data:
            item_str += l + ", "
        return item_str

#ll = CustomList("./ignore_domains.txt")

#ll.list()

#print(ll)

#print("True", ll.in_list("ally.com"))
#print("False", ll.in_list("alllly.com"))
