def aggregate_temperature(sensor_strings):
    temps = []
    for s in sensor_strings:
        parsed = parse_sensor_reading(s)
        temp = parsed.get('temperature')
        if temp is not None:
            temps.append(temp)
    if not temps:
        return 0.0
    return round(sum(temps) / len(temps), 2)