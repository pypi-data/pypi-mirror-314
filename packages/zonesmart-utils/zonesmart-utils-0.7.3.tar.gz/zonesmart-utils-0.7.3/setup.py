from setuptools import setup, find_packages


def parse_requirements() -> list[str]:
    reqs = []
    with open("requirements.txt") as f:
        for line in f.read().splitlines():
            line = line.split("#")[0].strip()
            if line:
                reqs.append(line)
    return reqs


setup(
    name="zonesmart-utils",
    version="0.7.3",
    author="Zonesmart",
    author_email="e.beliakov@dev.kokoc.com",
    packages=find_packages(include=["zs_utils", "zs_utils.*"]),
    install_requires=parse_requirements(),
    include_package_data=True,
    package_data={"zs_utils.views": ["*.mmdb"]}
)
