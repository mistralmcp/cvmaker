from typing import List, Optional
from pathlib import Path

from .utils import validate_resume_model, render_tex, compile_pdf


def generate_resume(
    base_name: str,
    template_name: str,
    templates_dir: Path,
    output_dir: Path,
    # Required Document meta
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
) -> Path:
    model = validate_resume_model(
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

    out_tex = output_dir / f"{base_name}.tex"
    out_pdf = output_dir / f"{base_name}.pdf"

    render_tex(
        resume_data=model.model_dump(),
        output_tex_path=out_tex,
        template_name=template_name,
        templates_dir=templates_dir,
    )

    compile_pdf(out_tex, out_pdf)

    return out_pdf
