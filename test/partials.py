from .init import init_score
import unittest.mock


def test_simple_partial():
    score = init_score(finalize=False)
    loader = unittest.mock.Mock()
    loader.load.return_value = (False, '{{> a}}')
    score.tpl.loaders['mustache'].append(loader)
    score._finalize()
    assert score.tpl.render('custom.mustache') == 'a\n'


def test_variable_in_partial():
    score = init_score(finalize=False)
    loader = unittest.mock.Mock()
    loader.load.return_value = (False, '{{> echo}}')
    score.tpl.loaders['mustache'].append(loader)
    score._finalize()
    assert score.tpl.render('custom.mustache', {'data': 'foo'}) == 'foo\n'


def test_nested_partials():
    score = init_score(finalize=False)
    loader = unittest.mock.Mock()
    loader.load.return_value = (False, '{{> partial}}')
    score.tpl.loaders['mustache'].append(loader)
    score._finalize()
    assert score.tpl.render('custom.mustache') == 'a\n'
