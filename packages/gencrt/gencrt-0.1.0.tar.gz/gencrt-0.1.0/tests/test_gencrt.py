from gencrt import crt, crt_two_eqs, extended_gcd


def test_extended_gcd():
    # Test with some standard cases
    assert extended_gcd(56, 15) == (1, -4, 15)
    assert extended_gcd(100, 0) == (100, 1, 0)


def test_crt_two_eqs():
    # Test with valid cases
    assert crt_two_eqs(2, 3, 3, 5) == 8
    assert crt_two_eqs(1, 4, 3, 5) == 13
    assert crt_two_eqs(4, 6, 1, 5) == 16

    # Test with no solution case
    assert crt_two_eqs(1, 2, 2, 4) is None


def test_crt():
    # Test with valid cases
    assert crt([(2, 3), (3, 5)]) == 8
    assert crt([(1, 4), (3, 5)]) == 13
    assert crt([(4, 6), (1, 5), (19, 7)]) == 166
    assert crt([(1, 6), (2, 3)]) is None

    # Test with empty input
    assert crt([]) is None

    # Test with single equation
    assert crt([(4, 7)]) == 4
