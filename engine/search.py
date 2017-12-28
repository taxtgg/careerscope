import elasticsearch_dsl as es_dsl
import elasticsearch_dsl.connections
import datetime

#elasticsearch_dsl.connections.connections.create_connection(hosts=['localhost'])


class Position(object):
    """
    Helper class to make position result hashable.
    Might be a good idea to try this, instead: https://stackoverflow.com/questions/1151658/python-hashable-dicts
    """

    def __init__(self, d):
        self.update(d)

    def update(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Position(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Position(b) if isinstance(b, dict) else b)

    def __eq__(self, other):
        return self.company == other.company \
               and self.title == other.title \
               and str(self.locations_text) == str(other.locations_text) \
               and self.department == other.department \
               and self.url == other.url

    def __hash__(self):
        return hash('%s%s%s%s%s' % (self.company, self.title, self.department, self.locations_text, self.url))



class ScraperOutputIndex(es_dsl.DocType):
    """
    Defines ElasticSearch index for raw jobs scraper result.
    """

    company = es_dsl.Text()
    #description = es_dsl.Text()
    extracted = es_dsl.Date()
    output = es_dsl.Text()
    iterative = es_dsl.Boolean()

    class Meta:
        index = 'scraper-raw-index'

    def save(self, ** kwargs):
        """
        :param kwargs: dict representation of object to save to index
        :return Boolean, True if saved successfully, False otherwise
        """

        self.extracted = datetime.datetime.now()
        return super().save(** kwargs)

    def get_last_pairs(self):
        """
        Method for extracting current and previous result for diffing
        :return:
        """
        # TODO: Implement method
        pass


class JobPostIndex(es_dsl.DocType):
    """
    Defines ElasticSearch index for job posting
    """

    status = es_dsl.Text()
    company = es_dsl.Text()
    title = es_dsl.Text()
    url = es_dsl.Text()
    locations_text = es_dsl.Text()
    locations = es_dsl.GeoPoint()
    department = es_dsl.Text()
    description = es_dsl.Text()
    posted_date = es_dsl.Date()
    closed_date = es_dsl.Date()
    open = es_dsl.Boolean()

    class Meta:
        index = 'jobpost-index'


class CompanyLocationsIndex(es_dsl.DocType):
    """
    Defines ElasticSearch index for company locations
    """

    company = es_dsl.Text()
    location_text = es_dsl.Text()
    location = es_dsl.GeoPoint()
    address = es_dsl.Text()
    google_place_id = es_dsl.Text()

    class Meta:
        index = 'company-locations-index'


class SkillsIndex(es_dsl.DocType):
    """
    Defines ElasticSearch index for job skills
    """

    skill = es_dsl.Text()

    class Meta:
        index = 'skills-index'
