from round_a_number import rounding_upwards

def test_rounding_upwards():
    assert rounding_upwards.round_up(number = 1.28, decimals = 1)
    assert rounding_upwards.round_up(number = -1.5)
    assert rounding_upwards.round_up(number = -1.225, decimals = 2)