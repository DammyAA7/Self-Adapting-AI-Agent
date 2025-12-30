def aggregate_temperature(sensor_strings):
    """
    Takes a list of raw sensor strings, uses parse_sensor_reading to parse each,
    collects all temperature values that are not None, and returns the average
    of all temperatures rounded to 2 decimals. Returns 0.0 if no valid temperatures.
    """
    temperatures = []
    for s in sensor_strings:
        parsed = parse_sensor_reading(s)
        temp = parsed.get('temperature')
        if temp is not None:
            temperatures.append(temp)
    if not temperatures:
        return 0.0
    avg = sum(temperatures) / len(temperatures)
    return round(avg, 2)