from datetime import datetime, timezone

local_datetime = datetime.now()
utc_datetime = datetime.now(timezone.utc)

local_iso_str = datetime.strftime(local_datetime, "%Y-%m-%dT%H:%M:%S.%f")[:-3]
utc_iso_str = datetime.strftime(utc_datetime, "%Y-%m-%dT%H:%M:%S.%f")[:-3]

print(f"local dt: {local_iso_str}, tzname: {local_datetime.tzname()}")
print(f"  utc dt: {utc_iso_str}, tzname: {utc_datetime.tzname()}")

print("\n")

print(f"local dt: {local_datetime.isoformat()}")
print(f"  utc dt: {utc_datetime.isoformat()}")