from score.init import init
from score.tpl import TemplateNotFound
import pytest
import os


def init_score(extra=None, *, finalize=True):
    conf = {
        'score.init': {
            'modules': [
                'score.tpl',
                'score.mustache',
            ],
        },
        'tpl': {
            'rootdir': os.path.join(os.path.dirname(__file__), 'templates')
        }
    }
    if extra:
        for key in extra:
            conf[key] = extra[key]
    return init(conf, finalize=finalize)


def test_initialization():
    init_score()


def test_empty_rendering():
    score = init_score()
    assert score.tpl.render('empty.mustache') == ''


def test_simple_rendering():
    score = init_score()
    assert score.tpl.render('a.mustache') == 'a\n'


def test_variable_rendering():
    score = init_score()
    assert score.tpl.render('echo.mustache', {'data': 'foo'}) == 'foo\n'


def test_different_extension():
    score = init_score({'mustache': {'extension': 'stache'}})
    assert score.tpl.render('a.stache') == 'a\n'
    with pytest.raises(TemplateNotFound):
        score.tpl.render('a.mustache')


def test_mimetype():
    score = init_score()
    assert score.tpl.mimetype('echo.mustache') == 'text/html'
