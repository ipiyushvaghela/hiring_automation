import http.client
import urllib.parse
import ast

def fetch_profile(query):
    conn = http.client.HTTPSConnection("real-time-web-search.p.rapidapi.com")

    # query = "site:linkedin.com/in intitle:ahmedabad+data science intern+1 year"

    encoded_query = urllib.parse.quote(query)
    headers = {
        'x-rapidapi-key': "6e2b605f73msh1686a021a37cc83p1e1e7djsn037f4052cc94",
        'x-rapidapi-host': "real-time-web-search.p.rapidapi.com"
    }

    conn.request("GET", f"/search?q={encoded_query}&limit=3", headers=headers)

    res = conn.getresponse()
    data = res.read()

    profile = data.decode("utf-8")
    profile_list = ast.literal_eval(profile)

    profiles = profile_list["data"]
    profile_urls = []
    for profile_url in profiles:
        profile_urls.append(profile_url["url"])
    return profile_urls