from enum import Enum 

class PATHS(Enum):
    CONTENT_FILE = "data/content_files.json"
    PARSED_FILE = "data/processed/class_definitions.json"
    GEN_DESCRIPTIONS = "data/processed/gen_desriptions.json"
    GEN_OVERVIEW = "data/processed/gen_overview.json"
    GEN_CODE_SNIPPETS ="data/processed/gen_code_snippets.json"
    HOW_TO = "data/processed/how_to.json"
    PUBLISH_LOCATION = "data/processed/publish/"
    LOG_FILE = "data/log.txt"

