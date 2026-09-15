"""CI entry point: fetch live contributionCalendar via GraphQL, regenerate heatmap.svg.

Run daily by .github/workflows/refresh.yml. Needs GITHUB_TOKEN (Actions provides
one automatically) and GH_LOGIN (the profile username) in the environment.
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from make_heatmap import build as build_heatmap

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""

def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def main():
    login = os.environ.get("GH_LOGIN", "adityamondal-ai-spec")
    token = os.environ["GITHUB_TOKEN"]
    data = fetch(login, token)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    contrib_path = os.path.join(root, "contrib.json")
    with open(contrib_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    build_heatmap(contrib_path, os.path.join(root, "heatmap.svg"))

if __name__ == "__main__":
    main()
