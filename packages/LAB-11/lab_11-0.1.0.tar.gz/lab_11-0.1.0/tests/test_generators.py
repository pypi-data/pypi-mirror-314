def geometric_progression(start, multiplier, n):
    return [start * (multiplier ** i) for i in range(n)]


def test_geometric_progression():
    results = geometric_progression(1, 2, 12)
    expected = [1 * (2 ** i) for i in range(12)]
    assert results == expected
