"""
This module contains general purpose utility functions used throughout the
library.
"""
from __future__ import absolute_import

from .collections import OrderedDefaultListDict
from .path import join_norm, restore_sys_path
from .equality import nearly_equal, xml_equal
from .validation import (
    check_inferred_against_declared, ensure_valid_identifier,
    assert_no_duplicates)
