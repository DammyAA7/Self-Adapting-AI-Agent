def parse_sensor_reading(reading: str) -> dict:
    result = {'temperature': None, 'humidity': None, 'timestamp': None}
    parts = reading.split('|')
    for part in parts:
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