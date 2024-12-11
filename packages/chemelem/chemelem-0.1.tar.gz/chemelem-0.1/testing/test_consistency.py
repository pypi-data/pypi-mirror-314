import chemelem as ce

def test_consistency():
    for i,x in ce.chemelem.items():
        z = x['atomic_number']
        e = x['symbol']
        m = x['mass']
        r = x['covalent_radius']
        assert e == ce.element[z]
        assert z == ce.atomic_number[e]
        assert m == ce.mass[z]
        assert m == ce.mass[e]
        assert r == ce.covalent_radius[z]
        assert r == ce.covalent_radius[e]
