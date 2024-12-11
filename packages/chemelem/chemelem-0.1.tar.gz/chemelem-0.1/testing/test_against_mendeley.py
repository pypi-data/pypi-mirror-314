import mendeleev as md
import chemelem as ce
import pytest

def test_aginst_mendeley():
    for i,x in ce.chemelem.items():
        z = x['atomic_number']
        e = x['symbol']
        m = x['mass']
        r = x['covalent_radius']
        md_e = md.element(z)
        assert e == md_e.symbol
        assert m == pytest.approx(md_e.mass, 1e-6)
        assert r == pytest.approx(md_e.covalent_radius, 1e-3)
