from __future__ import annotations

import os
import stat
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TECTONIC_BIN = PROJECT_ROOT / "bin" / "tectonic"


def compile_pdf(
    output_tex_path: Path,
    output_pdf_path: Path,
    extra_tex_inputs: list[Path] | None = None,
) -> None:
    outdir = output_pdf_path.parent
    _run_tectonic(output_tex_path, outdir, extra_tex_inputs=extra_tex_inputs)

    if not output_pdf_path.exists():
        possible = output_tex_path.with_suffix(".pdf")
        if possible.exists():
            possible.rename(output_pdf_path)
        else:
            raise RuntimeError(f"No PDF file found: {output_pdf_path}")


def _ensure_tectonic() -> None:
    if not TECTONIC_BIN.exists():
        raise RuntimeError(f"Tectonic binary not found at {TECTONIC_BIN}")
    
    mode = TECTONIC_BIN.stat().st_mode
    if not mode & stat.S_IEXEC:
        TECTONIC_BIN.chmod(mode | stat.S_IEXEC)


def _run_tectonic(
    tex_path: Path, outdir: Path, extra_tex_inputs: list[Path] | None = None
) -> None:
    _ensure_tectonic()

    env = os.environ.copy()
    texinputs_parts = []
    if extra_tex_inputs:
        texinputs_parts.extend([str(p) for p in extra_tex_inputs if p])

    texinputs_parts.append(str(tex_path.parent))

    existing = env.get("TEXINPUTS", "")
    if existing:
        env["TEXINPUTS"] = os.pathsep.join(texinputs_parts + [existing])
    else:
        env["TEXINPUTS"] = os.pathsep.join(texinputs_parts)
    
    env["TECTONIC_CACHE_DIR"] = "/tmp/tectonic-cache"
    env["TMPDIR"] = "/tmp"
    env["TMP"] = "/tmp"
    env["TEMP"] = "/tmp"
    
    cache_dir = Path("/tmp/tectonic-cache")
    cache_dir.mkdir(parents=True, exist_ok=True)

    outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(TECTONIC_BIN),
        "--keep-logs",
        "--synctex=0",
        "--outdir",
        str(outdir),
        str(tex_path),
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)
    except subprocess.CalledProcessError as e:
        error_msg = f"Tectonic compilation failed for {tex_path}\n"
        if e.stdout:
            error_msg += f"STDOUT:\n{e.stdout}\n"
        if e.stderr:
            error_msg += f"STDERR:\n{e.stderr}\n"
        raise RuntimeError(error_msg) from e
