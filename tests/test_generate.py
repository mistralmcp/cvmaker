from pathlib import Path
from src.generate import generate_resume
from src.utils import upload_to_bucket
from uuid import uuid4


SAMPLE_RESUME_DATA = {
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
    "education_highlights": [["Dean's List", "GPA: 3.8", "Thesis: AI in Healthcare"]],
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


def main():
    project_root = Path(__file__).parent
    templates_dir = project_root / "templates"
    output_dir = project_root / "build"
    base_name = str(uuid4().hex)

    pdf_path = generate_resume(
        base_name=base_name,
        templates_dir=templates_dir,
        output_dir=output_dir,
        template_name="classic.tex.j2",
        **SAMPLE_RESUME_DATA,
    )

    if pdf_path.exists():
        url = upload_to_bucket(
            file_path=pdf_path, destination_blob_name=f"{base_name}.pdf"
        )
        print(f"Resume uploaded successfully. Access it at: {url}")
    else:
        print("Error: PDF file not found")


if __name__ == "__main__":
    main()
