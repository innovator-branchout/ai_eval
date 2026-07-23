import sqlite3
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).parent.parent / "database" / "prompts.db"


# Dataclasses


@dataclass(slots=True)
class Prompt:
    prompt_id: int
    category_id: int
    model_id: int
    conversation_id: int
    prompt_number: int

    prompt_text: str
    raw_output: str | None = None
    label_id: int | None = None

    source: str | None = None
    notes: str | None = None


@dataclass(slots=True)
class Category:
    category_id: int
    category_name: str
    description: str | None = None


@dataclass(slots=True)
class Model:
    model_id: int
    model_name: str
    provider: str | None = None
    model_version: str | None = None
    notes: str | None = None


@dataclass(slots=True)
class Conversation:
    conversation_id: int
    started_at: str
    title: str | None = None
    source: str | None = None
    notes: str | None = None


@dataclass(slots=True)
class Label:
    label_id: int
    label_name: str
    status: bool
    severity: int
    description: str | None = None


# Row mappers


def _row_to_prompt(row: sqlite3.Row) -> Prompt:
    return Prompt(
        prompt_id=row["prompt_id"],
        category_id=row["category_id"],
        model_id=row["model_id"],
        conversation_id=row["conversation_id"],
        prompt_number=row["prompt_number"],
        prompt_text=row["prompt_text"],
        raw_output=row["raw_output"],
        label_id=row["label_id"],
        source=row["source"],
        notes=row["notes"],
    )


def _row_to_category(row: sqlite3.Row) -> Category:
    return Category(
        category_id=row["category_id"],
        category_name=row["category_name"],
        description=row["description"],
    )


def _row_to_model(row: sqlite3.Row) -> Model:
    return Model(
        model_id=row["model_id"],
        model_name=row["model_name"],
        provider=row["provider"],
        model_version=row["model_version"],
        notes=row["notes"],
    )


def _row_to_conversation(row: sqlite3.Row) -> Conversation:
    return Conversation(
        conversation_id=row["conversation_id"],
        started_at=row["started_at"],
        title=row["title"],
        source=row["source"],
        notes=row["notes"],
    )


def _row_to_label(row: sqlite3.Row) -> Label:
    return Label(
        label_id=row["label_id"],
        label_name=row["label_name"],
        status=bool(row["status"]),
        severity=row["severity"],
        description=row["description"],
    )


# DB connection


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Categories


def add_category(name: str, description: str = ""):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO categories(category_name, description)
            VALUES (?, ?)
            """,
            (name, description),
        )


# updates both the name and description
def update_category(category_id: int, name: str, description: str = ""):
    with connect() as conn:
        conn.execute(
            """
            UPDATE categories
            SET category_name = ?, description = ?
            WHERE category_id = ?
            """,
            (name, description, category_id),
        )


# This will delete all prompts associated with the category first to avoid foreign key constraint error.
# All prompts of the category will be deleted(and will not be moved into another category) Might have to edit so that prompts are moved to a different category.
def delete_category(category_id: int):
    with connect() as conn:
        conn.execute(
            """
            DELETE FROM prompts
            WHERE category_id = ?
            """,
            (category_id,),
        )
        conn.execute(
            """
            DELETE FROM categories
            WHERE category_id = ?
            """,
            (category_id,),
        )


def list_categories() -> list[Category]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM categories
            ORDER BY category_name
            """
        ).fetchall()

    return [_row_to_category(r) for r in rows]


# Labels


def add_label(name: str, status: bool, severity: int, description: str = ""):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO labels(
                label_name,
                status,
                severity,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                status,
                severity,
                description,
            ),
        )


def list_labels() -> list[Label]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM labels
            ORDER BY severity DESC
            """
        ).fetchall()

    return [_row_to_label(r) for r in rows]


def get_label(label_id: int) -> Label | None:
    with connect() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM labels
            WHERE label_id = ?
            """,
            (label_id,),
        ).fetchone()

    return _row_to_label(row) if row else None


def search_labels_labelname(labelname: str) -> list[Label]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM labels
            WHERE label_name LIKE ?
            """,
            (f"%{labelname}%",),
        ).fetchall()
    return [_row_to_label(r) for r in rows]

def search_labels_status(status: bool) -> list[Label]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM labels
            WHERE status = ?
            """,
            (status,)
        ).fetchall()
    return [_row_to_label(r) for r in rows]

# Models


def add_model(name: str, provider: str, version: str, notes: str | None = None):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO models(
                model_name,
                provider,
                model_version,
                notes
            )
            VALUES (?, ?, ?, ?)
            """,
            (name, provider, version, notes),
        )


def list_models() -> list[Model]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM models
            ORDER BY model_name
            """
        ).fetchall()

    return [_row_to_model(r) for r in rows]


# you don't have to provide new notes but it will be deleted if set to None
def update_model(
    model_id: int, name: str, provider: str, version: str, notes: str | None = None
):
    with connect() as conn:
        conn.execute(
            """
            UPDATE models
            SET model_name = ?, provider = ?, model_version = ?, notes = ?
            WHERE model_id = ?
            """,
            (name, provider, version, notes, model_id),
        )


# Conversations


