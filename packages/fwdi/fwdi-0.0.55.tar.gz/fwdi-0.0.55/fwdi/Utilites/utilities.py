class Utilities():
    
    @staticmethod
    def search_key(lst_param:list, key:str)->bool:
        search_item_key = [item for item in lst_param if item['name'] == key]
        if len(search_item_key) > 0:
            return True
        else:
            return False