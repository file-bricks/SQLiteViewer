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
    assert "Notice" in content
    assert "Issues" in content
    assert "Microsoft Store" in content
    assert '"Parent Organization"' in content
    assert '"Umbrella Ecosystem"' in content
    assert "addopts" in content and "-ra -v" in content


def test_llms_txt_integrity():
    """Verify llms.txt context index recency and structure."""
    llms_file = REPO_ROOT / "llms.txt"
    assert llms_file.is_file(), "llms.txt must exist"
    content = llms_file.read_text(encoding="utf-8")
    assert any(marker in content for marker in [
        "Stand: 2026-09-14",
        "Stand: 2026-09-22",
        "Stand: 2026-10-11",
        "Stand: 2026-10-18",
        "Last-checked: 2026-09-14",
        "Last-checked: 2026-09-22",
        "Last-checked: 2026-10-08",
        "Last-checked: 2026-10-11",
        "Last-checked: 2026-10-18",
    ])
    for i in range(1, 5):
        assert f"[PERSONA-{i:02d}]" in content
    assert "INV-LOCAL-01" in content
    assert "THIRD_PARTY_LICENSES.md" in content
    assert "THIRD_PARTY_LICENSES.txt" in content


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


def test_notice_file_exists_and_valid():
    """Verify root NOTICE file presence, invariants, statutory disclaimer, and attributions."""
    notice_file = REPO_ROOT / "NOTICE"
    assert notice_file.is_file(), "NOTICE file must exist in repository root"
    content = notice_file.read_text(encoding="utf-8")
    assert "SQLiteViewer" in content
    assert "Copyright (c) 2026 Lukas Geiger" in content
    assert "file-bricks" in content
    assert "INV-LOCAL-01" in content
    assert "§ 521 BGB" in content
    assert "PSF-2.0" in content
    assert "Tcl/Tk" in content


def test_gitignore_lock_defense():
    """Verify .gitignore includes multi-host sync and lock protection patterns."""
    gi_file = REPO_ROOT / ".gitignore"
    assert gi_file.is_file(), ".gitignore must exist"
    content = gi_file.read_text(encoding="utf-8")
    for pattern in [
        "LOCK.user.*",
        "LOCK.until.*",
        "LOCK.condition.*",
        "LOCK.antigravity.*",
        "LOCK.team.*",
        "*-WORKSTATION-LG*",
        "*-ASUS*",
        "*-LAPTOP*",
        ".pytest_tmp/",
        "* (kopie)*",
        "* (copy)*",
        "uv.lock",
    ]:
        assert pattern in content, f".gitignore missing safety pattern: {pattern}"


def test_github_actions_workflows_hardened():
    """Verify CI workflows enforce timeout-minutes, concurrency control, and master branch triggers."""
    wf_dir = REPO_ROOT / ".github" / "workflows"
    smoke_wf = wf_dir / "source-platform-smoke.yml"
    stale_wf = wf_dir / "stale.yml"
    welcome_wf = wf_dir / "welcome.yml"

    assert smoke_wf.is_file(), "source-platform-smoke.yml must exist"
    smoke_content = smoke_wf.read_text(encoding="utf-8")
    assert "master" in smoke_content
    assert "windows-latest" in smoke_content
    assert '"3.10"' in smoke_content
    assert "ruff check" in smoke_content
    assert "timeout-minutes:" in smoke_content
    assert "concurrency:" in smoke_content
    assert "permissions:" in smoke_content

    assert stale_wf.is_file(), "stale.yml must exist"
    stale_content = stale_wf.read_text(encoding="utf-8")
    assert "timeout-minutes:" in stale_content
    assert "concurrency:" in stale_content

    assert welcome_wf.is_file(), "welcome.yml must exist"
    welcome_content = welcome_wf.read_text(encoding="utf-8")
    assert "timeout-minutes:" in welcome_content
    assert "concurrency:" in welcome_content


def test_pyproject_pep621_hardening():
    """Verify PEP 621 license-files, minversion, and ruff settings in pyproject.toml."""
    pyproject_file = REPO_ROOT / "pyproject.toml"
    assert pyproject_file.is_file(), "pyproject.toml must exist"
    content = pyproject_file.read_text(encoding="utf-8")
    assert "license-files" in content
    assert '"NOTICE"' in content
    assert "minversion =" in content
    assert "[tool.ruff]" in content


