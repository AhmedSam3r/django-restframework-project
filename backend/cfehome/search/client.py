from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def get_index(index_name='al_search_Product'):
    client = get_client()
    # our Index name al_search_Product
    index = client.init_index(index_name)
    return index


def perform_search(query, **kwargs):
    """
        we want it to be like:
        perform_search('hello', tag=["electronics"], public=True)
        Examples:
            perform_search('hello', public=False)
            perform_search('meow', tag=['goods'], public=False)
            perform_search('hello', tag=['goods'], public=True)
    """
    index = get_index()
    params = {}  # to narrow down our search
    if "tag" in kwargs:
        params["tagFilters"] = kwargs.pop('tag') or []  # 1)we can now search by tags
    print("kwargs.items() = ",kwargs.items())
    index_filters = [f"{k}:{v}" for k, v in kwargs.items() if v is not None] # to handle boolean which is False
    print("index_filters = ", index_filters)
    print("params = ", params)
    if len(index_filters) != 0:
        params["facetFilters"] = index_filters  # 2) then filter it by any given arguments that we might have
    results = index.search(query, params)
    return results
