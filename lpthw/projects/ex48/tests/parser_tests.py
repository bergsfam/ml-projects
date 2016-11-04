from nose.tools import *
from ex48 import parser

def test_peek():
    result = parser.peek([('verb', 'hit')])
    assert_equal(result, 'verb')

def test_match():
    result = parser.match([('verb', 'hit')], 'verb')
    assert_equal(result, ('verb', 'hit'))
    result = parser.match([('noun', 'princess'),('verb', 'hit')], 'noun')
    assert_equal(result, ('noun', 'princess'))

def test_parse_verb():
    result = parser.parse_verb([('verb', 'hit')])
    assert_equal(result, ('verb', 'hit'))
    result = parser.parse_verb([('stop', 'the'),('verb', 'hit')])
    assert_equal(result, ('verb', 'hit'))

def test_parse_sentence():
	result = parser.parse_sentence([('verb', 'hit'), ('noun', 'bear')])
	assert_equal(result.subject, 'player')
	assert_equal(result.verb, 'hit')
	assert_equal(result.object, 'bear')
