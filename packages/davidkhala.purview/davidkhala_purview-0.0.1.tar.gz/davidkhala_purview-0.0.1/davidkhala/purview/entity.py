from davidkhala.purview.relationship import Relationship


class Asset:
    def __init__(self, value: dict):
        self.score = value["@search.score"]
        self.assetType = value['assetType'][0]
        self.collectionId = value['collectionId']
        self.domainId = value['domainId']
        self.entityType = value['entityType']
        self.id = value['id']
        self.name = value['name']
        self.qualifiedName = value['qualifiedName']

    def as_entity(self):
        return Entity({
            'entity': {
                'guid': self.id,
                'attributes': {
                    'name': self.name,
                    'qualifiedName': self.qualifiedName,
                },
                'typeName': self.entityType,
            },
            'referredEntities': None
        })


class Entity:
    def __init__(self, body: dict):
        self.entity = body['entity']
        self.referredEntities = body['referredEntities']

    @property
    def guid(self):
        return self.entity['guid']

    @property
    def name(self):
        return self.entity['attributes']['name']

    @name.setter
    def name(self, value):
        self.entity['attributes']['name'] = value

    @property
    def qualifiedName(self):
        return self.entity['attributes']['qualifiedName']

    @property
    def id(self):
        return self.guid

    @property
    def relationship(self):
        return self.entity['relationshipAttributes']

    def relation_by_source_id(self, guid):
        found = next((source for source in self.relationship['sources'] if source['guid'] == guid), None)
        if found:
            return Relationship(found.get('relationshipGuid'), found.get('relationshipType'))

    def relation_by_sink_id(self, guid):
        found = next((sink for sink in self.relationship['sinks'] if sink['guid'] == guid), None)
        if found:
            return Relationship(found.get('relationshipGuid'), found.get('relationshipType'))

    @property
    def upstream_relations(self):
        return [source['relationshipGuid'] for source in self.relationship['sources']]

    @property
    def downstream_relations(self):
        return [sink['relationshipGuid'] for sink in self.relationship['sinks']]

    @property
    def type(self):
        return self.entity['typeName']

    @property
    def entityType(self):
        return self.type
