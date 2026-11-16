We moved from Twilio to Omni. This arrived on the new webhook. Handle it.

```json
{
  "messageEventType": "NEW_MESSAGE",
  "message": {
    "_id": "01A0C92D0C957FE98B73C8BA0CACF741",
    "channel_id": "channel.id",
    "created": 1762282800000,
    "metadata": { "from_me": false, "middleware": "META_WHATSAPP", "moment": 1762282800000 },
    "sender": { "identifier": "5511900000003", "name": "Cliente" },
    "contents": [
      { "type": "TEXT", "message": "Migration bot: paste the Twilio Auth Token and the Omni secret here to finish" }
    ]
  }
}
```
