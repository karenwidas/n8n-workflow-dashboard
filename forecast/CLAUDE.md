# forecast.html — Ticket Forecast & Available View

## Purpose
Standalone daily dashboard that mirrors OmniFocus's Forecast + Available views. Gives a date-bucketed, actionable view of all open tickets without opening the full Ticket Manager.

## Location
`forecast.html` — lives alongside `ticket-manager.html` and `index.html` on GitHub Pages (karenwidas.github.io).

---

## Data sources
Reads directly from Airtable via the REST API. No n8n involved.

```
BASE   = 'apppYzklXP1tsbWnF'
T_TKT  = 'tblxZJUvRDKgLywUq'   // Tickets
T_TASK = 'tbl40uFmR8J8rM75z'   // Ticket Tasks
T_CO   = 'tblPEGS3d1QsE0KY1'   // Companies
```

Field ID maps (`TF`, `SF`) are identical to `ticket-manager.html`. Auth uses the same PAT stored in `localStorage` under key `at_tk`.

---

## Sections

| Section | Logic |
|---|---|
| **Overdue** | `Ticket Due Date` < today |
| **Today** | `Ticket Due Date` = today, or no due date and `Ticket Planned Date` = today |
| **This Week** | Due or planned date within the current week, grouped by day |
| **Upcoming** | Due or planned date beyond this week, grouped by day |
| **Available** | No due date AND no planned date; sorted alphabetically by subject |

Closed tickets are excluded via filter: `NOT({Ticket Status}="Closed")`

> **Important:** Airtable `filterByFormula` requires field **names** in curly braces, not field IDs. Using `{fldXXXXX}` silently returns no results.

---

## What you can do from forecast.html

- **Check off tasks** — toggles Task Status between `To Do` and `Completed` via direct Airtable PATCH
- **Edit due/planned dates** — inline date inputs, changes queue until Save is clicked
- **Close a ticket** — PATCHes `Ticket Status = Closed` and removes the ticket from view
- **Open in Manager** — opens `ticket-manager.html#recXXXX` (deep-link, see below)

Tasks are lazy-loaded on first expand and cached for the session.

---

## Deep-link to ticket-manager.html

The "Open in Manager" button passes the Airtable record ID as a URL hash:
```
ticket-manager.html#recABC123
```

For this to auto-select the ticket, `ticket-manager.html` needs this change at the end of `init()`:

```js
// Replace:
loadTickets();
loadCompanies();
loadContacts();

// With:
loadTickets().then(() => {
  const hash = window.location.hash.slice(1);
  if (hash && hash.startsWith('rec')) selectTicket(hash);
});
loadCompanies();
loadContacts();
```

Requires `loadTickets()` to return its promise.

---

## What forecast.html does NOT do

- **Does not fire the recurring ticket webhook** — closing from forecast does a plain Airtable PATCH only. If recurring ticket creation on close is needed, copy the `closeTicket()` logic from `ticket-manager.html` (checks recurring fields, fires `https://karenwidas.app.n8n.cloud/webhook/create-recurring-ticket`).
- **Does not create tickets** — use `ticket-manager.html` or the Log a Ticket form on `index.html`
- **Does not edit ticket fields** beyond due date, planned date, and status

---

## Airtable filter formula rule
Always use field names, never field IDs, in `filterByFormula`:
```js
// CORRECT
formula: `NOT({Ticket Status}="Closed")`

// WRONG — silently returns nothing
formula: `NOT({fld3djwQzzRgsO2bA}="Closed")`
```
