class FileSystem():
    def __init__(self, filePath=None):
        self.children = []
        if filePath != None:
            try:
                self.name, child = filePath.split("/", 1)
                self.children.append(FileSystem(child))
            except (ValueError):
                self.name = filePath

    def addChild(self, filePath):
        try:
            thisLevel, nextLevel = filePath.split("/", 1)
            try:
                if thisLevel == self.name:
                    thisLevel, nextLevel = nextLevel.split("/", 1)
            except (ValueError):
                self.children.append(FileSystem(nextLevel))
                return
            for child in self.children:
                if thisLevel == child.name:
                    child.addChild(nextLevel)
                    return
            self.children.append(FileSystem(nextLevel))
        except (ValueError):
            self.children.append(FileSystem(filePath))

    def getChildren(self):
        return self.children

    def printAllChildren(self, depth=-1):
        depth += 1
        print("\t" * depth + "Name: " + self.name)
        if len(self.children) > 0:
            print("\t" * depth + "{ Children:")
            for child in self.children:
                child.printAllChildren(depth)
            print("\t" * depth + "}")

    def makeDict(self):
        dictionary = {self.name: []}
        if len(self.children) > 0:
            for child in self.children:
                dictionary[self.name].append(child.makeDict())

        return dictionary

    def filter_by_extension(self, data: dict, extensions: list) -> dict:
        """
        Return filtered data by extensions
        :param data, extensions:
        :return: data:
        :rtype: dict:
        """
        del_keys = []
        for key, values in data.items():
            ext_files = []
            for value in values:
                if isinstance(value, dict):
                    res = self.filter_by_extension(value, extensions=extensions)
                    for k, v in value.items():
                        ext_files.append(res)
                else:
                    cnt = 0
                    for ext in extensions:
                        if value.endswith(ext):
                            cnt += 1
                            ext_files.append(value)
            values = ext_files
            if ext_files == []:
                del_keys.append(key)
            else:
                data[key] = values
        for key in del_keys:
            del data[key]

        return data
