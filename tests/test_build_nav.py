import subprocess, sys, pathlib, tempfile, textwrap, os

REPO = pathlib.Path(__file__).resolve().parent.parent

def run_build_nav(tmp_includes):
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build_nav.py"),
         "--includes", str(tmp_includes), "--out", str(tmp_includes / "generated")],
        capture_output=True, text=True,
    )

def test_generates_prereq_partial(tmp_path):
    (tmp_path / "prereqs.yml").write_text(textwrap.dedent("""
        solow_intro:
          track: growth
          title: "The Solow Growth Model"
          tldr: "Savings sets the level, not the growth rate."
          prereqs: [cobb_d_prod]
        cobb_d_prod:
          track: growth
          title: "Cobb-Douglas Production"
          tldr: "CRS production from K and L."
          prereqs: []
    """))
    (tmp_path / "glossary.yml").write_text("[]\n")
    r = run_build_nav(tmp_path)
    assert r.returncode == 0, r.stderr
    partial = (tmp_path / "generated" / "solow_intro-prereqs.md").read_text()
    assert "im-prereq-chip" in partial
    assert "Cobb-Douglas Production" in partial
    assert "cobb_d_prod.html" in partial

def test_generates_related_partial_with_roles(tmp_path):
    (tmp_path / "prereqs.yml").write_text(textwrap.dedent("""
        solow_intro:
          track: growth
          title: "The Solow Growth Model"
          tldr: "x"
          prereqs: [cobb_d_prod]
        cobb_d_prod:
          track: growth
          title: "Cobb-Douglas Production"
          tldr: "y"
          prereqs: []
        solow_transition:
          track: growth
          title: "Solow Transition"
          tldr: "z"
          prereqs: [solow_intro]
    """))
    (tmp_path / "glossary.yml").write_text("[]\n")
    r = run_build_nav(tmp_path)
    assert r.returncode == 0, r.stderr
    related = (tmp_path / "generated" / "solow_intro-related.md").read_text()
    assert "prereq" in related and "Cobb-Douglas Production" in related
    assert "next" in related and "Solow Transition" in related

def test_generates_tooltip_json(tmp_path):
    (tmp_path / "prereqs.yml").write_text("solow_intro: {track: growth, title: S, tldr: t, prereqs: []}\n")
    (tmp_path / "glossary.yml").write_text(textwrap.dedent("""
        - term: steady state
          short: "Where k stops changing."
          first_mention: solow_intro
          aka: ["k*"]
    """))
    r = run_build_nav(tmp_path)
    assert r.returncode == 0, r.stderr
    import json
    data = json.loads((tmp_path / "generated" / "glossary-tooltips.json").read_text())
    assert data["steady state"]["short"].startswith("Where k")
    assert "k*" in data["steady state"]["aka"]
