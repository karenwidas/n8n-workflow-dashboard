# Leads Module — CLAUDE.md

This module adds a full merchant lead pipeline to the DevPlus / CoCard ops stack.
Read the root `CLAUDE.md` and `DESIGN_SYSTEM.md` before building anything here.

---

## Purpose

Manage prospective merchants from first contact through processor approval and conversion
to active customer. Lead contacts and application data are kept **strictly separate** from
the live Companies and Contacts tables until explicit conversion.

---

## Airtable

### New table: Leads

**Table ID:** `tblQe6TUV4DayDMUQ`
**Base:** `apppYzklXP1tsbWnF`

**Adding new leads will be managed in Airtable for now

#### Field spec — with field IDs

| Field name | Field ID | Type | Notes |
|---|---|---|---|
| `Lead Name` | `fldlnf7keCuQScL5x` | Single line text | Lead name. Primary field. |
| `Legal Name` | `fldqTZmcM4uvq4nme` | Single line text | |
| `DBA Name` | `fldMC8iKsaUTiN9EL` | Single line text | |
| `Status` | `fldPvwhRju0EZSqqp` | Single select | See status list below |
| `Notes` | `fldChiTTtNi1GyvOq` | Long text | Underwriting back-and-forth |
| `Contact First` | `fldrNtOZnZ9FMt5xO` | Single line text | |
| `Contact Last` | `fldFIMNnQKxWon4J9` | Single line text | |
| `Contact Suffix` | `fldJVBVESaqLqqjGW` | Single line text | |
| `Contact Phone` | `fldQ6icbrUPqQhqf2` | Phone | |
| `Contact Email` | `fldHLpnkpSWb0yROn` | Email | |
| `Legal Address` | `flduraFTAA5Zojkkb` | Single line text | |
| `Legal City` | `fldQN9AvrNLo8wBB7` | Single line text | |
| `Legal State` | `flddINm3KVefa02SI` | Single line text | |
| `Legal Zip` | `fldEWYV6LVYm6jbcX` | Single line text | |
| `DBA Address` | `fld8Ikpd8MohemqoP` | Single line text | |
| `DBA City` | `fldIgVfMGVGcANYxd` | Single line text | |
| `DBA State` | `fld4F2By99erAba9h` | Single line text | |
| `DBA Zip` | `fldZXbGNZVOieFTWf` | Single line text | |
| `DBA Phone` | `fldXT2R3xzmoFJlJN` | Phone | |
| `Form Sent Date` | `flddwRdsRzQhMQENI` | Date | |
| `Form Received Date` | `fldI6AOC1iCe9uB4J` | Date | |
| `Linked Company` | `fldLFz5gMemU2tMYn` | Link to Companies | Populated on conversion only |
| `Business Type` | `fldxvtGvqKVOMcax9` | Single line text | From form |
| `Products Services` | `fldQE4vGe54dK11ft` | Single line text | |
| `Dropbox Folder Path` | `fldtH3r7q2FINxUAu` | Single line text | Written by Lead Created workflow |

#### Lead statuses (in pipeline order)

```
New
Contacted
Form Sent
Form Received
Submitted to Processor
Approved
Declined by Processor
Lost
Converted
```

#### Encrypted fields (AES-256, client-side before transmission)

- `EIN`
- `Owner1 DOB`, `Owner1 SSN`
- `Owner2 DOB`, `Owner2 SSN`
- `Owner3 DOB`, `Owner3 SSN`

These fields are not to be stored in Airtable. These fields need to be encrypted for form
transmission to and from the lead.
Decryption is done locally via `decrypt-tool.html` only.

---

## Files to build

| File | Location | Notes |
|---|---|---|
| `merchant-form.html` | `karenwidas.github.io/_DevPlus/_Self/leads/merchant-form.html` | Merchant-facing, multi-page, CoCard branded |
| `decrypt-tool.html` | Local only — never hosted

---

## merchant-form.html

