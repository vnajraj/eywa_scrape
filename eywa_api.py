import json, os, requests
import graphqlclient

SERVER = os.getenv("EYWA_HOST", "http://localhost:8080")
LOGINURL = SERVER + "/eywa/login"
GRAPHQLURL = SERVER + "/graphql"

LOGINDATA = {
    "username": os.getenv("EYWA_USER", "dummy"),
    "password": os.getenv("EYWA_PASSWORD", "dummy"),
}


def get_token(login=LOGINDATA):
    r = requests.post(LOGINURL, json=login)

    if r.status_code != 200:
        raise ValueError("Login failed")

    return r.text


TOKEN = get_token(LOGINDATA)


def send_query(query, variables=None, token=TOKEN):
    client = graphqlclient.GraphQLClient(GRAPHQLURL)
    client.inject_token(token)
    return client.execute(query=query, variables=variables)


def measurement_exists(m):
    query = """
    query CheckMeasurementExists ($date: String, $hour: Int, $station_name: String) {
        searchMeasurement {
            date (_eq:$date)
            hour (_eq:$hour)
            station {
                name (_eq:$station_name)
            }
        }
    }
    """
    variables = {
                "date": m["date"],
                "hour": m["hour"],
                "station_name": m["station"]
            }
    return send_query(query, variables=variables)


def sync_measurement(m):
    mutation = """
    mutation SyncMeasurement ($measurement: MeasurementInput) {
        syncMeasurement(measurement: $measurement) {
           euuid
        }
    }
    """
    # model refactored - station now a separate entity
    m["station"] = {"name": m["station"]}

    return send_query(mutation, variables={"measurement": m})


def load_measurement(m):
    result = measurement_exists(m)
    exists = json.loads(result)["data"]["searchMeasurement"]
    if exists:
        return result

    return sync_measurement(m)
