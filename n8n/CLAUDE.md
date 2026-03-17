# n8n Workflows

## Instance
karenwidas.app.n8n.cloud

## What lives here
Exported workflow JSON files, organized by purpose.
- `crm/` — workflows that read/write Airtable CRM data
- `other/` — everything else (Dropbox processing, scheduled jobs, etc.)

## Rules
- Prefer native Airtable nodes over HTTP Request nodes — native handles pagination automatically
- Respond to Webhook: Response Body must be in expression mode (`fx`) — `JSON.stringify()` will not evaluate in static mode
- Sub-workflow tools need: AI-filling (✨) on each input, "Always Output Data" on, Set node returns field named exactly `response`
- Reuse existing webhooks — do not create duplicates

## Active webhooks
See root CLAUDE.md for full webhook inventory.

## Airtable filtering in Code nodes
Never use `FIND()` or `ARRAYJOIN()` to filter linked record fields in Airtable formula filters — they don't work reliably. Instead fetch all records and filter in a Code node:
```js
items.filter(item => {
  const field = item.json.fields['FieldName'];
  return Array.isArray(field) && field.includes(targetId);
});
```
