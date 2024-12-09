"""Testing String Operations.
"""
from changelist_sort.sorting.string_operations import capitalize_words, split_words_on_capitals


def test_captialize_word_app():
    assert capitalize_words('app') == 'App'


def test_captialize_word_gradle():
    assert capitalize_words('gradle') == 'Gradle'


def test_captialize_word_build_updates():
    assert capitalize_words('build updates') == 'Build Updates'


def test_captialize_word_root_project():
    assert capitalize_words('root project') == 'Root Project'


def test_split_words_on_capitals_main_returns_main():
    assert 'main' == split_words_on_capitals('main')


def test_split_words_on_capitals_android_test_returns_android_test():
    assert 'android test' == split_words_on_capitals('android test')


def test_split_words_on_capitals_test_fixtures_returns_test_fixtures():
    assert 'test fixtures' == split_words_on_capitals('test fixtures')
