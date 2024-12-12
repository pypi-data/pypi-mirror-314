def merge(a, b, path: str = None, allow_new_key: bool = True):
    """Recursively merge two dictionaries"""
    path = path or []
    a = {} if a is None else a
    b = {} if b is None else b

    for key in b:
        if key in a:
            # For float and int, cast both to float.
            if (
                a[key] is not None
                and b[key] is not None
                and (
                    (isinstance(a[key], int) and isinstance(b[key], float))
                    or (isinstance(a[key], float) and isinstance(b[key], int))
                )
            ):
                a[key] = float(a[key])
                b[key] = float(b[key])

            # Sanity check that we don't merge different types.
            if (
                a[key] is not None
                and b[key] is not None
                and not isinstance(a[key], type(b[key]))
            ):
                raise ValueError(
                    f"Conflicting types '{a[key].__class__.__name__}' and "
                    f"'{b[key].__class__.__name__}' at '{'.'.join(path + [str(key)])}'"
                )

            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)], allow_new_key)
            else:
                a[key] = b[key]
        elif not allow_new_key:
            raise ValueError(
                f"Key '{'.'.join(path + [str(key)])}' missing in source dictionary"
            )
        else:
            a[key] = b[key]

    return a
