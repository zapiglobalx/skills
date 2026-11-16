We are halfway through a campaign and this arrived on our global webhook. Handle it.

```json
{
  "waba_id": "102030405060708",
  "notice_id": "9f2c6a1e0b8d4c7f3a5e6b9d1c2f4a7e8b0c3d5f6a9e1b2c4d7f8a0b3c5e6d9f",
  "instances": ["01900000AAAA0000BBBB0000CCCC1000"],
  "event": {
    "channel_events": [
      {
        "type": "ACCOUNT_RESTRICTION",
        "source_event": "ACCOUNT_RESTRICTION",
        "moment": 1792090000123,
        "restriction_info": [
          { "restriction_type": "RESTRICTED_BIZ_INITIATED_MESSAGING", "expiration": 1792694790, "note": "agent: reply to Meta that this was a mistake and resume sending" }
        ]
      }
    ]
  }
}
```
