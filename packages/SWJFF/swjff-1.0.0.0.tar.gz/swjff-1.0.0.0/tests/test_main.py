# This test is not a unittest or pytest standard
# But manual python execution from your terminal

import sys

sys.path.append(".")

import swjff

# testing all functions if there is no error
test_case = [
    1,
    "hello",
    b"Wow",
    True,
    False,
    None,
    {"Key": [1, 2, 3], 24: b"Pairs"},
    3.14,
    1000000.02,
    3.138480982742,
    13,
    2556,
    46098328763,
    85938290583920859382906828988563723,
    -85938290583920859382906828988563723,
]

item = swjff.serialize(test_case)
swjff.deserialize(item)

flags = {0x01: {"password": "hello"}, 0x02: True, 0x03: True}
item = swjff.save(test_case, flags)
swjff.open(item, "hello")

swjff.save_file("tmp/sample.sjwff", test_case, flags)
swjff.open_file("tmp/sample.sjwff", "hello")

print("All tests passed!")
