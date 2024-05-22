class HashMap:
    def __init__(self):
        self.size = 128
        self.map = [None] * self.size
        self.length = 0

    def __index__(self, usr_input):
        pre = 0
        usr_input = str(usr_input)

        for c in usr_input:
            pre += ord(c)
        return pre % self.size

    def keys(self):
        key_list = []
        for bucket in self.map:
            if bucket:
                for kv in bucket:
                    key_list.append(kv[0])
        return key_list

    # add a pair to hashmap
    def add(self, key, valu):
        hashm = self.__index__(key)

        value = [key, valu]

        if self.map[hashm] is None:
            self.map[hashm] = [value]
            self.length += 1
        else:
            found = False
            for KVPair in self.map[hashm]:
                if KVPair[0] == key:
                    KVPair[1] = valu
                    found = True
                    break
            if not found:
                self.map[hashm].append(value)
                self.length += 1

    # retrieve a pair from the hashmap
    def get(self, key):
        hashm = self.__index__(key)

        if self.map[hashm] is None:
            return None

        for KVPair in self.map[hashm]:
            if KVPair[0] == key:
                return KVPair[1]

        return None

    # delete a pair from hashmap

    def dlt(self, key):
        hashm = self.__index__(key)

        if self.map[hashm] is None:
            return False

        for i in range(len(self.map[hashm])):
            if self.map[hashm][i][0] == key:
                self.map[hashm].pop(i)
                self.length -= 1
                return True

        return False

    # print function
    def pnt(self, key):
        hashm = self.__index__(key)

        if self.map[hashm] is None:
            print("Key not found")
            return

        for item in self.map[hashm]:
            if item[0] == key:
                print(item[1])
                return

        print("Key not found")
