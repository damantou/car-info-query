import json
from pathlib import Path


def iter_json(f):
    for l in Path(f).read_text().splitlines():
        yield json.loads(l)


def aggregate_trims(it):
    years = {}
    for m,t in it:
        year, make, model = m
        trims = t or []
        year = str(year)

        years.setdefault("index", set()).add(year)
        year_data = years.setdefault("data", {}).setdefault(year, {})

        year_data.setdefault("index", set()).add(make)
        make_data = year_data.setdefault("data", {}).setdefault(make, {})

        make_data.setdefault("index", set()).add(model)
        model_data = make_data.setdefault("data", {}).setdefault(model, {})

        model_data["index"] = trims

    return years


def sort_index(data):
    print(data.keys())
    data["index"] = sorted(data["index"])
    if "data" in data:
        for d in data["data"].values():
            sort_index(d)


if __name__ == "__main__":
    years = aggregate_trims(iter_json("trims"))
    sort_index(years)
    years["index"] = sorted(years["index"], reverse=True)
    # Path("all.json").write_text(json.dumps(years, indent=4))

    for y,d in years["data"].items():
        Path(f"years/{y}.json").write_text(json.dumps(d))
