class CustDict(dict):

    def update(self, key, value):
        if key in self:
            self[key] = value
        else:
            pass

    def insert(self, key, value):
        if key not in self:
            self[key] = value
        else:
            pass

#==========================================================
