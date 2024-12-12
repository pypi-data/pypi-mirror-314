from typing import List, Any, Generator

def list_duplicates(input_list : List[Any]) -> List[Any]:
    seen = set()
    dupes = []

    for x in input_list:
        if x in seen:
            dupes.append(x)
        else:
            seen.add(x)
    
    return dupes

def remove_duplicates(input_list: List[Any]) -> List[Any]:
    return list(dict.fromkeys(input_list))

def divide_chunks(input_list: List[Any], size: int) -> List[List[Any]]:
    return list(_yield_chunks(input_list, size))

def _yield_chunks(input_list: List[Any], size: int) -> Generator[List[List[Any]], None, None]:
    # looping till length l
    for i in range(0, len(input_list), size): 
        yield input_list[i:i + size]
