# FM Workflows — Claude Project Context
**Last updated:** March 17, 2026

---

## Project Overview

Building 5 n8n Cloud workflows for CoCard Pay Center's Farmers Market (FM) operations, connected to an Airtable CRM and QuickBooks Online (QBO). The goal is to automate seasonal FM account management — from annual setup through close.

**Owner:** Karen Widas (`kwidas@me.com` → swap to `support@imgservices.com` for production)
**n8n instance:** `https://karenwidas.app.n8n.cloud`
**Airtable base:** `apppYzklXP1tsbWnF` (CRM)

---

## The 5 Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| FM_Season_Annual_Creator | Manual (was Schedule: March 1st 8am CST) | Creates FM Season records, Tickets, Tasks in Airtable; sends date-request emails to FM contacts |
| FM_Season_Date_Submission_Form | Form Trigger (n8n form) | FM market managers submit their season start/end dates |
| FM_Season_Remove_Hold | Form Trigger | Requests account hold removal from office; logs task updates |
| FM_Season_Close_Account | Form Trigger | Requests account closure from office; logs task updates |
| FM_QB_Invoice_Creator | Manual / Trigger TBD | Creates QBO invoices for FM data plan charges |

---

## Airtable CRM Structure

### Tables Used

**FM Seasons**
| Field | Type | Notes |
|---|---|---|
| Season Name | Formula | Format: `[Market Name] – [Year]` e.g. "Downtown Green Bay – 2025" |
| Season Year | Number | e.g. 2025 |
| Year Round | Checkbox | Military Ave is year-round |
| Company | Linked record → Companies | |
| Contact | Linked record → Contacts | |
| Tickets | Linked record → Tickets | |

**Tickets**
| Field | Field ID | Notes |
|---|---|---|
| Subject | `fldIsJTQjAYN7ajXl` | |
| Status | `fld3djwQzzRgsO2bA` | e.g. 'Open' |
| FM Season | `fldMrv5gUTSEmWKYy` | Linked record |
| Company | use field name "Company" | Linked record — Airtable rejects field IDs for this |
| Contact | use field name "Contact" | Linked record — Airtable rejects field IDs for this |

**Ticket Tasks**
- Fields: Task (text), Order (number), linked Ticket, linked FM Season

**Contacts**
- Fields include: Full Name, First Name, Last Name, Email, Company (linked), Phone, Cell, Title, Address, etc.

**Companies**
- Standard company fields

---

## FM Markets (as of 2025/2026)

| Market | Company | Contact | Year Round |
|---|---|---|---|
| Military Avenue, Inc. | Military Avenue, Inc. | Leah Weycker | ✓ Yes |
| On Broadway, Inc. | On Broadway, Inc. | Molly Gray Ivanovska | No |
| City of Manitowoc | City of Manitowoc | Courtney Hansen | No |
| Downtown Green Bay | Downtown Green Bay | Alissa Cotter | No |

Year-round markets get 2 tasks (data plan only). Seasonal markets get 11 tasks.

---

## FM_Season_Annual_Creator — Full Workflow Logic

### Flow
1. **Schedule / Manual Trigger**
2. **Set: Config** — sets `currentYear`, `formUrl` (production form URL from Date Submission Form)
3. **HTTP: Get Previous FM Seasons** — fetches last year's FM Season records from Airtable (`filterByFormula: {Season Year}=PREV_YEAR`)
4. **Code: Prep Season Payloads** — builds payloads for new season creation
5. **HTTP: Create FM Season** — creates new FM Season records in Airtable (4 items)
6. **Code: Prep Ticket Payload** — pairs new season IDs with market context
7. **HTTP: Create Ticket** — creates Ticket records linked to seasons (4 items)
8. **Code: Expand to Task Items** — expands each ticket into individual task definitions (35 items for 3 seasonal + 1 year-round)
9. **HTTP: Create Task** — creates Task records with batching (1 item/500ms to avoid 429)
10. **HTTP: Link Ticket to Season** — (4 items)
11. **Code: Dedupe Season-Ticket Pairs** — (4 items)
12. **HTTP: Get Contact** — fetches contact records for all markets (3 items — excludes year-round)
13. **Code: Filter Seasonal Markets** — filters to seasonal markets only (3 items)
14. **Code: Extract Email** — pairs contact email with market context (3 items)
15. **Gmail: Send Date Request** — sends HTML email to each FM contact with form link (3 emails)
16. **Code: Build Summary** — builds summary text
17. **Gmail: Notify Pooks** — sends summary to `kwidas@me.com`

### Key Code Nodes

**Code: Prep Season Payloads**
- Reads previous year's seasons from HTTP: Get Previous FM Seasons
- Outputs one item per market with: `marketLabel`, `companyIds`, `contactIds`, `yearRound`, `currentYear`

