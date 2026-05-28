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

def test_related_partial_includes_sibling_role(tmp_path):
    # 4-chapter growth track: solow_intro has a prereq (cobb_d_prod), a next
    # (solow_transition which lists solow_intro as prereq), and a fourth chapter
    # (foundations_growth) that is in the same track but is not the prereq, not
    # the next, and not solow_intro itself — so it must land in the sibling slot.
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
        solow_transition:
          track: growth
          title: "Solow Transition Dynamics"
          tldr: "How the economy moves toward steady state."
          prereqs: [solow_intro]
        foundations_growth:
          track: growth
          title: "Foundations of Growth Theory"
          tldr: "Why do some countries grow faster?"
          prereqs: []
    """))
    (tmp_path / "glossary.yml").write_text("[]\n")
    r = run_build_nav(tmp_path)
    assert r.returncode == 0, r.stderr
    related = (tmp_path / "generated" / "solow_intro-related.md").read_text()
    # sibling role must appear in the output
    assert "sibling" in related, "sibling role card missing from related partial"
    # the sibling chapter's title must be present
    assert "Foundations of Growth Theory" in related, (
        "sibling chapter title missing; sibling card was not rendered"
    )
    # verify the card element itself carries the role text (not just coincidental match)
    assert '<div class="im-role">sibling</div>' in related, (
        "im-role sibling div missing; sibling card was not rendered with correct markup"
    )


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
