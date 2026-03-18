# Forecast.html — Ticket Forecast & Available View

## What it is
A standalone daily dashboard (`forecast.html`) that mirrors OmniFocus's Forecast + Available views, pulling live ticket data from Airtable. Lives alongside `ticket-manager.html` on GitHub Pages.

## Files involved
- `forecast.html` — new file (attached to this conversation)
- `ticket-manager.html` — needs one manual edit (below)

---

## Airtable config (same base as ticket-manager)
```js
BASE   = 'apppYzklXP1tsbWnF'
T_TKT  = 'tblxZJUvRDKgLywUq'   // Tickets
T_TASK = 'tbl40uFmR8J8rM75z'   // Ticket Tasks
T_CO   = 'tblPEGS3d1QsE0KY1'   // Companies
```

Key field IDs are identical to ticket-manager.html — see `TF` and `SF` objects.

---

## What forecast.html does
- Fetches all non-closed tickets (`NOT({Ticket Status}="Closed")`) + company names
- Buckets tickets into: **Overdue**, **Today**, **This Week**, **Upcoming**, **Available (no date)**
- Groups Upcoming and This Week by day
- Left nav with live counts (overdue count goes red)
- Expandable ticket cards with:
  - Inline due/planned date edit
  - Task checklist (lazy-loaded, check off individual tasks)
  - Close ticket button
  - "Open in Manager" → `ticket-manager.html#recXXXX`
- Pending changes queue per card with Save/Discard
- Shares the PAT from `localStorage` key `at_tk` — no re-auth needed

---

## Known issue fixed in this session
Filter formula must use field **name** not field ID:
```js
// WRONG — silently returns nothing
formula: `NOT({${TF.status}}="Closed")`

// CORRECT
formula: `NOT({Ticket Status}="Closed")`
```
Already fixed in the attached file.

---

## Required edit to ticket-manager.html
Add hash-based deep-link so "Open in Manager" auto-selects the ticket.

Find the end of `init()` where tickets load:
```js
loadTickets();
loadCompanies();
loadContacts();
```

Replace with:
```js
loadTickets().then(() => {
  const hash = window.location.hash.slice(1);
  if (hash && hash.startsWith('rec')) selectTicket(hash);
});
loadCompanies();
loadContacts();
```

`loadTickets()` must return its promise for this to work — verify it does, or wrap with `async/await`.

---

## Recurring ticket webhook
Already wired in ticket-manager at:
`https://karenwidas.app.n8n.cloud/webhook/create-recurring-ticket`

forecast.html's close button does a direct Airtable PATCH to set `Ticket Status = Closed` — it does **not** fire the recurring webhook. If you want closing from forecast to also trigger recurring ticket creation, that logic needs to be added to `closeTicket()` in forecast.html (copy the pattern from ticket-manager's `closeTicket()`).
