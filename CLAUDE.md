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

---

## Tech stack rules
- Vanilla HTML/JS only — no frameworks, no build steps, no npm
- Single-file per app — keep CSS and JS inline inside the HTML file
- No external CSS libraries (no Bootstrap, no Tailwind, etc.)
- Nested template literals cause syntax errors — extract inner `.map()` calls to named helper functions
- CORS errors when served from `file://` — always test via GitHub Pages or a local server

---

## Airtable

- Base ID: `apppYzklXP1tsbWnF`
- API base URL: `https://api.airtable.com/v0`
- API key stored in browser `localStorage` under key `at_tk` — never hardcode it

### Tables
| Table | ID |
|---|---|
| Companies | `tblPEGS3d1QsE0KY1` |
| Contacts | `tblR80p5dAGRBx68K` |
| Vendors | `tblMbMaXpdlUB7Bum` |
| Equipment | `tblvVqQhGPQCcSCuT` |
| ACH | `tbll7N8X8F84LSoFR` |
| CoCard Pay Center | `tblGFwsZYcKHoW8yJ` |
| Pin Debit | `tblcyqVcs7XnHyBwM` |
| EBT | `tblvNHF9z0b6Yr0NP` |
| VT_Gateway | `tblFgFg7YoejZ5cK3` |
| SwipeSimple | `tblMT4UO5B5bmuAQJ` |
| Tickets | `tblxZJUvRDKgLywUq` |
| Ticket Tasks | `tbl40uFmR8J8rM75z` |
| FM Seasons | `tblbfy2peOy17gYvx` |
| Merchant Application | `tblbQFNdkjOsg3BSg` |

### Key field IDs — Companies
| Field | ID | Type |
|---|---|---|
| Company (name) | `fldgddNMEx5h9t38q` | singleLineText |
| Record ID | `fldi7SzvxoR9QO0Ar` | formula |
| Account Type | `fldDb2igRb4fYjsXw` | multipleSelects |
| Account Status | `fldJ2McgKTwx3di6a` | singleSelect |
| Account Agent | `fldkvbYMjF4X7iFu2` | singleSelect |
| Agent Number | `fldY6vu9V1Mr10Djv` | singleLineText |
| Processor | `fldi6QjJWXZ5WssmQ` | singleSelect |
| MID | `fldBK3qw2myLrNXDu` | singleLineText |
| Pricing Type | `fldkfMQ9BnDAEWRoo` | singleSelect |
| Contact (link) | `fldMHDMokVaad49pE` | multipleRecordLinks → Contacts |
| Tickets (link) | `fldrnYB7B08XOJOSn` | multipleRecordLinks → Tickets |
| FM Seasons (link) | `fldZpsTwbWX9yFIL9` | multipleRecordLinks → FM Seasons |

### Key field IDs — Contacts
| Field | ID | Type |
|---|---|---|
| Full Name (formula) | `fldXW2KwH9nKHFf7E` | formula |
| First Name | `fldiSzTyesKtAWPti` | singleLineText |
| Last Name | `fldy2WLuwftEd2HOM` | singleLineText |
| Email | `fldNMGwxfHZaAA0zQ` | email |
| Phone | `fldV1ZbiWfVcTn2nA` | phoneNumber |
| Company (link) | `fldgHAbjybm0T8imT` | multipleRecordLinks → Companies |

