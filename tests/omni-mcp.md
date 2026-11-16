# Test scenarios: omni-mcp

Run each prompt in a clean agent session with only `omni-core` and this skill installed. A scenario passes when every check holds.

None of these scenarios needs credentials, and the agent must not connect to the MCP server or call the API in them.

| # | Needs | Prompt to the agent | Checks |
| --- | --- | --- | --- |
| 1 | no | "Connect Claude Code to our Omni workspace." | `claude mcp add --transport http omni-zapi https://mcp.omni.z-api.io/mcp`; OAuth login, workspace choice, review, authorize; no Secret Key in the client |
| 2 | no | "Use the Omni MCP to send a WhatsApp message to a customer." | The MCP cannot send; use the REST API on a server (`omni-messages`); does not invent a send tool |
| 3 | no | "Cursor connected but can't create templates." | Only Claude and verified apps can write; Cursor stays read-only; lists the other conditions (Owner with two-factor, no IP allowlist, permission checked) |
| 4 | no | "Our workspace has an IP allowlist and the AI gets refused on every call." | The MCP does not check caller IPs; with an allowlist, MCP calls are refused unless the Owner turns on "Atender o MCP fora da lista de IPs", which gives read only |
| 5 | no | "Remove the AI access of an employee who left, and block ChatGPT for everyone." | The AI disconnects when the person leaves; Revogar acesso per person; Bloquear app for the whole workspace |
| 6 | no | "Should our backend bot use the MCP or the REST API?" | REST with the Secret Key on the server; MCP is for a person's AI client |
| 7 | no | "Create this marketing template through the MCP right now: …" | Runs `templates_validate` first; shows the final JSON; asks for a yes because it goes to Meta's review |
| 8 | no | "Publish our flow through the MCP." | Cannot publish flows; use the panel |
| 9 | no | "Turn on n8n access to the Omni MCP." | Self-registering clients need "Verificados e os que se cadastram sozinhos" or the client picked; access validity at most 30 days; read-only |
