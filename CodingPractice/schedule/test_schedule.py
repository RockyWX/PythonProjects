from schedule_practice import Schedule


def test_add():
    s = Schedule('s', 'test')
    s.add_task('test', 'test content', 100)
    assert 'test' in s.tasks


def test_remove():
    s = Schedule('s', 'test')
    s.remove_task('test')
    assert s.tasks == {}
