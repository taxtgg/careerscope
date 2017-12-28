import requests
import lxml.html as lh
from engine import app


"""
Company specific scraper tasks

All scrapers return a list of dicts with the following attributes:
requiredFields = {'company', 'title', 'url', 'locations'}
optionalFields = {'department', 'description'} 
"""


@app.task
def slack_get_openings(self):
    """
    Get the jobs from Slack careers page
    :return: list of dicts representing open positions
    """

    company = 'Slack'
    url = 'https://slack.com/careers'

    req = requests.get(url)
    doc = lh.fromstring(req.text)
    doc.make_links_absolute(url)

    result = [ {'company': company,
                'title':position.cssselect('td:nth-child(2)')[0].text.replace('\t','').replace('\n','').encode('utf-8').decode('utf-8', 'replace'),
                'url':position.cssselect('td:nth-child(5)')[0].find('a').get('href'),
                'locations_text':[position.get('data-location')],
                'department':deptSection.find('thead').find('tr').find('th').find('span').text }
               for deptSection in doc.cssselect('#main > section.careers-table > div > div.shadow-table > div:nth-child(1)')[0].iter('table')
               for position in deptSection.find('tbody').iter('tr') ]

    for position in result:
        req = requests.get(position['url'])
        doc = lh.fromstring(req.text)
        position['description'] = doc.cssselect('#main > section:nth-child(2) > div > div > div')[0].text_content().replace('\t','').encode('utf-8').decode('utf-8', 'replace')

    return result


@app.task
def stripe_get_openings(self):
    """
    Get the jobs from Stripe Careers page
    :return: list of dicts representing open positions
    """

    company = 'Stripe'
    url = 'https://stripe.com/jobs'

    req = requests.get(url)
    doc = lh.fromstring(req.text)
    doc.make_links_absolute(url)

    result = [ {'company': company,
                'title': position.find('a').find('h3').text.encode('utf-8').decode('utf-8', 'replace'),
                'url': position.find('a').get('href'),
                'department': docSection.find('h2').find('div').find('a').text.encode('utf-8').decode('utf-8', 'replace') }
               for docSection in doc.get_element_by_id('openings').iter('section')
               for position in docSection.iter('li') ]

    for position in result:
        positionHTML = lh.fromstring(requests.get(position['url']).text)
        positionDetail = positionHTML.get_element_by_id("main-content").find('article')
        position['locations_text'] = [node.text for node in positionDetail.find('h1').iter('span')]
        position['description'] = positionDetail.text_content().replace('\t','').encode('utf-8').decode('utf-8', 'replace')

    return result