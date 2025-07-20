#!/usr/bin/env python3
'''unitest file'''
import unittest
from parameterized import parameterized
from unittest.mock import Mock, patch
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
    Tuple,
    Union,
)
from utils import (
    access_nested_map,
    get_json,
    memoize,
)


class TestAccessNestedMap(unittest.TestCase):
    '''TestAccessNestedMap class'''
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Dict,
        path: Tuple[str],
        expected: Union[Dict, int]
    ) -> None:
        '''test_access_nested_map method'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Dict,
        path: Tuple[str],
        exception: Exception,
    ) -> None:
        '''test_access_nested_map_exception method'''
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''TestGetJson class'''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict,
    ) -> None:
        '''test_get_json method'''
        atrbs = {'json.return_value': test_payload}
        with patch("requests.get", return_value=Mock(**atrbs)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    '''TestMemorize class'''
    def test_memoize(self) -> None:
        '''test_memoize method'''
        class TestClass:
            '''TestClass class'''
            def a_method(self):
                '''a_method method'''
                return 42

            @memoize
            def a_property(self):
                '''a_property method'''
                return self.a_method()
        with patch.object(
                TestClass,
                "a_method",
                return_value=lambda: 42,
                ) as memo_fxn:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            memo_fxn.assert_called_once()
