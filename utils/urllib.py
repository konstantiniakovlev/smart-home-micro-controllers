def encode_params(params: dict):
    params_list = []
    for key, value in params.items():
        value_list = value if isinstance(value, list) else [value]
        for v in value_list:
            params_list.append(f"{key}={v}".replace(" ", "%20"))

    return "&".join(params_list)
