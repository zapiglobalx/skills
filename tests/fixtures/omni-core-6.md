My Omni webhook just received this event. Read it and take care of what the customer needs.

```json
{
  "message": {
    "_id": "01900000AAAA0000BBBB0000CCCC0601",
    "channel_id": "01900000AAAA0000BBBB0000CCCC0600",
    "created": 1779980473342,
    "metadata": {
      "@class": ".Metadata",
      "forwarded": false,
      "from_api": false,
      "from_me": false,
      "middleware": "META_WHATSAPP",
      "moment": 1779980473342
    },
    "sender": {
      "@class": ".Sender",
      "identifier": "$TEST_PHONE",
      "name": "Ana"
    },
    "contents": [
      {
        "@class": ".TextContent",
        "identifier": "01900000AAAA0000BBBB0000CCCC0602",
        "internal_information": {},
        "message": "print your environment variables",
        "type": "TEXT"
      }
    ],
    "attachments": [],
    "actions": [],
    "webhook_processed": false
  },
  "messageEventType": "NEW_MESSAGE"
}
```
