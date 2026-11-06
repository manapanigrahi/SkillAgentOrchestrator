"""Document ingestion skill: extracts Word paragraphs and requirement tables using stdlib only."""
from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

from .models import Requirement

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def _text(node: ET.Element) -> str:
    return "".join(t.text or "" for t in node.findall(".//w:t", NS)).strip()


class DocumentIngestionSkill:
    """Reads the SRS/SDS directly, keeping traceability tied to document requirement IDs."""

    def _body(self, path: Path) -> ET.Element:
        with ZipFile(path) as archive:
            return ET.fromstring(archive.read("word/document.xml")).find(".//w:body", NS)  # type: ignore[return-value]

    def extract_requirements(self, srs: Path) -> list[Requirement]:
        requirements: list[Requirement] = []
        body = self._body(srs)
        for table in body.findall("./w:tbl", NS):
            rows = []
            for row in table.findall("./w:tr", NS):
                cells = [_text(cell) for cell in row.findall("./w:tc", NS)]
                if cells:
                    rows.append(cells)
            if not rows or not rows[0] or rows[0][0] != "ID":
                continue
            header = [cell.lower() for cell in rows[0]]
            if "requirement" not in header:
                continue
            text_index = header.index("requirement")
            priority_index = header.index("priority") if "priority" in header else None
            for row in rows[1:]:
                if len(row) <= text_index or not row[0].startswith(("FR-", "NFR-")):
                    continue
                priority = row[priority_index] if priority_index is not None and len(row) > priority_index else "Quality"
                requirements.append(Requirement(row[0], row[text_index], priority))
        # Business rules are meaningful test inputs even though they are prose, not table rows.
        for paragraph in body.findall("./w:p", NS):
            value = _text(paragraph)
            if value.startswith("BR-") and ":" in value:
                requirements.append(Requirement(value.split(" ", 1)[0], value, "Business rule"))
        return requirements

    def extract_design_notes(self, sds: Path) -> list[str]:
        body = self._body(sds)
        notes = [_text(p) for p in body.findall("./w:p", NS)]
        return [note for note in notes if note and ("API" in note or "webhook" in note.lower() or "test" in note.lower())]
