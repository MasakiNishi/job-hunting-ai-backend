# Job Hunting AI Tool: clean_data.py
# Members: Masaki Nishi, Christian McKinnon, Susan Joh, and Alexander Wong
# Project Partner: Professor Gates
# CS 467 Portfolio Project
#
# Description:
# This is a standalone Python script that executes the Data Preparation
# Phase of the Job Hunting AI Web Tool. It uses several methods, to extract
# and tidy company names, job titles, qualifications and descriptions
# in the google_listings.json file and outputs them to
# cleaned_listings.json The purpose of this script is to prepare
# the raw data for processing in our job recommender algorithm.
#
# Source:
# 1.) re Documentation: https://docs.python.org/3/library/re.html


# Imports: json os, and re for regex operations
import json
import os
import re


def load_data(path):
    """A function to load the raw data from google_listings.json"""
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except IOError as error:
        print(f"Error loading '{path}' file due to: {error}")

def check_word(filter_list, text):
    """A helper function to check for words in the filter methods below."""
    return any(word in text for word in filter_list)

def check_experience(patterns, text):
    """Helper function to check work experience in filter_experience."""
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False

# Function to filter for work arrangements: Remote, Hybrid, On-site
def filter_arrangement(title, location, desc):
    """A function that iterates through job titles, locations, and
    descriptions to determine whether they are remote, on-site, or hybrid."""
    remote_words = ['remote', 'work from home', 'work-from-home']
    remote_location = ['anywhere']
    hybrid_words = ['hybrid']
    title_lower = title.lower()  # Assign all input json data to lowercase
    location_lower = location.lower()
    desc_lower = desc.lower()

    # We prioritize iterating through titles, check for "anywhere"
    if check_word(remote_words, title_lower) or check_word(remote_location,
                                                           location_lower):
        return 'Remote'
    if check_word(hybrid_words, title_lower):
        return 'Hybrid'

    # We then iterate through the descriptions
    if check_word(remote_words, desc_lower):
        return 'Remote'
    if check_word(hybrid_words, desc_lower):
        return 'Hybrid'
    # We can assume anything that is not remote or hybrid is on-site
    return 'On-site'


# Function to Job Experience
def filter_experience(title, description, job_highlights):
    """A function that iterates through job titles, descriptions, and
    qualifications to determine whether they a job is entry, junior,
    intermediate, or senior level."""
    entry_level = [
        r'\bentry level\b', r'\bentry-level\b', r'\binternship\b',
        r'\bintern\b', r'\bintern\b', r'\bpursuing a bachelor\b',
        r'\brecent graduate\b', r'\sde-1', r'\bSoftware Engineer I\b']
    junior_level = [
        r'\bjunior\b', r'\b1-year\b', r'\b1 year\b', r'\b2-years\b',
        r'\b2 years\b', r'\bbachelor\b', r"\bbachelor's\b",
        r'\bbachelors\b']
    int_level = [
        r'\bintermediate level\b', r'\bintermediate-level\b',
        r'\b3-year\b', r'\b3 year\b', r'\b4-year\b', r'\b4 year\b',
        r'\sde-2', r'\bSoftware Engineer II\b']
    senior_level = [
        r'\sde-3', r'\bprincipal\b', r'\bsenior\b', r'\b5-year\b',
        r'\b5 years\b', r'\b6-years\b', r'\b6 years\b', r'\b7-year\b',
        r'\b7 years\b', r'\b8-years\b', r'\b8 years\b', r'\b9-years\b',
        r'\b9 years\b', r'\b10-years\b', r'\b10 years\b', r'\bphd\b',
        r'\bmasters\b', r'\bmasters degree\b', r'\bdoctorate\b',
        r'\bph.d\b', r'\b5+\b', r'\b6+\b', r'\b7+\b',
        r'\badvanced knowledge\b', r'\bSr\b', r'\bphd+\b', r'\bmasters+\b',
        r'\btech lead\b', r'\bSenior\b', r'\bstaff software\b',
        r'\bSoftware Engineer III\b']

    title_lower = title.lower()
    # Combine the description and job highlights and make them lowercase
    combined = (
        f'{description}'
        f"{' '.join(it for sec in job_highlights for it in sec['items'])}"
        ).lower()

    # We again prioritize iterating through titles to categorize the data
    if check_experience(senior_level, title_lower):
        return 'Senior-Level'
    if check_experience(entry_level, title_lower):
        return 'Entry-Level'
    if check_experience(junior_level, title_lower):
        return 'Junior-Level'
    if check_experience(int_level, title_lower):
        return 'Intermediate-Level'

    # Next, iterate through the combined descriptions and qualifications
    if check_experience(entry_level, combined):
        return 'Entry-Level'
    if check_experience(junior_level, combined):
        return 'Junior-Level'
    if check_experience(senior_level, combined):
        return 'Senior-Level'
    if check_experience(int_level, combined):
        return 'Intermediate-Level'

    return 'Not specified'


