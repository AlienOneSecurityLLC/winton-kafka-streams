"""
Test of sink processor behaviour
"""

import unittest.mock as mock

import winton_kafka_streams.processor as wks_processor

_expected_timestamp = 1234567890


def test_createSinkProcessorObject():
    wks_processor.SinkProcessor('topic1')

def test_sinkProcessorTopic():
    sink = wks_processor.SinkProcessor('topic1')
    assert sink.topic == 'topic1'

def test_sinkProcessorProcess():

    with mock.patch('winton_kafka_streams.processor.ProcessorContext.timestamp', new_callable=mock.PropertyMock) as mock_timestamp:
        mock_timestamp.return_value = _expected_timestamp
        processor_context = wks_processor.ProcessorContext(None, None, {})
        processor_context.recordCollector = mock.MagicMock()

        sink = wks_processor.SinkProcessor('topic1')
        sink.initialise('test-sink', processor_context)
        assert sink.name == 'test-sink'

        test_key, test_value = 'test-key', 'test-value'
        sink.process(test_key, test_value)
        assert processor_context.recordCollector.called_with(test_key, test_value, _expected_timestamp)
