import os
import sys

MAX_FILES = 2000
MAX_SIZE_MB = 100
UPLOAD_WORKERS = 10
PLATFORM_API = os.environ.get("ST_PLATFORM_API", "https://prod-api.scalegen.ai")
CACHE_PATH = os.path.expanduser("~/.scaletorch/creds_cache")
SSH_KEY_PATH = os.path.expanduser("~/.scaletorch")
AUTH0_TENANT = "https://scaletorch.us.auth0.com"
AUTH0_API_AUDIENCE = "api.scaletorch.ai"
PRODUCT_TYPE = "SCALETORCH" if sys.argv[0].endswith("scaletorch") else "SCALEGEN"
