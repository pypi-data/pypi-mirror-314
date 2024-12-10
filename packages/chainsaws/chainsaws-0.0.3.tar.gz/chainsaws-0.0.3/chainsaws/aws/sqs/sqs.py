"""AWS SQS high-level client providing simplified interface for queue operations."""
import json
from typing import Any

from chainsaws.aws.shared import session
from chainsaws.aws.sqs._sqs_internal import SQS
from chainsaws.aws.sqs.sqs_models import (
    SQSAPIConfig,
    SQSMessage,
    SQSMessageAttributes,
    SQSMessageBatchResponse,
    SQSQueueAttributes,
    SQSReceiveMessageResponse,
    SQSResponse,
)


class SQSAPI:
    """SQS high-level client."""

    def __init__(
        self,
        queue_url: str,
        config: SQSAPIConfig | None = None,
    ) -> None:
        """Initialize SQS client.

        Args:
            queue_url: The URL of the Amazon SQS queue
            config: Optional SQS configuration

        """
        self.config = config or SQSAPIConfig()
        self.queue_url = queue_url
        self.boto3_session = session.get_boto_session(
            self.config.credentials if self.config.credentials else None,
        )
        self._sqs = SQS(
            boto3_session=self.boto3_session,
            config=config,
        )

    def send_message(
        self,
        message_body: str | dict[str, Any],
        delay_seconds: int | None = None,
        attributes: dict[str, SQSMessageAttributes] | None = None,
        deduplication_id: str | None = None,
        group_id: str | None = None,
    ) -> SQSResponse:
        """Send a single message to the queue.

        Args:
            message_body: Message content (string or dict)
            delay_seconds: Optional delay for message visibility
            attributes: Optional message attributes
            deduplication_id: Optional deduplication ID (for FIFO queues)
            group_id: Optional group ID (for FIFO queues)

        """
        return self._sqs.send_message(
            queue_url=self.queue_url,
            message_body=message_body,
            delay_seconds=delay_seconds,
            message_attributes=attributes,
            message_deduplication_id=deduplication_id,
            message_group_id=group_id,
        )

    def send_message_batch(
        self,
        messages: list[str | dict[str, Any]],
        delay_seconds: int | None = None,
    ) -> SQSMessageBatchResponse:
        """Send multiple messages in a single request.

        Args:
            messages: List of messages (strings or dicts)
            delay_seconds: Optional delay for all messages

        """
        msg_objects = [
            SQSMessage(
                queue_url=self.queue_url,
                message_body=json.dumps(msg) if isinstance(msg, dict) else msg,
                delay_seconds=delay_seconds,
            )
            for msg in messages
        ]
        return self._sqs.send_message_batch(self.queue_url, msg_objects)

    def receive_messages(
        self,
        max_messages: int = 1,
        visibility_timeout: int | None = None,
        wait_time_seconds: int | None = None,
    ) -> SQSReceiveMessageResponse:
        """Receive messages from the queue.

        Args:
            max_messages: Maximum number of messages to receive (1-10)
            visibility_timeout: How long the messages should remain invisible
            wait_time_seconds: How long to wait for messages (long polling)

        """
        return self._sqs.receive_message(
            queue_url=self.queue_url,
            max_number_of_messages=max_messages,
            visibility_timeout=visibility_timeout,
            wait_time_seconds=wait_time_seconds,
        )

    def delete_message(self, receipt_handle: str) -> None:
        """Delete a message from the queue.

        Args:
            receipt_handle: Receipt handle of the message to delete

        """
        self._sqs.delete_message(
            queue_url=self.queue_url,
            receipt_handle=receipt_handle,
        )

    def delete_message_batch(self, receipt_handles: list[str]) -> dict[str, Any]:
        """Delete multiple messages in a single request.

        Args:
            receipt_handles: List of receipt handles to delete

        """
        return self._sqs.delete_message_batch(
            queue_url=self.queue_url,
            receipt_handles=receipt_handles,
        )

    def get_attributes(self, attributes: list[str] | None = None) -> SQSQueueAttributes:
        """Get queue attributes.

        Args:
            attributes: List of attribute names to retrieve

        """
        return self._sqs.get_queue_attributes(
            queue_url=self.queue_url,
            attribute_names=attributes or ["All"],
        )

    def delete_all_message(self) -> None:
        """Delete all messages from the queue."""
        self._sqs.purge_queue(self.queue_url)
