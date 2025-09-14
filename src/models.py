from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class DocumentMeta(BaseModel):
    pdf_title: str
    pdf_author: str
    last_updated_text: str = Field(
        default_factory=lambda: datetime.now().strftime("%B %Y")
    )


class Header(BaseModel):
    name: str
    location: str
    email: EmailStr
    phone: Optional[str] = None
    website_url: Optional[HttpUrl] = None
    website_label: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None
    linkedin_handle: Optional[str] = None
    github_url: Optional[HttpUrl] = None
    github_handle: Optional[str] = None


class EducationEntry(BaseModel):
    degree: str
    date_range: str
    institution: str
    field_of_study: Optional[str] = None
    highlights: List[str] = []


class ExperienceEntry(BaseModel):
    company: str
    role: str
    location: str
    date_range: str
    highlights: List[str] = []


class PublicationEntry(BaseModel):
    date: str
    title: str
    authors: List[str]
    doi_url: Optional[HttpUrl] = None
    doi_label: Optional[str] = None


class ProjectEntry(BaseModel):
    title: str
    repo_url: Optional[HttpUrl] = None
    repo_label: Optional[str] = None
    highlights: List[str] = []


class Technologies(BaseModel):
    languages: List[str] = []
    technologies: List[str] = []


class Resume(BaseModel):
    meta: DocumentMeta
    header: Header
    intro_paragraphs: List[str] = []
    education: List[EducationEntry] = []
    experience: List[ExperienceEntry] = []
    projects: List[ProjectEntry] = []
    technologies_section: Technologies
