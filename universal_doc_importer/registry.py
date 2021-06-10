from swag_auth.registry import ConnectorRegistry


class CustomConnectorRegistry(ConnectorRegistry):
    def get_list(self):
        self.load()
        return [connector_cls for connector_cls in self.connector_map.values()]

    def by_id(self, provider_id):
        return self.connector_map[provider_id]


registry = ConnectorRegistry('universal_doc_importer')
