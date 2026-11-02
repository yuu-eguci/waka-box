import main


def test_run_keeps_its_name_and_docstring():
    assert main.run.__name__ == 'run'
    assert main.run.__doc__.startswith('メインメソッドです。')


def test_bar_chart_for_zero_percent_is_empty():
    assert main._generate_bar_chart(0, 15) == '░' * 15


def test_bar_chart_always_has_given_size():
    for percent in (0, 0.01, 6.67, 50, 99.99, 100):
        assert len(main._generate_bar_chart(percent, 15)) == 15
