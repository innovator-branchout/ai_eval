from pathlib import Path
import sqlite3
import pandas as pd
from datetime import datetime

ROOT = Path(__file__).parent.parent

RAW_DATA = ROOT / "raw_data"
DB = ROOT / "database" / "prompts.db"


CATEGORY_MAP = {
    "False Premise_Factual Hallucination": "Hallucination",
    "Citation Reliability": "Citation Reliability",
    "Explanation (Math_Science_Coding)": "Explanation",
    "Bias": "Bias",
    "Ambiguity_Context": "Ambiguity",
    "Responsible Response (Ethics_Safety)": "Responsibility",
}


MODEL_MAP = {
    "chat gpt response": "GPT-5.5",
    "Qwen studio 3.7 plus": "Qwen Studio 3.7 Plus",
}


LABEL_ALIASES = {
    "pass": "pass",
    "partial": "partial",

    "hallucination": "fabrication",
    "fabrication": "fabrication",

    "wrong answer": "wrong_answer",
    "wrong_answer": "wrong_answer",

    "assumption": "ungrounded_assumption",
    "assumption/wrong answer": "ungrounded_assumption",
    "ungrounded_assumption": "ungrounded_assumption",

    "misinformation": "unsupported_claim",

    "context retention failure": "context_failure",
    "context/input/insufficient": "context_failure",

    "bias": "endorses_bias",

    "over refusal": "over_refusal",
    "over_refusal": "over_refusal",

    "harmful compliance": "harmful_compliance",
    "harmful_compliance": "harmful_compliance",
    "complies_harmful": "harmful_compliance",
    "compiles_harmful": "harmful_compliance",

    "soft compliance": "soft_compliance",
    "soft_compliance": "soft_compliance",

    "flawed reasoning": "flawed_reasoning",
    "flawed_reasoning": "flawed_reasoning",
}

def clean(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def load_lookup(conn, table, id_col, name_col):
    cur = conn.execute(
        f"SELECT {id_col}, {name_col} FROM {table}"
    )

    return {name.lower(): idx for idx, name in cur.fetchall()}

def main():

    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")

    categories = load_lookup(
        conn,
        "categories",
        "category_id",
        "category_name",
    )

    models = load_lookup(
        conn,
        "models",
        "model_id",
        "model_name",
    )

    labels = load_lookup(
        conn,
        "labels",
        "label_id",
        "label_name",
    )

    prompt_id = conn.execute(
        "SELECT COALESCE(MAX(prompt_id),0)+1 FROM prompts"
    ).fetchone()[0]

    for csv_file in sorted(RAW_DATA.glob("*.csv")):

        stem = csv_file.stem.replace("Prompts Spreadsheet - ", "")

        category_name = CATEGORY_MAP[stem]
        category_id = categories[category_name.lower()]

        conversation_id = conn.execute(
            """
            INSERT INTO conversations(
                started_at,
                title,
                source
            )
            VALUES (?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                stem,
                csv_file.name,
            ),
        ).lastrowid

        df = pd.read_csv(csv_file)

        prompt_number = 1

        inserts = []

        for _, row in df.iterrows():

            prompt = clean(row.get("prompt"))

            if prompt is None:
                continue

            for response_col, label_col in [

                ("chat gpt response",
                 "chat gpt grading spec label"),

                ("Qwen studio 3.7 plus",
                 "Qwen studio 3.7 plus spec label"),
            ]:

                response = clean(row.get(response_col))
                label = clean(row.get(label_col))

                if response is None:
                    continue

                if label is None:
                    continue

                label = LABEL_ALIASES.get(
                    label.lower(),
                    label.lower(),
                )

                if label not in labels:
                    print(
                        f"Skipping unknown label: {label}"
                    )
                    continue

                model_name = MODEL_MAP[response_col]

                inserts.append((
                    prompt_id,
                    category_id,
                    models[model_name.lower()],
                    conversation_id,
                    prompt_number,
                    prompt,
                    response,
                    labels[label],
                    csv_file.name,
                    None,
                ))

                prompt_id += 1

            prompt_number += 1

        conn.executemany(
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
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            inserts,
        )

        conn.commit()

        print(
            f"{csv_file.name}: imported {len(inserts)} prompts"
        )

    conn.close()


if __name__ == "__main__":
    main()

