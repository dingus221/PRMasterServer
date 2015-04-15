def uint16(number):
    number = int(number)
    assert 0 <= number < 2 ** 16, "ERROR encoding invalid uint16: {}".format(number)
    (high, low) = divmod(number, 256)
    return chr(high) + chr(low)


def uint8(number):
    number = int(number)
    assert 0 <= number < 256, "ERROR encoding invalid uint8: {}".format(number)
    return chr(number)

def ipaddr(addr):
    # only v4
    numbers = addr.split('.')
    assert len(numbers) == 4, "ERROR encoding invalid ipv4 address: {}".format(addr)
    r = ''
    for number in numbers:
        i = int(number)
        assert 0 <= i < 256, "ERROR encoding invalid ipv4 address: {}".format(addr)
        r += chr(i)
    return r
