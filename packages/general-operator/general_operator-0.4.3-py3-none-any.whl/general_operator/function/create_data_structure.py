def create_update_dict(create: bool = True, update: bool = True, delete: bool = False, sql: bool = True, temp: bool = False) -> dict:
    result = dict()
    if create:
        result["create_list"] = []
    if update:
        result["update_list"] = []
    if sql:
        result["sql_list"] = []
    if delete:
        result["delete_id_set"] = set()
        result["delete_data_list"] = []
    if temp:
        result["temp_list"] = []
    return result


def create_delete_dict():
    return {
        "id_set": set(),
        "data_list": []
    }
    
class CreateUpdateClass():
    def __init__(self, create: bool = False, update: bool = False, delete: bool = False, sql: bool = False, temp: bool = False) -> None:
        '''
        Store schema data into create_list, update list, delete_list
        Store sql model into sql_list
        '''
        if create:
            self.create_list = []
        if update:
            self.update_list = []
        if sql:
            self.sql_list = []
        if delete:
            self.delete_id_set = set()
            self.delete_list = []
        if temp:
            self.temp_list = []