def filter_sector(company_name, description):
    """A function that iterates through company names in google_listings.json
    and checks them against the categorized databases that structured as
    lists: technology, finance, healthcare, retail, energy, & education."""
    tech_companies = ['Google', 'Microsoft', 'Apple', 'Amazon', 'Facebook',
                      'Meta', 'IBM', 'Intel', 'Oracle',
                      'Business Transformation Institute', 'robot',
                      'Whisker Labs', 'T-Rex Solutions', 'Renewance',
                      'VirtualVocations', 'Dice', 'Innovative Systems',
                      'Daikin', 'Axiom Space', 'KBR', 'Motorola', 'NVIDIA',
                      'Samsung', 'LG', 'Databento', 'Echo Global Logistics',
                      'Sabanto', 'Wayve', 'Parallel Partners Inc', 'crypto',
                      'Your Next Hire', 'Boeing', 'Clarivate', 'Garmin',
                      'Leidos', 'Quora', 'Lambda', 'Palantir', 'Osaro, Inc',
                      'Perpetual Solutions', 'Torii studio', 'H-E-B',
                      'Tangerine Search', 'Katmai', 'TED Conference',
                      'RAPS Consulting Inc', 'Lockheed Martin', 'Flexjobs',
                      'Accelerated Connections', 'Naka Technologies',
                      'Booz Allen Hamilton', 'HireTeq', 'nuArch', 'Boxed',
                      'Elevate HR', 'RemoteWorker', 'Experis', 'Magna',
                      'Tesla', 'BYD', 'Nio', 'Toyota', 'BMW', 'Honda', 'GM',
                      'Chevrolet', 'Ford', 'WARNERMEDIA', 'Philips',
                      'Tech Valley Talent', 'Coinbase', 'Block', 'Chewy',
                      'Blockchain', 'Indium', 'Semgrep', 'Jesica.ai',
                      'Jobot', 'Snowflake', 'Evolutyz', 'WATI',
                      'IT TrailBlazers', 'ACS Consult', 'SpaceX',
                      'Franklin Fitch', 'EROS Technologies Inc',
                      'Azad, inc', 'Siemens', 'Wolters Kluwer',
                      'Procom Consultants Group', 'ARCKIT', 'mindpal',
                      'AditiStaffing', 'game', 'Sterling Engineering',
                      'Activision Blizzard', 'Universal Orlando Resort',
                      'QDStaff', 'ServiceNow', 'Universal Creative',
                      'SambaNova Systems', 'WeWork', 'WEX', 'Bose',
                      'NextPath', 'Nuro', 'Karkidi', 'BAE Systems',
                      'Progression Inc.', 'Affiliated Engineers, Inc.',
                      'Secunetics, inc.', 'Marriott FLEX', 'Taobao',
                      'Department of Justice', 'bluestone', 'RTX',
                      'Kavaliro', 'Fuel Talent', 'Insight Global',
                      'V-Soft Consulting Group, Inc.', 'News Corp',
                      'FL Innovation Connect', 'ALTTRIX CLOUD',
                      'Crossroads Technologies', 'Disney', 'Adobe',
                      'Solidus Labs', 'Yeah! Global', 'Fourier',
                      'DoorDash', 'matchsource llc', 'Virtualitics',
                      'American Traction Systems', 'Databricks',
                      'Siri InfoSolutions Inc', 'Capgemini North America',
                      '.ai', 'Openmesh Network', 'DecisionEngines',
                      'Notion', 'The Job Network', 'Palo Alto Networks',
                      r'\bAEG\b', 'Bosch', 'Synopsys', 'Autodesk',
                      'Imperial Auto USA Corporation', 'Alibaba',
                      'Keeper Security, Inc.', 'SDH Systems LLC',
                      'Anywhere Real Estate', 'CPS Recruitment',
                      'CrowdStrike', 'New York City', 'Infojini Inc',
                      'NextPit GmbH', 'Conquest Technical Associates',
                      'CEDENT',  'Eastridge', 'VANTA Partners, Inc',
                      'Software People Inc.', 'AIYA TECHNOLOGY SYSTEM LLC',
                      'Amentum', 'Month2Month.com', 'Airbnb', 'Fortinet',
                      'Pacific Northwest National Laboratory', 'Fleetcor',
                      'TikTok', 'Bytedance', 'Tencent', 'NASA', 'Dropbox',
                      'Futronics', 'Accenture', 'Advanced Micro Devices',
                      'Akamai Technologies', 'Amphenol', 'Analog Devices',
                      'Ansys', 'Applied Materials', 'Arista Networks',
                      'Autodesk', 'Automatic Data Processing', 'Corning',
                      'Broadcom', 'Broadridge Financial Solutions',
                      'Cadence Design Systems', 'CDW', 'Ceridian',
                      'Cisco Systems', 'Citrix Systems', 'Enphase Energy',
                      'Cognizant Technology Solutions', 'DXC Technology',
                      'F5 Networks', 'Fiserv', 'Gartner', 'Global Payments',
                      'Hewlett Packard Enterprise', 'Intuit', 'Xilinx',
                      r'\bHP\b',  'Jack Henry & Associates', 'NetApp',
                      'Juniper Networks', 'Keysight Technologies', 'NXP',
                      'KLA Corporation', 'Lam Research', 'NortonLifeLock',
                      'Microchip Technology', 'Micron Technology',
                      'Monolithic Power Systems', 'IPG Photonics',
                      r'\bPTC\b', 'Qorvo', 'Qualcomm', 'Zebra Technologies',
                      'Salesforce', 'Seagate Technology', 'Teradyne',
                      'Skyworks Solutions', 'Texas Instruments', 'Trimble',
                      'TE Connectivity', 'Tyler Technologies', 'Verisign',
                      'Western Digital']

    fin_companies = ['Goldman Sachs', 'JPMorgan Chase', 'Morgan Stanley',
                     'Stripe', 'Citibank', 'Wells Fargo', 'Robert Half',
                     'Bank of America', 'BOA', 'Citadel', 'Jane Street',
                     'Capital One', 'CSC', 'Countercyclical', 'Ramp',
                     'Fidelity', 'State Street', 'ACL Digital', 'invest',
                     'wall street', 'Esri', 'Geico', 'The Hartford',
                     'Freddie Mac', 'Hartford Fire Ins. Co', 'Optiver',
                     'BlackRock', 'Open Systems Technologies',
                     'Mastercard', 'Visa', 'Selby Jennings', 'Cboe',
                     'Early Warning', 'Kin Insurance', 'Valid8 Financial',
                     'The D. E. Shaw Group', 'PDT Partners', 'Deshaw',
                     'Paycom', 'Point72', 'RedShift', 'array',
                     'Ejadah Management Consultancy', 'Allstate Corp',
                     'Central Mutual Insurance Company', 'PayPal',
                     'Cast & Crew', 'Cross River', 'financial',
                     'Western Union', 'Aflac', 'Charles Schwab Corporation',
                     'American Express', 'American International Group',
                     'Ameriprise Financial', 'Aon', 'BNY Mellon',
                     'Arthur J. Gallagher & Co.', 'Assurant',
                     'Berkshire Hathaway',  'Cincinnati Financial',
                     'Brown & Brown', 'Chubb', 'Citigroup', 'CME Group',
                     'Citizens Financial Group', 'Discover Financial',
                     'Comerica', 'Everest Re', 'Fifth Third Bancorp',
                     'First Republic Bank', 'Franklin Resources',
                     'Globe Life', 'Huntington Bancshares',
                     'Intercontinental Exchange', 'Invesco',
                     'KeyCorp', 'Willis Towers Watson', 'Marsh & McLennan',
                     'Loews Corporation', 'M&T Bank', 'MarketAxess',
                     'MetLife', "Moody's Corporation", 'Lincoln National',
                     'Morgan Stanley', 'MSCI', 'Nasdaq', 'U.S. Bancorp',
                     'Northern Trust', "People's United Financial",
                     'PNC Financial Services', 'T. Rowe Price',
                     'Principal Financial Group', 'SVB Financial',
                     'Progressive Corporation', 'Prudential Financial',
                     'Raymond James Financial', 'Zions Bancorp'
                     'Regions Financial Corporation', 'S&P Global',
                     'Synchrony Financial', 'W. R. Berkley Corporation',
                     'The Travelers Companies', 'Truist Financial']

    hc_companies = ['Pfizer', 'Johnson & Johnson', 'Merck', 'Roche',
                    'med', 'Novartis' 'health', r'\bhealth\b',
                    'NYU Langone', 'Dana Farber', 'Anderson Cancer',
                    'Duke Cancer', 'Sidney Kimmel', 'MUFG',
                    'Emergent Holdings', 'Centene Corporation',
                    'bioscience', 'Veeva', 'pharm', 'WellSky',
                    'Akina', 'SmarterDx', 'MMIT', 'Healthcare',
                    'adonis',         'Abbott Laboratories',
                    'AbbVie', 'Abiomed', 'Agilent Technologies',
                    'Align Technology', 'AmerisourceBergen',
                    'Amgen', 'Anthem', 'Baxter International',
                    'Becton Dickinson', 'Bio-Rad Laboratories',
                    'Bio-Techne', 'Biogen', 'Boston Scientific',
                    'Bristol Myers Squibb', 'Cardinal Health',
                    'Catalent', 'Centene Corporation', 'Cerner',
                    'Charles River Laboratories', 'Cigna',
                    'CVS Health', 'Danaher Corporation',
                    'DaVita', 'Dentsply Sirona', 'DexCom',
                    'Edwards Lifesciences', 'Eli Lilly & Co',
                    'Gilead Sciences', 'HCA Healthcare',
                    'Henry Schein', 'Hologic', 'Humana',
                    'Idexx Laboratories', 'Illumina',
                    'Incyte', 'Intuitive Surgical', 'IQVIA',
                    'LabCorp', 'McKesson Corporation',
                    'Medtronic', 'Merck & Co.',
                    'Mettler Toledo', 'Moderna', 'Organon & Co.',
                    'PerkinElmer', 'Quest Diagnostics',
                    'Regeneron Pharmaceuticals', 'ResMed',
                    'Steris', 'Stryker Corporation', 'Teleflex',
                    'The Cooper Companies',
                    'Thermo Fisher Scientific', 'UnitedHealth Group',
                    'Universal Health Services',
                    'Vertex Pharmaceuticals', 'Viatris',
                    'Waters Corporation',
                    'West Pharmaceutical Services', 'Zimmer Biomet',
                    'Zoetis']
    hc_phrase = ['healthcare software']
    re_companies = ['Walmart', 'Publix', 'Nordstrom', 'Target', 'Costco',
                    'Walgreens', "Lowe's", 'Aldi', 'Tesco', 'H&M',
                    'Best Buy', 'Adidas', 'Nike', 'IKEA',
                    'Estée Lauder', 'LVMH', 'Gucci', 'Burberry',
                    'Prada', 'General Mills', "Kellogg's", "Kimberly-Clark",
                    'Kraft Heinz', 'Kroger', 'Lamb Weston',
                    'McCormick & Company', 'Molson Coors',
                    'Mondelez International', 'Monster Beverage',
                    'Pepsi', 'Coca-Cola', 'Philip Morris',
                    'Procter & Gamble', 'P&G', 'P & G', 'Sysco',
                    'The Hershey Company', 'Tyson Foods', 'The Home Depot',
                    'JD.com', 'CVS Corporation', 'Aeon',
                    'Seven & I Holdings', 'Woolworths', 'Auchan',
                    "Macy's", 'Rite Aid', "Kohl's", 'Wayfair', 'The Gap',
                    'Decathlon', 'Coupang']
    en_companies = ['ExxonMobil', 'Chevron', 'Shell', 'BP',
                    'ConocoPhillips', 'SLB', 'oxy', 'Valero Energy',
                    'Con Edison Company of New York',
                    'Universe Energy, Inc.', 'APA Corporation',
                    'Baker Hughes', 'Coterra', 'Devon Energy',
                    'Diamondback Energy', 'EOG Resources', 'Oneok',
                    'Halliburton', 'Hess Corporation', 'Phillips 66',
                    'Kinder Morgan', 'Marathon Oil', 'Schlumberger',
                    'Marathon Petroleum', 'Occidental Petroleum',
                    'Pioneer Natural Resources', 'Williams Companies']

    edu_companies = ['Pearson', 'McGraw-Hill', 'Cengage', 'udacity',
                     'Houghton Mifflin Harcourt', 'Coursera',
                     'Synergistic IT', 'jobsbridge', 'Apollo Education',
                     'Carnegie Mellon University', 'university',
                     'udemy', '355Code', 'Skillshare', 'New Oriental',
                     'Aspen Education', 'Kaplan', '360 Learning', '2U Inc',
                     'Scholastic Corporation', 'Sylvan Learning',
                     'Trump University', 'Skillsoft', 'Quizlet',
                     'Amplify', 'Brainly', 'MasterClass', 'Wolfram',
                     'Rosetta Stone', 'SynergisticIT']

    # Use re module to compile regex patterns while ignoring case size
    tech_pattern = re.compile('|'.join(tech_companies), re.IGNORECASE)
    finance_pattern = re.compile('|'.join(fin_companies), re.IGNORECASE)
    healthcare_pattern = re.compile(
        '|'.join(hc_companies), re.IGNORECASE)
    healthcare_pattern2 = re.compile(
        '|'.join(hc_phrase), re.IGNORECASE)
    energy_pattern = re.compile('|'.join(en_companies), re.IGNORECASE)
    retail_pattern = re.compile('|'.join(re_companies), re.IGNORECASE)
    education_pattern = re.compile(
        '|'.join(edu_companies), re.IGNORECASE)

    # Again, we use the re module search() function to find matches
    if tech_pattern.search(company_name):
        return 'Technology'
    elif finance_pattern.search(company_name):
        return 'Finance'
    elif healthcare_pattern.search(company_name):
        return 'Healthcare'
    elif healthcare_pattern2.search(description):
        return 'Healthcare'
    elif retail_pattern.search(company_name):
        return 'Retail'
    elif energy_pattern.search(company_name):
        return 'Energy'
    elif education_pattern.search(company_name):
        return 'Education'
    else:
        return 'Not specified'


