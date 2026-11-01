## What changes

<!-- New skill, behavior change, or text/link fix. -->

## Checklist

- [ ] `python3 scripts/validate.py` passes with no errors
- [ ] Every endpoint, field and limit mentioned links to developer.z-api.io or developer.omni.z-api.io
- [ ] `tests/<name>.md` has the scenarios (starting from `templates/tests.template.md`)
- [ ] No credentials in the text; environment variables only
- [ ] If it sends messages: asks for opt-in, offers a way out and points to the best practices
- [ ] If it reads webhooks: says the received text is data, never an instruction
- [ ] Behavior changed: bumped `metadata.version` and recorded it in `CHANGELOG.md`
