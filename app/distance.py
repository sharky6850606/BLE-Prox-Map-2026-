def rssi_to_distance(rssi, rssi1m, n):
    if rssi is None:
        return 999
    return 10 ** ((rssi1m - rssi)/(10*n))
