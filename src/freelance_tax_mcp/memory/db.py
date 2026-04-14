from __future__ import annotations

import sqlite3
from pathlib import Path


def get_connection(db_path: Path) -> sqlite3.Connection:
	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row
	conn.execute("PRAGMA foreign_keys = ON")
	return conn


def init_db(db_path: Path) -> None:
	db_path.parent.mkdir(parents=True, exist_ok=True)
	conn = get_connection(db_path)
	with conn:
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS user_profiles (
				user_id TEXT PRIMARY KEY,
				full_name TEXT NOT NULL,
				gst_number TEXT,
				tax_regime TEXT NOT NULL,
				tax_year TEXT NOT NULL,
				updated_at TEXT DEFAULT CURRENT_TIMESTAMP
			)
			"""
		)
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS clients (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id TEXT NOT NULL,
				client_name TEXT NOT NULL,
				client_email TEXT NOT NULL,
				created_at TEXT DEFAULT CURRENT_TIMESTAMP,
				UNIQUE(user_id, client_email)
			)
			"""
		)
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS invoices (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id TEXT NOT NULL,
				invoice_number TEXT NOT NULL,
				client_name TEXT NOT NULL,
				amount REAL NOT NULL,
				issue_date TEXT NOT NULL,
				due_date TEXT NOT NULL,
				status TEXT NOT NULL,
				created_at TEXT DEFAULT CURRENT_TIMESTAMP,
				UNIQUE(user_id, invoice_number)
			)
			"""
		)
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS transactions (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id TEXT NOT NULL,
				txn_type TEXT NOT NULL,
				amount REAL NOT NULL,
				txn_date TEXT NOT NULL,
				notes TEXT DEFAULT '',
				created_at TEXT DEFAULT CURRENT_TIMESTAMP
			)
			"""
		)
		conn.execute(
			"""
			CREATE TABLE IF NOT EXISTS reminders (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id TEXT NOT NULL,
				title TEXT NOT NULL,
				due_date TEXT NOT NULL,
				channel TEXT NOT NULL DEFAULT 'app',
				is_done INTEGER NOT NULL DEFAULT 0,
				created_at TEXT DEFAULT CURRENT_TIMESTAMP
			)
			"""
		)
	conn.close()

