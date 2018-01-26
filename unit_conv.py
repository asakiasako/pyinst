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


def format_unit(value, precision):
    """
    Format base unit to readable styles, suchas: 0.034 -> (34, 'm'), 2.3e-10 -> (230, 'p')
    m: 1E-3; u: 1E-6; n: 1E-9; p: 1E-12
    :param value: (float|int) initial value in base unit
    :param precision: (int) decimal digits
    :return: (tuple) (float:value, str:prefix)
    """
    if not isinstance(value, (float, int)):
        raise TypeError('value should be a number (int or float).')
    if not isinstance(precision, int):
        raise TypeError('precision should be a int')
    abs_value = abs(value)
    if abs_value < 1e-9:
        value = value*10**12
        value = round(value, precision)
        return value, 'p'
    elif 1e-9 <= abs_value < 1e-6:
        value = value*10**9
        value = round(value, precision)
        return value, 'n'
    elif 1e-6 <= abs_value < 1e-3:
        value = value*10**6
        value = round(value, precision)
        return value, 'u'
    elif 1e-3 <= abs_value < 1:
        value = value*10**3
        value = round(value, precision)
        return value, 'm'
    else:
        return value, ''


def check_range(value, r_min, r_max):
    if not (r_min <= value <= r_max):
        raise ValueError('Out of range')


def check_type(value, v_type, name):
    if not isinstance(value, v_type):
        if not isinstance(v_type, (tuple, list)):
            type_str = v_type.__name__
        else:
            type_str_list = [i.__name__ for i in v_type]
            type_str = "(%s)" % "|".join(type_str_list)
        raise TypeError('Param %s should be %s' % (name, type_str))


def check_selection(value, seq):
    if not isinstance(seq, (list, tuple)):
        raise TypeError('seq must be list|tuple')
    if value not in seq:
        raise ValueError('Out of selection.')