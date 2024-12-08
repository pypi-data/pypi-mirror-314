from round_a_number import rounding_downwards

def test_rounding_downwards():
    assert rounding_downwards.round_down(number = 2.5)
    assert rounding_downwards.round_down(number = -2.5)
    assert rounding_downwards.round_down(number = 2.25, decimals = 1)