def add_conversation(
    started_at: str,
    title: str | None = None,
    source: str | None = None,
    notes: str | None = None,
) -> int:
    with connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO conversations(
                started_at,
                title,
                source,
                notes
            )
            VALUES (?, ?, ?, ?)
            """,
            (started_at, title, source, notes),
        )
        return cur.lastrowid


def get_conversation(conversation_id: int) -> Conversation | None:
    with connect() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM conversations
            WHERE conversation_id = ?
            """,
            (conversation_id,),
        ).fetchone()

    return _row_to_conversation(row) if row else None


def list_conversations() -> list[Conversation]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM conversations
            ORDER BY started_at DESC
            """
        ).fetchall()

    return [_row_to_conversation(r) for r in rows]


def delete_conversation(conversation_id: int):
    with connect() as conn:
        # delete prompts first to avoid foreign key constraint error
        conn.execute(
            """
            DELETE FROM prompts
            WHERE conversation_id = ?
            """,
            (conversation_id,),
        )
        conn.execute(
            """
            DELETE FROM conversations
            WHERE conversation_id = ?
            """,
            (conversation_id,),
        )


# Prompts


def add_prompt(prompt: Prompt):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO prompts(
                prompt_id,
                category_id,
                model_id,
                conversation_id,
                prompt_number,
                prompt_text,
                raw_output,
                label_id,
                source,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                prompt.prompt_id,
                prompt.category_id,
                prompt.model_id,
                prompt.conversation_id,
                prompt.prompt_number,
                prompt.prompt_text,
                prompt.raw_output,
                prompt.label_id,
                prompt.source,
                prompt.notes,
            ),
        )


def get_prompt(prompt_id: int) -> Prompt | None:
    with connect() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM prompts
            WHERE prompt_id = ?
            """,
            (prompt_id,),
        ).fetchone()

    return _row_to_prompt(row) if row else None


def get_prompts() -> list[Prompt]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM prompts
            ORDER BY conversation_id, prompt_number
            """
        ).fetchall()

    return [_row_to_prompt(r) for r in rows]


def prompts_by_category(category: str) -> list[Prompt]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT p.*
            FROM prompts p
            JOIN categories c
                ON p.category_id = c.category_id
            WHERE c.category_name = ?
            """,
            (category,),
        ).fetchall()

    return [_row_to_prompt(r) for r in rows]


def prompts_by_model(model: str) -> list[Prompt]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT p.*
            FROM prompts p
            JOIN models m
                ON p.model_id = m.model_id
            WHERE m.model_name = ?
            """,
            (model,),
        ).fetchall()

    return [_row_to_prompt(r) for r in rows]


def prompts_by_label(label: str) -> list[Prompt]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT p.*
            FROM prompts p
            JOIN labels l
                ON p.label_id = l.label_id
            WHERE l.label_name = ?
            """,
            (label,),
        ).fetchall()

    return [_row_to_prompt(r) for r in rows]


def delete_prompt(prompt_id: int):
    with connect() as conn:
        conn.execute(
            """
            DELETE FROM prompts
            WHERE prompt_id = ?
            """,
            (prompt_id,),
        )


def search_prompts(keyword: str) -> list[Prompt]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM prompts
            WHERE prompt_text LIKE ?
            """,
            (f"%{keyword}%",),
        ).fetchall()

    return [_row_to_prompt(r) for r in rows]


def update_prompt_label(prompt_id: int, label_id: int):
    with connect() as conn:
        conn.execute(
            """
            UPDATE prompts
            SET label_id = ?
            WHERE prompt_id = ?
            """,
            (label_id, prompt_id),
        )


# update the prompt and its response(if you edit the prompt it is expected to have a new response)
def update_prompt_and_response(prompt_id: int, prompt: str, response: str):
    with connect() as conn:
        conn.execute(
            """
            UPDATE prompts
            SET prompt_text = ?, raw_output = ?
            WHERE prompt_id = ?
            """,
            (prompt, response, prompt_id),
        )


def update_prompt_category(prompt_id: int, category_id: int):
    with connect() as conn:
        conn.execute(
            """
            UPDATE prompts
            SET category_id = ?
            WHERE prompt_id = ?
            """,
            (category_id, prompt_id),
        )


def update_prompt_model(prompt_id: int, model_id: int):
    with connect() as conn:
        conn.execute(
            """
            UPDATE prompts
            SET model_id = ?
            WHERE prompt_id = ?
            """,
            (model_id, prompt_id),
        )


def update_prompt_conversation(prompt_id: int, conversation_id: int):
    with connect() as conn:
        conn.execute(
            """
            UPDATE prompts
            SET conversation_id = ?
            WHERE prompt_id = ?
            """,
            (conversation_id, prompt_id),
        )


def update_prompt_source(prompt_id: int, source: str):
    with connect() as conn:
        conn.execute(
            """
            UPDATE prompts
            SET source = ?
            WHERE prompt_id = ?
            """,
            (source, prompt_id),
        )


def update_prompt_notes(prompt_id: int, notes: str):
    with connect() as conn:
        conn.execute(
            """
            UPDATE prompts
            SET notes = ?
            WHERE prompt_id = ?
            """,
            (notes, prompt_id),
        )


def export_prompts_to_csv(path: str):
    with connect() as conn:
        df = pd.read_sql("SELECT * FROM prompts", conn)
        df.to_csv(path, index=False)
