import json
import os


class JsonSchemaLoader:

    def __init__(self, schemas_dirs, cache=None, *, schema_file_extension=".schema.json"):
        self.cache = {} if cache is None else cache
        self.schema_file_extension = schema_file_extension
        self._index_begin_file_extension = len(self.schema_file_extension) * -1
        self.schemas_dirs = schemas_dirs
        self.index = None
        self.cache = {}

    def load(self, schema_name):
        if self.index is None:
            self.find_schemas()
        try:
            path = self.index[schema_name]
        except KeyError:
            return FileNotFoundError(f"Schema not found ({schema_name})")

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    def find_schemas(self):
        '''
        Ищем формы для каждого из предустановленных типов, в общем каталог и каталоге устройства
        :param kwargs:
        :return:
        '''

        self.index = {}
        for schemas_dir in self.schemas_dirs:
            # bubot_obj_dir = f'{path1}/BubotObj/ObjSchema'
            # if not os.path.isdir(bubot_obj_dir):
            #     continue
            # schemas_dir = os.path.normpath(f'{bubot_obj_dir}/schema')
            if not os.path.isdir(schemas_dir):
                continue
            schema_list = os.listdir(schemas_dir)
            for schema_name in schema_list:
                if schema_name[self._index_begin_file_extension:] != self.schema_file_extension:
                    continue
                self.index[schema_name[:self._index_begin_file_extension]] = os.path.join(schemas_dir, schema_name)
        pass
