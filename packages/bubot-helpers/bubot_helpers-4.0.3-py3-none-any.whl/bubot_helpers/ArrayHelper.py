import copy


class ArrayHelper:
    # делаем список уникальных записей, объединяемые массивы должны быть однотипными
    # списки объектов объединаются по ключевому полю которое есть в первой записи списка
    default_object_uid_props = ['_id', 'id', 'di', 'title', 'name', 'n']

    @classmethod
    def unique_extend(cls, a, b, **kwargs):
        if not len(a):
            return b
        if not len(b):
            return a
        # if isinstance(a[0], str):
        #     for elem in b:
        #         if elem not in a:
        #             a.append(elem)
        #     return a
        if isinstance(a[0], dict):
            object_uid_prop = cls.detect_object_uid_prop(a, kwargs.get('object_uid', cls.default_object_uid_props))
            if object_uid_prop is None:
                c = copy.deepcopy(b)
                a.extend(c)
                return a
            index = cls.index_list(a, object_uid_prop)
            for elem in b:
                uid = elem.get(object_uid_prop)
                if uid not in index:
                    a.append(elem)
            return a
        return b

    @classmethod
    def detect_object_uid_prop(cls, data, object_uid_fields):
        for _key in object_uid_fields:
            if _key in data[0]:
                return _key
        return None

    @classmethod
    def update(cls, items, item, field='id'):
        for i in range(len(items)):
            if items[i][field] == item[field]:
                items[i] = item
                return
        items.append(item)

    @classmethod
    def index_list(cls, items, field='id'):
        res = {}
        for index in range(len(items)):
            try:
                res[items[index][field]] = index
            except KeyError:
                pass
        return res

    @classmethod
    def find_by_key(cls, items, key_value, key_field='id'):
        for i in range(len(items)):
            if items[i].get(key_field) == key_value:
                return i
        return -1

    @classmethod
    def find_one(cls, items, where):
        for i in range(len(items)):
            found = True
            for key in where:
                if items[i].get(key) != where[key]:
                    found = False
                    break
            if found:
                return i
        return -1
