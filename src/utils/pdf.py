from __future__ import annotations

import os
import stat
import tarfile
import platform
import subprocess
from pathlib import Path
from urllib.request import urlopen


BIN_DIR = Path(__file__).resolve().parent.parent / "bin"
TECTONIC_BIN = BIN_DIR / "tectonic"


TECTONIC_URLS = {
    (
        "Linux",
        "x86_64",
    ): "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-unknown-linux-musl.tar.gz",
    (
        "Linux",
        "AMD64",
    ): "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-unknown-linux-musl.tar.gz",
    (
        "Linux",
        "aarch64",
    ): "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-aarch64-unknown-linux-musl.tar.gz",
    (
        "Linux",
        "arm64",
    ): "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-aarch64-unknown-linux-musl.tar.gz",
}


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


def _chmod_x(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IEXEC)


def _download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url) as r, open(dest, "wb") as f:
        f.write(r.read())


def _extract_tectonic_from_tgz(tgz_path: Path, dest_bin: Path) -> None:
    with tarfile.open(tgz_path, "r:gz") as tf:
        member = next(
            (
                m
                for m in tf.getmembers()
                if m.name.endswith("/tectonic") or m.name == "tectonic"
            ),
            None,
        )
        if member is None:
            for m in tf.getmembers():
                if os.path.basename(m.name) == "tectonic":
                    member = m
                    break
        if member is None:
            raise RuntimeError("Tectonic binary not found in archive.")

        tf.extract(member, path=dest_bin.parent)
        extracted_path = dest_bin.parent / member.name
        if extracted_path.resolve() != dest_bin.resolve():
            dest_bin.parent.mkdir(parents=True, exist_ok=True)
            extracted_path.replace(dest_bin)
    _chmod_x(dest_bin)


def _ensure_tectonic() -> None:
    if TECTONIC_BIN.exists():
        return

    system = platform.system()
    machine = platform.machine()

    url = (
        TECTONIC_URLS.get((system, machine))
        or TECTONIC_URLS.get((system, machine.upper()))
        or TECTONIC_URLS.get((system, "x86_64"))
    )
    if not url:
        raise RuntimeError(f"No preconfigured Tectonic binary for {system}/{machine}")

    BIN_DIR.mkdir(parents=True, exist_ok=True)
    tgz_path = BIN_DIR / "tectonic.tgz"
    _download_file(url, tgz_path)
    _extract_tectonic_from_tgz(tgz_path, TECTONIC_BIN)
    tgz_path.unlink(missing_ok=True)


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
