import subprocess, sys, pathlib, textwrap

REPO = pathlib.Path(__file__).resolve().parent.parent

def test_generates_alphabetical_glossary(tmp_path):
    gloss = tmp_path / "glossary.yml"
    gloss.write_text(textwrap.dedent("""
        - term: zeta term
          short: "Last alphabetically."
          first_mention: solow_intro
          aka: []
        - term: alpha term
          short: "First alphabetically."
          first_mention: cobb_d_prod
          aka: ["a"]
    """))
    out = tmp_path / "_glossary.qmd"
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build_glossary.py"),
         "--glossary", str(gloss), "--out", str(out)],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    text = out.read_text()
    assert text.index("alpha term") < text.index("zeta term")
    assert "cobb_d_prod.html" in text
    assert "a" in text
