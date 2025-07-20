#!/usr/bin/env python3
"""Parameterize a unit test"""
import requests
import unittest
from typing import Dict
from parameterized import parameterized
from unittest.mock import patch, Mock
import memoize

access_nested_map = __import__('utils').access_nested_map
get_json = __import__('utils').get_json


class TestAccessNestedMap(unittest.TestCase):
    """UnitTest Class"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test method that check assertEqual"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a"), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """Test method that check assertRaises"""
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Mocks HTTP Calls"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict,
            ) -> None:
        """Test method for getting JSON"""
        attrs = {'json.return_value': test_payload}
        with patch("requests.get", return_value=Mock(**attrs)) as r_g:
            self.assertEqual(get_json(test_url), test_payload)
            r_g.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests the memoize function."""
    def test_memoize(self) -> None:
        """Tests memoize's output."""
        class TestClass:
            """A random test class"""
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(TestClass, "a_method", returnvalue=42) as pear:
            result1 = TestClass().a_property()
            result2 = TestClass().a_property()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            pear.assert_called_once()