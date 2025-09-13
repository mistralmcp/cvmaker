from fastmcp import FastMCP
from pathlib import Path
from uuid import uuid4

from src.prompts import RESUME_INSTRUCTIONS_PROMPT
from src.generate import generate_resume
from src.utils import upload_to_bucket


PROJECT_ROOT = Path(__file__).parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
TEMPLATE_NAME = "classic.tex.j2"
OUTPUT_DIR = PROJECT_ROOT / "build"


mcp = FastMCP(name="cvmaker")


@mcp.prompt
def base_instructions():
    """
    Base instructions to follow when extracting the candidate's information for the resumé.
    """
    return RESUME_INSTRUCTIONS_PROMPT


@mcp.tool(
    name="generate_resume_pdf",
    description="Generate a professional resume PDF from structured data. Takes personal information, education, experience, publications, projects, and skills as input and produces a formatted PDF using LaTeX.",
)
def generate_resume_pdf(
    pdf_title: str,
    pdf_author: str,
    # Required Header
    name: str,
    location: str,
    email: str,
    phone: str,
    # Optional Header
    website_url: str = None,
    website_label: str = None,
    linkedin_url: str = None,
    linkedin_handle: str = None,
    github_url: str = None,
    github_handle: str = None,
    # Intro section
    intro_paragraphs: list = None,
    # Education entries
    education_degrees: list = None,
    education_date_ranges: list = None,
    education_institutions: list = None,
    education_fields_of_study: list = None,
    education_highlights: list = None,
    # Experience entries
    experience_companies: list = None,
    experience_roles: list = None,
    experience_locations: list = None,
    experience_date_ranges: list = None,
    experience_highlights: list = None,
    # Publication entries
    publication_dates: list = None,
    publication_titles: list = None,
    publication_authors: list = None,
    publication_doi_urls: list = None,
    publication_doi_labels: list = None,
    # Project entries
    project_titles: list = None,
    project_repo_urls: list = None,
    project_repo_labels: list = None,
    project_highlights: list = None,
    # Technologies
    languages: list = None,
    technologies: list = None,
) -> str:
    """
    Generate a professional resume PDF from structured data using LaTeX templating.

    Args:
        pdf_title (str): Title metadata for the PDF document
        pdf_author (str): Author metadata for the PDF document
        name (str): Full name of the candidate
        location (str): Current location/city of the candidate
        email (str): Contact email address
        phone (str): Contact phone number
        website_url (str, optional): URL to personal website
        website_label (str, optional): Display label for website URL
        linkedin_url (str, optional): URL to LinkedIn profile
        linkedin_handle (str, optional): LinkedIn username/handle
        github_url (str, optional): URL to GitHub profile
        github_handle (str, optional): GitHub username/handle
        intro_paragraphs (list, optional): List of introduction/summary paragraphs
        education_degrees (list, optional): List of degree names/titles
        education_date_ranges (list, optional): List of education date ranges (e.g., ["2018-2022"])
        education_institutions (list, optional): List of educational institutions
        education_fields_of_study (list, optional): List of fields/majors studied
        education_highlights (list, optional): List of lists containing bullet points for each education entry
        experience_companies (list, optional): List of company names
        experience_roles (list, optional): List of job titles/roles
        experience_locations (list, optional): List of job locations
        experience_date_ranges (list, optional): List of employment date ranges
        experience_highlights (list, optional): List of lists containing bullet points for each experience entry
        publication_dates (list, optional): List of publication dates
        publication_titles (list, optional): List of publication titles
        publication_authors (list, optional): List of author lists for each publication
        publication_doi_urls (list, optional): List of DOI URLs for publications
        publication_doi_labels (list, optional): List of DOI display labels
        project_titles (list, optional): List of project titles
        project_repo_urls (list, optional): List of repository/project URLs
        project_repo_labels (list, optional): List of repository/project display labels
        project_highlights (list, optional): List of lists containing bullet points for each project
        languages (list, optional): List of programming languages
        technologies (list, optional): List of technologies/frameworks/tools

    Returns:
        str: Absolute path to the generated PDF file

    Note:
        - All list parameters should have matching lengths within their respective sections
        - For optional sections, all related parameters should either all be provided or all be None
        - The generated PDF uses the classic LaTeX template located in the templates directory
    """
    base_name = str(uuid4().hex)

    pdf_path = generate_resume(
        base_name=base_name,
        # Document meta
        pdf_title=pdf_title,
        pdf_author=pdf_author,
        # Header
        name=name,
        location=location,
        email=email,
        phone=phone,
        website_url=website_url,
        website_label=website_label,
        linkedin_url=linkedin_url,
        linkedin_handle=linkedin_handle,
        github_url=github_url,
        github_handle=github_handle,
        # Intro section
        intro_paragraphs=intro_paragraphs,
        # Education entries
        education_degrees=education_degrees,
        education_date_ranges=education_date_ranges,
        education_institutions=education_institutions,
        education_fields_of_study=education_fields_of_study,
        education_highlights=education_highlights,
        # Experience entries
        experience_companies=experience_companies,
        experience_roles=experience_roles,
        experience_locations=experience_locations,
        experience_date_ranges=experience_date_ranges,
        experience_highlights=experience_highlights,
        # Publication entries
        publication_dates=publication_dates,
        publication_titles=publication_titles,
        publication_authors=publication_authors,
        publication_doi_urls=publication_doi_urls,
        publication_doi_labels=publication_doi_labels,
        # Project entries
        project_titles=project_titles,
        project_repo_urls=project_repo_urls,
        project_repo_labels=project_repo_labels,
        project_highlights=project_highlights,
        # Technologies
        languages=languages,
        technologies=technologies,
        # Template configuration
        template_name=TEMPLATE_NAME,
        templates_dir=TEMPLATES_DIR,
        output_dir=OUTPUT_DIR,
    )

    if pdf_path.exists():
        return upload_to_bucket(
            file_path=pdf_path, destination_blob_name=f"{base_name}.pdf"
        )
    else:
        return "Error: PDF file not found"


if __name__ == "__main__":
    mcp.run(transport="stdio")
