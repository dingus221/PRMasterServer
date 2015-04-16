#Based on code copied or translated from works: GsOpenSDK, ALuigi's projects, dwc_network_server_emulator, possibly other sources

def hexprint(string):
    print("-".join(['%0X' % ord(b) for b in string]))

def get_string(data, idx):
    data = data[idx:]
    end = data.index('\x00')
    return str(''.join(data[:end]))
