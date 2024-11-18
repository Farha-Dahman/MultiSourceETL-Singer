import json
import sys
from singer import utils
from tap_github.discover import discover as github_discover
from tap_github.client import GithubClient
from tap_github.sync import sync as github_sync

from datasource.datasource_interface import DataSourceInterface

REQUIRED_CONFIG_KEYS_GITHUB = ['start_date', 'access_token', 'repository', 'base_url']

class GitHub(DataSourceInterface):
    def __init__(self, config):
        self.config = config

    def do_discover(self, client, discover_func):
        catalog = discover_func(client)
        json.dump(catalog, sys.stdout, indent=2)

    def extract_data(self):
        print("extract_data github")
        args = utils.parse_args(REQUIRED_CONFIG_KEYS_GITHUB)
        client = GithubClient(self.config)

        state = {}
        if args.state:
            state = args.state

        if args.discover:
            self.do_discover(client, github_discover)
        else:
            catalog = args.properties if args.properties else github_discover(client)
            github_sync(client, self.config, state, catalog)