### Key field IDs — Tickets (TF)
| Field | ID | Type |
|---|---|---|
| Ticket ID | `fld0F5wRHSFO3HkMl` | autoNumber |
| Company | `fldnOGvAKjysqcvwt` | multipleRecordLinks |
| Contact | `fldlsMsvHy7Ox0Ok6` | multipleRecordLinks |
| Ticket Type | `fld5actTxHND0ETkD` | singleSelect |
| Ticket Status | `fld3djwQzzRgsO2bA` | singleSelect |
| Ticket Priority | `fldwm0abmxlanWuEY` | singleSelect |
| Channel | `fldKquNzh3hQwQAps` | singleSelect |
| Subject | `fldIsJTQjAYN7ajXl` | singleLineText |
| Ticket Due Date | `fldyDnxmdJUwDEtr1` | date |
| Ticket Planned Date | `fld76SUcpLTHEiu83` | date |
| Ticket Description | `fldLSZwPikCVGMTGR` | multilineText |
| Next Task | `fldTxFgVq2DvZhH6A` | singleLineText |
| Ticket Created | `fldn0NIHSga9I1dd6` | createdTime |
| Ticket Updated | `fld0V8axhiLl1occX` | lastModifiedTime |
| Ticket Closed Date | `fldqLPuic5m4RcanL` | dateTime |
| Ticket Tasks (link) | `fldzfbSOdOxx6bMIk` | multipleRecordLinks → Ticket Tasks |
| Task Mode | `fldWQ8jMZMZNVk3jq` | singleSelect |
| Recurring | `fldbKk0OyeF1fq3bv` | checkbox |
| Recurring Interval | `flduhmYB4jF2CZI61` | number |
| Recurring Frequency | `fldLHVs5Vo0PCPICK` | singleSelect |
| Recurring Schedule | `fldwjELZJfJst5mEJ` | singleSelect |
| Recurring End | `fldFduNsWJtwwHwq7` | date |
| FM Season (link) | `fldMrv5gUTSEmWKYy` | multipleRecordLinks |

### Key field IDs — Ticket Tasks (SF)
| Field | ID | Type |
|---|---|---|
| Task ID | `fldjlkXc7EWfZM9IV` | autoNumber |
| Task | `fldZKDhv2MogYM6xV` | singleLineText |
| Tickets (link) | `fldS9lPWMkcf5Hr9r` | multipleRecordLinks |
| Order | `fldLPrjNWGqkCp9dm` | number |
| Task Status | `fldfTkbMH4xh9AfEb` | singleSelect |
| Task Planned Date | `fldQatx2uh8rjXt14` | date |
| Task Due Date | `fld1mEb0v51FvnIzj` | date |
| Task Notes | `fldgvcTe3mHQUIDk2` | multilineText |

### Critical API rules
- Use `returnFieldsByFieldId=true` on all read calls — reference fields by ID, not name
- **Exception:** `filterByFormula` requires field **names** in curly braces, NOT field IDs — `{Ticket Status}="Closed"` works; `{fld3djwQzzRgsO2bA}="Closed"` silently returns nothing
- Linked record fields in write calls: use field **names** ("Company", "Contact") not IDs — IDs return 422 Unknown field name
- Linked record values in write calls: plain string arrays `["recXXX"]` — NOT `{ id: "recXXX" }`
- Multi-select fields: arrays, not comma-separated strings
- Never filter linked record fields with `FIND()` or `ARRAYJOIN()` in formulas — fetch all records and filter in JS: `Array.isArray(fields.FieldName) && fields.FieldName.includes(id)`
- Batch PATCH supports max 10 records per request
- Rate limit: 5 req/sec — batch HTTP create tasks at 1 item / 500ms to avoid 429

### Data normalization helpers (use these consistently)
```js
// singleSelect: may return plain string OR { name, id, color }
function sv(v) { return v ? (typeof v === 'object' ? (v.name || '') : String(v)) : ''; }

// linked record: may return plain string ID OR { id, name }
function linkId(v)   { return v ? (typeof v === 'object' ? v.id   : v) : null; }
function linkName(v) { return v ? (typeof v === 'object' ? v.name : v) : ''; }
```

