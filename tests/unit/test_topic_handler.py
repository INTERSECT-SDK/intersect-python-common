from intersect_sdk_common.control_plane.topic_handler import TopicHandler


def test_topic_handler_more_complex_wildcard():
    # test that the topic handler correctly matches topics based on its wildcard pattern
    topic_handler = TopicHandler(
        topic_persist=False, queue_name='irrelevant', regex_pattern='a/*/c/#'
    )
    assert (
        topic_handler.does_topic_match('a/b/c') is not None
    )  # * should match b, # should match nothing
    assert (
        topic_handler.does_topic_match('a/x/c/d/e') is not None
    )  # * should match x, # should match d/e
    assert not topic_handler.does_topic_match(
        'a/b/d'
    )  # * should match b but then c doesn't match d
    assert not topic_handler.does_topic_match('x/b/c')  # a doesn't match x
