import pytest

from gravitools.quantity import (
    AbsGValue,
    Gradient,
    GValue,
    parse_coord_angle,
    parse_gradient,
    parse_gravity,
    parse_height,
    parse_pressure_admittance,
    parse_quantity,
)


@pytest.mark.parametrize(
    "text,value,uncert,units",
    [
        ("1234 ± 5 m", 1234, 5, "m"),
        ("1,234.5 ± 1,234.5 m", 1234.5, 1234.5, "m"),
        ("1_234.5 ± 1_234.5 m", 1234.5, 1234.5, "m"),
        ("1234.5 ± 0.6 m", 1234.5, 0.6, "m"),
        ("1234.5 ± 0.6 nm/s²", 1234.5, 0.6, "nm/s²"),
        ("    1234.5 ± 0.6 m   \n", 1234.5, 0.6, "m"),
        ("1234±5 m", 1234, 5, "m"),
        ("1234 ± 5", 1234, 5, None),
        ("1234 m", 1234, None, "m"),
        ("1234", 1234, None, None),
        ("1234.56", 1234.56, None, None),
        (1234, 1234, None, None),
        ("-123.4e-6 rad", -123.4e-6, None, "rad"),
        ("12.3456°", 12.3456, None, "°"),
    ],
)
def test_parse_quantity(text, value, uncert, units):
    result = parse_quantity(text)
    assert result == (value, uncert, units)
    value, uncert, _ = result
    assert value is None or isinstance(value, float)
    assert uncert is None or isinstance(uncert, float)


@pytest.mark.parametrize("text", ["invalid\tstring"])
def test_parse_quantity_invalid(text):
    with pytest.raises(ValueError) as exc:
        parse_quantity(text)
    assert repr(text) in str(exc.value)


def test_gvalue_str():
    assert str(GValue(200)) == "200.0 nm/s²"
    assert str(GValue(200, 10)) == "200.0 ± 10.0 nm/s²"


@pytest.mark.parametrize("g", [GValue(1234), GValue(1234, 12)])
def test_gvalue_str_parse(g):
    assert parse_gravity(str(g)) == g


def test_gvalue_add():
    assert GValue(200, 10) + 100 == GValue(300, 10)
    assert 100 + GValue(200, 10) == GValue(300, 10)


def test_gvalue_sub():
    assert GValue(200, 10) - 100 == GValue(100, 10)
    assert 100 - GValue(200, 10) == GValue(-100, 10)


def test_gvalue_mul():
    assert 10 * GValue(200, 10) == GValue(2000, 100)
    assert GValue(200, 10) * 10 == GValue(2000, 100)


def test_gvalue_neg():
    assert -GValue(200, 10) == GValue(-200, 10)


def test_gvalue_astuple():
    assert GValue(200, 10).as_tuple() == (200, 10)


def test_gvalue_error_prop():
    g = GValue(100, 10) + GValue(0, 10)
    assert g.error == pytest.approx(14.14213)
    g = GValue(100, 10) - GValue(0, 10)
    assert g.error == pytest.approx(14.14213)


def test_gradient_str():
    assert str(Gradient(-3200)) == "-3200.0 nm/s²/m"
    assert str(Gradient(-3200, 10)) == "-3200.0 ± 10.0 nm/s²/m"


@pytest.mark.parametrize("vgg", [Gradient(-3000), Gradient(-3000, 10)])
def test_parse_gradient(vgg):
    assert parse_gradient(str(vgg)) == vgg


def test_gradient_sign():
    with pytest.raises(ValueError):
        Gradient(3000)


def test_gradient_dg_height():
    assert Gradient(-3200).dg_height(1.25) == GValue(-4000)
    assert Gradient(-3200, 8).dg_height(1.25) == GValue(-4000, 10)


def test_absgvalue_str():
    assert str(AbsGValue(9.8081234567e9)) == "9,808,123,456.7 nm/s²"
    assert str(AbsGValue(9.8081234567e9, 10)) == "9,808,123,456.7 ± 10.0 nm/s²"
    assert (
        str(AbsGValue(9.8081234567e9, height=1.25)) == "9,808,123,456.7 nm/s² (1.25 m)"
    )
    assert (
        str(AbsGValue(9.8081234567e9, 10, 1.25))
        == "9,808,123,456.7 ± 10.0 nm/s² (1.25 m)"
    )


def test_absgvalue_add():
    assert AbsGValue(9.81e9, 10) + GValue(1e7) == AbsGValue(9.82e9, 10)
    g = AbsGValue(9.81e9, 10) + GValue(1e7, 10)
    assert g.error == pytest.approx(14.14213)


def test_absgvalue_sub():
    assert AbsGValue(9.81e9) - AbsGValue(9.80e9) == GValue(1e7)
    assert AbsGValue(9.81e9) - GValue(1e7) == AbsGValue(9.80e9)


def test_absgvalue_sub_wrong_height():
    with pytest.raises(ValueError):
        AbsGValue(9e9, height=0) - AbsGValue(9e9, height=1)


def test_absgvalue_transfer():
    vgg = Gradient(-3200)
    assert AbsGValue(9.8e9, height=1.25, vgg=vgg).transfer(0) == AbsGValue(
        9.8e9 + 4000, height=0, vgg=vgg
    )


def test_parse_pressure_admittance_sign():
    with pytest.raises(ValueError):
        # Admittance factor should be negative
        parse_pressure_admittance(3)


def test_parse_pressure_admittance_units():
    with pytest.raises(ValueError):
        parse_pressure_admittance("-3 m")


def test_parse_height_units_error():
    with pytest.raises(ValueError):
        parse_height("123.45 µGal")


def test_parse_coord_angle_units_error():
    with pytest.raises(ValueError):
        parse_coord_angle("123.45 m")
