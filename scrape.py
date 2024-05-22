import re, requests_html

import model

URL = "https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n&sat={hour:02d}"

REGEX = r"^Vrijeme u Hrvatskoj (\d\d.\d\d.\d\d\d\d.) u (\d\d) h$"


def get_urls():
    return (URL.format(hour=hour) for hour in range(24))


def slice(cols, size):
    return (cols[pos : pos + size] for pos in range(0, len(cols), size))


def scrape_url(url):
    session = requests_html.HTMLSession()
    r = session.get(url)

    # fetch the measurement date and hour
    date_hour = r.html.find("h4", containing="Vrijeme u", first=True).text

    if m := re.match(REGEX, date_hour):
        date, hour = m.groups()
    else:
        raise ValueError("Invalid data: missing date and hour")

    # fetch the measurements
    for row in slice(r.html.xpath("//div[@id='primary']/div/table[contains(@class, 'fd-c-table1')]//td"), 8):
        yield model.Measurement.new(date, hour, row)


def main():
    from eywa_api import load_measurement

    for url in get_urls():
        for m in scrape_url(url):
            r = load_measurement(m.to_dict())
            print(r)


if __name__ == "__main__":
    main()
