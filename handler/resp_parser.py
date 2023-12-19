def parse_resp(resp):
    if not resp:
        return None

    first_char = resp[0]

    if first_char == '+':  # String
        return resp[1:].strip('\r\n')
    elif first_char == '-':  # Error
        return resp[1:].strip('\r\n')
    elif first_char == ':':  # Integer
        return int(resp[1:].strip('\r\n'))
    elif first_char == '$':  # Bulk String
        length = int(resp[1:resp.find('\r\n')])
        if length == -1:
            return None
        start = resp.find('\r\n') + 2
        return resp[start:start + length]
    elif first_char == '*':  # Array
        parts = resp.split('\r\n')
        length = int(parts[0][1:])
        elements = []
        for i in range(1, length * 2, 2):
            elements.append(parse_resp(parts[i] + '\r\n' + parts[i + 1]))
        return elements
    else:
        raise ValueError("Invalid RESP value")
