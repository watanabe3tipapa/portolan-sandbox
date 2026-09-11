from __future__ import annotations

import base64
import json
import os
import subprocess
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path
from typing import Literal

import geopandas as gpd
from fastmcp import FastMCP

mcp = FastMCP("portolan-colab-server")

API = "https://api.github.com"


def _load_parquet(source: str) -> gpd.GeoDataFrame:
    """Load a GeoParquet from a local path or a public HTTP(S) URL."""
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source) as res:
            return gpd.read_parquet(BytesIO(res.read()))
    return gpd.read_parquet(source)


def _github_token() -> str:
    """Resolve a GitHub token from env GITHUB_TOKEN or the gh CLI cache."""
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        out = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(
            "GitHub token not found: set env GITHUB_TOKEN or run `gh auth login`"
        ) from exc
    token = out.stdout.strip()
    if not token:
        raise RuntimeError("GitHub token resolved to empty string")
    return token


def _github_request(
    method: str,
    path: str,
    *,
    payload: dict | None = None,
    token: str | None = None,
) -> dict:
    """Send an authenticated request to the GitHub REST API."""
    token = token or _github_token()
    url = f"{API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()
        raise RuntimeError(f"GitHub API {exc.code} on {method} {path}: {detail}") from exc


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
    gdf = _load_parquet(source)
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
        source: Local path or public URL to input .parquet.
        target: Local path to write converted .parquet.
        crs_out: Target CRS, e.g. EPSG:4326.
    """
    gdf = _load_parquet(source)
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


@mcp.tool
def deploy_to_github_pages(
    repo: str,
    file_path: str,
    content: str,
    message: str,
    branch: str = "main",
) -> str:
    """Deploy a file to a GitHub repo via the Contents API.

    Publishes (creates/updates) a single text file on the given branch, which
    triggers the repo's GitHub Actions Pages workflow on push. Works without a
    local git clone.

    Args:
        repo: Owner/name, e.g. "watanabe3tipapa/portolan-sandbox".
        file_path: Path in the repo, e.g. "portolan-lp/public/demo-collection/collection.json".
        content: New file text content.
        message: Commit message.
        branch: Target branch (default main).
    """
    token = _github_token()
    path = file_path.lstrip("/")

    try:
        existing = _github_request("GET", f"/repos/{repo}/contents/{path}?ref={branch}", token=token)
        sha = existing.get("sha")
    except RuntimeError as exc:
        if "404" not in str(exc):
            raise
        sha = None

    payload: dict = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch,
    }
    if sha:
        payload["sha"] = sha

    method = "PUT"
    put = _github_request(method, f"/repos/{repo}/contents/{path}", payload=payload, token=token)
    result = {
        "message": "committed",
        "repo": repo,
        "path": path,
        "branch": branch,
        "commit": put.get("commit", {}).get("sha"),
        "html_url": put.get("content", {}).get("html_url"),
    }
    if not sha:
        result["message"] = "created"
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool
def write_to_drive(filename: str, content: str) -> str:
    """Write a text file under the mounted Google Drive in Colab.

    Returns a message (or a hint when Drive is not mounted).

    Args:
        filename: Destination under mounted Drive, e.g. "Portolan/collection.json".
        content: File text content.
    """
    mount = Path("/content")
    candidates = [d for d in mount.iterdir() if d.is_dir() and "drive" in d.name.lower()]
    if not candidates:
        return json.dumps(
            {
                "ok": False,
                "message": "Drive not mounted. Run: from google.colab import drive; drive.mount('/content/drive')",
            },
            ensure_ascii=False,
        )
    drive_root = candidates[0]
    target = drive_root / filename.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return json.dumps({"ok": True, "path": str(target), "bytes": len(content)}, ensure_ascii=False)


if __name__ == "__main__":
    transport: Literal["http", "stdio"] = "http"
    mcp.run(transport=transport)