# WARNING

When adding new commands, please use `localisation.localised_command` and specify their name and description in `en.json` in following format:

```
{
    "PING_COMMAND_NAME":"ping",
    "PING_COMMAND_DOC": "Gets bot latency.",
    ...
}
```

Then, add russian translation of both in `ru.json` in the same format _(optional)_