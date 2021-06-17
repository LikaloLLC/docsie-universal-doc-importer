class FileSystem():
    def __init__(self, filePath=None, extensions=None):
        self.children = []
        self.extensions = extensions or ['md']
        if filePath != None:
            try:
                self.name, child = filePath.split("/", 1)
                self.children.append(FileSystem(extensions=self.extensions, filePath=child))
            except (ValueError):
                self.name = filePath

    def addChild(self, filePath):
        """
        Recursive function that bind files to folder
        :param: filePath:
        :return: None:
        """
        try:
            thisLevel, nextLevel = filePath.split("/", 1)
            try:
                if thisLevel == self.name:
                    thisLevel, nextLevel = nextLevel.split("/", 1)
            except (ValueError):
                self.children.append(FileSystem(extensions=self.extensions, filePath=nextLevel))
                return
            for child in self.children:
                if thisLevel == child.name:
                    child.addChild(filePath=nextLevel)
                    return
            self.children.append(FileSystem(extensions=self.extensions, filePath=nextLevel))
        except (ValueError):
            self.children.append(FileSystem(extensions=self.extensions, filePath=filePath))

    def getChildren(self):
        return self.children

    def printAllChildren(self, depth=-1):
        """
        Print data pretty
        :param depth, default=-1
        :return: data:
        """
        depth += 1
        print("\t" * depth + "Name: " + self.name)
        if len(self.children) > 0:
            print("\t" * depth + "{ Children:")
            for child in self.children:
                child.printAllChildren(depth)
            print("\t" * depth + "}")

    def _buildDict(self):
        """
        Recursive function that Built dict from file names of the repo:
        :param: None:
        :return: data:
        :rtype: dict:
        """
        if len(self.children) > 0:
            dictionary = {self.name: []}
            for child in self.children:
                dictionary[self.name].append(child._buildDict())
            return dictionary
        else:
            return self.name

    def buildDict(self):
        """
        Make filtered data
        :param: None:
        :return: data:
        :rtype: dict:
        """
        #  Get data from buildDict method and check if data is empty
        #  it returns data like this { repo_name : []}
        data = self._buildDict()
        repo_name = '/'.join(list(data)[0].split('-')[:2])
        result = self.filter_by_extension(data)
        if result == {}:
            result[repo_name] = []
        else:
            answer = dict()
            for key, value in result.items():
                answer[repo_name] = value
            result = answer
        return result

    def filter_by_extension(self, data: dict) -> dict:
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
                    res = self.filter_by_extension(value)
                    for k, v in value.items():
                        ext_files.append(res)
                else:
                    cnt = 0
                    for ext in self.extensions:
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
