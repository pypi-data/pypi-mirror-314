from setuptools import find_packages, setup

PACKAGE_NAME = "nest_gen_accelerator_azure"

setup(
    name=PACKAGE_NAME,
    version="1.0.6",
    description="NestGen Accelerator Promptflow Package",
    packages=find_packages(
        exclude=["tests", "tests.*"]
    ),
    entry_points={
        "package_tools": [
            "llm_tool = nest_gen_accelerator_azure.tools.utils:list_package_tools"
        ],
    },
    include_package_data=True,  # Include files from MANIFEST.in
)
