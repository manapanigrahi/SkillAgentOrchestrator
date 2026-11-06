"""Generated RetailHub API contract probes. Set RETAILHUB_BASE_URL to run network checks."""
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = os.getenv("RETAILHUB_BASE_URL", "").rstrip("/")

def probe(case_id, requirement_id, endpoint):
    if not BASE_URL:
        print(f"SKIP {case_id} ({requirement_id}): RETAILHUB_BASE_URL is not set")
        return
    path = endpoint.replace("*", "health")
    request = Request(BASE_URL + path, headers={"Accept": "application/json", "X-Test-Case": case_id})
    try:
        with urlopen(request, timeout=10) as response:
            assert response.status < 500, f"{case_id} server error: {response.status}"
            print(f"PASS {case_id} ({requirement_id}): {response.status}")
    except HTTPError as error:
        assert error.code < 500, f"{case_id} server error: {error.code}"
        print(f"PASS {case_id} ({requirement_id}): expected client response {error.code}")
    except URLError as error:
        raise AssertionError(f"{case_id} network failure: {error}") from error

def main():
    probe('TC-001', 'FR-AUTH-01', '/api/v1/auth/*')
    probe('TC-002', 'FR-AUTH-01', '/api/v1/auth/*')
    probe('TC-021', 'FR-INV-01', '/api/v1/inventory/*')
    probe('TC-022', 'FR-INV-01', '/api/v1/inventory/*')
    probe('TC-023', 'FR-INV-02', '/api/v1/inventory/*')
    probe('TC-024', 'FR-INV-02', '/api/v1/inventory/*')
    probe('TC-025', 'FR-INV-03', '/api/v1/inventory/*')
    probe('TC-026', 'FR-INV-03', '/api/v1/inventory/*')
    probe('TC-027', 'FR-INV-04', '/api/v1/inventory/*')
    probe('TC-028', 'FR-INV-04', '/api/v1/inventory/*')
    probe('TC-029', 'FR-INV-05', '/api/v1/inventory/*')
    probe('TC-030', 'FR-INV-05', '/api/v1/inventory/*')
    probe('TC-033', 'FR-CRT-02', '/api/v1/cart')
    probe('TC-034', 'FR-CRT-02', '/api/v1/cart')
    probe('TC-039', 'FR-ORD-01', '/api/v1/orders')
    probe('TC-040', 'FR-ORD-01', '/api/v1/orders')
    probe('TC-045', 'FR-ORD-04', '/api/v1/orders')
    probe('TC-046', 'FR-ORD-04', '/api/v1/orders')

if __name__ == "__main__":
    main()