### singleSelect enum values
**Ticket Status:** `Open`, `Waiting on Customer`, `Waiting on Others`, `Waiting on Office`, `On Hold`, `Closed`
**Ticket Priority:** `Low`, `Normal`, `Medium`, `High`
**Ticket Type:** `Question`, `Problem`, `Other`, `FM Season`
**Task Status:** `Not Started`, `To Do`, `In Progress`, `Waiting on Customer`, `Waiting on Others`, `Waiting on Office`, `Completed`
**Task Mode:** `Sequential`, `Parallel`
**Recurring Frequency:** `Day`, `Week`, `Month`, `Year`
**Recurring Schedule:** `Regularly`, `From Completion`
**Account Status:** `Active`, `Active - Seasonal Hold`, `Request to Close`, `Closed`

---

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
- Respond to Webhook: Response Body must be in expression mode (`fx`) — `JSON.stringify()` will not evaluate in static mode
- Sub-workflow tools require: AI-filling (✨) on each input field, "Always Output Data" on, Set node returns field named exactly `response` containing `JSON.stringify(...)` with "Include Other Input Fields" off
- Reuse existing webhooks — do not create duplicates
- HTTP node JSON body: use `{{ JSON.stringify({ ... }) }}` pattern — not `={{ ... }}`
- Multi-item Code nodes: never use `.item` or `.first()` when multiple items are expected — always explicit index map:
  ```js
  const inputItems = $input.all();
  const upstream   = $('Node Name').all();
  return inputItems.map((item, i) => ({ json: { ...upstream[i].json } }));
  ```

---

## Interface patterns

### App structure patterns

**Dashboard (`index.html`)** — card grid layout
- Sticky navy header + green bottom border
- Background grid texture via `body::before` SVG
- Cards grouped by section with `.group` + `.group-label` (small-caps with trailing rule)
- Each card has `--card-accent` CSS variable for the 3px top border color
- `max-width: 1400px`, `padding: 32px 40px`

**Ticket Manager** — sidebar + main panel layout
- Left sidebar: `380px` fixed, navy header, filter chips, ticket list
- Right main: sticky detail header + scrollable body grid (`1fr 290px`)
- `height: 100vh; overflow: hidden` on body — internal scroll only

**Forecast** — sticky header + nav + content layout
- Sticky nav: `240px`, navy header with green border
- Content: `28px 32px` padding
- Sections bucketed by date: Overdue, Today, This Week, Upcoming, Available

### Component patterns

**Typeahead search**
- Debounce: 300ms, min 2 chars before firing
- Calls n8n webhook with `?q=` param
- Dropdown: `.typeahead-dropdown` / `.typeahead-item` / `.typeahead-empty`
- On blur: close with 150ms delay (allows `mousedown` to register)
- On select: store record ID separately from display text

**Merchant/company deep-link**
- Airtable Interface: `https://airtable.com/apppYzklXP1tsbWnF/pag83Qpg8L6MNygVQ`
- Param key: `?y8G2k={recordId}` — this key is page-specific, do not change

**Workflow status cards**
- Poll `/webhook/n8n-status-proxy?workflowId=` on load + every 5min
- Card element: `id="status-{workflowId}"`
- Three states: `.status-success` / `.status-error` / `.status-loading` (with pulse animation)
- Status dot is a 7px circle; success = green, error = red, loading = muted + pulsing

**Chat panel**
- Toggle open/close with `chat-panel.open` class
- Session ID via `crypto.randomUUID()` stored per panel
- POST `{ chatInput, sessionId }` → returns `data.output || data.response || data.text`
- Typing indicator: 3 bouncing dots while awaiting response

**Task checklist**
- Lazy-loaded on first expand, cached for session
- Checkbox: `.task-cb` — `.done` adds green fill + checkmark
- Sequential mode: only first incomplete task is active; rest locked
- Drag-and-drop reorder → batch PATCH in chunks of 10

**Toggle panels (ticket form, chat, obsidian)**
- Pattern: `display:none` → `display:block/flex` via `.open` class
- Button text changes to indicate state; panel has padding 16px, border 1px, border-radius 8px

