from docsie_universal_importer.import_adapter import ImportAdapter


class GitlabImportAdapter(ImportAdapter):
    def import_content(self, file, content):
        print(file)
        print(type(content))