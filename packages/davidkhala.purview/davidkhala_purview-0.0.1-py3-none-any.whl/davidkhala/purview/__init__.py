from azure.identity import DefaultAzureCredential
from azure.purview.catalog import PurviewCatalogClient
from davidkhala.purview.entity import Entity, Asset
from davidkhala.purview.relationship import Relationship


class Catalog:
    def __init__(self, **kwargs):
        credentials = DefaultAzureCredential()
        self.client = PurviewCatalogClient("https://api.purview-service.microsoft.com", credentials, **kwargs)

    def assets(self, options: dict = None, raw=True):
        """
        for filter syntax, see in https://learn.microsoft.com/en-us/rest/api/purview/datamapdataplane/discovery/query?view=rest-purview-datamapdataplane-2023-09-01&tabs=HTTP#examples
        :param raw:
        :param options:
        :return:
        """
        if options is None:
            options = {"keywords": "*"}
        r = self.client.discovery.query(search_request=options)
        if raw:
            return r['value']
        else:
            return list(map(lambda value: Asset(value), r['value']))

    def get_entity(self, *, guid=None, type_name=None, qualified_name=None):
        if guid:
            r = self.client.entity.get_by_guid(guid)
        else:
            r = self.client.entity.get_by_unique_attributes(type_name, attr_qualified_name=qualified_name)
        return Entity(r)

    def update_entity(self, _entity: Entity, **kwargs):
        options = {
            'entity': {
                'attributes': {
                    'qualifiedName': _entity.qualifiedName,
                    'name': _entity.name
                },
                'typeName': _entity.type,
                **kwargs,
            }
        }
        return self.client.entity.create_or_update(entity=options)