### Behavior
- Multi-page form (6 pages matching Cognito structure — see page spec below)
- Reads `leadId` URL parameter on load: `merchant-form.html?leadId=recXXXXX`
- On submit: encrypts sensitive fields client-side (CryptoJS AES-256), POSTs to n8n webhook
- Encryption key stored as a constant at top of file — must be changed before deploy
- CoCard brand colors (see CSS variable template in root `CLAUDE.md`)
- No frameworks — vanilla HTML/JS, single file
- CryptoJS loaded from CDN: `https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js`

### Encrypted fields (encrypt before POST)
`ein`, `owner1_dob`, `owner1_ssn`, `owner2_dob`, `owner2_ssn`, `owner3_dob`, `owner3_ssn`

### Page structure

**Page 1 — Legal & DBA & Contact**
- Legal name of business (required)
- Legal address: line 1, city, state, zip (required)
- DBA name (required)
- DBA address same as legal? (yes/no radio) — if no, show DBA address fields
- DBA address: line 1, city, state, zip (conditional)
- DBA phone (required)
- Contact name: first, last, suffix (required)
- Contact phone (required)
- Contact email (required)

**Page 2 — Business Profile**
- Business type (dropdown, required): Sole Proprietor / Partnership / Corporation / LLC / Non-Profit / Government
- EIN or Tax ID (required) ← encrypt
- State incorporated (required)
- Incorporated month/year (required)
- Products or services sold (required)
- Refund/return policy (multiline, required)

**Page 3 — Owner / Officer Information**
- Owner 1: first, last, suffix, home address (line1/city/state/zip), home phone, country of citizenship, date of birth (encrypt), SSN (encrypt), title, percent owned — all required
- "Are there other owners with ≥25% ownership?" (yes/no)
  - If yes: show Additional Owner section — repeatable up to 2 more owners (Owner 2, Owner 3), same fields as Owner 1

**Page 4 — Inventory Information**
- Do you own the product/inventory? (Yes / No / Does not apply)
- Is product/inventory stored on-site? (Yes / No / Does not apply)
- When is the customer charged? (Time of order / Upon shipment / Does not apply / Other)
- Do you use a fulfillment house? (Yes / No / Does not apply)
- Delivery timeframe: 1–7 days %, 8–14 days %, 14+ days % (numbers, total shown calculated)

**Page 5 — Payment Processing**
- Business % vs Public % (numbers, total shown calculated)
- Total monthly credit card sales (currency, required)
- Average credit card transaction (currency)
- Number of transactions per month (integer)
- Do you want to apply for ACH processing? (yes/no)
  - If yes, show: total monthly check sales, checks per month, avg check amount, max single check amount

**Page 6 — File Uploads**

*Always shown (credit card application):*
- Voided check / bank letter
- Driver's license
- Articles of incorporation
- IRS Tax ID letter
- Bank statements — last 3 months (if requested)
- Processing statements — last 3 months (if requested)
- Business financials (if requested)

*Shown only if ACH = yes:*
- Bank statement — latest month available
- Proof of business (credit card processing statement OR business license OR sales tax license OR utility bill)

### POST payload shape (to n8n webhook `/webhook/merchant-form-submit`)

