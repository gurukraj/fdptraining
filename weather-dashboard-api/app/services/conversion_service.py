"""Temperature conversion service."""


class ConversionService:
    """Service for temperature unit conversions."""

    VALID_UNITS = ('celsius', 'fahrenheit', 'kelvin')

    @staticmethod
    def convert(value, from_unit, to_unit):
        """
        Convert temperature between units.

        Args:
            value: Temperature value (numeric)
            from_unit: Source unit ('celsius', 'fahrenheit', 'kelvin')
            to_unit: Target unit ('celsius', 'fahrenheit', 'kelvin')

        Returns:
            Converted temperature value (rounded to 2 decimal places)

        Raises:
            ValueError: If units are invalid
        """
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if from_unit not in ConversionService.VALID_UNITS:
            raise ValueError(f"Invalid source unit: {from_unit}. Must be one of {ConversionService.VALID_UNITS}")
        if to_unit not in ConversionService.VALID_UNITS:
            raise ValueError(f"Invalid target unit: {to_unit}. Must be one of {ConversionService.VALID_UNITS}")

        if from_unit == to_unit:
            return round(value, 2)

        # Convert to Celsius first
        if from_unit == 'celsius':
            celsius = value
        elif from_unit == 'fahrenheit':
            celsius = (value - 32) * 5 / 9
        elif from_unit == 'kelvin':
            celsius = value - 273.15

        # Convert from Celsius to target
        if to_unit == 'celsius':
            result = celsius
        elif to_unit == 'fahrenheit':
            result = (celsius * 9 / 5) + 32
        elif to_unit == 'kelvin':
            result = celsius + 273.15

        return round(result, 2)

    @staticmethod
    def batch_convert(values, from_unit, to_unit):
        """
        Convert a list of temperature values.

        Args:
            values: List of temperature values
            from_unit: Source unit
            to_unit: Target unit

        Returns:
            List of converted values
        """
        return [ConversionService.convert(v, from_unit, to_unit) for v in values]
