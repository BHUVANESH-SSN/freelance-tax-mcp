from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
	app_name: str
	app_version: str
	db_path: Path
	invoice_output_dir: Path
	default_gst_rate: float
	rate_limit_per_minute: int
	tax_year: str
	enable_auth: bool


def get_settings() -> Settings:
	root = Path.cwd()
	db_path = Path(os.getenv("FTMCP_DB_PATH", root / "data" / "freelance_tax.db"))
	invoice_dir = Path(os.getenv("FTMCP_INVOICE_DIR", root / "invoices"))
	invoice_dir.mkdir(parents=True, exist_ok=True)
	db_path.parent.mkdir(parents=True, exist_ok=True)

	return Settings(
		app_name="Freelance Tax MCP",
		app_version=os.getenv("FTMCP_APP_VERSION", "0.1.0"),
		db_path=db_path,
		invoice_output_dir=invoice_dir,
		default_gst_rate=float(os.getenv("FTMCP_DEFAULT_GST_RATE", "18")),
		rate_limit_per_minute=int(os.getenv("FTMCP_RATE_LIMIT_PER_MIN", "120")),
		tax_year=os.getenv("FTMCP_TAX_YEAR", "FY 2025-26"),
		enable_auth=os.getenv("FTMCP_ENABLE_AUTH", "false").lower() == "true",
	)

