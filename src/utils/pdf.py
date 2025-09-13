from __future__ import annotations

import subprocess, platform
from pathlib import Path


def run_tectonic(tex_path: Path, outdir: Path) -> None:
    cmd = [
        "tectonic",
        "--outdir",
        str(outdir),
        str(tex_path),
    ]
    subprocess.run(cmd, check=True)


def run_latexmk(tex_path: Path, outdir: Path) -> None:
    cmd = [
        "latexmk",
        "-pdf",
        "-synctex=1",
        "-interaction=nonstopmode",
        f"-output-directory={outdir}",
        str(tex_path),
    ]
    subprocess.run(cmd, check=True)


def compile_pdf(output_tex_path: Path, output_pdf_path: Path) -> None:
    outdir = output_pdf_path.parent
    outdir.mkdir(parents=True, exist_ok=True)

    engine_preference = "latexmk" if platform.system() == "Linux" else "tectonic"

    if engine_preference == "latexmk":
        try:
            run_latexmk(output_tex_path, outdir)
        except (FileNotFoundError, subprocess.CalledProcessError):
            run_tectonic(output_tex_path, outdir)
    else:
        try:
            run_tectonic(output_tex_path, outdir)
        except (FileNotFoundError, subprocess.CalledProcessError):
            run_latexmk(output_tex_path, outdir)

    if not output_pdf_path.exists():
        raise RuntimeError(f"No PDF file found: {output_pdf_path}")