**Modal**
- `.modal-bg.show` = `display:flex` with backdrop blur
- `.modal-box`: white, 10px radius, 4px top accent border, max-width 95vw

**Date picker (custom)**
- Trigger div shows formatted date or placeholder
- Popup calendar: `.dp-pop.dp-open`
- Quick-pick buttons for Today, Tomorrow, +1 week
- Clear button (`×`) to remove date

**Save bar**
- Appears when unsaved changes exist: `#save-bar` with `display:flex`
- Green top border, green text "Unsaved changes"

### Form field conventions
- Labels: `10-11px`, `font-weight: 700`, `text-transform: uppercase`, `letter-spacing: 0.5-0.8px`
- Inputs: `padding: 8px 10px`, `border-radius: 6px`, `border: 1px solid var(--border)`
- Focus: `border-color: var(--cocard-blue)` + optional `box-shadow: 0 0 0 2-3px rgba(105,147,47,.12)`
- Textareas: `resize: vertical`, `min-height: 60-80px`
- Full-width submit button, `font-weight: 700`, `border-radius: 8px`
- Feedback message: `.success` = green bg, `.error` = red bg — `display:none` by default

### Ticket recurring logic
- **Regularly**: next due = closed date + interval (fixed cadence)
- **From Completion**: next due = today + interval (resets from when you finish)
- On close → fire `/webhook/create-recurring-ticket` → n8n creates next ticket, duplicates tasks

### Forecast date buckets
| Section | Logic |
|---|---|
| Overdue | `Ticket Due Date` < today |
| Today | `Ticket Due Date` = today, OR no due date and `Ticket Planned Date` = today |
| This Week | Due or planned within current week, grouped by day |
| Upcoming | Due or planned beyond this week, grouped by day |
| Available | No due date AND no planned date — sorted alphabetically |

### Deep-link pattern
Forecast → Ticket Manager: `ticket-manager.html#recXXXX`
Ticket Manager hash handler at end of `init()`:
```js
loadTickets().then(() => {
  const hash = window.location.hash.slice(1);
  if (hash && hash.startsWith('rec')) selectTicket(hash);
});
```

---

## Brand / CSS rules
- Always use CSS variables — never hardcode colors
- Root variables defined in `:root` at top of `<style>` block
- Background grid texture: `body::before` with inline SVG data URL, `fill-opacity: 0.04`, `pointer-events: none`
- See `DESIGN_SYSTEM.md` for full token reference

---

## Email templates
Three HTML email files for FM workflows. All use base64-embedded CoCard logo.
| File | Workflow | Recipient |
|---|---|---|
| `email-date-request.html` | FM_Season_Annual_Creator | FM market managers |
| `email-remove-hold.html` | FM_Season_Remove_Hold | Office (internal) |
| `email-close-account.html` | FM_Season_Close_Account | Office (internal) |

When pasting into Gmail node in n8n: paste only content between `<!-- EMAIL BODY -->` comments.

---

## FM Seasons context
See `farmers market-workflows-project-context.md` for full FM workflow documentation.

**4 markets:**
| Market | Year Round |
|---|---|
| Military Avenue, Inc. | Yes (2 tasks) |
| On Broadway, Inc. | No (11 tasks) |
| City of Manitowoc | No (11 tasks) |
| Downtown Green Bay | No (11 tasks) |

**Open items:**
- Fix `Code: Find FM Season` — run debug snippet, fix `filterByFormula` if 2026 seasons don't match
- Swap Gmail sender: `kwidas@me.com` → `support@imgservices.com`
- QB production keys — waiting on Intuit compliance portal bug resolution

---

## Do not
- Do not add npm, bundlers, or external CSS frameworks
- Do not break single-file structure
- Do not move `index.html` out of repo root
- Do not hardcode API keys or colors
- Do not use `{fieldId}` in `filterByFormula` — use `{Field Name}` only
- Do not use field IDs for linked record writes — use field names ("Company", "Contact")