def test_ascii_four_view_topology_bilateral_parity():
    """Verify ASCII Four-View Architectural Topology presence and bilateral parity in README and README_de."""
    content_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    content_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "Visual Four-View Architectural Topology" in content_en
    assert "Visuelle Vier-Sichten-Architekturtopologie" in content_de

    # Check 4 English views
    assert "[VIEW 1: TKINTER GUI, USER INPUT & CLI INTEGRATION]" in content_en
    assert "[VIEW 2: ATOMIC TRANSACTIONAL EXPORT & SERIALIZATION ENGINE]" in content_en
    assert "[VIEW 3: SQLITE3 CORE DRIVER & DDL SCHEMA INTROSPECTION]" in content_en
    assert "[VIEW 4: RUNASINVOKER NON-ELEVATION, ZERO-EGRESS & AUDIT INTEGRITY]" in content_en

    # Check 4 German views
    assert "[SICHT 1: TKINTER-BENUTZEROBERFLÄCHE, NUTZEREINGABEN & CLI-INTEGRATION]" in content_de
    assert "[SICHT 2: ATOMARER TRANSAKTIONALER EXPORT & SERIALISIERUNG]" in content_de
    assert "[SICHT 3: SQLITE3-KERN, SCHEMA-INTROSPEKTION & SICHERE ABFRAGEN]" in content_de
    assert "[SICHT 4: RUNASINVOKER-ISOLATION, ZERO-EGRESS & AUDIT-INTEGRITÄT]" in content_de

    # Check 17 bilateral section anchors in both
    for i in range(1, 18):
        anchor = f'<a id="sec-{i:02d}"></a>'
        assert anchor in content_en, f"Anchor {anchor} missing in README.md"
        assert anchor in content_de, f"Anchor {anchor} missing in README_de.md"


def test_contributing_bilingual_contract():
    """Verify CONTRIBUTING.md contains bilateral Plan D guidelines, 10 invariants, disclaimer, and 48h SLA."""
    contrib_file = REPO_ROOT / "CONTRIBUTING.md"
    assert contrib_file.is_file(), "CONTRIBUTING.md must exist"
    content = contrib_file.read_text(encoding="utf-8")

    assert "## Deutsch" in content
    assert "## English" in content
    assert r"C:\_Local_DEV\repos\SQLiteViewer" in content
    assert "RunAsInvoker" in content
    assert "§ 521 BGB" in content
    assert "support@lukasgeiger.com" in content
    for i in range(1, 11):
        inv = f"INV-LOCAL-{i:02d}"
        assert inv in content, f"{inv} missing in CONTRIBUTING.md"


def test_pep_621_contributing_and_plain_license_urls():
    """Verify pyproject.toml includes Contributing and Level 1 SBOM URLs and license-files whitelist."""
    pyproject_file = REPO_ROOT / "pyproject.toml"
    assert pyproject_file.is_file(), "pyproject.toml must exist"
    content = pyproject_file.read_text(encoding="utf-8")

    assert 'Contributing = "https://github.com/file-bricks/SQLiteViewer/blob/master/CONTRIBUTING.md"' in content
    assert '"Level 1 SBOM (Plain Text)" = "https://github.com/file-bricks/SQLiteViewer/blob/master/THIRD_PARTY_LICENSES.txt"' in content
    assert '"CONTRIBUTING.md"' in content


def test_level_1_sbom_currency_20261011():
    """Verify Level 1 SBOM plain-text companion currency and audit integrity."""
    sbom_txt = REPO_ROOT / "THIRD_PARTY_LICENSES.txt"
    sbom_md = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    assert sbom_txt.is_file(), "THIRD_PARTY_LICENSES.txt must exist"
    assert sbom_md.is_file(), "THIRD_PARTY_LICENSES.md must exist"

    txt_content = sbom_txt.read_text(encoding="utf-8")
    md_content = sbom_md.read_text(encoding="utf-8")

    assert "Checked: 2026-10-11" in txt_content
    assert "Audited: 2026-10-11" in txt_content
    assert "Stand:** 2026-10-11" in md_content
    assert "THIRD_PARTY_LICENSES.txt" in md_content

    # Invariants in both
    for i in range(1, 11):
        inv = f"INV-LOCAL-{i:02d}"
        assert inv in txt_content, f"{inv} missing in THIRD_PARTY_LICENSES.txt"
        assert inv in md_content, f"{inv} missing in THIRD_PARTY_LICENSES.md"


