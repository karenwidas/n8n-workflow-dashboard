# CoCard Operations Stack — Design System

## Brand colors

| Name | Hex | CSS Variable | Usage |
|---|---|---|---|
| CoCard Navy | `#00304F` | `--cocard-blue` / `--navy` | Primary brand, headers, sidebar, buttons |
| CoCard Green | `#69932F` | `--cocard-green` / `--green` / `--accent` | Accents, success states, active indicators |
| Navy Dark | `#001f33` | `--text` / `--sidebar2` | Body text, darkest navy |
| Navy Mid | `#004570` | `--navy2` | Hover states on navy |
| Green Hover | `#527323` | `--accent-hover` | Hover on green buttons |
| Green Light (bg) | `#eef4e2` | `--chat-light` | Green tint backgrounds |
| Green Border | `#c0d48a` | `--chat-border` | Green-tinted borders |

## Semantic tokens

| Token | Hex | CSS Variable | Usage |
|---|---|---|---|
| Background | `#eef2f5` | `--bg` | Page background |
| Surface / Card | `#ffffff` | `--surface` / `--card` | Card backgrounds |
| Surface 2 | `#e8eef3` | `--surface2` | Inset areas, sidebar bg, toggleable panels |
| Border | `#c8d8e4` | `--border` | Default borders everywhere |
| Border Light | `#dce8f0` | `--border-light` / `--form-light` | Lighter borders, form tints |
| Border Strong | `#9ab5c8` | `--border-strong` | Emphasized borders, form-accent borders |
| Text Primary | `#001f33` | `--text` | All body text |
| Text Secondary | `#2a5070` | `--text-secondary` | Subtitles, card meta, nav items |
| Muted | `#6a8fa8` | `--muted` | Placeholders, disabled, timestamps |
| Sidebar Text | `#9ab5c8` | `--sidebar-text` | Text inside navy sidebar/header |
| Success / Green | `#69932F` | `--success` | Success states (same as brand green) |
| Error / Danger | `#b33000` | `--error` | Error messages, close feedback |
| Danger Alt | `#c0392b` | `--danger` | Danger buttons, destructive actions |
| Warning | `#b86e00` | `--warning` | Warning states |
| Warning Bg | `#e68a00` | (btn-warn) | Warning button fill |

## Shadows

```css
--shadow:    0 2px 8px  rgba(0,48,79,0.10);   /* default card shadow */
--shadow-md: 0 4px 16px rgba(0,48,79,0.14);   /* hover / elevated */
```

Sidebar box-shadow: `2px 0 12px rgba(0,48,79,.1)` (right edge shadow)

## Typography

### Font stack
```css
font-family: Arial, Tahoma, Helvetica, sans-serif;
```
Used for everything. No web fonts loaded — no external dependencies.

Headings/brand text use `Tahoma, Arial, sans-serif` (Tahoma first for the slightly wider feel).

### Scale
| Role | Size | Weight | Transform | Letter-spacing |
|---|---|---|---|---|
| Page title (header h1) | 22px | 700 | uppercase | 1px |
| App title (sidebar h1) | 15px | 700 | uppercase | 0.5px |
| Card title | 15px | 700 | — | — |
| Detail title | 19px | 700 | — | -0.2px |
| Section label (group) | 11px | 600 | uppercase | 2.5px |
| Section title (panel) | 10px | 700 | uppercase | 0.6px |
| Form label | 10–11px | 600–700 | uppercase | 0.5–0.8px |
| Body / inputs | 13px | 400 | — | — |
| Badge / chip | 9–10px | 700 | uppercase | 0.3–0.8px |
| Meta / timestamps | 11–12px | 400–500 | — | — |
| Tiny label (count) | 10px | 700 | uppercase | 0.6px |

---

## Spacing

### Standard padding values
- Page content: `32px 40px` (dashboard), `28px 32px` (forecast)
- Card padding: `22px`
- Sidebar header: `18px 16px 14px`
- Detail header: `16px 22px`
- Section title bar: `10px 16px`
- Form field grid: `14px 16px`
- Button (standard): `7px 15px`
- Button (small): `4px 10px`
- Input: `8px 10px`
- Badge/chip: `2–3px 7–9px`

### Gap values
- Card grid gap: `16px`
- Section-to-section (group): `40px` bottom margin
- Group label to cards: `14px`
- Field grid gap: `12px`
- Button row gap: `7px`
- Badge row gap: `4px`

### Max widths
- Dashboard main: `1400px`
- Modal: `440px` (95vw on mobile)

