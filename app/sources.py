"""Reference material ("sources") a question can be traced back to.

A source is one of three kinds:
  * text — a pasted passage (stored inline)
  * file — an uploaded document saved on the /data volume; for PDFs and plain
           text we extract the text once and cache it so generation + viewing
           are cheap. The raw file stays downloadable for troubleshooting.
  * url  — just a recorded link (we do NOT fetch it).

Questions carry an optional source_id (ON DELETE SET NULL), so deleting a
source never deletes questions — it just drops the back-reference.
"""
import io
import os
import re

from . import db

# Extensions we can pull text out of for AI generation. Anything else is still
# stored and downloadable, just not used as generation input.
TEXT_EXTS = {".txt", ".md", ".markdown", ".csv", ".rst", ".text"}


def _safe_name(name):
    name = os.path.basename(name or "file")
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name).strip("._") or "file"
    return name[:120]


def _extract_text(filename, data):
    """Best-effort text extraction from uploaded bytes. Returns '' on anything
    we can't read — generation then degrades to 'fewer questions', never a crash."""
    ext = os.path.splitext(filename or "")[1].lower()
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            return "\n".join((page.extract_text() or "") for page in reader.pages).strip()
        except Exception:
            return ""
    if ext in TEXT_EXTS:
        try:
            return data.decode("utf-8", errors="replace").strip()
        except Exception:
            return ""
    return ""


# --- queries --------------------------------------------------------------

def list_for_subject(conn, subject_id):
    return [dict(r) for r in conn.execute(
        "SELECT * FROM sources WHERE subject_id = ? ORDER BY created_at DESC, id DESC",
        (subject_id,))]


def get(conn, source_id):
    row = conn.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()
    return dict(row) if row else None


def label(source):
    """Short display string for a source row (dict)."""
    if not source:
        return ""
    if source["kind"] == "url":
        return source["title"] or source["url"]
    if source["kind"] == "file":
        return source["title"] or source["filename"]
    return source["title"] or "Pasted text"


def text_for_generation(source):
    """The extracted/pasted text usable as generation input ('' for URLs)."""
    return (source["content"] or "").strip() if source else ""


# --- mutations ------------------------------------------------------------

def create_text(conn, subject_id, title, content):
    cur = conn.execute(
        "INSERT INTO sources (subject_id, title, kind, content) VALUES (?, ?, 'text', ?)",
        (subject_id, (title or "Pasted text").strip(), content.strip()))
    return cur.lastrowid


def create_url(conn, subject_id, title, url):
    cur = conn.execute(
        "INSERT INTO sources (subject_id, title, kind, url) VALUES (?, ?, 'url', ?)",
        (subject_id, (title or url).strip(), url.strip()))
    return cur.lastrowid


def save_file(conn, subject_id, title, filename, data):
    """Persist an uploaded file under SOURCES_DIR and cache its extracted text.
    The row is inserted first so its id can name the file on disk."""
    cur = conn.execute(
        "INSERT INTO sources (subject_id, title, kind, filename) VALUES (?, ?, 'file', ?)",
        (subject_id, (title or filename or "file").strip(), filename))
    sid = cur.lastrowid
    path = os.path.join(db.SOURCES_DIR, f"{sid}__{_safe_name(filename)}")
    with open(path, "wb") as f:
        f.write(data)
    conn.execute("UPDATE sources SET file_path = ?, content = ? WHERE id = ?",
                 (path, _extract_text(filename, data), sid))
    return sid


def delete(conn, source_id):
    row = conn.execute("SELECT file_path FROM sources WHERE id = ?", (source_id,)).fetchone()
    if row and row["file_path"]:
        try:
            os.remove(row["file_path"])
        except OSError:
            pass
    conn.execute("DELETE FROM sources WHERE id = ?", (source_id,))