def test_marketing_log_section_7_pfad_b_20261011():
    """Verify local MARKETING-LOG.txt documents Section 7 Pfad B revision and 3 recommendations."""
    marketing_file = REPO_ROOT / "MARKETING-LOG.txt"
    assert marketing_file.is_file(), "MARKETING-LOG.txt must exist"
    content = marketing_file.read_text(encoding="utf-8")

    assert "7. PFAD B MARKETING, DISCOVERABILITY & VISUELLE TOPOLOGIE REVISION (2026-10-11)" in content
    assert "REC-20261011-01" in content
    assert "REC-20261011-02" in content
    assert "REC-20261011-03" in content


def test_badges_recency_and_test_count_20261011():
    """Verify badges in README.md and README_de.md reflect currency and passing tests."""
    content_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    content_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "Verified-2026--10--11-blue.svg" in content_en or "Verified-2026--10--18-blue.svg" in content_en
    assert "Gepr%C3%BCft-2026--10--11-blue.svg" in content_de or "Gepr%C3%BCft-2026--10--18-blue.svg" in content_de
    assert "Contributing-Guidelines" in content_en
    assert "Beitragsrichtlinie" in content_de


def test_version_freeze_discipline_210():
    """Verify version 2.1.0 remains strictly frozen across all metadata manifests per policy T-20260920-167562623."""
    pyproject_file = REPO_ROOT / "pyproject.toml"
    content_pyproject = pyproject_file.read_text(encoding="utf-8")
    assert 'version = "2.1.0"' in content_pyproject

    llms_file = REPO_ROOT / "llms.txt"
    content_llms = llms_file.read_text(encoding="utf-8")
    assert "Version: 2.1.0" in content_llms

    sbom_txt = (REPO_ROOT / "THIRD_PARTY_LICENSES.txt").read_text(encoding="utf-8")
    assert "Version: 2.1.0" in sbom_txt

    sbom_md = (REPO_ROOT / "THIRD_PARTY_LICENSES.md").read_text(encoding="utf-8")
    assert "**Version:** 2.1.0" in sbom_md


def test_pytest_configuration_unified_smoke_discovery():
    """Verify pyproject.toml pytest configuration automatically discovers smoke tests."""
    pyproject_file = REPO_ROOT / "pyproject.toml"
    assert pyproject_file.is_file(), "pyproject.toml must exist"
    content = pyproject_file.read_text(encoding="utf-8")
    assert "*_smoke.py" in content, "pytest configuration must include *_smoke.py pattern"


def test_extended_gitignore_patterns():
    """Verify .gitignore includes duplicate copy patterns and toolchain cache patterns."""
    gi_file = REPO_ROOT / ".gitignore"
    assert gi_file.is_file(), ".gitignore must exist"
    content = gi_file.read_text(encoding="utf-8")
    for pattern in ["* (Kopie)*", "* (Copy)*", ".wheel-smoke/", "wheelhouse/", ".tox/"]:
        assert pattern in content, f".gitignore missing pattern: {pattern}"


def test_subfolder_readme_inventory_documented():
    """Verify Unterordner-README inventory (web_companion) is documented in MARKETING-LOG.txt per P-006."""
    marketing_file = REPO_ROOT / "MARKETING-LOG.txt"
    assert marketing_file.is_file(), "MARKETING-LOG.txt must exist"
    content = marketing_file.read_text(encoding="utf-8")
    assert "web_companion/README.md" in content, "web_companion README inventory must be documented"
    assert "web_companion/README_de.md" in content, "web_companion German parity status must be documented"


def test_marketing_log_section_8_pfad_a_20261018():
    """Verify Section 8 Pfad A technical hygiene entry exists in MARKETING-LOG.txt."""
    marketing_file = REPO_ROOT / "MARKETING-LOG.txt"
    assert marketing_file.is_file(), "MARKETING-LOG.txt must exist"
    content = marketing_file.read_text(encoding="utf-8")
    assert "8. PFAD A REPOSITORY-HYGIENE, CI-MATRIX-HÄRTUNG & PEP 621 STANDARDISIERUNG (2026-10-18)" in content


def test_badges_recency_and_test_count_20261018():
    """Verify badges in README.md and README_de.md reflect 2026-10-18 currency and passing tests."""
    content_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    content_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    assert "Verified-2026--10--18-blue.svg" in content_en
    assert "Gepr%C3%BCft-2026--10--18-blue.svg" in content_de
    assert "Tests-146%20passed" in content_en
    assert "Tests-146%20bestanden" in content_de
    assert "Contributing-Guidelines" in content_en
    assert "Beitragsrichtlinie" in content_de
