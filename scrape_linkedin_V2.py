import requests
import json

url = "https://api.theirstack.com/v1/jobs/search"

technology = [
    1594, 6, 2458, 3134, 3128, 3252, 84, 1285, 3127, 4, 109, 3131, 5, 3130, 3101,
    3099, 3100
]
finance = [
    43, 129, 1720, 45, 46, 1713, 106, 1673, 41, 141, 1696, 1678, 1742, 1743, 1745,
    42, 1738, 1737, 1725
]
healthcare = [
    14, 2115, 2112, 2081, 88, 2128, 2122, 2125, 13, 125, 2077, 2048, 2045, 2060, 2074,
    2069, 139, 2050, 2063, 2054, 2040, 2091
]
retail = []
energy = []
education = []

payload = {
    "order_by": [
        {"desc": True, "field": "date_posted"},
        {"desc": True, "field": "discovered_at"}
    ],
    "page": 0,  # Start from page 0
    "limit": 500,
    "company_description_pattern_or": [],
    "company_description_pattern_not": [],
    "company_description_pattern_accent_insensitive": False,
    "min_revenue_usd": None,
    "max_revenue_usd": None,
    "min_employee_count": None,
    "max_employee_count": None,
    "min_employee_count_or_null": None,
    "max_employee_count_or_null": None,
    "min_funding_usd": None,
    "max_funding_usd": None,
    "funding_stage_or": [],
    "industry_or": [],  # deprecated per API
    "industry_not": [],
    "industry_id_or": [],
    "industry_id_not": [],
    "company_tags_or": [],
    "company_type": "all",
    "company_investors_or": [],
    "company_investors_partial_match_or": [],
    "company_technology_slug_or": [],
    "company_technology_slug_and": [],
    "company_technology_slug_not": [],
    "only_yc_companies": False,
    "company_location_pattern_or": [],
    "company_country_code_or": [],
    "company_country_code_not": [],
    "company_list_id_or": [],
    "company_list_id_not": [],
    "company_linkedin_url_exists": None,
    "revealed_company_data": None,
    "company_name_or": [],
    "company_name_case_insensitive_or": [],
    "company_id_or": [],
    "company_domain_or": [],
    "company_domain_not": [],
    "company_name_not": [],
    "company_name_partial_match_or": [],
    "company_name_partial_match_not": [],
    "company_linkedin_url_or": [],
    "job_title_or": [],
    "job_title_not": [],
    "job_title_pattern_and": [],
    "job_title_pattern_or": [],
    "job_title_pattern_not": [],
    "job_country_code_or": ["US"],
    "job_country_code_not": [],
    "posted_at_max_age_days": None,
    "posted_at_gte": None,
    "posted_at_lte": None,
    "discovered_at_max_age_days": None,
    "discovered_at_min_age_days": None,
    "discovered_at_gte": None,
    "discovered_at_lte": None,
    "job_description_pattern_or": [],
    "job_description_pattern_not": [],
    "job_description_pattern_is_case_insensitive": True,
    "remote": None,
    "only_jobs_with_reports_to": None,
    "reports_to_exists": None,
    "final_url_exists": None,
    "only_jobs_with_hiring_managers": None,
    "hiring_managers_exists": None,
    "job_id_or": [],
    "job_ids": [],
    "min_salary_usd": None,
    "max_salary_usd": None,
    "job_technology_slug_or": [],
    "job_technology_slug_not": [],
    "job_technology_slug_and": [],
    "job_location_pattern_or": [],
    "job_location_pattern_not": [],
    "scraper_name_pattern_or": [],
    "include_total_results": False,
    "blur_company_data": False,
    "group_by": []
}

headers = {
    "Content-Type": "application/json",
    "Authorization": (
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ3b25nYTlAb3JlZ29uc3RhdGUuZWR1IiwicGVybWlzc2lvbnMiOiJ1c2VyIn0."
        "WqpiPmZA5xjtN_0TvEKIBrPTubZz1dyQhtaxXfEVXk8"
    )
}

all_job_results = []

while True:
    response = requests.post(url, json=payload, headers=headers)
    json_obj = json.loads(response.text)
    data_part = json_obj.get('data', [])

    if not data_part:
        break

    all_job_results.extend(data_part)
    payload['page'] += 1

with open('job_results.json', 'w') as f:
    json.dump(all_job_results, f, indent=2)

print("Job results saved successfully")
