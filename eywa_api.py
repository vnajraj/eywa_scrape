import eywa


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
    return eywa.graphql({"query": query, "variables": variables})


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

    return eywa.graphql({"query": mutation, "variables": {"measurement": m}})


def load_measurement(m):
    result = measurement_exists(m)

    exists = result["searchMeasurement"]
    if exists:
        return result

    return sync_measurement(m)


def get_scrape_hours():
    task = eywa.get_task()

    hours = task["data"]["scrapeHours"]
    return int(hours["start"]), int(hours["stop"])
