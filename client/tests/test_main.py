import privoxy_mode


class TestMain(object):
    def test_two(self):
        result = privoxy_mode.get_gfwlist()
        assert result == 'Success'
