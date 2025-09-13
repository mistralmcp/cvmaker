import pytest
from pathlib import Path
from unittest.mock import patch
from pydantic import ValidationError

from src.generate import generate_resume


class TestGenerateResume:
    def test_generate_resume_with_minimal_data(
        self, minimal_resume_data, temp_build_dir, mock_render_tex, mock_compile_pdf
    ):
        with patch("src.generate.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "test123"

            result = generate_resume(output_dir=temp_build_dir, **minimal_resume_data)

            assert result == temp_build_dir / "test123.pdf"
            mock_render_tex.assert_called_once()
            mock_compile_pdf.assert_called_once()

    def test_generate_resume_with_full_data(
        self, sample_resume_data, temp_build_dir, mock_render_tex, mock_compile_pdf
    ):
        """Test generate_resume with complete data."""
        with patch("src.generate.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "full_test456"

            result = generate_resume(output_dir=temp_build_dir, **sample_resume_data)

            assert result == temp_build_dir / "full_test456.pdf"
            mock_render_tex.assert_called_once()
            mock_compile_pdf.assert_called_once()

            # Check that render_tex was called with correct data structure
            call_args = mock_render_tex.call_args
            resume_data = call_args[1]["resume_data"]

            # Verify key sections are present
            assert "meta" in resume_data
            assert "header" in resume_data
            assert "education" in resume_data
            assert "experience" in resume_data
            assert "technologies_section" in resume_data

            # Verify header data
            assert resume_data["header"]["name"] == "John Doe"
            assert resume_data["header"]["email"] == "john.doe@example.com"

            # Verify education data
            assert len(resume_data["education"]) == 1
            assert resume_data["education"][0]["degree"] == "Bachelor of Science"

            # Verify experience data
            assert len(resume_data["experience"]) == 2
            assert resume_data["experience"][0]["company"] == "Tech Corp"

    def test_generate_resume_with_invalid_email(
        self, minimal_resume_data, temp_build_dir
    ):
        """Test generate_resume with invalid email raises validation error."""
        minimal_resume_data["email"] = "invalid-email"

        with pytest.raises(ValidationError):
            generate_resume(output_dir=temp_build_dir, **minimal_resume_data)

    def test_generate_resume_with_mismatched_education_arrays(
        self, minimal_resume_data, temp_build_dir, mock_render_tex, mock_compile_pdf
    ):
        """Test generate_resume handles mismatched education array lengths gracefully."""
        minimal_resume_data.update(
            {
                "education_degrees": ["Bachelor of Science", "Master of Science"],
                "education_date_ranges": ["2015-2019"],
                "education_institutions": ["MIT", "Stanford"],
                "education_highlights": [["Magna Cum Laude"]],
            }
        )

        with patch("src.generate.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "mismatch_test"

            result = generate_resume(output_dir=temp_build_dir, **minimal_resume_data)

            assert result == temp_build_dir / "mismatch_test.pdf"

            # Verify the function completes without error
            mock_render_tex.assert_called_once()
            mock_compile_pdf.assert_called_once()

    def test_generate_resume_with_empty_lists(
        self, minimal_resume_data, temp_build_dir, mock_render_tex, mock_compile_pdf
    ):
        """Test generate_resume with empty optional lists."""
        minimal_resume_data.update(
            {
                "intro_paragraphs": [],
                "languages": [],
                "technologies": [],
                "education_degrees": [],
                "experience_companies": [],
            }
        )

        with patch("src.generate.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "empty_test"

            result = generate_resume(output_dir=temp_build_dir, **minimal_resume_data)

            assert result == temp_build_dir / "empty_test.pdf"
            mock_render_tex.assert_called_once()
            mock_compile_pdf.assert_called_once()

    def test_generate_resume_default_paths(
        self, minimal_resume_data, temp_build_dir, mock_render_tex, mock_compile_pdf
    ):
        """Test generate_resume uses default paths when not provided."""
        with patch("src.generate.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "default_paths"

            # Use the default template from main.py
            templates_dir = Path(temp_build_dir).parent / "templates"
            result = generate_resume(
                templates_dir=templates_dir,
                template_name="classic.tex.j2",
                **minimal_resume_data,
            )

            # Should use default project structure for output
            expected_path = Path(__file__).parent.parent / "build" / "default_paths.pdf"
            assert result == expected_path

            mock_render_tex.assert_called_once()
            mock_compile_pdf.assert_called_once()

    def test_generate_resume_custom_template(
        self, minimal_resume_data, temp_build_dir, mock_render_tex, mock_compile_pdf
    ):
        """Test generate_resume with custom template configuration."""
        custom_template_dir = Path(temp_build_dir).parent / "custom_templates"

        with patch("src.generate.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "custom_template"

            result = generate_resume(
                template_name="custom.tex.j2",
                templates_dir=custom_template_dir,
                output_dir=temp_build_dir,
                **minimal_resume_data,
            )

            assert result == temp_build_dir / "custom_template.pdf"

            # Verify custom template configuration was used
            call_args = mock_render_tex.call_args
            assert call_args[1]["template_name"] == "custom.tex.j2"
            assert call_args[1]["templates_dir"] == custom_template_dir

    def test_generate_resume_publications_and_projects(
        self, minimal_resume_data, temp_build_dir, mock_render_tex, mock_compile_pdf
    ):
        """Test generate_resume with publications and projects."""
        minimal_resume_data.update(
            {
                "publication_titles": ["Research Paper 1", "Research Paper 2"],
                "publication_dates": ["2023", "2024"],
                "publication_authors": [["John Doe", "Jane Smith"], ["John Doe"]],
                "publication_doi_urls": ["https://doi.org/10.1000/test1", None],
                "publication_doi_labels": ["DOI:10.1000/test1", None],
                "project_titles": ["Project A", "Project B"],
                "project_repo_urls": [
                    "https://github.com/test/a",
                    "https://github.com/test/b",
                ],
                "project_repo_labels": ["GitHub", "GitHub"],
                "project_highlights": [["Feature 1", "Feature 2"], ["Feature 3"]],
            }
        )

        with patch("src.generate.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "pub_proj_test"

            result = generate_resume(output_dir=temp_build_dir, **minimal_resume_data)

            assert result == temp_build_dir / "pub_proj_test.pdf"

            # Verify publications and projects were processed
            call_args = mock_render_tex.call_args
            resume_data = call_args[1]["resume_data"]

            assert len(resume_data["publications"]) == 2
            assert resume_data["publications"][0]["title"] == "Research Paper 1"
            assert resume_data["publications"][0]["authors"] == [
                "John Doe",
                "Jane Smith",
            ]

            assert len(resume_data["projects"]) == 2
            assert resume_data["projects"][0]["title"] == "Project A"
            assert resume_data["projects"][0]["highlights"] == [
                "Feature 1",
                "Feature 2",
            ]

    @patch("src.generate.compile_pdf")
    @patch("src.generate.render_tex")
    def test_generate_resume_compilation_error_propagates(
        self, mock_render_tex, mock_compile_pdf, minimal_resume_data, temp_build_dir
    ):
        """Test that compilation errors are propagated."""
        mock_compile_pdf.side_effect = RuntimeError("PDF compilation failed")

        with pytest.raises(RuntimeError, match="PDF compilation failed"):
            generate_resume(output_dir=temp_build_dir, **minimal_resume_data)

    @patch("src.generate.render_tex")
    def test_generate_resume_render_error_propagates(
        self, mock_render_tex, minimal_resume_data, temp_build_dir
    ):
        """Test that render errors are propagated."""
        mock_render_tex.side_effect = Exception("Template rendering failed")

        with pytest.raises(Exception, match="Template rendering failed"):
            generate_resume(output_dir=temp_build_dir, **minimal_resume_data)

    def test_generate_resume_with_social_links(
        self, minimal_resume_data, temp_build_dir, mock_render_tex, mock_compile_pdf
    ):
        """Test generate_resume with all social media links."""
        minimal_resume_data.update(
            {
                "website_url": "https://johndoe.com/",
                "website_label": "Portfolio",
                "linkedin_url": "https://linkedin.com/in/johndoe/",
                "linkedin_handle": "johndoe",
                "github_url": "https://github.com/johndoe/",
                "github_handle": "johndoe",
            }
        )

        with patch("src.generate.uuid4") as mock_uuid:
            mock_uuid.return_value.hex = "social_test"

            result = generate_resume(output_dir=temp_build_dir, **minimal_resume_data)

            assert result == temp_build_dir / "social_test.pdf"

            # Verify social links are in header
            call_args = mock_render_tex.call_args
            resume_data = call_args[1]["resume_data"]
            header = resume_data["header"]

            assert str(header["website_url"]) == "https://johndoe.com/"
            assert header["website_label"] == "Portfolio"
            assert str(header["linkedin_url"]) == "https://linkedin.com/in/johndoe/"
            assert header["linkedin_handle"] == "johndoe"
            assert str(header["github_url"]) == "https://github.com/johndoe/"
            assert header["github_handle"] == "johndoe"
