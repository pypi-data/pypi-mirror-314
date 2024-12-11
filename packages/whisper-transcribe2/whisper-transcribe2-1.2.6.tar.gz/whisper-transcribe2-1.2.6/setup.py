import pathlib
import sys
import platform
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

requirements = []
requirements_file = HERE / "requirements.txt"

if requirements_file.exists():
    with open(requirements_file, encoding="utf-8") as f:
        requirements = f.read().splitlines()       

if sys.platform.startswith("linux") and platform.machine() == "x86_64":
    requirements.append("triton>=2.0.0,<3")

def read_version(fname="src/whisper_transcribe2/version.py"):
    exec(compile(open(fname, encoding="utf-8").read(), fname, "exec"))
    return locals()["__version__"]

setup(
    name="whisper-transcribe2",
    version=read_version(),
    description="Whisper command line client that uses CTranslate2 and faster-whisper to use different transcription styles",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/fdorch/whisper-transcribe2",
    author="Artem Fedorchenko",
    author_email="iloaf13@outlook.com",
    python_requires=">=3.8",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    include_package_data=True,
    extras_require={
        "dev": ["flake8==7.*", "black==24.*", "nose2"],
    },
    entry_points={
        "console_scripts": [
            "whisper-transcribe2=whisper_transcribe2.transcribe:cli",
        ]
    },
)
