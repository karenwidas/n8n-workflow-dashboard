# Dashboard

## File
`index.html` — MUST stay at repo root (GitHub Pages requirement)

## What it does
Central operations hub. Cards for: Merchant Lookup, Ticket Manager link, n8n workflow status, forms, chat agents.

## Patterns

### Typeahead (company search)
- Debounce: 300ms, min 2 chars
- Calls `/webhook/search-companies?q=` 
- On select: stores record ID, triggers contact fetch via `/webhook/search-contacts`
- Used by: Merchant Lookup card, Log a Ticket form

### Merchant Lookup
- Typeahead → select → opens Airtable Interface Designer in new window
- Deep-link pattern: `https://airtable.com/apppYzklXP1tsbWnF/pag83Qpg8L6MNygVQ?y8G2k={recordId}`
- Param key is `y8G2k` — this is page-specific, do not change to generic `recordId`

### Workflow status cards
- Polls `/webhook/n8n-status-proxy?workflowId=` on load and refresh
- Each card has a `id="status-{workflowId}"` element
- Workflow IDs in WORKFLOWS array at bottom of script

### Log a Ticket form
- Panel toggles open/closed
- Company typeahead → auto-populates contact dropdown
- Submits to `/webhook/create-ticket`
- At least one task row required before submit

## Layout rules
- Cards grouped by section with `.group` + `.group-label`
- Each card uses `--card-accent` CSS variable for top border color
- Status states: `.status-success` / `.status-error` / `.status-loading`
- New cards should follow existing card HTML structure exactly

## Do not
- Do not add npm, bundlers, or external CSS frameworks
- Do not break single-file structure
- Do not move `index.html` out of repo root
