
def aggregate_temperature(sensor_strings):
    '''
    Takes a list of raw sensor strings, parses each one to extract temperature
    values, computes the average of valid temperatures rounded to 2 decimals.
    Returns 0.0 if no valid temperatures.
    '''
    temps = []
    for sensor_string in sensor_strings:
        parsed = parse_sensor_reading(sensor_string)
        temp = parsed.get('temperature')
        if temp is not None:
            temps.append(temp)
    if not temps:
        return 0.0
    avg = sum(temps) / len(temps)
    return round(avg, 2)



# Test Session 1: parse_sensor_reading
parsed = parse_sensor_reading('T:25.5|H:60|TS:1234567890')
assert isinstance(parsed, dict)
assert 'temperature' in parsed
assert 'humidity' in parsed
assert 'timestamp' in parsed
assert parsed['temperature'] == 25.5
assert parsed['humidity'] == 60.0
assert parsed['timestamp'] == 1234567890

# Test Session 2: aggregate_temperature
readings = ['T:22.0|H:50|TS:1000', 'T:24.0|H:55|TS:2000', 'T:26.0|H:60|TS:3000']
avg_temp = aggregate_temperature(readings)
assert isinstance(avg_temp, float)
assert avg_temp == 24.0  # (22+24+26)/3 = 24.0

# Test with invalid readings
readings_with_invalid = ['T:22.0|H:50|TS:1000', 'T:invalid|H:55|TS:2000', 'T:26.0|H:60|TS:3000']
avg_temp_partial = aggregate_temperature(readings_with_invalid)
assert avg_temp_partial == 24.0  # (22+26)/2 = 24.0

print('IoT Sensor Pipeline tests passed')

