import json

if __name__ == "__main__":

    with open("coverage.json") as file:
        coverage_info = json.load(file)

    print("Coverage:", coverage_info["totals"]["percent_covered"], "%")

    assert coverage_info["totals"]["percent_covered"] > 75