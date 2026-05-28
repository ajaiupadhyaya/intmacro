import subprocess, sys, pathlib, textwrap

REPO = pathlib.Path(__file__).resolve().parent.parent

def run_check(cfg_dir):
    return subprocess.run(
        [sys.executable, str(REPO / "scripts" / "check_toc.py"), "--root", str(cfg_dir)],
        capture_output=True, text=True)

def test_passes_when_all_sidebar_files_exist(tmp_path):
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "a.ipynb").write_text("{}")
    (tmp_path / "index.qmd").write_text("x")
    (tmp_path / "_quarto.yml").write_text(textwrap.dedent("""
        website:
          sidebar:
            contents:
              - section: S
                contents:
                  - content/a.ipynb
    """))
    r = run_check(tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr

def test_fails_when_sidebar_file_missing(tmp_path):
    (tmp_path / "index.qmd").write_text("x")
    (tmp_path / "_quarto.yml").write_text(textwrap.dedent("""
        website:
          sidebar:
            contents:
              - section: S
                contents:
                  - content/missing.ipynb
    """))
    r = run_check(tmp_path)
    assert r.returncode != 0
    assert "missing.ipynb" in r.stdout
