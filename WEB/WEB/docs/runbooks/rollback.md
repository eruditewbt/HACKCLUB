# Rollback Runbook (Starter)

Rollback should be safe and fast:
- keep previous container images available
- use DB migrations that are backward compatible
- keep feature flags for risky changes

## Steps
1. Roll back app deploy to previous image tag.
2. If schema changed, use compatible migrations only.
3. Verify health endpoints and key flows.

