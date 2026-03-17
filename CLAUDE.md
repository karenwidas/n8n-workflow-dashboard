# DevPlus — CoCard Operations Stack

## What this repo is
Custom tooling for DevPlus Corporation / CoCard merchant services.
- `index.html` — main dashboard (served via GitHub Pages, must stay at repo root)
- `ticket-manager/ticket-manager.html` — ticket management app
- `forecast/forecast.html` — forecasting tool
- `n8n/` — n8n workflow JSON exports
- `airtable/` — schema reference

## Hosting
- GitHub Pages: karenwidas.github.io
- `index.html` MUST stay at repo root — moving it breaks the live site
- All other HTML files can live in subfolders

## Airtable
- Base ID: `apppYzklXP1tsbWnF`
- API base URL: `https://api.airtable.com/v0`
- API key stored in browser localStorage only — never hardcode it

### Critical rules
- Linked record fields require plain string arrays: `["recXXXXX"]` — NOT `{ id: "recXXXXX" }`
- Multi-select fields require arrays, not comma-separated strings
- Never filter linked record fields with FIND() or ARRAYJOIN() in Airtable formulas — fetch all records and filter in JS: `Array.isArray(fields.FieldName) && fields.FieldName.includes(id)`
- Use `returnFieldsByFieldId=true` on all API calls — reference fields by ID, not name
- singleSelect values may return as plain string OR `{ name, id, color }` — always use `sv()` helper to normalize: `function sv(v) { return v ? (typeof v === 'object' ? (v.name || '') : String(v)) : ''; }`
- Linked record values may return as plain string ID OR `{ id, name }` — always use `linkId()` and `linkName()` helpers
- Batch PATCH supports max 10 records per request

### Tables
| Table | ID |
|---|---|
| Companies | `tblPEGS3d1QsE0KY1` |
| Contacts | `tblR80p5dAGRBx68K` |
| Tickets | *(see ticket-manager/CLAUDE.md)* |
| Ticket Tasks | *(see ticket-manager/CLAUDE.md)* |
| FM Seasons | linked from Companies |

### Key field IDs
| Table | Field | ID |
|---|---|---|
| Companies | Company (name) | `fldgddNMEx5h9t38q` |
| Companies | Record ID | `fldi7SzvxoR9QO0Ar` |
| Contacts | Full Name (formula) | `fldXW2KwH9nKHFf7E` |
| Contacts | Company (link) | `fldgHAbjybm0T8imT` |

## n8n
- Instance: karenwidas.app.n8n.cloud
- Webhook base: `https://karenwidas.app.n8n.cloud/webhook/`

### Active webhooks (do not rename without updating all callers)
| Webhook | Used by |
|---|---|
| `/webhook/search-companies` | dashboard, ticket-manager |
| `/webhook/search-contacts` | ticket-manager |
| `/webhook/create-ticket` | dashboard ticket form |
| `/webhook/create-recurring-ticket` | ticket-manager on close |
| `/webhook/n8n-status-proxy` | dashboard workflow status cards |

### Critical rules
- Prefer native Airtable nodes over HTTP Request nodes — native handles pagination automatically
- Respond to Webhook: Response Body must be in expression mode (`fx`) to evaluate `JSON.stringify()`
- Sub-workflow tools require: AI-filling (✨) on each input field, "Always Output Data" on, Set node returns a field named exactly `response` containing `JSON.stringify(...)` with "Include Other Input Fields" off
- Reuse existing webhooks — do not create duplicates

## Brand (CoCard)
- Navy: `#00304F`
- Green: `#69932F`
- Background: `#eef2f5`
- Cards: white
- Always use CSS variables — never hardcode colors

## General rules
- Vanilla HTML/JS only — no frameworks, no build steps, no npm
- Single-file per app — keep CSS and JS inside the HTML file
- Nested template literals cause syntax errors — extract inner map calls to named helper functions
- CORS errors when served from `file://` — always test via GitHub Pages or a local server
