# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "generate_cards.py"
    )
    spec = importlib.util.spec_from_file_location("generate_cards", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_extract_section_parses_markdown_block() -> None:
    module = _load_module()
    body = "## Scenario\n\n### Description\nAlpha\n\n### How Might We\nBeta\n"
    assert module.extract_section(body, "Description") == "Alpha"
    assert module.extract_section(body, "How Might We") == "Beta"


def test_template_selection_for_supported_card_types() -> None:
    module = _load_module()
    assert module.template_for_type("Vision Statement").name == "vision.content.yaml"
    assert module.template_for_type("Problem Statement").name == "problem.content.yaml"
    assert module.template_for_type("Scenario").name == "scenario.content.yaml"
    assert module.template_for_type("Use Case").name == "use-case.content.yaml"
    assert module.template_for_type("Persona").name == "persona.content.yaml"


def test_emit_content_yaml_shape(tmp_path: Path) -> None:
    module = _load_module()
    canonical = tmp_path / "canonical"
    canonical.mkdir(parents=True)
    (canonical / "vision-statement.md").write_text(
        "---\ntitle: Vision Statement\n---\n\n## Vision Statement\nA customer-ready vision.",
        encoding="utf-8",
    )

    cards = module.collect_cards(canonical)
    output_dir = tmp_path / "render" / "content"
    module.write_outputs(cards, output_dir)

    rendered = (output_dir / "slide-001" / "content.yaml").read_text(encoding="utf-8")
    assert "slide:" in rendered
    assert "elements:" in rendered
    assert "{{TITLE}}" not in rendered


def test_regression_body_max_does_not_raise(tmp_path: Path) -> None:
    module = _load_module()
    canonical = tmp_path / "canonical"
    (canonical / "scenarios").mkdir(parents=True)
    (canonical / "scenarios" / "scenario-a.md").write_text(
        "---\ntitle: Scenario A\n---\n\n## Scenario A\n\n"
        "### Description\nA\n\n"
        "### Scenario Narrative\nB\n\n"
        "### How Might We\nC\n",
        encoding="utf-8",
    )

    cards = module.collect_cards(canonical)
    output_dir = tmp_path / "render" / "content"
    module.write_outputs(cards, output_dir)

    assert (output_dir / "slide-001" / "content.yaml").exists()


def test_regression_t_s_escaped_in_rendered_yaml() -> None:
    module = _load_module()
    card = module.Card(
        artifact_type="Vision Statement",
        title='A "quoted" title',
        summary='Summary with "quotes" and newline\\nnext',
        source_path="vision-statement.md",
        last_updated="2026-04-21",
    )
    rendered = module.render_slide(card, 1)
    assert '\\"quoted\\"' in rendered
    assert "Summary with \\" in rendered
