from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Boolean, GeoPoint, Nested

connections.create_connection(hosts=['localhost'])

class ScraperOutputIndex(DocType):
    name = Text()
    description = Text()
    date = Date()
    output = Nested()

    class Meta:
        index = 'scraper-raw-index'

class JobPostRawIndex(DocType):
    state = Text()
    company = Text()
    title = Text()
    url = Text()
    locations_text = Text()
    locations = GeoPoint()
    department = Text()
    description = Text()
    extract_date = Date()

    class Meta:
        index = 'jobpost-raw-index'

class JobPostIndex(DocType):
    company = Text()
    title = Text()
    url = Text()
    locations = GeoPoint()
    department = Text()
    description = Text()
    posted_date = Date()
    closed_date = Date()
    open = Boolean()

    class Meta:
        index = 'jobpost-index'

class CompanyLocationsIndex(DocType):
    company = Text()
    location_text = Text()
    location = GeoPoint()
    address = Text()
    google_place_id = Text()

    class Meta:
        index = 'company-locations-index'

class SkillsIndex(DocType):
    skill = Text()

    class Meta:
        index = 'skills-index'