**Code: Prep Ticket Payload** — final working version
```javascript
const createSeasonItems = $input.all();
const marketItems = $('Code: Prep Season Payloads').all();

return createSeasonItems.map((item, i) => {
  const seasonId = item.json.records[0].id;
  const market   = marketItems[i].json;

  return {
    json: {
      seasonId,
      ticketSubject: market.currentYear + ' Season Setup - ' + market.marketLabel,
      yearRound:     market.yearRound,
      companyIds:    market.companyIds,
      contactIds:    market.contactIds,
      marketLabel:   market.marketLabel
    }
  };
});
```

**HTTP: Create Ticket** — body (JSON mode)
```
{{ JSON.stringify({ records: [{ fields: { fldIsJTQjAYN7ajXl: $json.ticketSubject, "Company": $json.companyIds, "Contact": $json.contactIds, fld3djwQzzRgsO2bA: 'Open', fldMrv5gUTSEmWKYy: [$json.seasonId] } }] }) }}
```
> Note: Use field names "Company" and "Contact" — Airtable rejects field IDs (`fldn0GvAKjysqcvwt`, `fldlsMsvHy70x00k6`) with 422 Unknown field name.

**Code: Expand to Task Items** — final working version
```javascript
const ticketItems = $input.all();
const ctxItems = $('Code: Prep Ticket Payload').all();
const result = [];

ticketItems.forEach((ticketItem, i) => {
  const ticketId = ticketItem.json.records[0].id;
  const ctx = ctxItems[i].json;

  const taskDefs = ctx.yearRound ? [
    { Task: 'Confirm data plan is active', Order: 1 },
    { Task: 'Create QB invoice for data plan', Order: 2 }
  ] : [
    { Task: 'Get market start and end dates from market manager', Order: 1 },
    { Task: 'Send Remove Hold request to office (email)', Order: 2 },
    { Task: 'Office confirms hold removed - account open', Order: 3 },
    { Task: 'Activate data plan in Dejavoo', Order: 4 },
    { Task: 'Notify customer - account ready, request test transaction', Order: 5 },
    { Task: 'Confirm test transaction successful', Order: 6 },
    { Task: '[POST-SEASON] Confirm all batches closed with customer', Order: 7 },
    { Task: '[POST-SEASON] Send Close request to office (email)', Order: 8 },
    { Task: '[POST-SEASON] Office confirms account closed', Order: 9 },
    { Task: '[POST-SEASON] Deactivate data plan in Dejavoo', Order: 10 },
    { Task: 'Create QB invoice for data plan', Order: 11 }
  ];

  taskDefs.forEach(t => {
    result.push({
      json: {
        task: t.Task,
        order: t.Order,
        ticketId,
        seasonId: ctx.seasonId,
        yearRound: ctx.yearRound,
        contactIds: ctx.contactIds,
        marketLabel: ctx.marketLabel
      }
    });
  });
});

return result;
```

**HTTP: Create Task** — batching settings
- Items per Batch: 1
- Batch Interval: 500ms
- (Required to avoid Airtable 429 rate limit errors on 35+ rapid requests)

**Code: Extract Email** — final working version
```javascript
const contacts = $input.all();
const markets  = $('Code: Filter Seasonal Markets').all();
const formUrl  = $('Set: Config').first().json.formUrl;

return contacts.map((contactItem, i) => {
  const contact = contactItem.json;
  const market  = markets[i].json;
  const email   = contact.fields?.Email || null;
  if (!email) throw new Error('No email found for ' + market.marketLabel);
  return { json: { email, marketLabel: market.marketLabel, formUrl } };
});
```

**Code: Build Summary** — final working version
```javascript
const currentYear = new Date().getFullYear();
const items = $('Code: Extract Email').all();
const markets = items.map(i => i.json.marketLabel + ' (' + i.json.email + ')').join(', ');
return [{
  json: {
    summary: 'FM Season Annual Creator completed for ' + currentYear +
             '. Records, tickets, and tasks created for all markets. Date request emails sent to: ' +
             (markets || 'none') + '.'
  }
}];
```

**HTTP: Get Previous FM Seasons — filterByFormula**
```
{{ '{Season Year}=' + (new Date().getFullYear()-1) }}
```
> Parentheses around the subtraction are required — without them, JS string concatenation runs first and produces `NaN`.

---

## FM_Season_Remove_Hold — Status: Bug Unresolved

**Error:** `No FM Season found for Downtown Green Bay [line 10]` in Code: Find FM Season

**Root cause (suspected):** HTTP: Get FM Seasons node has a `filterByFormula` filtering by year. Either:
- The 2026 seasons don't exist / don't match the filter, OR
- The Season Name format doesn't match the form's Market Name field

**Debug snippet to add at line 10:**
```javascript
if (!match) throw new Error('Searched: "' + marketName + '" | Got ' + records.length + ' seasons: ' + records.map(r => r.fields['Season Name']).join(' | '));
```

