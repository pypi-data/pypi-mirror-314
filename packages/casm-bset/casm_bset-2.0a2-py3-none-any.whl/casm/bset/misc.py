import copy


def almost_zero(value, abs_tol=1e-5) -> bool:
    """Check if value is approximately zero, using an absolute tolerance"""
    return abs(value) < abs_tol


def almost_equal(value1, value2, abs_tol=1e-5) -> bool:
    """Check if two values are approximately equal, using an absolute tolerance"""
    return almost_zero(value1 - value2, abs_tol=abs_tol)


def almost_int(value, abs_tol=1e-5) -> bool:
    """Check if a floating point value is approximately integer, using an \
    absolute tolerance"""
    return almost_zero(abs(value - round(value)), abs_tol=abs_tol)


def signof(value, abs_tol=1e-5) -> float:
    """Return the sign of a floating point value (or zero)

    Parameters
    ----------
    value: float
        The value to check.
    abs_tol: float = 1e-5
        The absolute tolerance to check for zero.

    Returns
    -------
    signof: float
        One of -1.0, 0.0, or 1.0.

    """
    if value < -abs_tol:
        return -1.0
    elif value > abs_tol:
        return 1.0
    else:
        return 0.0


def irrational_to_tex_string(
    value: float,
    limit: int,
    max_pow: int,
    abs_tol: 1e-5,
) -> str:
    """Find irrational approximation and return as a tex string

    Finds best irrational number approximation of a floating point value and
    returns a tex-formated string that contains an irrational approximation.

    This method searches numbers of the form (x/y)^(1/z), where x and y range
    from 1 to `limit` and z ranges from 1 to `max_pow`.

    Notes
    -----
    This is a pure Python reproduction of the C++ function irrational_to_tex_string
    found in libcasm-global.

    Parameters
    ----------
    value: float
        A floating point number.
    limit: int
        Searches for `x` and `y` in the range `[1, limit]`.
    max_pow: int
        Search for `z` in range `[1, max_pow]`.

    Returns
    -------
    texstring: str
        The approximation, :math:`(x/y)^(1/z)` of `value`, as a tex-formatted string.
    """

    texstring = ""
    if almost_int(value, abs_tol=abs_tol):
        return str(round(value))
    if value < 0.0:
        texstring += "-"
        value = abs(value)

    tmp_value = copy.copy(value)
    tmp_denom = 0
    tmp_num = 0
    y = 0
    x = 0

    z = 1
    while z < max_pow + 1:
        i = 1
        while i < limit + 1:
            tmp_denom = i / tmp_value
            tmp_num = tmp_value / i
            if tmp_denom > 1.0 and almost_int(tmp_denom, abs_tol=abs_tol):
                x = i
                y = round(tmp_denom)
            elif tmp_num > 1.0 and almost_int(tmp_num, abs_tol=abs_tol):
                y = i
                x = round(tmp_num)
            else:
                i += 1
                continue

            if z == 1:
                texstring += str(x) + "/" + str(y)
                return texstring

            if z == 2:
                texstring += "\\sqrt{" + str(x)
                if y != 1:
                    texstring += "/" + str(y)
                texstring += "}"
                return texstring
            else:
                texstring += "(" + str(x)
                if y != 1:
                    texstring += "/" + str(y)
                texstring += ")^{1/" + str(z) + "}"
                return texstring

            i += 1
        tmp_value *= value
        z += 1
    texstring += str(value)
    return texstring


def factor_by_mode(x, abs_tol=1e-5):
    """Factor array of float by the mode value

    Parameters
    ----------
    x: np.ndarray[np.float]
        Array of float
    abs_tol: float
        Absolute tolerance for comparison

    Returns
    -------
    mode: float
        The most commonly occurring value in `x`.
    x_factored: np.ndarray[np.float]
        The input array, `x`, divided by the mode.
    """
    counts = []
    for _x in x:
        found = False
        for i in range(len(counts)):
            key, count = counts[i]
            if almost_equal(_x, key, abs_tol=abs_tol):
                counts[i] = (key, count + 1)
                found = True
                break
        if not found:
            counts.append((_x, 1))
    max_count = None
    mode = None
    for i in range(len(counts)):
        key, count = counts[i]
        if max_count is None:
            max_count = count
            mode = key
        else:
            if count > max_count:
                max_count = count
                mode = key
    return (mode, x / mode)
