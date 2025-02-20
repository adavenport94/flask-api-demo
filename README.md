# Flask Demo - Health Insurance Policy API 

Provides an interface (Flask API) for managing policyholder and insured event data. Utilizing a Postgres DB for storage.

## Installation
To run the flask app locally, first install all packages from requirements.txt into either your global Python environment, or
preferably a virtual environment for testing. 
### Install locally
```
git clone https://github.com/andrewdaveport94/gs-takehome.git
cd gs-takehome
virtualenv -p python3 .
source bin/activate or Scripts\activate on windows
pip install -r requirements.txt
```

## Running Postgres DB via Docker
```
docker pull postgres:alpine
docker run --name postgres_gs -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 postgres:alpine
docker exec -it postgres_gs
psql -U postgres
create database gs;
```

## Running the App
Assuming you're using a local postgres db.
```
set DATABASE_URL=postgresql://postgres:1234@localhost/gs
python app.py
```

## Using the Service
Routes and example payloads can be viewed within the Swagger UI being served at the following location: 
```
http://127.0.0.1:5000/docs/
```

![image](images/swagger.png)

### Routes
To call the route to create a new policyholder, direct a POST request to the following URL:
```
http://127.0.0.1:5000/policyholder/create_insured

Example payload:
{
	"gender": "Male",
	"date_of_birth": "2/6/1980",
	"ssn": 111223333,
	"smoking_status": true,
	"allergies": "Nuts, Pollen",
	"medical_conditions": "Asthma, Hypertension"
}

*ssn stored as a sha256 hash value (29,000 iterations & 16 byte salt)
```

To call the route to get all policyholders, direct a GET request to the following URL:
```
http://127.0.0.1:5000/policyholder/

Example response:
{
  "policyholders": [
    {
      "allergies": "Nuts, Pollen",
      "date_of_birth": "Sat, 06 Feb 1960 00:00:00 GMT",
      "gender": "Female",
      "id": 1,
      "insured_events": [
        {
          "billed_amount": 250.99,
          "covered_amount": 170.49,
          "date_of_incidence": "Tue, 06 Oct 2020 00:00:00 GMT",
          "id": 1,
          "policyholder_id": 1,
          "type_of_issue": "Broken Foot"
        }
        ...
        ...

*ssn-hash is not returned. Ideally we wouldn't want to store ssn/sensitive data as is. An alternative solution might be to leverage multiple servers with cert and keys to perform encryption and decryption.

```

To call the route to validate a policyholders ssn, direct a POST request to the following URL:
```
http://127.0.0.1:5000/policyholder/validate_ssn

Example payload:
{
  "policyholder_id": 1,
  "ssn": 11122333
}

Use case: to validate the user's identity. Checks hashed ssn with value provided.
```

To call the route to return a policyholder by id, direct a GET request to the following URL:
```
http://127.0.0.1:5000/policyholder/{policyholder_id}
```

To call the route to create a new insured event, direct a POST request to the following URL:
```
http://127.0.0.1:5000/insured_event/create_insured_event

Example payload:
{
  "date_of_incidence": "10/10/2020",
  "billed_amount": 250,
  "covered_amount": 150.5,
  "type_of_issue": "Broken Wrist",
  "policyholder_id": 1
}
```

To call the route to return all insured events, direct a GET request to the following URL:
```
http://127.0.0.1:5000/insured_event/

Example response:
{
  "insured_events": [
    {
      "billed_amount": 250.99,
      "covered_amount": 170.49,
      "date_of_incidence": "Tue, 06 Oct 2020 00:00:00 GMT",
      "id": 1,
      "policyholder_id": 1,
      "type_of_issue": "Broken Foot"
    }
  ]
}
```

To call the route to retrieve aggregated metrics, direct a GET request to the following URL:
```
http://127.0.0.1:5000/aggregated_metrics/

Example response:
{
  "aggregated_metrics": {
    "average_age": 60.676712328767124,
    "claims": 2,
    "covered_amount": 340.98
  }
}
```

### DB Schema

![image](images/db-schema.png)

## Built With
- Python 3.7
- Flask 1.1.2
- Flask-SQLAlchemy 2.4.4
- Werkzeug 0.16.1
- aniso8601 8.0.0
- flask-restplus 0.13.0
- passlib 1.7.4
- psycopg2 2.8.6


