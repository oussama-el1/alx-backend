#!/usr/bin/env python3
"""
0. Simple helper function
"""


def index_range(page: int, page_size: int) -> tuple:
    """ index_range """
    start_indx = (page - 1) * page_size
    end_endex = start_indx + page_size

    return start_indx, end_endex
