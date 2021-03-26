from azure.storage.queue import (
    QueueClient,
    BinaryBase64EncodePolicy,
    BinaryBase64DecodePolicy
)

import os, uuid

# The following code is from the tutorial located at
# https://docs.microsoft.com/en-us/azure/storage/queues/storage-python-how-to-use-queue-storage?tabs=python

# Retrieve the connection string from an environment
# variable named AZURE_STORAGE_CONNECTION_STRING
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Create a unique name for the queue
q_name = "queue-" + str(uuid.uuid4())

# Instantiate a QueueClient object which will
# be used to create and manipulate the queue
print("Creating queue: " + q_name)
queue_client = QueueClient.from_connection_string(connect_str, q_name)

# Create the queue
queue_client.create_queue()

# Send a message to the queue
message = u"Hello World"
print("Adding message: " + message)
queue_client.send_message(message)

# Send multiple messages to the queue
for x in range(10):
    message = u"message-" + str(uuid.uuid4())
    print("Adding message: " + message)
    queue_client.send_message(message)

# Peek at a message in the queue
messages = queue_client.peek_messages()

for peeked_message in messages:
    print("Peeked message: " + peeked_message.content)

# Change the contents of a queued message
messages = queue_client.receive_messages()
list_result = next(messages)

print("Initial message content: " + list_result.content)

message = queue_client.update_message(
        list_result.id, list_result.pop_receipt,
        visibility_timeout=0, content=u'Hello World Again')

print("Updated message to: " + message.content)

# Receive and delete a message
message = queue_client.receive_message()
print("Dequeueing message: " + message.content)
queue_client.delete_message(message.id, message.pop_receipt)

# Get the queue length
properties = queue_client.get_queue_properties()
count = properties.approximate_message_count
print("Message count: " + str(count))