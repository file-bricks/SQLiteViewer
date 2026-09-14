# -*- coding: utf-8 -*-
"""Contract tests for SQLiteViewer metadata, discoverability, and documentation parity."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_readme_files_exist_and_not_empty():
    readme_en = REPO_ROOT / "README.md"
    readme_de = REPO_ROOT / "README_de.md"
    assert readme_en.is_file(), "README.md must exist"
    assert readme_de.is_file(), "README_de.md must exist"
    assert readme_en.stat().st_size > 3000, "README.md should have full documentation"
    assert readme_de.stat().st_size > 3000, "README_de.md should have full documentation"


def test_readme_bilingual_parity():
    content_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    content_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    # Language switcher checks
    assert "README_de.md" in content_en, "README.md must link to README_de.md"
    assert "README.md" in content_de, "README_de.md must link to README.md"

    # All 10 local invariants present in both
    for i in range(1, 11):
        inv = f"INV-LOCAL-{i:02d}"
        assert inv in content_en, f"{inv} missing in README.md"
        assert inv in content_de, f"{inv} missing in README_de.md"

    # Ecosystem links in both
    assert "https://github.com/file-bricks" in content_en
    assert "https://github.com/file-bricks" in content_de
    assert "https://github.com/open-bricks" in content_en
    assert "https://github.com/open-bricks" in content_de


def test_banner_guardrails_compliance():
    """Verify exactly one banner reference exists on line 1 and no duplicate banners were added (HOOK-BANNER-ASSET-01)."""
    for doc_name in ("README.md", "README_de.md"):
        content = (REPO_ROOT / doc_name).read_text(encoding="utf-8")
        banners = re.findall(r"<img\s+[^>]*banner[^>]*>", content, re.IGNORECASE)
        assert len(banners) == 1, f"Expected exactly 1 banner tag in {doc_name}, found {len(banners)}"
        first_line = content.splitlines()[0]
        assert "assets/banner.svg" in first_line, f"Banner must reside on line 1 of {doc_name}"


def test_mermaid_diagram_syntax():
    """Verify all Mermaid code blocks comply with GitHub parsing rules and HOOK-BANNER-ASSET-01."""
    illegal_chars = set("()[]{}<>")
    edge_label_re = re.compile(r"((?:--+>|<-+>|-\.-+>|==+>)\|)([^|\r\n]+)(\|)")

    for doc_name in ("README.md", "README_de.md"):
        content = (REPO_ROOT / doc_name).read_text(encoding="utf-8")
        blocks = re.findall(r"```mermaid\s*\n(.*?)\n```", content, re.DOTALL)
        assert len(blocks) == 2, f"{doc_name} should contain exactly 2 Mermaid diagrams"

        for block in blocks:
            for line in block.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("%%"):
                    continue
                # Check edge labels for unquoted special characters
                for match in edge_label_re.finditer(line):
                    _, label, _ = match.groups()
                    trimmed = label.strip()
                    if not (trimmed.startswith('"') and trimmed.endswith('"')):
                        for c in illegal_chars:
                            assert c not in trimmed, (
                                f"Unquoted '{c}' in edge label '{trimmed}' in {doc_name}: line '{line}'"
                            )


def test_target_personas_present():
    """Verify all 4 target personas are documented in both README files."""
    for doc_name in ("README.md", "README_de.md"):
        content = (REPO_ROOT / doc_name).read_text(encoding="utf-8")
        for i in range(1, 5):
            persona_id = f"[PERSONA-{i:02d}]"
            assert persona_id in content, f"{persona_id} missing in {doc_name}"


def test_comparative_matrix_present():
    """Verify the 10-dimension comparative matrix covers key competitors."""
    competitors = ["DB Browser for SQLite", "DBeaver", "SQLiteStudio"]
    for doc_name in ("README.md", "README_de.md"):
        content = (REPO_ROOT / doc_name).read_text(encoding="utf-8")
        for competitor in competitors:
            assert competitor in content, f"Competitor '{competitor}' missing in comparative matrix of {doc_name}"


def test_third_party_licenses_audit():
    """Verify THIRD_PARTY_LICENSES.md audit file exists and is complete."""
    lic_file = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    assert lic_file.is_file(), "THIRD_PARTY_LICENSES.md must exist"
    content = lic_file.read_text(encoding="utf-8")
    assert "SPDX-License-Identifier" in content and "MIT" in content
    assert "PSF-2.0" in content
    assert "Tcl/Tk License" in content
    assert "Zero Network Egress" in content
    assert "RunAsInvoker" in content
    for i in range(1, 11):
        assert f"INV-LOCAL-{i:02d}" in content


def test_marketing_log_present():
    """Verify local MARKETING-LOG.txt exists and documents personas and invariants."""
    marketing_file = REPO_ROOT / "MARKETING-LOG.txt"
    assert marketing_file.is_file(), "MARKETING-LOG.txt must exist"
    content = marketing_file.read_text(encoding="utf-8")
    assert "2026-09-14" in content
    for i in range(1, 5):
        assert f"[PERSONA-{i:02d}]" in content
    for i in range(1, 11):
        assert f"INV-LOCAL-{i:02d}" in content


def test_pyproject_metadata_and_urls():
    """Verify PEP 621 URLs and pytest configuration in pyproject.toml."""
    pyproject_file = REPO_ROOT / "pyproject.toml"
    assert pyproject_file.is_file(), "pyproject.toml must exist"
    content = pyproject_file.read_text(encoding="utf-8")
    assert 'version = "2.1.0"' in content
    assert "[project.urls]" in content
    assert "Documentation" in content
    assert "German Documentation" in content
    assert "LLM Context Index" in content
    assert "Third-Party Licenses" in content
    assert "Marketing Log" in content
    assert "Issues" in content
    assert "Microsoft Store" in content
    assert 'addopts = "-ra -v"' in content


def test_llms_txt_integrity():
    """Verify llms.txt context index recency and structure."""
    llms_file = REPO_ROOT / "llms.txt"
    assert llms_file.is_file(), "llms.txt must exist"
    content = llms_file.read_text(encoding="utf-8")
    assert "Stand: 2026-09-14" in content or "Last-checked: 2026-09-14" in content
    for i in range(1, 5):
        assert f"[PERSONA-{i:02d}]" in content
    assert "INV-LOCAL-01" in content
    assert "THIRD_PARTY_LICENSES.md" in content


def test_store_package_consistency():
    """Verify store_package.json identity and Store ID."""
    import json
    store_file = REPO_ROOT / "store_package.json"
    assert store_file.is_file(), "store_package.json must exist"
    with open(store_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data.get("store_id") == "9P6H501XB8JT"
    assert data.get("identity_name") == "Geiger.SQLiteViewerPro"


def test_changelog_recency():
    """Verify CHANGELOG.md contains the 2.1.0 release entry."""
    changelog_file = REPO_ROOT / "CHANGELOG.md"
    assert changelog_file.is_file(), "CHANGELOG.md must exist"
    content = changelog_file.read_text(encoding="utf-8")
    assert "## [2.1.0] - 2026-09-14" in content
