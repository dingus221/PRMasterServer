#

UNSOLICITED_UDP_FLAG = 1
PRIVATE_IP_FLAG = 2
CONNECT_NEGOTIATE_FLAG = 4
ICMP_IP_FLAG = 8
NONSTANDARD_PORT_FLAG = 16
NONSTANDARD_PRIVATE_PORT_FLAG = 32
HAS_KEYS_FLAG = 64
HAS_FULL_RULES_FLAG = 128

ghchal = """\x41\x43\x4E\x2B\x78\x38\x44\x6D\x57\x49\x76\x6D\x64\x5A\x41\x51\x45\x37\x68\x41\x00"""

gngk = {'civ4':        'y3D9Hw',
        'civ4bts':     'Cs2iIq',
        'civ4btsjp':   'Cs2iIq',
        'civ4colpc':   '2yheDS',
        'civ4coljp':   '5wddmt',
        'gmtest':      'HA6zkS',
        'gslive':      'Xn221z'}

defaultfields = ['hostname', 'gamemode', 'hostname', 'gamever', 'passwd', 'hostport', 'staging', 'newgame', 'mapname',
                 'gametype', 'mynumplayers', 'maxnumplayers', 'nummissing', 'pitboss']

fakenames = {
    'types': ['teamer', 'Teamer', 'TEAMER', 'TEAMERXP', 't e a m e r', 'Teams', 'FFA', 'pangea', 'ffa', 'earth',
              'normalgame', 'f.f.a', 'F F A', 'PangeaFFA', 'FFABalanced', 'FFA XP', 'duel', 'DUEL', '1v1', 'islands',
              'island ffa'],
    'tags': ['expirienced', 'no crashers', 'no joiners', 'no retards', 'retards', 'just', 'blazing', 'noobs',
             'no noobs',
             'NN', 'TBG', '2v2', '3v3', '5v5', 'boobs', 'hurry', 'no laggers', 'no lagsters', 'no cheaters', 'no tards',
             'NOOBS FREE', '+1', 're', 'rehost', 'pro', 'newbs', 'PLS', 'PLEASE', 'quick', 'fast turns', 'HOST HERE',
             'hot',
             'bacon', 'chilling'],
    'maps': ['Pangea', 'Balanced', 'Team battle ground', 'tbg', 'Fractal', 'Inland Sea', 'Donut', 'E18', 'inland_sea',
             'islands']}
