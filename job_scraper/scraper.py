from serpapi import GoogleSearch

def search_jobs_serpapi(keywords, location="Bengaluru, Karnataka, India", max_results=10):
    api_key = "4054f95c3b3f883f0588dc129a0e4c2531383649f07a4fba536e0b814be9e265"

    # query = " ".join(keywords)
    params = {
        "engine": "google_jobs",
        "q": "Software Engineer",
        "location": location,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    jobs = []
    for job in results.get("jobs_results", [])[:max_results]:
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "description": job.get("description"),
            "url": job.get("related_links", [{}])[0].get("link", ""),
            "source": "SerpAPI - Google Jobs"
        })
    print(jobs)
    return jobs

# if __name__ == '__main__':
#     search_jobs_serpapi("Software Engineer")
