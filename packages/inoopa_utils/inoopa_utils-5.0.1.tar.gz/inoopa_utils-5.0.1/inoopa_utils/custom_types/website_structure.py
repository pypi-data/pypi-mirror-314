from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class WebsiteStructure:
    """Dataclass to represent the website_structure MongoDB collection's documents."""

    _id: str  # This is the base_url. We use it as the unique key
    domain: str

    # Extracted from the website's structure
    home_url: str | None = None
    about_url: str | None = None
    contact_url: str | None = None

    # Extracted from the website's content
    company_mission: str | None = None
    phones: list[str] = field(default_factory=list)
    emails: list[str] = field(default_factory=list)
    social_networks: list[str] = field(default_factory=list)
    vat_numbers: list[str] = field(default_factory=list)

    # Updated by the best_finder
    companies_ids: list[str] = field(default_factory=list)
    # Updated by the websites_crawler
    last_crawling: datetime = field(default_factory=datetime.now)
