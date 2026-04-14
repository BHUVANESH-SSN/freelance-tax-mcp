from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserProfile:
	user_id: str
	full_name: str
	gst_number: str | None
	tax_regime: str
	tax_year: str


@dataclass
class Client:
	user_id: str
	client_name: str
	client_email: str


@dataclass
class Invoice:
	user_id: str
	invoice_number: str
	client_name: str
	amount: float
	issue_date: str
	due_date: str
	status: str = "issued"


@dataclass
class Transaction:
	user_id: str
	txn_type: str
	amount: float
	txn_date: str
	notes: str = ""


@dataclass
class Reminder:
	user_id: str
	title: str
	due_date: str
	channel: str = "app"

