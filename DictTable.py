from collections import UserList
from collections import defaultdict as dd

class DictTable(UserList):
   
    # def filter_lambda(self, filter):
    #     return [i for i in self if all(i in filter and i.get(k) == v for k, v in filter.items())]
        # return lambda x: (x.get(k) == v and v is not None for k, v in filter.items())
    
    #filter = { "field_name": value }
    #projection = { "field_name": 1 }


    def find(
    self, 
    filter=None,            #basic querying parameter
    projection=None,        #basic querying parameter @alex for now realisation is not needed
    sort=None,
    limit=None,
    max=None,
    min=None,
    return_key=False,
    indexes=None
    ):   
        #realisation of filter
        def filter_function(item):
            filtered_items = []
            if indexes is not None and all(key in indexes for key in filter.keys()): 
                for key, value in filter.items():
                    if key in indexes: 
                        for i in indexes[key]:
                            for k, v in i.items():
                                if k == value:
                                    filtered_items.extend(v)
                    else:
                        print("No such key in indexes")
        
                return filtered_items
            
            else:
                for key, value in filter.items():
                    if key not in item or item.get(key) == value:
                        filtered_items.append(item)

                return filtered_items
                                
      
        #realisation of conditional filters
       
        #filter typeproof section   
        if filter is None:
            filter = {}
        elif not isinstance(filter, dict):
            raise TypeError("filter must be a dictionary")

        #projection typeproof section
        if projection is None:
            projection = {}
        elif not isinstance(projection, dict):
            raise TypeError("projection must be a dictionary")
        
        #sort typeproof section
        if sort is None:
            sort = {}
        elif not isinstance(sort, dict):
            raise TypeError("sort must be a dictionary")

        #limit typeproof section  
        if limit is None:
            limit = 0
        elif not isinstance(limit, int) or limit < 0:
            raise ValueError("limit must be a non-negative integer")
        

        # Apply sorting
        results = self.data
        results = filter_function(results)

        #@daria
        # sort = { "field_name": 1 } - ascending
        # sort = { "field_name": not 1 } - descending
        for key, value in sort.items():
            results.sort(key=lambda x: x.get(key, 0), reverse=(value != 1))

        # Apply limit
        if limit > 0:
            results = results[:limit]

        #Apply projection
        if projection != {}:
            results = [{key: item[key] for key in projection if key in item} for item in results]

        return results
        
    #return 1 element as a dictionary
    def find_one(self, filter=None) -> dict:   
            return self.find(filter, limit=1)[0] if self.find(filter, limit=1) else None
    
    def distinct(self, key: str) -> set:
        return set([i[key] for i in self.data if i.get(key, None) != None])
    
    #return index of the key
    def index(self, key: str) -> dict:
        index = dd(list)
        keylist = self.distinct(key)
        for i in keylist:
            for a in self.data:
                if a.get(key) == i:
                    index[i].append(a)
        return index
    
    #def delete_index(self, key: str) -> dd:
        #return self.index(key).clear()
        

   # def __init__(self):
   #     self.indexes = dd(list)
        
   # def add_index(self, key: str):
   #     self.indexes[key].append(data.index(key))
   #     return self.indexes
        
   # def delete_index(self, key: str):
   #     return self.indexes[key].clear()
   #     
   # def find_index(self, key: str):
   #     return self.indexes[key]
   #     
   # def find_all_indexes(self):
   #     return self.indexes
    
    
data = DictTable([
{"name": "Alice", "age": 30, "job": "manager"},
{"name": "Bob", "age": 25, "job": "developer"},
{"name": "Alice", "age": 35, "job": "manager"},
{"name": "Alice", "age": 11, "job": None},
{"name": "Alice", "age": 30, "job": "accountant"},
{"name": "Carol", "age": 30, "job": "developer"},
{"name": "Dan", "age": 33, "job": "developer"}
])



indexes = dd(list)
indexes["name"].append(data.index("name"))
indexes["age"].append(data.index("age"))
indexes["job"].append(data.index("job"))
#print(indexes)
print()
print(data.find(filter={"fam": "abcd"}, indexes=indexes))


