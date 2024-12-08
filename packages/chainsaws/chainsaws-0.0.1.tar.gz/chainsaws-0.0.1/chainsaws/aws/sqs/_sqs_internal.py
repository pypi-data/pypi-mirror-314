"""Internal implementation of AWS SQS operations."""
import json
import logging
from typing import Any

import boto3

from chainsaws.aws.sqs.sqs_models import (
    SQSAPIConfig,
    SQSMessage,
    SQSMessageAttributes,
    SQSMessageBatchResponse,
    SQSQueueAttributes,
    SQSReceiveMessageResponse,
    SQSResponse,
)

logger = logging.getLogger(__name__)


class SQS:
    def __init__(
        self,
        boto3_session: boto3.Session,
        config: SQSAPIConfig | None = None,
    ) -> None:
        self.config = config or SQSAPIConfig()
        self.client = boto3_session.client(
            "sqs", region_name=self.config.region)

    def send_message(
        self,
        queue_url: str,
        message_body: str | dict[str, Any],
        delay_seconds: int | None = None,
        message_attributes: dict[str, SQSMessageAttributes] | None = None,
        message_deduplication_id: str | None = None,
        message_group_id: str | None = None,
    ) -> SQSResponse:
        """Send a single message to SQS queue."""
        try:
            if isinstance(message_body, dict):
                message_body = json.dumps(message_body)

            message = SQSMessage(
                queue_url=queue_url,
                message_body=message_body,
                delay_seconds=delay_seconds,
                message_attributes=message_attributes,
                message_deduplication_id=message_deduplication_id,
                message_group_id=message_group_id,
            )

            params = self._prepare_send_message_params(message)
            response = self.client.send_message(**params)
            logger.debug(
                f"[SQS.send_message] Successfully sent message to {queue_url}")

            return SQSResponse.model_validate(response)
        except Exception as e:
            logger.exception(f"[SQS.send_message] Failed: {e!s}")
            raise

    def send_message_batch(
        self,
        queue_url: str,
        messages: list[SQSMessage],
    ) -> SQSMessageBatchResponse:
        """Send multiple messages in a single request."""
        try:
            entries = []
            for i, msg in enumerate(messages):
                entry = {
                    "Id": str(i),
                    "MessageBody": msg.message_body,
                }
                if msg.delay_seconds is not None:
                    entry["DelaySeconds"] = msg.delay_seconds
                if msg.message_attributes:
                    entry["MessageAttributes"] = msg.message_attributes
                entries.append(entry)

            response = self.client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries,
            )
            return SQSMessageBatchResponse.model_validate(response)
        except Exception as e:
            logger.exception(f"[SQS.send_message_batch] Failed: {e!s}")
            raise

    def receive_message(
        self,
        queue_url: str,
        max_number_of_messages: int = 1,
        visibility_timeout: int | None = None,
        wait_time_seconds: int | None = None,
    ) -> SQSReceiveMessageResponse:
        """Receive messages from SQS queue.

        Args:
            queue_url: The URL of the Amazon SQS queue
            max_number_of_messages: Maximum number of messages to receive (1-10)
            visibility_timeout: The duration (in seconds) that the received messages are hidden
            wait_time_seconds: The duration (in seconds) for which the call waits for messages

        Raises:
            AppError: If max_number_of_messages is not between 1 and 10

        """
        try:
            # Validate max_number_of_messages
            if not 1 <= max_number_of_messages <= 10:
                msg = "max_number_of_messages must be between 1 and 10"
                raise ValueError(
                    msg)

            params = {
                "QueueUrl": queue_url,
                "MaxNumberOfMessages": max_number_of_messages,
            }
            if visibility_timeout is not None:
                params["VisibilityTimeout"] = visibility_timeout
            if wait_time_seconds is not None:
                params["WaitTimeSeconds"] = wait_time_seconds

            response = self.client.receive_message(**params)
            return SQSReceiveMessageResponse.model_validate(response)
        except ValueError:
            raise

        except Exception as ex:
            logger.exception(f"[SQS.receive_message] Failed: {ex!s}")
            raise

    def delete_message(
        self,
        queue_url: str,
        receipt_handle: str,
    ) -> None:
        """Delete a message from the queue."""
        try:
            self.client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle,
            )
            logger.debug(
                f"[SQS.delete_message] Successfully deleted message from {queue_url}")
        except Exception as e:
            logger.exception(f"[SQS.delete_message] Failed: {e!s}")
            raise

    def delete_message_batch(
        self,
        queue_url: str,
        receipt_handles: list[str],
    ) -> dict[str, Any]:
        """Delete multiple messages in a single request."""
        try:
            entries = [
                {"Id": str(i), "ReceiptHandle": rh}
                for i, rh in enumerate(receipt_handles)
            ]
            return self.client.delete_message_batch(
                QueueUrl=queue_url,
                Entries=entries,
            )
        except Exception as e:
            logger.exception(f"[SQS.delete_message_batch] Failed: {e!s}")
            raise

    def get_queue_attributes(
        self,
        queue_url: str,
        attribute_names: list[str] | None = None,
    ) -> SQSQueueAttributes:
        """Get queue attributes."""
        try:
            response = self.client.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=attribute_names or ["All"],
            )
            return SQSQueueAttributes.model_validate(response["Attributes"])
        except Exception as e:
            logger.exception(f"[SQS.get_queue_attributes] Failed: {e!s}")
            raise

    def purge_queue(self, queue_url: str) -> None:
        """Delete all messages from the queue."""
        try:
            self.client.purge_queue(QueueUrl=queue_url)
            logger.info(
                f"[SQS.purge_queue] Successfully purged queue {queue_url}")
        except Exception as e:
            logger.exception(f"[SQS.purge_queue] Failed: {e!s}")
            raise

    def _prepare_send_message_params(self, message: SQSMessage) -> dict[str, Any]:
        """Prepare parameters for send_message API call."""
        params = {
            "QueueUrl": message.queue_url,
            "MessageBody": message.message_body,
        }

        if message.delay_seconds is not None:
            params["DelaySeconds"] = message.delay_seconds
        if message.message_attributes:
            params["MessageAttributes"] = message.message_attributes
        if message.message_deduplication_id:
            params["MessageDeduplicationId"] = message.message_deduplication_id
        if message.message_group_id:
            params["MessageGroupId"] = message.message_group_id

        return params
