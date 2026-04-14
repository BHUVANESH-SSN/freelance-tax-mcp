from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Callable
from datetime import datetime, timezone
from threading import Lock
from typing import Any

from mcp.server.fastmcp import FastMCP

from freelance_tax_mcp.config import get_settings
from freelance_tax_mcp.memory.db import init_db
from freelance_tax_mcp.tools.advance_tax import (
	estimate_advance_tax_tool,
	set_deadline_reminder_tool,
)
from freelance_tax_mcp.tools.gst import calculate_gst_tool
from freelance_tax_mcp.tools.invoice import generate_invoice_pdf_tool
from freelance_tax_mcp.tools.tds import check_tds_liability_tool
from freelance_tax_mcp.utils.tax_calc import explain_tax_bracket

SETTINGS = get_settings()
init_db(SETTINGS.db_path)

mcp = FastMCP(name=SETTINGS.app_name)


class RateLimiter:
	def __init__(self, per_minute: int) -> None:
		self.per_minute = per_minute
		self._lock = Lock()
		self._history: dict[str, deque[float]] = defaultdict(deque)

	def check(self, tool_name: str) -> None:
		now = datetime.now(timezone.utc).timestamp()
		with self._lock:
			bucket = self._history[tool_name]
			while bucket and now - bucket[0] > 60.0:
				bucket.popleft()
			if len(bucket) >= self.per_minute:
				raise ValueError(f"Rate limit exceeded for tool '{tool_name}'")
			bucket.append(now)


rate_limiter = RateLimiter(SETTINGS.rate_limit_per_minute)


def _guarded(tool_name: str, fn: Callable[..., dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
	rate_limiter.check(tool_name)
	try:
		return fn(**kwargs)
	except Exception as exc:
		return {
			"ok": False,
			"tool": tool_name,
			"error": str(exc),
		}


@mcp.tool(description="Calculate GST amounts for a given taxable amount.")
def calculate_gst(
	amount: float,
	gst_rate: float = 18.0,
	intra_state: bool = True,
	annual_turnover: float | None = None,
) -> dict[str, Any]:
	return _guarded(
		"calculate_gst",
		calculate_gst_tool,
		amount=amount,
		gst_rate=gst_rate,
		intra_state=intra_state,
		annual_turnover=annual_turnover,
	)


@mcp.tool(description="Estimate quarterly advance tax obligations and next payment.")
def estimate_advance_tax(
	annual_tax_liability: float,
	paid_so_far: float,
	as_of_date: str | None = None,
) -> dict[str, Any]:
	return _guarded(
		"estimate_advance_tax",
		estimate_advance_tax_tool,
		annual_tax_liability=annual_tax_liability,
		paid_so_far=paid_so_far,
		as_of_date=as_of_date,
	)


@mcp.tool(description="Check TDS-adjusted tax liability or potential refund.")
def check_tds_liability(
	gross_income: float,
	deductible_expenses: float,
	tds_already_deducted: float,
	regime: str = "new",
) -> dict[str, Any]:
	return _guarded(
		"check_tds_liability",
		check_tds_liability_tool,
		gross_income=gross_income,
		deductible_expenses=deductible_expenses,
		tds_already_deducted=tds_already_deducted,
		regime=regime,
	)


@mcp.tool(description="Generate invoice PDF and persist invoice metadata.")
def generate_invoice_pdf(
	user_id: str,
	invoice_number: str,
	freelancer_name: str,
	client_name: str,
	service_description: str,
	amount: float,
	issue_date: str,
	due_date: str,
	gst_rate: float = 18.0,
) -> dict[str, Any]:
	return _guarded(
		"generate_invoice_pdf",
		generate_invoice_pdf_tool,
		db_path=SETTINGS.db_path,
		invoice_output_dir=SETTINGS.invoice_output_dir,
		user_id=user_id,
		invoice_number=invoice_number,
		freelancer_name=freelancer_name,
		client_name=client_name,
		service_description=service_description,
		amount=amount,
		issue_date=issue_date,
		due_date=due_date,
		gst_rate=gst_rate,
	)


@mcp.tool(description="Set deadline reminder for advance tax or GST filing dates.")
def set_deadline_reminder(
	user_id: str,
	due_date: str,
	kind: str = "advance_tax",
	channel: str = "app",
) -> dict[str, Any]:
	return _guarded(
		"set_deadline_reminder",
		set_deadline_reminder_tool,
		db_path=SETTINGS.db_path,
		user_id=user_id,
		due_date=due_date,
		kind=kind,
		channel=channel,
	)


@mcp.tool(description="Explain estimated tax by bracket and effective rate.")
def explain_tax_brackets(annual_income: float, regime: str = "new") -> dict[str, Any]:
	return _guarded(
		"explain_tax_brackets",
		explain_tax_bracket,
		annual_income=annual_income,
		regime=regime,
	)


@mcp.tool(description="Server health and configuration summary.")
def health() -> dict[str, Any]:
	return {
		"ok": True,
		"app_name": SETTINGS.app_name,
		"version": SETTINGS.app_version,
		"tax_year": SETTINGS.tax_year,
		"db_path": str(SETTINGS.db_path),
		"invoice_output_dir": str(SETTINGS.invoice_output_dir),
		"auth_mode": "oauth2.1_placeholder" if SETTINGS.enable_auth else "disabled",
	}


def main() -> None:
	mcp.run(transport="stdio")


if __name__ == "__main__":
	main()

