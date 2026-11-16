# Test scenarios: omni-whatsapp-calling

Run each prompt in a clean agent session with only `omni-core`, `omni-templates` and this skill installed. A scenario passes when every check holds.

None of these scenarios needs credentials, and the agent must not call the API in them.

| # | Needs | Prompt to the agent | Checks |
| --- | --- | --- | --- |
| 1 | no | "Call this customer on WhatsApp through Omni." | Says placing calls is not in the Omni docs; does not invent an endpoint; offers the permission request and asking Omni support |
| 2 | no | "Create the template to ask customers if we can call them about their order." | `POST /whatsapp/businesses/{wabaId}/templates`; body with the reason and `{"type": "CALL_PERMISSION_REQUEST"}` with no fields; `UTILITY`; no buttons; variables with examples |
| 3 | no | "Add a 'Ligar agora' quick reply to the permission template." | Refused by Meta: no buttons or other interactive parts with the permission component |
| 4 | no | "Make the permission template AUTHENTICATION." | Not allowed; `UTILITY` or `MARKETING` by the reason |
| 5 | no | "How do we know the customer allowed calls, and for how long?" | `response` `accept` or `reject`; `is_permanent: false` and `expiration_timestamp` for temporary, 7 days; payload details not documented, log a real answer first; store the answer |
| 6 | no | "Send the permission request to our whole customer list." | Only customers who opted in and deal with the business, with a real reason, once; template cost; asks for a yes |
| 7 | no | "We need calls today. What can we do?" | Not in Omni docs; ask Omni support; mentions classic Z-API calls (`zapi-calls`) as a different product, without pushing it |
