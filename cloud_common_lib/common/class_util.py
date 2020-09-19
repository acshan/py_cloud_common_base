def dict_to_obj(dict_item, object):
    item_entity = object()
    for k, v in dict_item.items():
        if hasattr(item_entity, k):
            item_entity.__setattr__(k, v)