---

## Border radius

| Context | Radius |
|---|---|
| Cards / modals | `12px` |
| Panels (ticket form, chat) | `8px` |
| Buttons (standard) | `8px` (dashboard), `5px` (ticket manager) |
| Inputs / selects | `6px` |
| Section containers | `8px` |
| Badges / chips | `3px` |
| Status dot / nav dot | `50%` (circle) |
| Toggle switch | `9px` (pill) |
| Typeahead dropdown | `6px` |
| Modal | `10px` |

---

## Components

### Header
```html
<header> <!-- background: --cocard-blue; border-bottom: 3px solid --cocard-green -->
  <div class="header-left">
    <h1>App Name</h1>          <!-- 22px, 700, uppercase, white -->
    <p>subtitle</p>            <!-- 12px, rgba(255,255,255,0.6) -->
  </div>
  <div class="status-bar">
    <div class="status-dot"></div>   <!-- 7px circle, --cocard-green, pulse animation -->
    <span>Last updated…</span>
    <button class="refresh-btn">↻ Refresh</button>
  </div>
</header>
```

Header is `position: sticky; top: 0; z-index: 100` in forecast/ticket manager.

### Sidebar (nav panel)
```html
<nav> <!-- width: 240–380px; border-right: 1px solid --border; box-shadow right edge -->
  <div id="nav-header"> <!-- background: --cocard-blue; border-bottom: 3px solid --cocard-green -->
    <h2>Section Title</h2>     <!-- white, 13–15px, uppercase -->
    <small>subtitle</small>    <!-- #9ab5c8, 10–11px, uppercase -->
  </div>
  <!-- nav items: 3px left border on active, --cocard-green; active bg: #eef4e2 -->
</nav>
```

### Card (dashboard)
```html
<div class="card" style="--card-accent: var(--cocard-blue);">
  <!-- 3px top border via ::before uses --card-accent -->
  <!-- hover: translateY(-2px) + shadow-md -->
  <div class="card-header">
    <div class="card-title">Title</div>
    <span class="card-type type-form">Form</span>  <!-- badge -->
  </div>
  <div class="card-meta">Description · <strong>Output</strong></div>
  <!-- content / buttons -->
</div>
```

Card accent colors by type:
- Form / ticket actions: `--cocard-blue` (`#00304F`)
- Chat / AI agents: `--cocard-green` (`#69932F`)
- Scheduled / Obsidian: `--cocard-blue`

### Card (ticket list item)
```html
<div class="tcard"> <!-- ::before = 3px green top border -->
  <div class="tc-top">
    <span class="tc-id">#123</span>
    <span class="tc-tasks">3/5 tasks</span>
  </div>
  <div class="tc-company">Company Name</div>
  <div class="tc-subject">Ticket subject line</div>
  <div class="tc-meta">
    <span class="badge bs-open">Open</span>
    <span class="badge bp-normal">Normal</span>
    <span class="badge btype">Question</span>
    <span class="due-lbl">Due Mar 20</span>
  </div>
</div>
```

Active state: `.tcard.active` → `background: #f0f8ea; border-color: #c0d48a`
Closed state: `.tcard.closed` → `background: #f5f8fa; border-color: #dce8f0; ::before = #9ab5c8`

### Section group label (dashboard)
```css
.group-label {
  font-size: 11px; font-weight: 600; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--muted);
  display: flex; align-items: center; gap: 12px;
}
.group-label::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}
```

### Section title bar (ticket manager panels)
```css
.sec-title {
  padding: 10px 16px;
  font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px;
  color: var(--sidebar); /* --cocard-blue */
  border-bottom: 1px solid var(--border-light);
  background: #f0f5f8;
  border-left: 3px solid var(--accent); /* green left accent */
}
```

### Buttons

**Primary (filled green)**
```css
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: var(--accent-hover); /* #527323 */ }
```

**Navy (filled navy)**
```css
.btn-navy { background: var(--cocard-blue); color: #fff; }
.btn-navy:hover { background: #001e30; }
```

**Ghost (outline)**
```css
.btn-ghost {
  background: transparent;
  border: 1.5px solid var(--border);
  color: var(--muted);
  text-transform: uppercase;
}
.btn-ghost:hover { background: var(--bg); color: var(--text); border-color: var(--text); }
```

**Danger**
```css
.btn-danger { background: #c0392b; color: #fff; }
.btn-danger:hover { background: #a81818; }
```

