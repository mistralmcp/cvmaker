#!/usr/bin/env python3

from pathlib import Path
from src.generate import generate_resume

PROJECT_ROOT = Path(__file__).parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
TEMPLATE_NAME = "classic.tex.j2"
OUTPUT_DIR = PROJECT_ROOT / "tmp"

OUTPUT_DIR.mkdir(exist_ok=True)

fake_data = {
    "base_name": "test_resume",
    "template_name": TEMPLATE_NAME,
    "templates_dir": TEMPLATES_DIR,
    "output_dir": OUTPUT_DIR,
    
    "pdf_title": "John Doe Resume",
    "pdf_author": "John Doe",
    
    "name": "John Doe",
    "location": "San Francisco, CA",
    "email": "john.doe@example.com",
    "phone": "+1 (555) 123-4567",
    "website_url": "https://johndoe.com",
    "website_label": "johndoe.com",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "linkedin_handle": "johndoe",
    "github_url": "https://github.com/johndoe",
    "github_handle": "johndoe",
    
    "intro_paragraphs": [
        "Experienced software engineer with 5+ years in full-stack development, specializing in Python and JavaScript ecosystems.",
        "Passionate about building scalable systems and mentoring junior developers. Strong background in machine learning and data engineering."
    ],
    
    "education_degrees": [
        "Master of Science in Computer Science",
        "Bachelor of Science in Computer Engineering"
    ],
    "education_date_ranges": [
        "2018-2020",
        "2014-2018"
    ],
    "education_institutions": [
        "Stanford University",
        "University of California, Berkeley"
    ],
    "education_fields_of_study": [
        "Machine Learning & AI",
        "Software Engineering"
    ],
    "education_highlights": [
        [
            "GPA: 3.9/4.0, Magna Cum Laude",
            "Research focus on deep learning for natural language processing",
            "Teaching Assistant for CS229 Machine Learning course"
        ],
        [
            "GPA: 3.8/4.0, Summa Cum Laude",
            "President of Computer Science Student Association",
            "Winner of hackathon competition for mobile app development"
        ]
    ],
    
    "experience_companies": [
        "Tech Innovators Inc.",
        "StartupXYZ",
        "University Research Lab"
    ],
    "experience_roles": [
        "Senior Software Engineer",
        "Full Stack Developer",
        "Research Assistant"
    ],
    "experience_locations": [
        "San Francisco, CA",
        "Palo Alto, CA",
        "Berkeley, CA"
    ],
    "experience_date_ranges": [
        "2021-Present",
        "2019-2021",
        "2017-2019"
    ],
    "experience_highlights": [
        [
            "Led development of microservices architecture serving 1M+ daily users",
            "Reduced system latency by 40% through optimization and caching strategies",
            "Mentored team of 5 junior engineers and established code review processes",
            "Implemented CI/CD pipelines reducing deployment time from hours to minutes"
        ],
        [
            "Built full-stack web applications using React, Node.js, and PostgreSQL",
            "Developed RESTful APIs and integrated third-party payment systems",
            "Collaborated with design team to implement responsive user interfaces",
            "Maintained 99.9% uptime for production applications"
        ],
        [
            "Conducted research on distributed systems and published 2 peer-reviewed papers",
            "Developed Python tools for large-scale data processing and analysis",
            "Collaborated with PhD students on machine learning model optimization"
        ]
    ],
    
    "publication_dates": [
        "2020",
        "2019"
    ],
    "publication_titles": [
        "Scalable Machine Learning Pipeline for Real-time Data Processing",
        "Optimizing Neural Networks for Edge Computing Devices"
    ],
    "publication_authors": [
        ["John Doe", "Dr. Jane Smith", "Prof. Robert Johnson"],
        ["John Doe", "Dr. Alice Chen"]
    ],
    "publication_doi_urls": [
        "https://doi.org/10.1000/182",
        "https://doi.org/10.1000/183"
    ],
    "publication_doi_labels": [
        "doi:10.1000/182",
        "doi:10.1000/183"
    ],
    
    "project_titles": [
        "Personal Finance Tracker",
        "Weather Prediction API",
        "Open Source Contribution: FastAPI Extension"
    ],
    "project_repo_urls": [
        "https://github.com/johndoe/finance-tracker",
        "https://github.com/johndoe/weather-api",
        "https://github.com/tiangolo/fastapi"
    ],
    "project_repo_labels": [
        "github.com/johndoe/finance-tracker",
        "github.com/johndoe/weather-api",
        "github.com/tiangolo/fastapi"
    ],
    "project_highlights": [
        [
            "Built with React frontend and Django REST API backend",
            "Implemented real-time budget tracking and expense categorization",
            "Used PostgreSQL database with automated backup system",
            "Deployed on AWS with Docker containers"
        ],
        [
            "RESTful API serving weather forecasts for 500+ cities worldwide",
            "Integrated multiple weather data sources with fallback mechanisms",
            "Implemented rate limiting and API key authentication",
            "Documented with OpenAPI/Swagger specifications"
        ],
        [
            "Contributed authentication middleware for FastAPI framework",
            "Added support for JWT token validation and refresh",
            "Pull request merged with 500+ GitHub stars",
            "Improved framework security for thousands of developers"
        ]
    ],
    
    "languages": [
        "Python",
        "JavaScript/TypeScript",
        "Java",
        "Go",
        "SQL"
    ],
    "technologies": [
        "React/Vue.js",
        "Django/FastAPI",
        "PostgreSQL/MongoDB",
        "Docker/Kubernetes",
        "AWS/GCP",
        "Git/GitHub",
        "Jenkins/GitHub Actions",
        "Redis/Elasticsearch"
    ]
}

def test_generate_resume():
    print("Testing generate_resume function with fake data...")
    print(f"Templates directory: {TEMPLATES_DIR}")
    print(f"Template name: {TEMPLATE_NAME}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    try:
        pdf_path = generate_resume(**fake_data)
        print(f"✅ Resume generated successfully!")
        print(f"📄 PDF saved to: {pdf_path}")
        print(f"📁 File exists: {pdf_path.exists()}")
        if pdf_path.exists():
            file_size = pdf_path.stat().st_size
            print(f"📏 File size: {file_size:,} bytes")
        
        tex_path = OUTPUT_DIR / f"{fake_data['base_name']}.tex"
        if tex_path.exists():
            print(f"📄 TEX file also created: {tex_path}")
            
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error generating resume: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_generate_resume()
