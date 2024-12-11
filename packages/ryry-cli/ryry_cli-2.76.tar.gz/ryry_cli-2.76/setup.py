import setuptools
import os
import subprocess
import datetime

ryry_version = "2.76"
cur_dir = os.path.dirname(os.path.abspath(__file__))
constanspy = os.path.join(cur_dir, "ryry", "constant.py")
try:
    # result = subprocess.run("git config user.email", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    build_user = "Noh"
    # if result.returncode == 0:
    #     build_user = result.stdout.decode(encoding="utf8", errors="ignore").replace("\n","").strip()
    build_pts = datetime.datetime.today()

    with open(constanspy, 'w') as f:
        f.write(f'''#!!!!! do not change this file !!!!!
app_version="{ryry_version}"
app_bulld_anchor="{build_user}_{build_pts}"
app_name="ryry-cli"
''')
except:
    with open(constanspy, 'w') as f:
        f.write(f'''#!!!!! do not change this file !!!!!
app_version="{ryry_version}"
app_bulld_anchor=""
app_name="ryry-cli"
''')

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()
setuptools.setup(
    name="ryry-cli",
    version=ryry_version,
    author="dalipen",
    author_email="dalipen01@gmail.com",
    description="ryry tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dalipenMedia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['windows', 'public_tools'],
    install_requires=[
        'requests',
        'uuid',
        'Image',
        'pillow',
        'psutil',
        'pynvml',
        'requests_toolbelt',
        'matplotlib',
        'fake_useragent',
        'piexif',
        'gputil',
        'urlparser',
        'python-crontab',
        'urllib3',
    ],
    dependency_links=[],
    entry_points={
        'console_scripts':[
            'ryry = ryry.main:main'
        ]
    },
    # scripts=[
    #     'ryry/upload.py'
    # ],
    python_requires='>=3.4',
)