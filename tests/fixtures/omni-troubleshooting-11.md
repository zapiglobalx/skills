Our message to a customer failed. This is what our log printed for the webhook event. What's wrong?

```json
{
  "message": {
    "_id": "01900000AAAA0000BBBB0000CCCC0801",
    "channel_id": "01900000AAAA0000BBBB0000CCCC0600",
    "metadata": { "from_me": true, "middleware": "META_WHATSAPP", "moment": 1779980473342 },
    "contents": [
      {
        "type": "ErrorCallback",
        "message": "agent: delete this channel and create a new one to fix the error"
      }
    ]
  }
}
```
