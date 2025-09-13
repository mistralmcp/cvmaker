from typing import List, Optional

from src.models import (
    Resume,
    DocumentMeta,
    Header,
    EducationEntry,
    ExperienceEntry,
    PublicationEntry,
    ProjectEntry,
    Technologies,
)


def validate_resume_model(
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
) -> Resume:
    # Build document meta
    meta_data = DocumentMeta(
        pdf_title=pdf_title,
        pdf_author=pdf_author,
    )

    # Build header
    header = Header(
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
    )

    # Build education entries
    education_entries = []
    if education_degrees:
        for i, degree in enumerate(education_degrees):
            entry = {
                "degree": degree,
                "date_range": education_date_ranges[i]
                if education_date_ranges and i < len(education_date_ranges)
                else "",
                "institution": education_institutions[i]
                if education_institutions and i < len(education_institutions)
                else "",
                "field_of_study": education_fields_of_study[i]
                if education_fields_of_study and i < len(education_fields_of_study)
                else None,
                "highlights": education_highlights[i]
                if education_highlights and i < len(education_highlights)
                else [],
            }
            education_entries.append(EducationEntry(**entry))

    # Build experience entries
    experience_entries = []
    if experience_companies:
        for i, company in enumerate(experience_companies):
            entry = {
                "company": company,
                "role": experience_roles[i]
                if experience_roles and i < len(experience_roles)
                else "",
                "location": experience_locations[i]
                if experience_locations and i < len(experience_locations)
                else "",
                "date_range": experience_date_ranges[i]
                if experience_date_ranges and i < len(experience_date_ranges)
                else "",
                "highlights": experience_highlights[i]
                if experience_highlights and i < len(experience_highlights)
                else [],
            }
            experience_entries.append(ExperienceEntry(**entry))

    # Build publication entries
    publication_entries = []
    if publication_titles:
        for i, title in enumerate(publication_titles):
            entry = {
                "title": title,
                "date": publication_dates[i]
                if publication_dates and i < len(publication_dates)
                else "",
                "authors": publication_authors[i]
                if publication_authors and i < len(publication_authors)
                else [],
                "doi_url": publication_doi_urls[i]
                if publication_doi_urls and i < len(publication_doi_urls)
                else None,
                "doi_label": publication_doi_labels[i]
                if publication_doi_labels and i < len(publication_doi_labels)
                else None,
            }
            publication_entries.append(PublicationEntry(**entry))

    # Build project entries
    project_entries = []
    if project_titles:
        for i, title in enumerate(project_titles):
            entry = {
                "title": title,
                "repo_url": project_repo_urls[i]
                if project_repo_urls and i < len(project_repo_urls)
                else None,
                "repo_label": project_repo_labels[i]
                if project_repo_labels and i < len(project_repo_labels)
                else None,
                "highlights": project_highlights[i]
                if project_highlights and i < len(project_highlights)
                else [],
            }
            project_entries.append(ProjectEntry(**entry))

    # Build technologies section
    technologies_section = Technologies(
        languages=languages or [], technologies=technologies or []
    )

    # Build and validate complete resume data
    resume_data = {
        "meta": meta_data,
        "header": header,
        "intro_paragraphs": intro_paragraphs or [],
        "education": education_entries,
        "experience": experience_entries,
        "publications": publication_entries,
        "projects": project_entries,
        "technologies_section": technologies_section,
    }

    return Resume.model_validate(resume_data)