```json
{
  "leadId": "recXXXXX",
  "legal_name": "",
  "legal_address_line1": "",
  "legal_city": "",
  "legal_state": "",
  "legal_zip": "",
  "dba_name": "",
  "dba_address_line1": "",
  "dba_city": "",
  "dba_state": "",
  "dba_zip": "",
  "dba_phone": "",
  "contact_first": "",
  "contact_last": "",
  "contact_suffix": "",
  "contact_phone": "",
  "contact_email": "",
  "business_type": "",
  "ein": "ENCRYPTED",
  "state_incorporated": "",
  "incorporated_date": "",
  "products_services": "",
  "refund_policy": "",
  "owner1_first": "", "owner1_last": "", "owner1_suffix": "",
  "owner1_address_line1": "", "owner1_city": "", "owner1_state": "", "owner1_zip": "",
  "owner1_phone": "", "owner1_citizenship": "",
  "owner1_dob": "ENCRYPTED", "owner1_ssn": "ENCRYPTED",
  "owner1_title": "", "owner1_percent": 0,
  "has_additional_owners": false,
  "owner2_first": "", "owner2_last": "", "owner2_suffix": "",
  "owner2_address_line1": "", "owner2_city": "", "owner2_state": "", "owner2_zip": "",
  "owner2_phone": "", "owner2_citizenship": "",
  "owner2_dob": "ENCRYPTED", "owner2_ssn": "ENCRYPTED",
  "owner2_title": "", "owner2_percent": 0,
  "owner3_first": "", "owner3_last": "", "owner3_suffix": "",
  "owner3_address_line1": "", "owner3_city": "", "owner3_state": "", "owner3_zip": "",
  "owner3_phone": "", "owner3_citizenship": "",
  "owner3_dob": "ENCRYPTED", "owner3_ssn": "ENCRYPTED",
  "owner3_title": "", "owner3_percent": 0,
  "owns_inventory": "",
  "inventory_on_site": "",
  "customer_charged_when": "",
  "uses_fulfillment_house": "",
  "delivery_1to7_pct": 0,
  "delivery_8to14_pct": 0,
  "delivery_14plus_pct": 0,
  "b2b_pct": 0,
  "public_pct": 0,
  "monthly_cc_sales": 0,
  "avg_cc_transaction": 0,
  "transactions_per_month": 0,
  "ach_requested": false,
  "monthly_check_sales": 0,
  "checks_per_month": 0,
  "avg_check_amount": 0,
  "max_check_amount": 0,
  "files": {
    "voided_check": { "name": "", "data": "base64..." },
    "drivers_license": { "name": "", "data": "base64..." },
    "articles_of_incorporation": { "name": "", "data": "base64..." },
    "irs_tax_id_letter": { "name": "", "data": "base64..." },
    "bank_statements": { "name": "", "data": "base64..." },
    "processing_statements": { "name": "", "data": "base64..." },
    "business_financials": { "name": "", "data": "base64..." },
    "ach_bank_statement": { "name": "", "data": "base64..." },
    "ach_proof_of_business": { "name": "", "data": "base64..." }
  }
}
```

---

## n8n Workflows

### Webhook registry additions

| Webhook path | Trigger | Action |
|---|---|---|
| `/webhook/lead-created` | New lead record in Airtable (or button) | Create Dropbox folder, write path back to lead |
| `/webhook/send-form` | Button in leads.html | Email merchant with form URL + leadId, set status → Form Sent |
| `/webhook/merchant-form-submit` | Form POST from merchant-form.html | Write all fields to lead, save files to Dropbox, set status → Form Received |
| `/webhook/convert-lead` | Button in leads.html | Create Company + Contact, move Dropbox folder, set status → Converted |

### Workflow 1 — Lead Created
Trigger: Airtable trigger on new Leads record
1. Read `Lead Name` from record
2. Dropbox: create folder at `_CoCard/_Leads/[Lead Name]/`
3. Airtable PATCH: write folder path to `Dropbox Folder Path` field

### Workflow 2 — Send Form
Trigger: POST from leads.html with `{ leadId, contactEmail, contactFirst, dbaName }`
1. Build form URL: `https://karenwidas.github.io/_DevPlus/_Self/leads/merchant-form.html?leadId=[leadId]`
2. Send email to `contactEmail` with form link
3. Airtable PATCH: set `Status` → `Form Sent`, set `Form Sent Date` → today

### Workflow 3 — Form Submitted
Trigger: POST from merchant-form.html with full payload
1. Extract `leadId` from payload
2. Airtable PATCH: write all non-file fields to lead record, set `Status` → `Form Received`, set `Form Received Date` → today
3. For each file in payload: upload base64 to Dropbox at `[Dropbox Folder Path]/[filename]`

### Workflow 4 — Convert Lead to Customer
Trigger: TBD
1. Airtable GET: fetch full lead record
2. Airtable POST to Companies: create record with legal name, DBA, address fields
3. Airtable POST to Contacts: create record with contact name/phone/email, linked to new Company
4. Dropbox: move folder from `_CoCard/_Leads/[DBA Name]/` to `_CoCard/_Customers/[DBA Name]/`
5. Airtable PATCH lead: set `Status` → `Converted`, set `Linked Company` → new company record ID

