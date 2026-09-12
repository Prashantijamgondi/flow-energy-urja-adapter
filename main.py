"""
Flock Energy - Urja Meter Ops API
Clean REST wrapper over the legacy portal.
"""
from fastapi import FastAPI, HTTPException
from app.client import UrjaPortalClient, SessionExpiredError
from app.config import settings
from app.models import MeterSummary, MeterDetail, ConsumptionHistory, HealthResponse

app = FastAPI(
    title="Flock Energy - Urja Meter Ops API",
    version="1.0.0",
    description="Clean REST API proxy layer over the legacy Urja Meter Ops portal.",
)

portal_client = UrjaPortalClient(settings.URJA_BASE_URL)


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health():
    return HealthResponse(status="ok", portal_reachable=True)


@app.get("/api/v1/meters", response_model=list[dict], tags=["meters"])
def list_meters():
    try:
        return portal_client.list_meters()
    except SessionExpiredError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/meters/{meter_id}", response_model=dict, tags=["meters"])
def get_meter(meter_id: str):
    try:
        return portal_client.get_meter_details(meter_id)
    except SessionExpiredError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/meters/{meter_id}/consumption", response_model=list[dict], tags=["consumption"])
def get_consumption(meter_id: str):
    try:
        return portal_client.get_consumption(meter_id)
    except SessionExpiredError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Optional extension - fill in once/if you tackle hierarchy
# @app.get("/api/v1/hierarchy", tags=["hierarchy"])
# def get_hierarchy():
#     ...
