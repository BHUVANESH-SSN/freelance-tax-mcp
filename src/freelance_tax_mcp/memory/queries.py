from __future__ import annotations

from pathlib import Path
from typing import Any

from freelance_tax_mcp.memory.db import get_connection
from freelance_tax_mcp.memory.models import (
	Client,
	Invoice,
	Reminder,
	Transaction,
	UserProfile,
)


def upsert_user_profile(db_path: Path, profile: UserProfile) -> None:
	conn = get_connection(db_path)
	with conn:
		conn.execute(
			"""
			INSERT INTO user_profiles (user_id, full_name, gst_number, tax_regime, tax_year)
			VALUES (?, ?, ?, ?, ?)
			ON CONFLICT(user_id) DO UPDATE SET
				full_name = excluded.full_name,
				gst_number = excluded.gst_number,
				tax_regime = excluded.tax_regime,
				tax_year = excluded.tax_year,
				updated_at = CURRENT_TIMESTAMP
			""",
			(
				profile.user_id,
				profile.full_name,
				profile.gst_number,
				profile.tax_regime,
				profile.tax_year,
			),
		)
	conn.close()


def add_client(db_path: Path, client: Client) -> None:
	conn = get_connection(db_path)
	with conn:
		conn.execute(
			"""
			INSERT OR IGNORE INTO clients (user_id, client_name, client_email)
			VALUES (?, ?, ?)
			""",
			(client.user_id, client.client_name, client.client_email),
		)
	conn.close()


def add_invoice(db_path: Path, invoice: Invoice) -> None:
	conn = get_connection(db_path)
	with conn:
		conn.execute(
			"""
			INSERT OR REPLACE INTO invoices
			(user_id, invoice_number, client_name, amount, issue_date, due_date, status)
			VALUES (?, ?, ?, ?, ?, ?, ?)
			""",
			(
				invoice.user_id,
				invoice.invoice_number,
				invoice.client_name,
				invoice.amount,
				invoice.issue_date,
				invoice.due_date,
				invoice.status,
			),
		)
	conn.close()


def add_transaction(db_path: Path, transaction: Transaction) -> None:
	conn = get_connection(db_path)
	with conn:
		conn.execute(
			"""
			INSERT INTO transactions (user_id, txn_type, amount, txn_date, notes)
			VALUES (?, ?, ?, ?, ?)
			""",
			(
				transaction.user_id,
				transaction.txn_type,
				transaction.amount,
				transaction.txn_date,
				transaction.notes,
			),
		)
	conn.close()


def add_reminder(db_path: Path, reminder: Reminder) -> int:
	conn = get_connection(db_path)
	with conn:
		cursor = conn.execute(
			"""
			INSERT INTO reminders (user_id, title, due_date, channel)
			VALUES (?, ?, ?, ?)
			""",
			(reminder.user_id, reminder.title, reminder.due_date, reminder.channel),
		)
		row_id = int(cursor.lastrowid)
	conn.close()
	return row_id


def list_recent_invoices(db_path: Path, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
	conn = get_connection(db_path)
	rows = conn.execute(
		"""
		SELECT invoice_number, client_name, amount, issue_date, due_date, status
		FROM invoices
		WHERE user_id = ?
		ORDER BY issue_date DESC
		LIMIT ?
		""",
		(user_id, limit),
	).fetchall()
	conn.close()
	return [dict(row) for row in rows]

