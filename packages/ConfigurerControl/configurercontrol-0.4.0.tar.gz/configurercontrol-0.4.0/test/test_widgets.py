import unittest
from ConfigurerControl import widgets as wdg


class TestType(unittest.TestCase):
    def test_CidPar_sort(self):
        cps = [wdg.CidPar(0, b'012'), w := wdg.CidPar(1, b'0123'), wdg.CidPar(2, b'24')]
        cps.sort()
        self.assertEqual(w, cps[0])