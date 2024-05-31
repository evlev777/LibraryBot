from .connect import get_book
def tuple_to_dict(user_str):
    dict_keys = ['id', 'year', 'name', 'author', 'url']
    user_result = get_book(user_str)
    new_list = []

    for item in user_result:
        new_list.append(dict(zip(dict_keys, item)))
    return new_list