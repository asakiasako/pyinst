import math


def w_to_dbm(value):
    """
    Convert optical power in watt to optical power in dbm
    :param value: (float|int) optical power in watt.
    :return: (float) optical power in dbm
    """
    if not isinstance(value, (float, int)):
        raise TypeError('value of optical power in watt should be a number (int or float).')
    if value < 0:
        raise ValueError('value of optical power in watt should >= 0')
    dbm_value = 10*math.log(value*1000, 10)
    dbm_value = float(dbm_value)
    return dbm_value


def dbm_to_w(value):
    """
    Convert optical power in dbm to power in watt
    :param value: (float|int) optical power in dbm
    :return: (float) optical power in watt
    """
    if not isinstance(value, (float, int)):
        raise TypeError('value of optical power in watt should be a number (int or float).')
    w_value = (10**(value/10))/1000
    w_value = float(w_value)
    return w_value
