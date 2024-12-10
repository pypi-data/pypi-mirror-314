from tafel.core.reader import Reader


class TestReader:
    def test_read_mpt(self):
        reader = Reader(ph=13.5, reference_potential=0.4, electrolyte_resistance=0.1)
        reader.read_mpt("tests/data/example.mpt")

        assert reader.electrode_surface_area == 0.046
        assert abs(reader.get_potential_shift() - 1.19785) < 1e-5

        logj, ircp = reader.get_tafel_plot()
        assert len(logj) == 35
        assert len(ircp) == 35
