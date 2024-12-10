from typing import NamedTuple, Optional, Dict, Any


class SearchQuery(NamedTuple):
    """
    SearchQuery represents the query when searching within a specific namespace.
    """

    inputs: Dict[str, Any]
    """
    The input data to search with.
    Required.
    """

    top_k: int
    """
    The number of results to return with each search.
    Required.
    """

    filter: Optional[Dict[str, Any]] = None
    """
    The filter to apply to the search.
    Optional.
    """

    def as_dict(self):
        """
        Returns the SearchQuery as a dictionary.
        """
        return self._asdict()
