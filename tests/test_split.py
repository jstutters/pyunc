from fixtures import pdt2, multi_volume


def test_split_echoes(pdt2):
    echo1, echo2 = pdt2.split_echoes()
    assert echo1.pixels.shape == (50, 240, 240)
    assert echo2.pixels.shape == (50, 240, 240)
    echo1_times = [s.echo_time for s in echo1.header.slices]
    assert all([x == 0.018888 for x in echo1_times])
    echo2_times = [s.echo_time for s in echo2.header.slices]
    assert all([x == 0.085 for x in echo2_times])
    assert len(echo1.header.slices) == 50
    assert len(echo2.header.slices) == 50


def test_split_volumes(multi_volume):
    vols = multi_volume.split_volumes(6)
    assert len(vols) == 6
    assert all([v.pixels.shape == (170, 256, 256) for v in vols])
    assert vols[0].header.slices[0].echo_time == 0.0019119999
    assert vols[1].header.slices[0].echo_time == 0.004312
    assert vols[2].header.slices[0].echo_time == 0.006712
    assert vols[3].header.slices[0].echo_time == 0.009112
    assert vols[4].header.slices[0].echo_time == 0.011512
    assert vols[5].header.slices[0].echo_time == 0.013912

