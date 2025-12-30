def aggregate_temperature(sensor_strings):
    temps = []
    for s in sensor_strings:
        reading = parse_sensor_reading(s)
        temp = reading.get('temperature')
        if temp is not None:
            temps.append(temp)
    if temps:
        return round(sum(temps) / len(temps), 2)
    return 0.0