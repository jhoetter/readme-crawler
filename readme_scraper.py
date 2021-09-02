import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from wasabi import msg


def get_readme(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    html_code = str(soup.find("article"))
    return html_code


def scrape_readmes(url_list):
    readmes = []
    for idx, url in enumerate(url_list):
        msg.info(f"{idx + 1} / {len(url_list)} | Accessing {url}")
        try:
            readme = get_readme(url)
            readmes.append({"url": url, "readme_html": readme})
        except:
            msg.fail(f"Couldn't access {url}")
        time.sleep(3)  # needed to not overload GitHub -> getting blocked
    readmes_df = pd.DataFrame(readmes)
    msg.good("Finished parsing")
    return readmes_df


if __name__ == "__main__":
    readmes_df = scrape_readmes(
        [
            # provide the url list here :-)
            "https://github.com/streamlit/streamlit",
            "https://github.com/CrowdDevHQ/awesome-community-building",
            "https://github.com/streamlit/streamlit",
        ]
    )
    readmes_df.to_json("readmes.json", orient="records")
