from unittest import mock

import pytest


@pytest.fixture
def sqs_message():
    message = {"Body": "test"}
    return {"Messages": [message]}


def sqs_send_message():
    return {
        "MessageId": "uuid",
        "MD5OfMessageBody": "md5",
        "ResponseMetada": {"RequestId": "uuid", "HTTPStatusCode": 200},
    }


@pytest.fixture
def sns_list_topics():
    return {"Topics": [{"TopicArn": "arn:aws:sns:region:id:topic-name"}]}


@pytest.fixture
def sns_publish():
    return {"ResponseMetadata": {"HTTPStatusCode": 200, "RequestId": "uuid"}, "MessageId": "uuid"}


# boto client mock


class ClientContextCreator:
    def __init__(self, client):
        self._client = client

    async def __aenter__(self):
        return self._client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def boto_client_sqs(sqs_message):
    mock_client = mock.Mock()
    mock_client.delete_message = mock.AsyncMock()
    mock_client.receive_message = mock.AsyncMock(return_value=sqs_message)
    mock_client.send_message = mock.AsyncMock(return_value=sqs_send_message)
    mock_client.change_message_visibility = mock.AsyncMock()
    mock_client.close = mock.AsyncMock()
    return mock_client


@pytest.fixture
def mock_boto_session_sqs(boto_client_sqs):
    return mock.patch("pyinsole.ext.aws.base.session.create_client", return_value=ClientContextCreator(boto_client_sqs))


@pytest.fixture
def boto_client_sns(sns_publish):
    mock_client = mock.Mock()
    mock_client.publish = mock.AsyncMock(return_value=sns_publish)
    mock_client.close = mock.AsyncMock()
    return mock_client


@pytest.fixture
def mock_boto_session_sns(boto_client_sns):
    return mock.patch("pyinsole.ext.aws.base.session.create_client", return_value=ClientContextCreator(boto_client_sns))