**Warning**
```css
.btn-warn { background: #e68a00; color: #fff; }
.btn-warn:hover { background: #c47400; }
```

**Toggle button (dashboard)** — fills on hover:
```css
/* Light bg / colored border / colored text → fills to solid on hover */
.chat-toggle { background: var(--chat-light); border: 1.5px solid var(--chat-border); color: var(--chat-accent); }
.chat-toggle:hover { background: var(--chat-accent); color: #fff; }
```

**All buttons shared**
```css
.btn {
  padding: 7px 15px; border-radius: 5px; border: none; cursor: pointer;
  font-size: 12px; font-weight: 700; letter-spacing: 0.2px;
  text-transform: uppercase; font-family: inherit;
  transition: all 0.15s;
}
.btn:disabled { opacity: 0.45; cursor: default; }
```

### Badges

```css
.badge { padding: 2px 7px; border-radius: 3px; font-size: 9px; font-weight: 700; letter-spacing: 0.4px; text-transform: uppercase; }
```

| Class | Background | Text | Usage |
|---|---|---|---|
| `.bs-open` | `#eef4e2` | `#527323` | Status: Open |
| `.bs-wc` / `.bs-wo` / `.bs-woff` | `#fef7e6` | `#7a4800` | Waiting states |
| `.bs-hold` | `#ede9f6` | `#4a2d8a` | On Hold |
| `.bs-closed` | `#fdecea` | `#b33000` | Closed |
| `.bp-low` | `#eef4e2` | `#527323` | Priority Low |
| `.bp-normal` | `#dce8f0` | `#00304F` | Priority Normal |
| `.bp-medium` | `#fef7e6` | `#7a4800` | Priority Medium |
| `.bp-high` | `#fdecea` | `#b33000` | Priority High |
| `.btype` | `#dce8f0` | `#2a5070`, border `#9ab5c8` | Ticket type |
| `.type-form` | `#dce8f0` | `#00304F`, border `#9ab5c8` | Card type: form |
| `.type-chat` | `#eef4e2` | `#69932F`, border `#c0d48a` | Card type: chat |

### Task status badges

| Class | Background | Text |
|---|---|---|
| `.ts-todo` | `#e8f0f8` | `#00304F` |
| `.ts-inprog` | `#edf7ed` | `#1e6630` |
| `.ts-wc` / `.ts-wo` / `.ts-woff` | `#fef7e6` | `#7a4800` |
| `.ts-done` | `#e8f4eb` | `#1e6630` |
| `.ts-ns` | `#f4f6f8` | `#4b5563` |

### Form fields

```html
<!-- Field wrapper -->
<div class="fg">                          <!-- .fg.fw spans full width -->
  <label class="flabel">Field Name</label>
  <input class="finput" type="text" />
  <!-- or <select class="finput"> or <textarea class="finput"> -->
</div>
```

```css
.flabel { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: var(--cocard-blue); }
.finput {
  padding: 7px 10px; border: 1.5px solid var(--border); border-radius: 5px;
  font-size: 13px; color: var(--text); background: #fff; width: 100%;
  font-family: inherit; transition: border 0.15s; outline: none;
}
.finput:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(105,147,47,.12); }
textarea.finput { resize: vertical; min-height: 80px; }
```

### Typeahead dropdown

```html
<div class="typeahead-wrap">
  <input class="ticket-input" type="text" />
  <div class="typeahead-dropdown" id="my-dropdown">
    <div class="typeahead-item" data-id="recXXX">Result Name</div>
    <div class="typeahead-empty">No matches found</div>
  </div>
</div>
```

```css
.typeahead-dropdown { display: none; position: absolute; top: 100%; left: 0; right: 0;
  background: var(--surface); border: 1px solid var(--border-strong);
  border-radius: 6px; z-index: 100; max-height: 180px; overflow-y: auto;
  box-shadow: var(--shadow-md); margin-top: 2px; }
.typeahead-dropdown.open { display: block; }
.typeahead-item { padding: 8px 12px; font-size: 13px; cursor: pointer; transition: background 0.1s; }
.typeahead-item:hover, .typeahead-item.active { background: var(--form-light); color: var(--cocard-blue); }
```

### Status indicator (workflow cards)

```html
<div class="last-run" id="status-{workflowId}">
  <div class="run-status status-loading">
    <div class="run-dot"></div>
    <span>Loading…</span>
  </div>
  <div class="run-time">—</div>
</div>
```

