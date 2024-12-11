from unittest import mock

import pytest
from botocore.exceptions import BotoCoreError, ClientError

from pyinsole.exceptions import ProviderError
from pyinsole.ext.aws.providers import SQSProvider


@pytest.mark.asyncio
async def test_confirm_message(mock_boto_session_sqs, boto_client_sqs):
    with mock_boto_session_sqs:
        message = {"ReceiptHandle": "message-receipt-handle"}

        async with SQSProvider("queue-url") as provider:
            await provider.confirm_message(message)

        assert boto_client_sqs.delete_message.call_args == mock.call(
            QueueUrl="queue-url",
            ReceiptHandle="message-receipt-handle",
        )


@pytest.mark.asyncio
async def test_confirm_message_not_found(mock_boto_session_sqs, boto_client_sqs):
    error = ClientError(error_response={"ResponseMetadata": {"HTTPStatusCode": 404}}, operation_name="whatever")
    boto_client_sqs.delete_message.side_effect = error
    message = {"ReceiptHandle": "message-receipt-handle-not-found"}

    with mock_boto_session_sqs:
        async with SQSProvider("queue-url") as provider:
            await provider.confirm_message(message)

    assert boto_client_sqs.delete_message.call_args == mock.call(
        QueueUrl="queue-url",
        ReceiptHandle="message-receipt-handle-not-found",
    )


@pytest.mark.asyncio
async def test_confirm_message_unknown_error(mock_boto_session_sqs, boto_client_sqs):
    error = ClientError(error_response={"ResponseMetadata": {"HTTPStatusCode": 400}}, operation_name="whatever")
    boto_client_sqs.delete_message.side_effect = error
    message = {"ReceiptHandle": "message-receipt-handle-not-found"}
    with mock_boto_session_sqs:
        async with SQSProvider("queue-url") as provider:
            with pytest.raises(ClientError):
                await provider.confirm_message(message)


@pytest.mark.asyncio
async def test_fetch_messages(mock_boto_session_sqs, boto_client_sqs):
    options = {"WaitTimeSeconds": 5, "MaxNumberOfMessages": 10}
    with mock_boto_session_sqs:
        async with SQSProvider("queue-url", options=options) as provider:
            messages = await provider.fetch_messages()

    assert len(messages) == 1
    assert messages[0]["Body"] == "test"

    assert boto_client_sqs.receive_message.call_args == mock.call(
        QueueUrl="queue-url",
        WaitTimeSeconds=options.get("WaitTimeSeconds"),
        MaxNumberOfMessages=options.get("MaxNumberOfMessages"),
    )


@pytest.mark.asyncio
async def test_fetch_messages_returns_empty(mock_boto_session_sqs, boto_client_sqs):
    options = {"WaitTimeSeconds": 5, "MaxNumberOfMessages": 10}
    boto_client_sqs.receive_message.return_value = {"Messages": []}
    with mock_boto_session_sqs:
        async with SQSProvider("queue-url", options=options) as provider:
            messages = await provider.fetch_messages()

    assert messages == []
    assert boto_client_sqs.receive_message.call_args == mock.call(
        QueueUrl="queue-url",
        WaitTimeSeconds=options.get("WaitTimeSeconds"),
        MaxNumberOfMessages=options.get("MaxNumberOfMessages"),
    )


@pytest.mark.asyncio
async def test_fetch_messages_with_client_error(mock_boto_session_sqs, boto_client_sqs):
    error = ClientError(error_response={"Error": {"Message": "unknown"}}, operation_name="whatever")
    boto_client_sqs.receive_message.side_effect = error
    with mock_boto_session_sqs:
        async with SQSProvider("queue-url") as provider:
            with pytest.raises(ProviderError):
                await provider.fetch_messages()


@pytest.mark.asyncio
async def test_fetch_messages_with_botocoreerror(mock_boto_session_sqs, boto_client_sqs):
    error = BotoCoreError()
    boto_client_sqs.receive_message.side_effect = error
    with mock_boto_session_sqs:
        async with SQSProvider("queue-url") as provider:
            with pytest.raises(ProviderError):
                await provider.fetch_messages()


@pytest.mark.asyncio
async def test_custom_visibility_timeout(mock_boto_session_sqs, boto_client_sqs):
    options = {"WaitTimeSeconds": 5, "MaxNumberOfMessages": 10, "VisibilityTimeout": 60}
    with mock_boto_session_sqs:
        async with SQSProvider("queue-url", options=options) as provider:
            messages = await provider.fetch_messages()

    assert len(messages) == 1
    assert messages[0]["Body"] == "test"

    assert boto_client_sqs.receive_message.call_args == mock.call(
        QueueUrl="queue-url",
        WaitTimeSeconds=options.get("WaitTimeSeconds"),
        MaxNumberOfMessages=options.get("MaxNumberOfMessages"),
        VisibilityTimeout=options.get("VisibilityTimeout"),
    )
