import logging
from google.cloud.datastore import Entity
from google.cloud import datastore


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BATCH_MAX_LIMIT = 500


class DataStoreAPI():
    def __init__(self, kind, project_name, cred):
        self.datastore_client = self._get_datastore_client(project_name, cred)
        self.kind = kind

    def insert(self, data):
        if isinstance(data, list):
            self.batch_insert(data)
        elif isinstance(data, dict):
            self.single_insert(data)

    def single_insert(self, data_map, long_column_list=[]):
        if not isinstance(data_map, dict):
            return None
        if isinstance(data_map, Entity):
            item = data_map
        else:
            item = self.dict_to_entity(data_map, long_column_list)
        self.datastore_client.put(item)
        logger.info('Saved {}: {}'.format(item.key.name, item))

    def batch_insert(self, data_list, long_column_list=()):
        if len(data_list) < 1:
            return None
        if isinstance(data_list[0], Entity):
            item_list = data_list
        else:
            item_list = [self.dict_to_entity(data, long_column_list) for data in data_list]
        for i in range(len(item_list) % BATCH_MAX_LIMIT):
            self.datastore_client.put_multi(item_list[i * BATCH_MAX_LIMIT:BATCH_MAX_LIMIT * (i + 1)])
        logger.info('Saved {} Records'.format(len(item_list)))

    def dict_to_entity(self, dict_data, long_column_list=[]):
        item = datastore.Entity(key=self._get_key(), exclude_from_indexes=long_column_list)
        self.format_dict_data(dict_data)
        item.update(dict_data)
        return item

    def batch_delete(self, key_list):
        for i in range(int(len(key_list) / BATCH_MAX_LIMIT) + 1):
            self.datastore_client.delete_multi(key_list[i * BATCH_MAX_LIMIT:BATCH_MAX_LIMIT * (i + 1)])
        logger.info('{} Records Deleted'.format(len(key_list)))

    def get(self, name):
        key = self._get_key(name)
        record = self.datastore_client.get(key)
        print(record)
        return record

    def _get_key(self, name=None):
        key = self.datastore_client.key(self.kind, name) if name else self.datastore_client.key(self.kind)
        return key

    def update(self, entity, long_column_list=[]):
        try:
            if isinstance(entity, list):
                self.datastore_client.put_multi(entity)
            else:
                if len(long_column_list) > 0:
                    entity.exclude_from_indexes = set(long_column_list)
                self.datastore_client.put(entity)
        except Exception as e:
            logger.error('DataStore Update Error:' + str(e))

    def get_query(self, kind=None):
        if kind is None:
            kind = self.kind
        query = self.datastore_client.query(kind=kind)
        return query

    def query_test(self):
        query = self.get_query()
        query.add_filter('app_annie_productid', '=', '20600008550414')
        query.order = ['date']
        result = list(query.fetch(None))
        return result

    def query(self, query_stmt_list, order=None, limit=None):
        query = self.get_query()
        for query_stmt in query_stmt_list:
            query.add_filter(query_stmt[0], query_stmt[1], query_stmt[2])
        if order:
            query.order = order
        entities = query.fetch(limit)
        return entities

    def query_list(self, query_stmt_list, order=None, limit=None):
        entities = self.query(query_stmt_list, order, limit)
        result = list(entities)
        return result

    def format_dict_data(self, dict_data):
        default_value = '-'
        for k, v in dict_data.items():
            if v is None:
                dict_data[k] = default_value

    def _get_datastore_client(self, project_name, cred):
        if cred:
            return datastore.Client.from_service_account_json(cred)
        return datastore.Client(project=project_name)


if __name__ == '__main__':
    kind = 'app_opinion'
    datastore_api = DataStoreAPI(kind)
    datastore_api.get(4504638204149760)
    # datastore_api.query_test()
