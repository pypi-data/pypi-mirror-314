"""Chemical elements with masses and radii

Very simple package that only implements basic functionalities
(geting atomic mass or covalent radius for a given element) 
and loads fast.

'mass' refers to isotope-weighted average atomic mass, value in amu
'covalent_radius' is covalent radius, value in pm
"""

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    pass

import argparse
import collections

class NormalizedKeyDictionary(collections.UserDict):
    def __init__(self, data=None, *, normalize):
        self.normalize = normalize
        # normalize any keys that are being passed in 
        data = data or {}
        super().__init__({normalize(k): v for k, v in data.items()})

    def __getitem__(self, key):
        return super().__getitem__(self.normalize(key))

    def __setitem__(self, key, value):
        return super().__setitem__(self.normalize(key), value)

    def __delitem__(self, key):
        return super().__delitem__(self.normalize(key))

class DecoratedNormalizedKeyDictionary(NormalizedKeyDictionary):
    def __init__(self, data=None, *, normalize, decorate):
        super().__init__(data, normalize=normalize)
        self.decorate = decorate

    def __getitem__(self, key):
        return self.decorate(key, super().__getitem__(key))

data = [
    ('H' ,     1.008 ,              32.0 ,    ),
    ('He' ,    4.002602 ,           46.0 ,    ),
    ('Li' ,    6.94 ,               133.0 ,   ),
    ('Be' ,    9.0121831 ,          102.0 ,   ),
    ('B' ,     10.81 ,              85.0 ,    ),
    ('C' ,     12.011 ,             75.0 ,    ),
    ('N' ,     14.007 ,             71.0 ,    ),
    ('O' ,     15.999 ,             63.0 ,    ),
    ('F' ,     18.998403163 ,       64.0 ,    ),
    ('Ne' ,    20.1797 ,            67.0 ,    ),
    ('Na' ,    22.98976928 ,        155.0 ,   ),
    ('Mg' ,    24.305 ,             139.0 ,   ),
    ('Al' ,    26.9815385 ,         126.0 ,   ),
    ('Si' ,    28.085 ,             116.0 ,   ),
    ('P' ,     30.973761998 ,       111.0 ,   ),
    ('S' ,     32.06 ,              103.0 ,   ),
    ('Cl' ,    35.45 ,              99.0 ,    ),
    ('Ar' ,    39.948 ,             96.0 ,    ),
    ('K' ,     39.0983 ,            196.0 ,   ),
    ('Ca' ,    40.078 ,             171.0 ,   ),
    ('Sc' ,    44.955908 ,          148.0 ,   ),
    ('Ti' ,    47.867 ,             136.0 ,   ),
    ('V' ,     50.9415 ,            134.0 ,   ),
    ('Cr' ,    51.9961 ,            122.0 ,   ),
    ('Mn' ,    54.938044 ,          119.0 ,   ),
    ('Fe' ,    55.845 ,             116.0 ,   ),
    ('Co' ,    58.933194 ,          111.0 ,   ),
    ('Ni' ,    58.6934 ,            110.0 ,   ),
    ('Cu' ,    63.546 ,             112.0 ,   ),
    ('Zn' ,    65.38 ,              118.0 ,   ),
    ('Ga' ,    69.723 ,             124.0 ,   ),
    ('Ge' ,    72.63 ,              121.0 ,   ),
    ('As' ,    74.921595 ,          121.0 ,   ),
    ('Se' ,    78.971 ,             116.0 ,   ),
    ('Br' ,    79.904 ,             114.0 ,   ),
    ('Kr' ,    83.798 ,             117.0 ,   ),
    ('Rb' ,    85.4678 ,            210.0 ,   ),
    ('Sr' ,    87.62 ,              185.0 ,   ),
    ('Y' ,     88.90584 ,           163.0 ,   ),
    ('Zr' ,    91.224 ,             154.0 ,   ),
    ('Nb' ,    92.90637 ,           147.0 ,   ),
    ('Mo' ,    95.95 ,              138.0 ,   ),
    ('Tc' ,    97.90721 ,           128.0 ,   ),
    ('Ru' ,    101.07 ,             125.0 ,   ),
    ('Rh' ,    102.9055 ,           125.0 ,   ),
    ('Pd' ,    106.42 ,             120.0 ,   ),
    ('Ag' ,    107.8682 ,           128.0 ,   ),
    ('Cd' ,    112.414 ,            136.0 ,   ),
    ('In' ,    114.818 ,            142.0 ,   ),
    ('Sn' ,    118.71 ,             140.0 ,   ),
    ('Sb' ,    121.76 ,             140.0 ,   ),
    ('Te' ,    127.6 ,              136.0 ,   ),
    ('I' ,     126.90447 ,          133.0 ,   ),
    ('Xe' ,    131.293 ,            131.0 ,   ),
    ('Cs' ,    132.90545196 ,       232.0 ,   ),
    ('Ba' ,    137.327 ,            196.0 ,   ),
    ('La' ,    138.90547 ,          180.0 ,   ),
    ('Ce' ,    140.116 ,            163.0 ,   ),
    ('Pr' ,    140.90766 ,          176.0 ,   ),
    ('Nd' ,    144.242 ,            174.0 ,   ),
    ('Pm' ,    144.91276 ,          173.0 ,   ),
    ('Sm' ,    150.36 ,             172.0 ,   ),
    ('Eu' ,    151.964 ,            168.0 ,   ),
    ('Gd' ,    157.25 ,             169.0 ,   ),
    ('Tb' ,    158.92535 ,          168.0 ,   ),
    ('Dy' ,    162.5 ,              167.0 ,   ),
    ('Ho' ,    164.93033 ,          166.0 ,   ),
    ('Er' ,    167.259 ,            165.0 ,   ),
    ('Tm' ,    168.93422 ,          164.0 ,   ),
    ('Yb' ,    173.045 ,            170.0 ,   ),
    ('Lu' ,    174.9668 ,           162.0 ,   ),
    ('Hf' ,    178.49 ,             152.0 ,   ),
    ('Ta' ,    180.94788 ,          146.0 ,   ),
    ('W' ,     183.84 ,             137.0 ,   ),
    ('Re' ,    186.207 ,            131.0 ,   ),
    ('Os' ,    190.23 ,             129.0 ,   ),
    ('Ir' ,    192.217 ,            122.0 ,   ),
    ('Pt' ,    195.084 ,            123.0 ,   ),
    ('Au' ,    196.966569 ,         124.0 ,   ),
    ('Hg' ,    200.592 ,            133.0 ,   ),
    ('Tl' ,    204.38 ,             144.0 ,   ),
    ('Pb' ,    207.2 ,              144.0 ,   ),
    ('Bi' ,    208.9804 ,           151.0 ,   ),
    ('Po' ,    209.0 ,              145.0 ,   ),
    ('At' ,    210.0 ,              147.0 ,   ),
    ('Rn' ,    222.0 ,              142.0 ,   ),
    ('Fr' ,    223.0 ,              223.0 ,   ),
    ('Ra' ,    226.0 ,              201.0 ,   ),
    ('Ac' ,    227.0 ,              186.0 ,   ),
    ('Th' ,    232.0377 ,           175.0 ,   ),
    ('Pa' ,    231.03588 ,          169.0 ,   ),
    ('U' ,     238.02891 ,          170.0 ,   ),
    ('Np' ,    237.0 ,              171.0 ,   ),
    ('Pu' ,    244.0 ,              172.0 ,   ),
    ('Am' ,    243.0 ,              166.0 ,   ),
    ('Cm' ,    247.0 ,              166.0 ,   ),
    ('Bk' ,    247.0 ,              168.0 ,   ),
    ('Cf' ,    251.0 ,              168.0 ,   ),
    ('Es' ,    252.0 ,              165.0 ,   ),
    ('Fm' ,    257.0 ,              167.0 ,   ),
    ('Md' ,    258.0 ,              173.0 ,   ),
    ('No' ,    259.0 ,              176.0 ,   ),
    ('Lr' ,    262.0 ,              161.0 ,   ),
    ('Rf' ,    267.0 ,              157.0 ,   ),
    ('Db' ,    268.0 ,              149.0 ,   ),
    ('Sg' ,    271.0 ,              143.0 ,   ),
    ('Bh' ,    274.0 ,              141.0 ,   ),
    ('Hs' ,    269.0 ,              134.0 ,   ),
    ('Mt' ,    276.0 ,              129.0 ,   ),
    ('Ds' ,    281.0 ,              128.0 ,   ),
    ('Rg' ,    281.0 ,              121.0 ,   ),
    ('Cn' ,    285.0 ,              122.0 ,   ),
    ('Nh' ,    286.0 ,              136.0 ,   ),
    ('Fl' ,    289.0 ,              143.0 ,   ),
    ('Mc' ,    288.0 ,              162.0 ,   ),
    ('Lv' ,    293.0 ,              175.0 ,   ),
    ('Ts' ,    294.0 ,              165.0 ,   ),
    ('Og' ,    294.0 ,              157.0 ,   ),
]

element = {i+1:e for i,(e,m,r) in enumerate(data)}
atomic_number = {element[z]: z for z in element}

mass = NormalizedKeyDictionary(
    {i+1: m for i,(e,m,r) in enumerate(data)},
    normalize = lambda key: key if key in element else atomic_number[key]
)

covalent_radius = NormalizedKeyDictionary(
    {i+1: r for i,(e,m,r) in enumerate(data)},
    normalize = lambda key: key if key in element else atomic_number[key]
)

chemelem = DecoratedNormalizedKeyDictionary(
    {i+1: v for i,v in enumerate(data)},
    normalize = lambda key: key if key in element else atomic_number[key],
    decorate = lambda key,value: {
        'atomic_number': key,
        'symbol': value[0],
        'mass': value[1],
        'covalent_radius': value[2]
    }
)
del data


def main():
    ap = argparse.ArgumentParser(
        prog='chemelem',
        description=__doc__)
    ap.add_argument('--version', action='version', version='%(prog)s ' + str(__version__))
    ap.add_argument('element', help="element symbol or atomic number")
    args = ap.parse_args()
    if args.element.isdecimal():
        args.element = int(args.element)
    print(chemelem[args.element])

if __name__ == "__main__":
    main()
