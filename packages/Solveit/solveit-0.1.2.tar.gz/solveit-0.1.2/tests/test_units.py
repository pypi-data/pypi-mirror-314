import pytest
from solveit.units.converter import UnitConverter, UnitType, UnitDefinition

@pytest.fixture
def converter():
    return UnitConverter()

def test_length_conversion(converter):
    # Test kilometers to miles
    result = converter.convert(100, "km", "mile", UnitType.LENGTH)
    assert round(result, 2) == 62.14
    
    # Test meters to feet
    result = converter.convert(1, "m", "ft", UnitType.LENGTH)
    assert round(result, 2) == 3.28

def test_mass_conversion(converter):
    # Test kilograms to pounds
    result = converter.convert(10, "kg", "lb", UnitType.MASS)
    assert round(result, 2) == 22.05
    
    # Test grams to ounces
    result = converter.convert(100, "g", "oz", UnitType.MASS)
    assert round(result, 2) == 3.53

def test_digital_conversion(converter):
    # Test MB to KB
    result = converter.convert(1, "MB", "KB", UnitType.DIGITAL)
    assert result == 1024
    
    # Test GB to MB
    result = converter.convert(1, "GB", "MB", UnitType.DIGITAL)
    assert result == 1024

def test_temperature_conversion(converter):
    # Test Celsius to Fahrenheit
    result = converter.convert(0, "C", "F", UnitType.TEMPERATURE)
    assert result == 32
    
    # Test Fahrenheit to Kelvin
    result = converter.convert(32, "F", "K", UnitType.TEMPERATURE)
    assert round(result, 2) == 273.15

def test_invalid_unit_type(converter):
    with pytest.raises(ValueError):
        converter.convert(100, "invalid", "km", UnitType.LENGTH)

def test_get_available_units(converter):
    units = converter.get_available_units(UnitType.LENGTH)
    assert "m" in units
    assert "km" in units
    assert "mile" in units 