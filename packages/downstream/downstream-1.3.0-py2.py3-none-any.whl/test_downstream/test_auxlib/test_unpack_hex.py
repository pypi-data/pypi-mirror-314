import numpy as np

from downstream._auxlib._unpack_hex import unpack_hex


def test_unpack_hex_valid_input():
    hex_str = "00FF00FABF00FF00"
    num_items = 2
    expected_output = np.array([0x00FF00FA, 0xBF00FF00], dtype=np.uint64)
    result = unpack_hex(hex_str, num_items)
    np.testing.assert_array_equal(result, expected_output)


def test_unpack_hex_padded_result():
    hex_str = "AA55AA55AA"
    num_items = 1
    expected_output = np.array([0xAA55AA55AA], dtype=np.uint64)
    result = unpack_hex(hex_str, num_items)
    np.testing.assert_array_equal(result, expected_output)


def test_unpack_hex_single_item():
    hex_str = "FFFFFFFFFFFFFFFF"
    num_items = 1
    expected_output = np.array([0xFFFFFFFFFFFFFFFF], dtype=np.uint64)
    result = unpack_hex(hex_str, num_items)
    np.testing.assert_array_equal(result, expected_output)


def test_unpack_hex_multiple_items():
    hex_str = "0123456789ABCDEF0123456789ABCDEF"
    num_items = 2
    expected_output = np.array(
        [0x0123456789ABCDEF, 0x0123456789ABCDEF], dtype=np.uint64
    )
    result = unpack_hex(hex_str, num_items)
    np.testing.assert_array_equal(result, expected_output)


def test_unpack_hex_short_hex_string():
    hex_str = "FF"
    num_items = 1
    expected_output = np.array([0xFF], dtype=np.uint64)
    result = unpack_hex(hex_str, num_items)
    np.testing.assert_array_equal(result, expected_output)


def test_unpack_hex_4bit_items():
    hex_str = "F0F0"
    num_items = 4
    expected_output = np.array([0xF, 0x0, 0xF, 0x0], dtype=np.uint64)
    result = unpack_hex(hex_str, num_items)
    np.testing.assert_array_equal(result, expected_output)


def test_unpack_hex_1bit_items():
    hex_str = "F8"
    num_items = 8
    expected_output = np.array([1, 1, 1, 1, 1, 0, 0, 0], dtype=np.uint64)
    result = unpack_hex(hex_str, num_items)
    np.testing.assert_array_equal(result, expected_output)


def test_unpack_hex_2bit_items():
    hex_str = "F8"
    num_items = 4
    expected_output = np.array([3, 3, 2, 0], dtype=np.uint64)
    result = unpack_hex(hex_str, num_items)
    np.testing.assert_array_equal(result, expected_output)
