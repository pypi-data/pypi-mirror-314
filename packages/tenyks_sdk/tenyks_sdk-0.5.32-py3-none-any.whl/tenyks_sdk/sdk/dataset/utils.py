from typing import Dict, List, Union


def split_dict_into_batches(
    data: Dict[str, Union[int, float]], batch_size: int
) -> List[Dict[str, Union[int, float]]]:
    items = list(data.items())
    return [dict(items[i : i + batch_size]) for i in range(0, len(items), batch_size)]
