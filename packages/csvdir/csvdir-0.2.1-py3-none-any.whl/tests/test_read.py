import typing

import csvdir


def test_simple():
    reader = csvdir.read_dir('tests/data')
    names = reader.names
    assert names == ['people2', 'people']
    iter_reader = iter(reader)
    row1 = next(iter_reader)
    row2 = next(iter_reader)
    row3 = next(iter_reader)
    row4 = next(iter_reader)
    row5 = next(iter_reader)
    row6 = next(iter_reader)
    assert row4 == {'id': '1', 'name': 'Odos', 'age': '38'}
    assert row5 == {'id': '2', 'name': 'Kayla', 'age': '31'}
    assert row6 == {'id': '3', 'name': 'Dexter', 'age': 'two'}
    assert row1 == {'id': '4', 'name': 'Joe', 'age': '44'}
    assert row2 == {'id': '5', 'name': 'James', 'age': '55'}
    assert row3 == {'id': '6', 'name': 'Luke', 'age': '0'}
