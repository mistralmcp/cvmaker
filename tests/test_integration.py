import pytest
from pathlib import Path

from src.generate import generate_resume


@pytest.mark.integration
def test_pdf_generation(sample_resume_data, temp_build_dir):
    """Integration test for actual PDF generation."""
    templates_dir = Path(temp_build_dir).parent / "templates"
    templates_dir.mkdir(exist_ok=True)

    project_template = Path(__file__).parent.parent / "templates" / "classic.tex.j2"
    if not project_template.exists():
        pytest.skip("Template file not found")

    template = templates_dir / "classic.tex.j2"
    template.write_text(project_template.read_text())

    pdf_path = generate_resume(
        templates_dir=templates_dir,
        template_name="classic.tex.j2",
        output_dir=temp_build_dir,
        **sample_resume_data,
    )


    assert pdf_path.exists(), "PDF file was not created"
    assert pdf_path.stat().st_size > 0, "PDF file is empty"