**Code: Find FM Season (current code)**
```javascript
const records    = $input.first().json.records || [];
const formData   = $('Form: Remove Hold Request').first().json;
const marketName = (formData['Market Name'] || '').toLowerCase();
const notes      = formData['Notes'] || '';

const match = records.find(r =>
  (r.fields['Season Name'] || '').toLowerCase().includes(marketName)
);

if (!match) throw new Error('No FM Season found for ' + formData['Market Name']);

const ticketIds  = match.fields['Tickets'] || [];
const companyIds = match.fields['Company'] || [];

if (!ticketIds.length) throw new Error('No ticket linked to FM Season for ' + formData['Market Name']);

return [{
  json: {
    seasonId:   match.id,
    seasonName: match.fields['Season Name'],
    ticketId:   ticketIds[0],
    companyId:  companyIds[0] || null,
    marketName: formData['Market Name'],
    notes
  }
}];
```

---

## Email Templates

Three HTML email files created for external-facing workflows. All use the CoCard signature with base64-embedded logo (`data:application/octet-stream;base64,...`).

| File | Workflow | Recipient |
|---|---|---|
| `email-date-request.html` | FM_Season_Annual_Creator | FM market managers |
| `email-remove-hold.html` | FM_Season_Remove_Hold | Office (internal) |
| `email-close-account.html` | FM_Season_Close_Account | Office (internal) |

**n8n expressions used in email-date-request.html:**
- `{{ new Date().getFullYear() }}` — current year
- `{{ $json.formUrl }}` — production form URL
- `{{ $json.marketLabel }}` — market name

> Important: When pasting into Gmail node in n8n, paste only the content between `<!-- EMAIL BODY -->` comments.

---

## Production Readiness Checklist

### For FM_Season_Annual_Creator + FM_Season_Date_Submission_Form
- [x] FM_Season_Date_Submission_Form activated → production form URL is live
- [x] Production form URL copied into Set: Config node as `formUrl`
- [ ] Gmail sender changed from `kwidas@me.com` → `support@imgservices.com`
- [x] Workflow deactivated (manual execution only — runs once a year)

### For all 5 workflows
- [ ] Swap `kwidas@me.com` → `support@imgservices.com` in Gmail nodes
- [ ] Switch QB sandbox → production (realm ID, credentials, base URL in Set Config nodes)

### QuickBooks Production Keys
- Intuit developer app at 100% App Details completion
- Compliance questionnaire blocked by Intuit help portal bug (REGISTRATION_HANDLER_ERROR loop)
- Email sent to Intuit support — awaiting resolution
- Privacy policy published: `outputs/privacy-policy.html`
- EULA published: `outputs/eula.html`

---

## Recurring Patterns & Rules

### n8n Item Pairing — Critical Rule
**Never use `.item` or `.first()` to reference upstream nodes when multiple items are expected.**

`.item` in a "Run Once For All Items" node only returns item 0. Always use explicit index mapping:

```javascript
const inputItems    = $input.all();
const upstreamItems = $('Some Other Node').all();

return inputItems.map((item, i) => {
  const upstream = upstreamItems[i].json;
  // ...
});
```

This pattern is used in: Code: Prep Ticket Payload, Code: Expand to Task Items, Code: Extract Email.

### Airtable API Rules
- Use field **names** (not IDs) for linked record fields — IDs return 422 Unknown field name
- Batch HTTP requests to Airtable: 1 item / 500ms minimum to avoid 429 rate limiting
- `filterByFormula` expressions go in Query Parameters, not the URL

### n8n HTTP Node JSON Body
Use `{{ JSON.stringify({ ... }) }}` pattern — not `={{ ... }}` (the `=` prefix gets sent literally as a string).

### Annual Creator Cron (if re-enabled)
```
0 8 1 3 *   →   8:00am on March 1st annually
```

---

## Files in Outputs Folder

| File | Description |
|---|---|
| `privacy-policy.html` | Minimal privacy policy for Intuit production key compliance |
| `eula.html` | Minimal EULA for Intuit production key compliance |
| `email-date-request.html` | HTML email — date request to FM market managers |
| `email-remove-hold.html` | HTML email — remove hold request to office |
| `email-close-account.html` | HTML email — close account request to office |
| `session-summary-2026-03-12.md` | Previous session summary |
| `fm-workflows-project-context.md` | This file |

---

## Open Items

1. **Fix Code: Find FM Season** — run debug snippet to identify whether it's a filter issue or name mismatch, then fix HTTP: Get FM Seasons filterByFormula accordingly
2. **Test remaining workflows** — Remove Hold Request, Close Account Request, QB Invoice Creator
3. **Swap email sender** — `kwidas@me.com` → `support@imgservices.com` across all workflows before go-live
4. **QB production keys** — waiting on Intuit support to resolve compliance portal bug
5. **Confirm 2026 Airtable records** — verify all 4 markets have correct 2026 Season, Ticket, and Task records after the production run of Annual Creator
