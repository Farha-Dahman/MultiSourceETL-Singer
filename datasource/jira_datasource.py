import tap_jira
from singer import utils
from singer.catalog import Catalog
from tap_jira.context import Context

from datasource.datasource_interface import DataSourceInterface

REQUIRED_CONFIG_KEYS_CLOUD = ["start_date", "user_agent", "cloud_id", "access_token", "refresh_token", "oauth_client_id", "oauth_client_secret"]
REQUIRED_CONFIG_KEYS_HOSTED = ["start_date", "username", "password", "base_url", "user_agent"]

class Jira(DataSourceInterface):
    def __init__(self, config):
        self.config = config

    def get_jira_args(self):
        unchecked_args = utils.parse_args([])
        if 'username' in unchecked_args.config.keys():
            return utils.parse_args(REQUIRED_CONFIG_KEYS_HOSTED)
        return utils.parse_args(REQUIRED_CONFIG_KEYS_CLOUD)

    def extract_data(self):
        print("extract_data jira")
        args = self.get_jira_args()
        jira_client = tap_jira.Client(self.config)

        # Setup Context (assuming Context is defined somewhere in tap_jira)
        Context.client = jira_client
        catalog = Catalog.from_dict(args.properties) if args.properties else tap_jira.discover()
        Context.config = self.config
        Context.state = args.state
        Context.catalog = catalog

        try:
            if args.discover:
                tap_jira.discover().dump()
            else:
                tap_jira.sync()
        finally:
            if Context.client and Context.client.login_timer:
                Context.client.login_timer.cancel()