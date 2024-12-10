def clear_phone(phone):
    import re
    _phone = ''.join(re.findall(r'\d+', phone))
    if _phone[1] == '8':
        _phone = f'7{_phone[1:]}'
    return _phone
