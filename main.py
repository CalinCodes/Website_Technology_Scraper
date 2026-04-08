import sqlite3
import requests
import json
import logging
import concurrent.futures
import builtwith

def analyze_domain(domain):
    url = f"http://{domain}" if not domain.startswith("http") else domain
    result = {
        "domain": domain,
        "technologies": [],
        "proof": {},
        "error": None
    }
    
    try:
        # We manually fetch the HTTP response to manage SSL verify and custom timeout
        response = requests.get(
            url, 
            timeout=10, 
            headers={"User-Agent": "Mozilla/5.0 Website Tech Scraper"},
            verify=False
        )
        status = response.status_code
        if status != 200:
            result["error"] = f"Status {status}"
            return result
            
        html_content = response.text
        headers = dict(response.headers)
        
        # Leverage builtwith to parse the massive catalog of WebTechs
        techs = builtwith.parse(url=url, headers=headers, html=html_content)
        
        if isinstance(techs, dict):
            for category, tech_list in techs.items():
                for tech in tech_list:
                    result["technologies"].append(tech)
                    result["proof"][tech] = [f"Detected by builtwith within category: '{category}'"]
                
    except Exception as e:
        result["error"] = str(e)
        
    return result

def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    conn = sqlite3.connect("dataset.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM dataset")
        domains = [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        print("Error: Could not read from dataset.db.")
        return
    finally:
        conn.close()
        
    print(f"Loaded {len(domains)} domains for analysis.")
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(analyze_domain, domain): domain for domain in domains}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            count = len(res["technologies"])
            if count > 0:
                print(f"Processed: {res['domain']} - Tech found: {count}")
            elif res["error"]:
                print(f"Processed: {res['domain']} - Error: {res['error']}")
            results.append(res)
            
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("Analysis complete. Saved to results.json")

if __name__ == "__main__":
    main()
