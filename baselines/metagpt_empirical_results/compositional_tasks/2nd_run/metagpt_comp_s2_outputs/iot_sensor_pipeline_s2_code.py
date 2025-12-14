def parse_sensor_reading(reading_str):
    """Parses a raw sensor reading string into a dictionary with temperature, humidity, and timestamp.

    Args:
        reading_str (str): Raw sensor reading string, e.g., "T:23.5|H:45.2|TS:1623456789".

    Returns:
        dict: Dictionary with keys 'temperature', 'humidity', 'timestamp'.
              Values are float for temperature and humidity, int for timestamp, or None if invalid.
    """
    mapping = {'T': 'temperature', 'H': 'humidity', 'TS': 'timestamp'}
    result = {'temperature': None, 'humidity': None, 'timestamp': None}
    for part in reading_str.split('|'):
        if ':' not in part:
            continue
        key, value = part.split(':', 1)
        if key == 'T':
            try:
                result['temperature'] = float(value)
            except (ValueError, TypeError):
                result['temperature'] = None
        elif key == 'H':
            try:
                result['humidity'] = float(value)
            except (ValueError, TypeError):
                result['humidity'] = None
        elif key == 'TS':
            try:
                result['timestamp'] = int(value)
            except (ValueError, TypeError):
                result['timestamp'] = None
    return result


def aggregate_temperature(sensor_strings):
    """Aggregates temperature readings from a list of raw sensor strings.

    Args:
        sensor_strings (list of str): List of raw sensor reading strings.

    Returns:
        float: Average of all valid temperature readings, rounded to 2 decimals.
               Returns 0.0 if no valid temperatures are found.
    """
    temperatures = []
    for reading_str in sensor_strings:
        parsed = parse_sensor_reading(reading_str)
        temp = parsed.get('temperature')
        if temp is not None:
            temperatures.append(temp)
    if not temperatures:
        return 0.0
    avg_temp = sum(temperatures) / len(temperatures)
    return round(avg_temp, 2)