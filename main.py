from typing import List, Optional

from fastmcp import FastMCP
from pathlib import Path
from uuid import uuid4
from decouple import config

from src.instructions import (
    RESUME_INSTRUCTIONS_PROMPT,
    SERVER_INSTRUCTIONS,
    TOOL_DESCRIPTION,
)
from src.generate import generate_resume
from src.utils import upload_to_bucket


SERVER_NAME = "salutcv"
PROJECT_ROOT = Path(__file__).parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
TEMPLATE_NAME = "classic.tex.j2"
OUTPUT_DIR = PROJECT_ROOT / "output"


server_kwargs = {
    "name": SERVER_NAME,
    "instructions": SERVER_INSTRUCTIONS,
}


if config("IS_DEV") == "true":
    mcp = FastMCP(**server_kwargs)
else:
    mcp = FastMCP(
        port=3000, 
        stateless_http=True, 
        debug=True, 
        **server_kwargs
    )


@mcp.prompt("")
def base_instructions():
    """
    Base instructions to follow when extracting the candidate's information for the resumé.
    """
    return RESUME_INSTRUCTIONS_PROMPT


@mcp.tool(name="generate_resume_pdf", description=TOOL_DESCRIPTION)
def generate_resume_pdf(
    pdf_title: str,
    pdf_author: str,
    # Required Header
    name: str,
    location: str,
    email: str,
    # Optional Header
    phone: Optional[str] = None,
    website_url: Optional[str] = None,
    website_label: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    linkedin_handle: Optional[str] = None,
    github_url: Optional[str] = None,
    github_handle: Optional[str] = None,
    # Intro section
    intro_paragraphs: Optional[List[str]] = None,
    # Education entries
    education_degrees: Optional[List[str]] = None,
    education_date_ranges: Optional[List[str]] = None,
    education_institutions: Optional[List[str]] = None,
    education_fields_of_study: Optional[List[str]] = None,
    education_highlights: Optional[List[List[str]]] = None,
    # Experience entries
    experience_companies: Optional[List[str]] = None,
    experience_roles: Optional[List[str]] = None,
    experience_locations: Optional[List[str]] = None,
    experience_date_ranges: Optional[List[str]] = None,
    experience_highlights: Optional[List[List[str]]] = None,
    # Publication entries
    publication_dates: Optional[List[str]] = None,
    publication_titles: Optional[List[str]] = None,
    publication_authors: Optional[List[List[str]]] = None,
    publication_doi_urls: Optional[List[str]] = None,
    publication_doi_labels: Optional[List[str]] = None,
    # Project entries
    project_titles: Optional[List[str]] = None,
    project_repo_urls: Optional[List[str]] = None,
    project_repo_labels: Optional[List[str]] = None,
    project_highlights: Optional[List[List[str]]] = None,
    # Technologies
    languages: Optional[List[str]] = None,
    technologies: Optional[List[str]] = None,
) -> str:
    """
    Generate a professional resume PDF from structured data using LaTeX templating.

    Args:
        pdf_title (str): Title metadata for the PDF document
        pdf_author (str): Author metadata for the PDF document
        name (str): Full name of the candidate
        location (str): Current location/city of the candidate
        email (str): Contact email address
        phone (Optional[str]): Contact phone number
        website_url (Optional[str]): URL to personal website
        website_label (Optional[str]): Display label for website URL
        linkedin_url (Optional[str]): URL to LinkedIn profile
        linkedin_handle (Optional[str]): LinkedIn username/handle
        github_url (Optional[str]): URL to GitHub profile
        github_handle (Optional[str]): GitHub username/handle
        intro_paragraphs (Optional[List[str]]): List of introduction/summary paragraphs
        education_degrees (Optional[List[str]]): List of degree names/titles
        education_date_ranges (Optional[List[str]]): List of education date ranges (e.g., ["2018-2022"])
        education_institutions (Optional[List[str]]): List of educational institutions
        education_fields_of_study (Optional[List[str]]): List of fields/majors studied
        education_highlights (Optional[List[List[str]]]): List of lists containing bullet points for each education entry
        experience_companies (Optional[List[str]]): List of company names
        experience_roles (Optional[List[str]]): List of job titles/roles
        experience_locations (Optional[List[str]]): List of job locations
        experience_date_ranges (Optional[List[str]]): List of employment date ranges
        experience_highlights (Optional[List[List[str]]]): List of lists containing bullet points for each experience entry
        publication_dates (Optional[List[str]]): List of publication dates
        publication_titles (Optional[List[str]]): List of publication titles
        publication_authors (Optional[List[List[str]]]): List of author lists for each publication
        publication_doi_urls (Optional[List[str]]): List of DOI URLs for publications
        publication_doi_labels (Optional[List[str]]): List of DOI display labels
        project_titles (Optional[List[str]]): List of project titles
        project_repo_urls (Optional[List[str]]): List of repository/project URLs
        project_repo_labels (Optional[List[str]]): List of repository/project display labels
        project_highlights (Optional[List[List[str]]]): List of lists containing bullet points for each project
        languages (Optional[List[str]]): List of programming languages
        technologies (Optional[List[str]]): List of technologies/frameworks/tools

    Returns:
        str: URL of the generated PDF file
    """
    base_name = str(uuid4().hex)

    pdf_path = generate_resume(
        base_name=base_name,
        template_name=TEMPLATE_NAME,
        templates_dir=TEMPLATES_DIR,
        output_dir=OUTPUT_DIR,
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
    )

    if pdf_path.exists():
        return upload_to_bucket(
            file_path=pdf_path, destination_blob_name=f"{base_name}.pdf"
        )
    else:
        return "Error: PDF file not found"


if __name__ == "__main__":
    mcp.run(transport="http", port=3000)
