import os
import requests
from distutils.version import LooseVersion
import jinja2


def versions(package_name, limit_releases=10):
    url = f"https://pypi.org/pypi/{package_name}/json"
    data = requests.get(url).json()
    versions = list(data["releases"].keys())
    versions.sort(key=LooseVersion, reverse=True)
    return versions[:limit_releases]


application_version = "0.0." + str(int(versions("scalegen-cli")[0].split(".")[2]) + 1)


binary = "scaletorch"
if os.environ.get("PRODUCT_TYPE", "scaletorch") == "scalegen":
    binary = "scalegen"


template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template_file = "pyproject.toml.j2"
template = template_env.get_template(template_file)

with open("pyproject.toml", "w") as f:
    content = template.render(application_version=application_version, binary=binary)
    f.write(content)

print("pyproject.toml file created successfully")
