import json

from davidkhala.purview import Catalog, Entity, Relationship


class Lineage(Catalog):

    def table(self, _entity: Entity, upstreams, downstreams):
        """
        create table lineage relationships
        :param _entity:
        :param upstreams:
        :param downstreams:
        :return:
        """
        sources = [{'guid': _id} for _id in upstreams] if upstreams else []
        sinks = [{'guid': _id} for _id in downstreams] if downstreams else []
        r = self.update_entity(_entity, relationshipAttributes={
            'sources': sources,
            'sinks': sinks
        })
        if r.get('mutatedEntities'):
            return r['mutatedEntities']['UPDATE']
        else:
            return r['guidAssignments']

    def column(self, _relationship: Relationship, columns):
        """
        create column lineage relationships
        :param _relationship:
        :param columns:
        :return:
        """
        column_mapping = json.dumps([
            {'Source': key, 'Sink': value or key} for key, value in columns.items()
        ])

        return self.client.relationship.update({
            'guid': _relationship.guid,
            'typeName': _relationship.typeName,
            'attributes': {
                'columnMapping': column_mapping,
            }
        })
