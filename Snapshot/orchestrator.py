import getSnapshots as gs
import getSnapShotExport as ge
import os
import time
import requests

# Base URL for API requests
url_base = "https://api.staging.landing.ai/v1/projects"
# API key for authentication
api_key = "land_sk_ZF74SGID25P4saw8z2iizbB8SgEidk1FMIBzPP4MrNRSKyMn0a"  # Org: landing
# Project ID
project_id = 27689531707438
# URL
url = f"{url_base}/{project_id}/dataset/snapshots"

start_time = time.perf_counter()  # Start the timer

listSnapShots = gs.listSnapShots(api_key, url)
print(listSnapShots)
lastSnapShot = gs.display_snapshot(listSnapShots)

snapshot_version = listSnapShots["version"]
print(snapshot_version)

# Start the snapshot export process
export_url = f"{url_base}/{project_id}/dataset/snapshots/{snapshot_version}/export"
print(export_url)
export_response = requests.post(export_url, headers={"apikey": api_key})

if export_response.status_code == 200:
    print("Export initiated successfully!")
else:
    print(f"Failed to initiate export: {export_response.text}")

# Wait until the snapshot is exported
export = None
while not export:
    print("Waiting for export to complete...")
    time.sleep(5)  # Wait 5 seconds before retrying
    export = ge.SnapShotExport(api_key, export_url)
    if not export:
        print("Export not ready yet...")

if export:
    output_filename = os.path.join(
        "Snapshot", f"project_{project_id}_version_{snapshot_version}_downloaded_file.tar.bz2"
    )
    url = export.get("downloadUrl")
    if url:
        print(url)
        ge.download_file_from_url(url=url, local_filename=output_filename)
        # Check if the file was downloaded successfully
        if os.path.exists(output_filename):
            print("File downloaded successfully!")
            # Delete the file after validation
            os.remove(output_filename)
            print("File deleted successfully!")
        else:
            print("File download failed or file not found.")
    else:
        print("No download URL available.")
else:
    print("The snapshot export is not available. Please check if the snapshot has been exported correctly.")

end_time = time.perf_counter()  # Stop the timer
execution_time_minutes = (end_time - start_time) / 60
print(f"Total execution time: {execution_time_minutes:.2f} minutes")
