# SIH Hackathon project backend

Our Idea for the Automatic Active Server Communication Alerts is to develop a Responsive Web Application which would act as an updated approach for checking the Network Breakdowns of multiple websites in a simplified way. The http status codes of the registered websites would be analyzed by this web application to identify the errors and this status codes would be stored into a separate database as a record. In case of receiving the critical status codes from the website or the server crash, the acknowledgements would be send using SMS API to the maintainer of the website. This would reduce the tedious present unattainable approach of checking the website regularly by the maintainer to receive the error codes. This Web Application can also be used by normal users for checking the status of the listed websites.

## Local Installation

### Dependencies Install
```
sudo apt-get install git
sudo apt-get install virtualenv
```

```
git clone https://github.com/Code-Blooded-007/Backend.git
cd Backend
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
flask run

```


### For accessing the app, open
```
http://0.0.0.0:5000
```

