#!/usr/bin/env python3
"""
2. Hypermedia pagination
"""
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """ index_range """
    start_indx = (page - 1) * page_size
    end_endex = start_indx + page_size

    return start_indx, end_endex


class Server:
    """
    Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        get_page
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        strat_idx, end_idx = index_range(page, page_size)
        self.dataset()
        if end_idx > len(self.__dataset):
            return []
        return self.__dataset[strat_idx:end_idx]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
            Hypermedia pagination
        """
        hypermedia_dict = {}

        data = self.get_page(page, page_size)

        hypermedia_dict['page_size'] = page_size
        hypermedia_dict['page'] = page
        hypermedia_dict['data'] = data

        next_start, next_end = index_range(page + 1, page_size)

        hypermedia_dict['next_page'] = page + 1\
            if next_end <= len(self.__dataset)else None
        hypermedia_dict['prev_page'] = page - 1\
            if page > 1 else None
        hypermedia_dict['total_pages'] = (
            math.ceil(len(self.__dataset) / page_size))

        return hypermedia_dict
