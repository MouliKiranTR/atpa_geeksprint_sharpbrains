 Cpa-cm-classifier : [tr/cp_cm-classifier](https://github.com/tr/cp_cm-classifier)     

This Service uses python 3.6 version, which is quite old. This service depends on c3-pycptam-cmclassifier==1.1.8 and c3-pycptam-data==1.2.7.
This is the requirements.txt file of the service:
--extra-index-url https://tr1.jfrog.io/artifactory/api/pypi/pypi/simple  
c3-pycptam-cmclassifier==1.1.8  
c3-pycptam-data==1.2.7  
certifi==2018.4.16  
chardet==3.0.4  
click==6.7  
Flask==0.12.2  
Flask-SQLAlchemy==2.3.2  
idna==2.6  
itsdangerous==0.24  
Jinja2==2.10  
logstash-formatter==0.5.17  
MarkupSafe==1.1  
nltk==3.8.1  
pex==1.3.2  
pluggy==0.6.0  
py==1.5.3  
pyyaml==3.12  
requests==2.18.4  
six==1.11.0  
SQLAlchemy==1.2.6  
tox==3.0.0  
urllib3==1.22  
virtualenv==15.2.0  
waitress==1.1.0  
Werkzeug==0.14.1  
psycopg2-binary==2.7.4  
gunicorn==19.7.1  
coreapi==2.3.3
You can find the snyk vulnerabilities for the project in the US : [User Story 168112 [Snyk] [cp_cm-classifier] [SCA] Fix Critical and High Snyk Vulnerabilities](https://dev.azure.com/tr-tax-checkpoint/Checkpoint/_workitems/edit/168112)

So,in order to resolve the snyk vulnerabilities ,I upgraded the nltk version to 3.8.1 (is  the version mentioned in snyk portal) ,I am getting the following error:

**When I Try to upgrade the nltk to 3.8.1 :**
ERROR: Could not find a version that satisfies the requirement nltk==3.8.2(from versions: 2.0b8.macosx-10.5-i386, 2.0.1rc1.macosx-10.6-x86_64, 2.0.1rc2-git, 2.0b4, 2.0b5, 2.0b6, 2.0b7, 2.0b8, 2.0b9, 2.0.1rc1, 2.0.1rc3, 2.0.1rc4, 2.0.1, 2.0.2, 2.0.3, 2.0.4, 2.0.5, 3.0.0b1, 3.0.0b2, 3.0.0, 3.0.1, 3.0.2, 3.0.3, 3.0.4, 3.0.5, 3.1, 3.2, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.5, 3.3.0, 3.4, 3.4.1, 3.4.2, 3.4.3, 3.4.4, 3.4.5, 3.5b1, 3.5, 3.6, 3.6.1, 3.6.2, 3.6.3, 3.6.4, 3.6.5, 3.6.6, 3.6.7)
ERROR: No matching distribution found for nltk==3.8.1

**When I Try to upgrade the waitress to 3.0.1 :**
  ERROR: Could not find a version that satisfies the requirement waitress==3.0.1 (from versions: 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.6.1, 0.7, 0.8, 0.8.1,
 0.8.2, 0.8.3, 0.8.4, 0.8.5, 0.8.6, 0.8.7, 0.8.8, 0.8.9, 0.8.10, 0.8.11b0, 0.9.0b0, 0.9.0b1, 0.9.0, 1.0a1, 1.0a2, 1.0.0, 1.0.1, 1.0.2, 1.1.0, 1.2.0b1, 1.2.0b2, 1.2.0b3, 1.2.0, 1.2.1, 1.3.0b0, 1.3.0, 1.3.1, 1.4.0, 1.4.1, 1.4.2, 1.4.3, 1.4.4, 2.0.0b0, 2.0.0b1, 2.0.0)
ERROR: No matching distribution found for waitress==3.0.1

**When I Try to upgrade the werkzeug to 3.0.6 :**
ERROR: Could not find a version that satisfies the requirement Werkzeug==3.0.6 (from versions: 0.1, 0.2, 0.3, 0.3.1, 0.4, 0.4.1, 0.5, 0.5.1, 0.6, 0.
6.1, 0.6.2, 0.7, 0.7.1, 0.7.2, 0.8, 0.8.1, 0.8.2, 0.8.3, 0.9, 0.9.1, 0.9.2, 0.9.3, 0.9.4, 0.9.5, 0.9.6, 0.10, 0.10.1, 0.10.2, 0.10.4, 0.11, 0.11.1,
0.11.2, 0.11.3, 0.11.4, 0.11.5, 0.11.6, 0.11.7, 0.11.8, 0.11.9, 0.11.10, 0.11.11, 0.11.12, 0.11.13, 0.11.14, 0.11.15, 0.12, 0.12.1, 0.12.2, 0.13, 0.
14, 0.14.1, 0.15.0, 0.15.1, 0.15.2, 0.15.3, 0.15.4, 0.15.5, 0.15.6, 0.16.0, 0.16.1, 1.0.0rc1, 1.0.0, 1.0.1, 2.0.0rc1, 2.0.0rc2, 2.0.0rc3, 2.0.0rc4, 2.0.0rc5, 2.0.0, 2.0.1, 2.0.2, 2.0.3)
ERROR: No matching distribution found for Werkzeug==3.0.6

**Upgraded from Python 3.6 to 3.9.7 :**
**Upgraded the version of nltk to 3.9  because 3.8.2 is not available :**
ERROR: Could not find a version that satisfies the requirement nltk==3.8.2 (from versions: 2.0b4, 2.0b5, 2.0b6, 2.0b7, 2.0b8, 2.0b9, 2.0.1rc1, 2.0.1
rc3, 2.0.1rc4, 2.0.1, 2.0.2, 2.0.3, 2.0.4, 2.0.5, 3.0.0b1, 3.0.0b2, 3.0.0, 3.0.1, 3.0.2, 3.0.3, 3.0.4, 3.0.5, 3.1, 3.2, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.5, 3.3.0, 3.4, 3.4.1, 3.4.2, 3.4.3, 3.4.4, 3.4.5, 3.5b1, 3.5, 3.6, 3.6.1, 3.6.2, 3.6.3, 3.6.5, 3.6.6, 3.6.7, 3.7, 3.8, 3.8.1, 3.9b1, 3.9, 3.9.1)
ERROR: No matching distribution found for nltk==3.8.2

**After Upgrading to 3.9 :**
ERROR: Cannot install c3-pycptam-cmclassifier==1.1.8 and nltk==3.9 because these package versions have conflicting dependencies.
The conflict is caused by:
    The user requested nltk==3.9
    c3-pycptam-cmclassifier 1.1.8 depends on nltk==3.2.5
**Upgraded the version of c3-pycptam-cmclassifier to 1.1.9 :**
ERROR: Cannot install -r requirements.txt (line 2) and c3-pycptam-data==1.2.7 because these package versions have conflicting dependencies.
The conflict is caused by:
    The user requested c3-pycptam-data==1.2.7
    c3-pycptam-cmclassifier 1.1.9 depends on c3-pycptam-data==1.3.0

**Upgraded the version of  c3-pycptam-data to 1.3.0 :**
ERROR: Cannot install -r requirements.txt (line 2) and Flask==0.12.2 because these package versions have conflicting dependencies.
The conflict is caused by:
    The user requested Flask==0.12.2
    c3-pycptam-cmclassifier 1.1.9 depends on flask==1.1.2
**Upgraded the version of  Flask to 1.1.2 :**
ERROR: Cannot install -r requirements.txt (line 2) and nltk==3.9 because these package versions have conflicting dependencies.
The conflict is caused by:
    The user requested nltk==3.9
    c3-pycptam-cmclassifier 1.1.9 depends on nltk==3.5

**This is the upgraded requirements.txt file according to python 3.9 compatibility ,Application is running,but snyk issues are not resolved,as there are many errors when trying to upgrade the versions of libraries.**
--extra-index-url https://tr1.jfrog.io/artifactory/api/pypi/pypi/simple  
c3-pycptam-cmclassifier==1.1.9  
c3-pycptam-data==1.3.0  
certifi==2018.4.16  
chardet==4.0.0  
click==6.7  
Cython==0.29.21  
scikit-build>=0.16.7  
cmake==3.28  
ddtrace==1.20.18  
Flask==1.1.2  
Flask-SQLAlchemy==2.5.1  
idna==2.6  
itsdangerous==0.24  
Jinja2>=2.10.1  
logstash-formatter==0.5.17  
MarkupSafe==1.1  
nltk>=3.5  
pex>=2.0.0  
pluggy==0.6.0  
py==1.5.3  
pyyaml==3.12  
requests==2.26.0  
six==1.12.0  
SQLAlchemy==1.3.24  
tox==3.0.0  
urllib3==1.26.7  
virtualenv==15.2.0  
waitress==3.0.1  
Werkzeug>=0.15  
psycopg2-binary==2.9.10  
gunicorn==20.1.0  
coreapi==2.3.3

Followed this approach ,while installing the requirements file :
  
1. Install Python 3.9.7 (http://python.org/downloads)  
2. Clone or download the repository to your local environment  
3. From command line: `$ cd <project directory>`  
  1. Create virtualenv:   
    1. If not installed, install virtualenv: `$ pip install virtualenv`  
    2. Create virtual env: `$ virtualenv venv`  
    3. Activate virtual env: `$ .\venv\Scripts\activate`   
  2. Install packages:  
     1. Uninstall the existing c3-pycptam-cmclassifier package: `$ pip uninstall c3-pycptam-data -y`  
     2. Install the specific version of c3-pycptam-cmclassifier without dependencies: `$ pip install --no-deps c3-pycptam-cmclassifier==1.1.9`  
     3. Verify the installation of c3-pycptam-cmclassifier: `$ pip show c3-pycptam-cmclassifier`  
     4. Install additional required packages from c3-pycptam-cmclassifier : `$ pip install flask pyyaml c3-pycptam-data`  
     5. Install the specific version of nltk: `$ pip install nltk==3.9`  
     6. Install the dependencies from the requirements.txt file, excluding c3-pycptam-cmclassifier: `$ pip install -r requirements.txt --no-deps c3-pycptam-cmclassifier`  
     7. When prompted enter the TR jfrog credentials         
4. Download WordNet Dependencies : `$ python -c "import nltk; nltk.download('wordnet'); nltk.download('stopwords'); nltk.download('punkt')"`

When I followed this approach ,Snyk vulnerabilities are resolved and Application is running fine in my local.But is failing in Pipeline with the following error : 

+ ./bundle.sh  
ERROR: Could not find a version that satisfies the requirement click==8.1.8 (from versions: 0.1, 0.2, 0.3, 0.4, 0.5, 0.5.1, 0.6, 0.7, 1.0, 1.1, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.0, 3.1, 3.2, 3.3, 4.0, 4.1, 5.0, 5.1, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7.dev0, 6.7, 7.0, 7.1, 7.1.1, 7.1.2, 8.0.0a1, 8.0.0rc1, 8.0.0, 8.0.1, 8.0.2, 8.0.3, 8.0.4)  
ERROR: No matching distribution found for click==8.1.8  
./bundle.sh: line 7: pex: command not found  
Looking in indexes: https://pypi.org/simple, https://C278692:****@tr1.jfrog.io/artifactory/api/pypi/pypi/simple, https://tr1.jfrog.io/artifactory/api/pypi/pypi/simpleCollecting c3-pycptam-cmclassifier==1.1.9  
  Downloading https://tr1.jfrog.io/artifactory/api/pypi/pypi/c3-pycptam-cmclassifier/1.1.9/c3_pycptam_cmclassifier-1.1.9-py3-none-any.whl (19 kB)  
Collecting c3-pycptam-data==1.3.0  
  Using cached https://tr1.jfrog.io/artifactory/api/pypi/pypi/c3-pycptam-data/1.3.0/c3_pycptam_data-1.3.0-py3-none-any.whl (915.0 MB)  
Collecting certifi==2018.4.16  
  Using cached https://tr1.jfrog.io/artifactory/api/pypi/pypi/packages/packages/7c/e6/92ad559b7192d846975fc916b65f667c7b8c3a32bea7372340bfe9a15fa5/certifi-2018.4.16-py2.py3-none-any.whl (150 kB)  
Collecting chardet==4.0.0  
Using cached https://tr1.jfrog.io/artifactory/api/pypi/pypi/packages/packages/19/c7/fa589626997dd07bd87d9269342ccb74b1720384a4d739a1872bd84fbe68/chardet-4.0.0-py2.py3-none-any.whl (178 kB)


