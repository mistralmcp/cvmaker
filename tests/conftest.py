import pytest
from unittest.mock import patch


@pytest.fixture
def minimal_resume_data():
    return {
        "pdf_title": "John Doe Resume",
        "pdf_author": "John Doe",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "location": "New York, NY",
        "intro_paragraphs": [
            "5+ years of software development experience",
            "Strong focus on clean code and architecture",
            "Experience with Python and JavaScript",
        ],
        "languages": ["English", "French"],
        "technologies": ["Python", "JavaScript"],
        "education_degrees": ["Bachelor of Science"],
        "education_date_ranges": ["2015-2019"],
        "education_institutions": ["MIT"],
        "education_highlights": [["Dean's List", "GPA: 3.8"]],
        "experience_companies": ["Tech Corp"],
        "experience_roles": ["Senior Software Engineer"],
        "experience_date_ranges": ["2019-Present"],
        "experience_highlights": [
            ["Led team of 5 engineers", "Improved system performance by 50%"]
        ],
    }


@pytest.fixture
def sample_resume_data():
    return {
        # Required Document meta
        "pdf_title": "John Doe - Software Engineer Resume",
        "pdf_author": "John Doe",
        # Required Header
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "location": "New York, NY",
        # Optional Header
        "website_url": "https://johndoe.dev",
        "website_label": "Portfolio",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "linkedin_handle": "johndoe",
        "github_url": "https://github.com/johndoe",
        "github_handle": "johndoe",
        # Intro section
        "intro_paragraphs": [
            "Senior software engineer with 5+ years of experience",
            "Passionate about clean code and scalable architecture",
        ],
        # Technologies
        "languages": ["English (Native)", "French (Fluent)"],
        "technologies": ["Python", "JavaScript", "React", "Docker", "AWS"],
        # Education
        "education_degrees": ["Bachelor of Science"],
        "education_date_ranges": ["2015-2019"],
        "education_institutions": ["MIT"],
        "education_fields_of_study": ["Computer Science"],
        "education_highlights": [
            ["Dean's List", "GPA: 3.8", "Thesis: AI in Healthcare"]
        ],
        # Experience
        "experience_companies": ["Tech Corp", "Startup Inc"],
        "experience_roles": ["Senior Software Engineer", "Software Engineer"],
        "experience_locations": ["New York, NY", "San Francisco, CA"],
        "experience_date_ranges": ["2021-Present", "2019-2021"],
        "experience_highlights": [
            ["Led team of 5 engineers", "Improved system performance by 50%"],
            ["Developed microservices architecture", "Reduced deployment time by 70%"],
        ],
        # Publications
        "publication_titles": ["Modern Software Architecture Patterns"],
        "publication_dates": ["2023"],
        "publication_authors": [["John Doe", "Jane Smith"]],
        "publication_doi_urls": ["https://doi.org/10.1000/example"],
        "publication_doi_labels": ["DOI:10.1000/example"],
        # Projects
        "project_titles": ["Open Source Resume Generator"],
        "project_repo_urls": ["https://github.com/johndoe/resume-gen"],
        "project_repo_labels": ["GitHub"],
        "project_highlights": [["Built with Python", "Used by 1000+ developers"]],
    }


@pytest.fixture
def temp_build_dir(tmp_path):
    build_dir = tmp_path / "build"
    build_dir.mkdir()

    # Create templates directory with the default template
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    template = templates_dir / "classic.tex.j2"
    template.write_text("Sample template content")

    # Create custom templates directory for custom template test
    custom_templates_dir = tmp_path / "custom_templates"
    custom_templates_dir.mkdir()
    custom_template = custom_templates_dir / "custom.tex.j2"
    custom_template.write_text("Custom template content")

    return build_dir


@pytest.fixture(autouse=True)
def mock_render_tex():
    with patch("src.generate.render_tex") as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_compile_pdf():
    with patch("src.generate.compile_pdf") as mock:
        yield mock
