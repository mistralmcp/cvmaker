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
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        error_msg = f"Tectonic compilation failed for {tex_path}\n"
        if e.stdout:
            error_msg += f"STDOUT: {e.stdout}\n"
        if e.stderr:
            error_msg += f"STDERR: {e.stderr}\n"
        raise RuntimeError(error_msg) from e


def run_latexmk(tex_path: Path, outdir: Path) -> None:
    cmd = [
        "latexmk",
        "-pdf",
        "-synctex=1",
        "-interaction=nonstopmode",
        f"-output-directory={outdir}",
        str(tex_path),
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        error_msg = f"Latexmk compilation failed for {tex_path}\n"
        if e.stdout:
            error_msg += f"STDOUT: {e.stdout}\n"
        if e.stderr:
            error_msg += f"STDERR: {e.stderr}\n"
        raise RuntimeError(error_msg) from e


def compile_pdf(output_tex_path: Path, output_pdf_path: Path) -> None:
    outdir = output_pdf_path.parent
    outdir.mkdir(parents=True, exist_ok=True)

    engine_preference = "latexmk" if platform.system() == "Linux" else "tectonic"

    first_error = None
    second_error = None

    if engine_preference == "latexmk":
        try:
            run_latexmk(output_tex_path, outdir)
        except FileNotFoundError as e:
            first_error = f"latexmk not found: {e}"
            try:
                run_tectonic(output_tex_path, outdir)
            except FileNotFoundError as e2:
                second_error = f"tectonic not found: {e2}"
            except (subprocess.CalledProcessError, RuntimeError) as e2:
                second_error = f"tectonic failed: {e2}"
        except (subprocess.CalledProcessError, RuntimeError) as e:
            first_error = f"latexmk failed: {e}"
            try:
                run_tectonic(output_tex_path, outdir)
            except FileNotFoundError as e2:
                second_error = f"tectonic not found: {e2}"
            except (subprocess.CalledProcessError, RuntimeError) as e2:
                second_error = f"tectonic failed: {e2}"
    else:
        try:
            run_tectonic(output_tex_path, outdir)
        except FileNotFoundError as e:
            first_error = f"tectonic not found: {e}"
            try:
                run_latexmk(output_tex_path, outdir)
            except FileNotFoundError as e2:
                second_error = f"latexmk not found: {e2}"
            except (subprocess.CalledProcessError, RuntimeError) as e2:
                second_error = f"latexmk failed: {e2}"
        except (subprocess.CalledProcessError, RuntimeError) as e:
            first_error = f"tectonic failed: {e}"
            try:
                run_latexmk(output_tex_path, outdir)
            except FileNotFoundError as e2:
                second_error = f"latexmk not found: {e2}"
            except (subprocess.CalledProcessError, RuntimeError) as e2:
                second_error = f"latexmk failed: {e2}"

    if first_error and second_error:
        raise RuntimeError(
            f"Both LaTeX engines failed:\n"
            f"1. {first_error}\n"
            f"2. {second_error}\n"
            f"Please install either tectonic or latexmk to compile LaTeX documents."
        )

    if not output_pdf_path.exists():
        raise RuntimeError(f"No PDF file found: {output_pdf_path}")
