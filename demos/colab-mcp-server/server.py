from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Literal

import geopandas as gpd
from fastmcp import FastMCP

mcp = FastMCP("portolan-colab-server")


@mcp.tool
def read_collection(url: str) -> str:
    """Read a Portolan collection.json from a public URL and return its overview.

    Args:
        url: Public URL of the collection.json (e.g. hosted on GitHub Pages).
    """
    with urllib.request.urlopen(url) as res:
        col = json.load(res)

    summary = {
        "id": col.get("id"),
        "description": col.get("description"),
        "license": col.get("license"),
        "bbox": col.get("extent", {}).get("spatial", {}).get("bbox"),
        "links": [
            {"rel": l.get("rel"), "href": l.get("href")}
            for l in col.get("links", [])
            if l.get("rel") in ("items", "via", "derived_from")
        ],
    }
    return json.dumps(summary, ensure_ascii=False, indent=2)


@mcp.tool
def read_geoparquet(
    source: str,
    crs_out: str = "EPSG:4326",
    limit: int = 20,
) -> str:
    """Read a GeoParquet file (local path or public URL) and summarize features.

    Args:
        source: Local path or public URL to a .parquet file.
        crs_out: Target CRS to reproject to (default EPSG:4326).
        limit: Max number of features to include in the summary.
    """
    gdf = gpd.read_parquet(source)
    if gdf.crs is not None:
        before = gdf.crs.to_epsg() if gdf.crs.to_epsg() else str(gdf.crs)
        gdf = gdf.to_crs(crs_out)
        epsg_out = crs_out.split(":")[-1]
    else:
        before = "unknown"
        epsg_out = "unknown"

    features = gdf.head(limit).to_dict(orient="records")
    for f in features:
        f.pop("geometry", None)

    return json.dumps(
        {
            "rows": len(gdf),
            "crs_before": before,
            "crs_after": epsg_out,
            "columns": list(gdf.columns),
            "sample": features,
        },
        ensure_ascii=False,
        indent=2,
        default=str,
    )


@mcp.tool
def convert_geoparquet(
    source: str,
    target: str,
    crs_out: str = "EPSG:4326",
) -> str:
    """Convert a GeoParquet file to another CRS and write it out.

    Args:
        source: Local path to input .parquet.
        target: Local path to write converted .parquet.
        crs_out: Target CRS, e.g. EPSG:4326.
    """
    gdf = gpd.read_parquet(source)
    before = gdf.crs.to_epsg() if gdf.crs is not None else None
    if gdf.crs is not None:
        gdf = gdf.to_crs(crs_out)
    gdf.to_parquet(target, schema_version="1.0.0")
    return json.dumps(
        {
            "message": "converted",
            "input_crs": before,
            "output_crs": crs_out,
            "output": target,
            "rows": len(gdf),
        },
        ensure_ascii=False,
    )


@mcp.tool
def validate_collection(path: str) -> str:
    """Validate a local collection.json against the Portolan/STAC basics.

    Args:
        path: Local path to a collection.json file.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    errors: list[str] = []
    checks = {
        "stac_version": ("stac_version" in data, "missing stac_version"),
        "type == Collection": (data.get("type") == "Collection", "type must be Collection"),
        "id": ("id" in data and data["id"], "missing id"),
        "description": ("description" in data and data["description"], "missing description"),
        "license": ("license" in data and data["license"], "missing license"),
        "links": (isinstance(data.get("links"), list) and len(data["links"]) > 0, "links must be a non-empty list"),
    }
    for name, (ok, msg) in checks.items():
        if not ok:
            errors.append(msg)
    return json.dumps(
        {
            "valid": len(errors) == 0,
            "errors": errors,
            "field_count": len(data),
        },
        ensure_ascii=False,
        indent=2,
    )


if __name__ == "__main__":
    transport: Literal["http", "stdio"] = "http"
    mcp.run(transport=transport)