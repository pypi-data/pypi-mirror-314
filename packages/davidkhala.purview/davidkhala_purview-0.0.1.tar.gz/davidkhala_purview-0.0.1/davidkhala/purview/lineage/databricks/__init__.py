from davidkhala.purview import Asset
from davidkhala.purview.lineage import Lineage


class Notebook(Asset):

    @property
    def notebook_id(self):
        """
        object_id in Databricks API
        :return:
        """
        return self.qualifiedName.split('/')[-1]


class Databricks:
    def __init__(self, l: Lineage):
        self.l = l

    def notebooks(self) -> list[Notebook]:
        values = self.l.assets({
            "filter": {
                "or": [{"entityType": "databricks_notebook"}]
            }
        })
        return list(map(lambda value: Notebook(value), values))

    def notebook_rename(self, notebook: Notebook, new_name: str):
        e = notebook.as_entity()
        e.name = new_name
        return self.l.update_entity(e)
