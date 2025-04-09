def default_value(value):
    def _default_value(_):
        return value
    return _default_value


TypeConvert = dict(
    s=str,
    b=bool,
    f=float,
    i=int,
    T=type,
    B=str.encode,
    N=default_value(float('nan')),
    I=default_value(float('inf')),
    n=default_value(None),
)