def clean_job_listing(job):
    """This functions performs the cleaning of the job listings by storing
    the results of the above filter methods into a dictionary."""
    # Assign variables that are used as parameters for the above methods
    arrangement_desc = job.get('description', '')
    location = job.get('location', 'Not specified')
    title = job.get('title', '')
    experience_desc = job.get('description', '')
    job_highlights = job.get('job_highlights', [])
    company_name = job.get('company_name', '')
    cleaned_job = {
        'title': job.get('title', 'Not specified'),
        'company': job.get('company_name', 'Not specified'),
        'location': job.get('location', '').split(',')[0].strip(),
        'arrangement': filter_arrangement(title, location, arrangement_desc),
        'jobType': job.get('detected_extensions',
                           {}).get('schedule_type', 'Not specified'),
        'sector': filter_sector(company_name, experience_desc),
        'experience': filter_experience(
            title,
            experience_desc,
            job_highlights),
        'description': job.get('description', 'Not specified')}
    # Let's Process Links and their Websites Separately
    job_url = job.get('apply_options', [])
    if job_url:
        first_apply_option = job_url[0]
        title = first_apply_option.get('title', 'No title')
        link = first_apply_option.get('link', 'No link')
        cleaned_job['job_url'] = f'{link}'
        cleaned_job['url_site'] = f'[{title}]'
    else:
        cleaned_job['job_url'] = 'No link available'

    return cleaned_job


def clean_data(data):
    """This function is called in main and triggers the above
    clean_job_listings method to return the cleaned_data that is ulimately
    written to cleaned_listings.json."""
    cleaned_data = [clean_job_listing(job) for job in data]
    return cleaned_data


def save_cleaned_data(path, data):
    """This function is called in main and writes the cleaned data to the
    output file cleaned_listings.json"""
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=2)
    except IOError as error:
        print(f"Error writing to '{path}' file due to: {error}")


def main():
    """This is our driver function which calls the methods: load_data(),
    clean_data(), and saved_clean_data() to effective perform the data
    preparation which involves cleaning the data and writing storing it
    in an external file."""
    # Use the os module to create portable paths for our JSON files
    input_path = os.path.join(os.path.dirname(__file__),
                              'json_files', 'google_listings.json')
    output_path = os.path.join(os.path.dirname(__file__),
                               'json_files', 'cleaned_listings.json')

    # Call the load_data, cleaned_data and saved_clean_data methods here
    data = load_data(input_path)
    cleaned_data = clean_data(data)
    save_cleaned_data(output_path, cleaned_data)
    # Print the success message
    print('Data formatted and written to cleaned_listings.json!')


if __name__ == '__main__':
    main()
