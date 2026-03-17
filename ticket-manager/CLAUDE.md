# Ticket Manager

## File
`ticket-manager.html` — standalone single-file app, opens in new tab from dashboard

## What it does
Full CRUD for tickets and tasks against Airtable. View, edit, close, reopen tickets.
Add/edit/delete/reorder tasks. Recurring ticket scheduling.

## Airtable tables used
| Table | ID |
|---|---|
| Tickets | `tblXXX` *(confirm from Airtable — not in schema export)* |
| Ticket Tasks | `tblXXX` *(confirm from Airtable)* |
| Companies | `tblPEGS3d1QsE0KY1` |
| Contacts | `tblR80p5dAGRBx68K` |

## Ticket field IDs (TF object)
```js
const TF = {
  id:                'fld0F5wRHSFO3HkMl',  // autoNumber
  company:           'fldnOGvAKjysqcvwt',  // multipleRecordLinks
  contact:           'fldlsMsvHy7Ox0Ok6',  // multipleRecordLinks
  type:              'fld5actTxHND0ETkD',  // singleSelect
  status:            'fld3djwQzzRgsO2bA',  // singleSelect
  priority:          'fldwm0abmxlanWuEY',  // singleSelect
  channel:           'fldKquNzh3hQwQAps',  // singleSelect
  subject:           'fldIsJTQjAYN7ajXl',  // singleLineText
  due:               'fldyDnxmdJUwDEtr1',  // date
  planned:           'fld76SUcpLTHEiu83',  // date
  desc:              'fldLSZwPikCVGMTGR',  // multilineText
  nextTask:          'fldTxFgVq2DvZhH6A',  // singleLineText
  created:           'fldn0NIHSga9I1dd6',  // createdTime
  updated:           'fld0V8axhiLl1occX',  // lastModifiedTime
  closed:            'fldqLPuic5m4RcanL',  // dateTime
  tasks:             'fldzfbSOdOxx6bMIk',  // multipleRecordLinks → Ticket Tasks
  recurring:         'fldbKk0OyeF1fq3bv',  // checkbox
  recurringInterval: 'flduhmYB4jF2CZI61',  // number
  recurringFrequency:'fldLHVs5Vo0PCPICK',  // singleSelect
  recurringSchedule: 'fldwjELZJfJst5mEJ',  // singleSelect
  recurringEnd:      'fldFduNsWJtwwHwq7',  // date
};
```

## Task field IDs (SF object)
```js
const SF = {
  id:      'fldjlkXc7EWfZM9IV',  // autoNumber
  task:    'fldZKDhv2MogYM6xV',  // singleLineText
  tickets: 'fldS9lPWMkcf5Hr9r',  // multipleRecordLinks → Tickets
  order:   'fldLPrjNWGqkCp9dm',  // number
  status:  'fldfTkbMH4xh9AfEb',  // singleSelect: 'To Do' | 'Completed'
  planned: 'fldQatx2uh8rjXt14',  // date
  due:     'fld1mEb0v51FvnIzj',  // date
  notes:   'fldgvcTe3mHQUIDk2',  // multilineText
};
```

## Recurring ticket logic
Mirrors OmniFocus scheduling model:
- **Regularly**: next due = closed date + interval (fixed cadence)
- **From Completion**: next due = today + interval (resets from when you finish)

On ticket close → fires `/webhook/create-recurring-ticket` → n8n calculates next due date, creates new ticket, duplicates tasks.

## Task modes
- **Parallel**: all tasks available at once
- **Sequential**: only next incomplete task is active; rest are locked

Task Mode field: `fldWQ8jMZMZNVk3jq` (singleSelect on Tickets table)
Field is auto-created via Airtable Meta API if missing — requires `schema:read` + `schema:write` PAT scopes.

## Key patterns
- Tasks loaded by fetching all task record IDs from `TF.tasks`, then querying with `OR(RECORD_ID()="rec...", ...)` formula
- Task reorder: drag-and-drop, batch PATCH in chunks of 10
- Company/contact loaded client-side on init, filtered in JS — no per-ticket API calls for lookups
- API key stored in localStorage as `at_tk`
- Task Mode field ID cached in localStorage as `at_tmf_{baseId}`

## Webhooks used
- `/webhook/create-recurring-ticket` — called on ticket close if recurring