```css
.run-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.status-success { color: var(--success); } .status-success .run-dot { background: var(--success); }
.status-error   { color: var(--error);   } .status-error   .run-dot { background: var(--error); }
.status-loading { color: var(--muted);   } .status-loading .run-dot { background: var(--muted); animation: pulse 1s infinite; }
```

### Toggle switch

```html
<div class="toggle-row" onclick="toggleSomething()">
  <div class="sw" id="my-sw"></div>
  <span>Label text</span>
</div>
```

```css
.sw { width: 34px; height: 18px; background: rgba(255,255,255,.12); border-radius: 9px; position: relative; transition: background .2s; }
.sw.on { background: var(--accent); }
.sw::after { content: ''; position: absolute; width: 14px; height: 14px; background: #fff; border-radius: 50%; top: 2px; left: 2px; transition: transform .2s; }
.sw.on::after { transform: translateX(16px); }
```

### Modal

```html
<div class="modal-bg" id="my-modal">
  <div class="modal-box">
    <h2>Modal Title</h2>
    <p>Description text.</p>
    <!-- form fields, then buttons -->
    <div style="display:flex; gap:8px; justify-content:flex-end; margin-top:16px;">
      <button class="btn btn-ghost" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="confirmModal()">Confirm</button>
    </div>
  </div>
</div>
```

```css
.modal-bg { position: fixed; inset: 0; background: rgba(0,20,35,.55); z-index: 100;
  display: none; align-items: center; justify-content: center; backdrop-filter: blur(2px); }
.modal-bg.show { display: flex; }
.modal-box { background: #fff; border-radius: 10px; padding: 26px; width: 440px;
  max-width: 95vw; box-shadow: 0 24px 64px rgba(0,0,0,.3); border-top: 4px solid var(--accent); }
```

### Feedback messages

```html
<div class="ticket-feedback" id="my-feedback"></div>
```

```css
.ticket-feedback { margin-top: 10px; font-size: 12px; text-align: center; padding: 8px; border-radius: 6px; display: none; }
.ticket-feedback.success { background: #e8f4ef; color: var(--success); display: block; }
.ticket-feedback.error   { background: #fdecea; color: var(--error);   display: block; }
```

---

## Animations

```css
/* Status dot pulse (header) */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.3; }
}

/* Typing indicator (chat) */
@keyframes typing {
  0%, 100% { opacity: 0.3; transform: translateY(0); }
  50%       { opacity: 1;   transform: translateY(-3px); }
}
```

---

## Background texture

Used on the dashboard (`index.html`) body to add a subtle grid:

```css
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%2300304F' fill-opacity='0.04'%3E%3Cpath d='M0 0h40v1H0zM0 0v40h1V0z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 0;
}
/* All content above it needs position: relative; z-index: 1; */
```

---

## Scrollbar styling

```css
::-webkit-scrollbar { width: 3–4px; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 2px; }
/* On dark backgrounds: background: rgba(255,255,255,.15) */
```

---

## Forecast section color scheme

| Section | Background | Dot color |
|---|---|---|
| Overdue | `#fdf1f0` | `#c0392b` (red) |
| Today | `#f0f7ea` | `#69932F` (green) |
| This Week | `#f0f5fa` | `#00304F` (navy) |
| Upcoming | `#f5f0fa` | `#7c5cbf` (purple) |
| Available | `#f5f8fa` | `#7a8a96` (muted) |

---

## PWA / manifest

All apps have PWA setup:
```html
<link rel="manifest" href="/manifest.json">   <!-- or /appname/manifest.json -->
<meta name="theme-color" content="#00304F">
<link rel="apple-touch-icon" href="/icons/icon-appname.svg">
```

Service worker registered in root `sw.js` (dashboard only).

---

## CSS variable template (for new interfaces)

```css
:root {
  --cocard-blue:  #00304F;
  --cocard-green: #69932F;
  --bg:           #eef2f5;
  --surface:      #ffffff;
  --surface2:     #e8eef3;
  --border:       #c8d8e4;
  --border-light: #dce8f0;
  --border-strong:#9ab5c8;
  --text:         #001f33;
  --text2:        #2a5070;
  --muted:        #6a8fa8;
  --accent:       #69932F;
  --accent-hover: #527323;
  --accent-light: rgba(105,147,47,.12);
  --success:      #69932F;
  --error:        #b33000;
  --danger:       #c0392b;
  --warning:      #b86e00;
  --shadow:       0 2px 8px rgba(0,48,79,.10);
  --shadow-md:    0 4px 16px rgba(0,48,79,.14);
}
```
