import importlib
import json
import sys
import singer
from singer import utils

LOGGER = singer.get_logger()

@singer.utils.handle_top_exception(LOGGER)
def main():
    unchecked_args = utils.parse_args([])
    config = unchecked_args.config

    # Load the function mapping from the JSON file
    with open('setup.json', 'r') as file:
        DATASOURCE_CLASS_MAPPING = json.load(file)
        print(DATASOURCE_CLASS_MAPPING)

    base_url = config.get("base_url", "")
    tool_object = None

    for url, class_name in DATASOURCE_CLASS_MAPPING.items():
        if url in base_url:
            # Dynamically import the module containing the class
            module_name = "datasource." + class_name.lower() + "_datasource"
            module = importlib.import_module(module_name)
            
            # Get the class object from the module
            DataSourceClass = getattr(module, class_name)
        
            # Instantiate the class
            tool_object = DataSourceClass(config)

            break

    if tool_object:
        tool_object.extract_data()
    else:
        LOGGER.error("Unsupported base_url")
        sys.exit(1)

if __name__ == "__main__":
    main()
