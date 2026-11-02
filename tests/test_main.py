import main


def test_run_keeps_its_name_and_docstring():
    assert main.run.__name__ == 'run'
    assert main.run.__doc__.startswith('メインメソッドです。')
