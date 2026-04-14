# Freelance Tax MCP

MCP server for Indian freelancers to automate common tax workflows: GST checks, advance tax planning, TDS tracking, expense classification, and invoice support.

This project now has a **working MVP**: core MCP server, SQLite memory layer, tax tools, and PDF invoice generation are implemented.

## Why This Project Exists

Freelancers often manage taxes using ad-hoc spreadsheets, scattered invoices, and manual reminders. That creates avoidable problems:

- Missed GST/advance-tax compliance dates
- Incorrect tax estimates due to incomplete expense capture
- Poor cash-flow visibility after TDS and tax obligations
- Time lost switching between CA advice, portals, and documents

This MCP aims to solve that by giving AI assistants a structured, auditable tax toolkit for Indian freelance workflows.

## Current State (13 April 2026)

### Implemented

- MCP server bootstrap and tool registration in [src/freelance_tax_mcp/server.py](src/freelance_tax_mcp/server.py)
- Core tools for GST, TDS, advance tax, reminder scheduling, and invoice PDF generation in [src/freelance_tax_mcp/tools](src/freelance_tax_mcp/tools)
- Tax calculation utilities in [src/freelance_tax_mcp/utils/tax_calc.py](src/freelance_tax_mcp/utils/tax_calc.py)
- Date helpers and PDF generation in [src/freelance_tax_mcp/utils](src/freelance_tax_mcp/utils)
- SQLite persistence layer (profiles, clients, invoices, transactions, reminders) in [src/freelance_tax_mcp/memory](src/freelance_tax_mcp/memory)
- Baseline tests for GST and advance tax in [tests](tests)

### Not Yet Implemented

- OAuth 2.1 production auth flow and scoped token verification
- Live integrations with GST/Income Tax data sources or compliant partner APIs
- Background scheduler/worker for reminders (current reminder tool stores schedule in DB)
- Expanded test coverage for invoice, TDS, and memory query paths
- Prompt strategy in [src/freelance_tax_mcp/prompts/system.py](src/freelance_tax_mcp/prompts/system.py)

## Target Architecture

```text
AI Client (Claude/GPT/other MCP host)
  -> MCP Transport (stdio)
	 -> freelance_tax_mcp.server
		-> Tool Registry
		  -> gst.py
		  -> advance_tax.py
		  -> tds.py
		  -> expenses.py
		  -> invoice.py
		-> Shared Utilities
		  -> tax_calc.py
		  -> date_helpers.py
		  -> pdf_gen.py
		-> Memory Layer
		  -> db.py
		  -> models.py
		  -> queries.py
```

### MCP Flow (How It Works)

1. User asks a tax question in an MCP-capable client.
2. Client chooses an exposed MCP tool from this server.
3. The selected tool validates inputs and invokes calculation utilities.
4. Optional memory read/write persists context (expenses, invoices, reminders).
5. Tool returns structured JSON output (estimates, due dates, warnings, actions).
6. Client presents guidance to the user in plain language.

## Planned MCP Tools

- `gst_status_check`: Estimate GST applicability from turnover and service type.
- `gst_due_dates`: Return filing/payment schedule for selected period.
- `advance_tax_estimate`: Estimate quarterly advance tax under selected regime.
- `tds_impact_report`: Track TDS deductions and expected final liability/refund.
- `classify_expense`: Categorize expense and estimate deductibility confidence.
- `generate_invoice`: Produce invoice payload and optionally export PDF.

## Data Model (Planned)

Primary entities in the memory layer:

- Freelancer profile (PAN/GST flags, tax regime preference)
- Clients and invoices
- Expenses (amount, category, date, evidence status)
- TDS entries
- Filing reminders and compliance events

## How This Solves Real Problems

- Converts scattered tax context into a single structured workflow.
- Reduces compliance risk through due-date and threshold awareness.
- Improves planning via consistent tax estimates tied to live data.
- Enables faster CA collaboration with cleaner summaries and exports.

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

### Install

```bash
uv sync
```

### Environment Setup

Create local env from template:

```bash
cp .env.example .env
```

Minimum required for MVP:

- `FTMCP_DB_PATH` (SQLite file location)
- `FTMCP_INVOICE_DIR` (generated PDF directory)
- `FTMCP_DEFAULT_GST_RATE`
- `FTMCP_RATE_LIMIT_PER_MIN`

Required for production completion:

- OAuth 2.1/JWT validation:
	- `FTMCP_ENABLE_AUTH=true`
	- `FTMCP_OAUTH_ISSUER`
	- `FTMCP_OAUTH_AUDIENCE`
	- `FTMCP_OAUTH_JWKS_URL`
	- `FTMCP_OAUTH_CLIENT_ID`
	- `FTMCP_OAUTH_CLIENT_SECRET`
- External integrations:
	- `GST_PROVIDER_BASE_URL`
	- `GST_PROVIDER_API_KEY`
	- `INCOME_TAX_PROVIDER_BASE_URL`
	- `INCOME_TAX_PROVIDER_API_KEY`
- Reminder delivery:
	- `FTMCP_REMINDER_PROVIDER`
	- `FTMCP_REMINDER_WEBHOOK_URL`
	- `FTMCP_REMINDER_WEBHOOK_SECRET`

### Run

```bash
uv run python main.py
```

You can also use:

```bash
uv run tax-mcp
```

## Development Roadmap

1. Implement MCP server bootstrap in [src/freelance_tax_mcp/server.py](src/freelance_tax_mcp/server.py):
	- Initialize MCP app.
	- Register all tax tools.
	- Add health/version tool.
2. Implement deterministic tax engines in [src/freelance_tax_mcp/utils/tax_calc.py](src/freelance_tax_mcp/utils/tax_calc.py):
	- Regime-aware slabs.
	- Surcharge/cess handling.
	- Advance-tax installment logic.
3. Implement tool modules in [src/freelance_tax_mcp/tools](src/freelance_tax_mcp/tools):
	- Input schemas and validation.
	- Structured outputs with assumptions.
4. Build persistence in [src/freelance_tax_mcp/memory/db.py](src/freelance_tax_mcp/memory/db.py):
	- SQLModel schema.
	- Migrations/initialization.
5. Add robust tests under [tests](tests):
	- Unit tests for tax calculators.
	- Tool-level contract tests.
	- Edge-case tests around dates and thresholds.
6. Add docs/examples:
	- `.env.example` configuration docs.
	- Sample MCP client config snippets.

## Quality and Safety Notes

- Tax outputs should always include assumptions and financial year context.
- Add explicit disclaimer: informational aid, not legal/tax filing advice.
- Validate date boundaries and currency precision to avoid silent errors.

## Immediate Next Milestones

- Milestone 1: OAuth 2.1 + scoped authorization (`read:tax`, `write:invoice`)
- Milestone 2: Tax API integrations and hardened error contracts
- Milestone 3: Production hardening (rate-limit persistence, observability, broader tests)

## License

Add a license file (recommended: MIT or Apache-2.0) before public release.
