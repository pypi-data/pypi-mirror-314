import argparse
from schemantis import Configuration, ApiClient, DefaultApi
from os import environ

from generate_python import generate_python



ENVIRONMENT = environ.get('SCHEMANTIS_ENV')
SCHEMANTIS_API_KEY = environ.get("SCHEMANTIS_API_KEY")

if ENVIRONMENT is None:
    raise ValueError("SCHEMANTIS_ENV environment variable not set. Must be either 'staging' or 'production'")

subdomain_suffix = '' 

if ENVIRONMENT == 'staging':
    subdomain_suffix = '-stg'

configuration = Configuration(host=f"https://api{subdomain_suffix}.schemantis.ca")

if SCHEMANTIS_API_KEY is None:
    raise ValueError("SCHEMANTIS_API_KEY environment variable is not set")

configuration.api_key["api_key"] = environ["SCHEMANTIS_API_KEY"]
api_client = ApiClient(configuration)
api_instance = DefaultApi(api_client)


def generate(generator, map_id_or_name, output_directory):
    get_map_kwargs = {}
    if map_id_or_name.isnumeric():
        get_map_kwargs["map_id"] = map_id_or_name
    else:
        get_map_kwargs["map_name"] = map_id_or_name

    api_response = api_instance.retrieve_map_get(**get_map_kwargs)

    if generator == "python":
        return generate_python(api_response, output_directory)


def main_cli():
    parser = argparse.ArgumentParser(description="Generate code from map data.")
    parser.add_argument(
        "--generator", "-g", type=str, help="The generator to use (e.g., 'python')."
    )
    parser.add_argument("--map_id_or_name", "-m", type=str, help="The map ID or name.")
    parser.add_argument(
        "--output-directory",
        "-o",
        required=True,
        type=str,
        help="Output Directory",
        default="./out",
    )

    args = parser.parse_args()
    generate(args.generator, args.map_id_or_name, args.output_directory)


if __name__ == "__main__":
    main_cli()