from collections import Counter
import re
import sys

def analyze_http_logs(file_path):
    status_code_pattern = re.compile(r'"HTTP/1\.1 (\d{3})')
    status_counts = Counter()

    with open(file_path, 'r', encoding='utf-8') as log_file:
        for line in log_file:
            match = status_code_pattern.search(line)
            if match:
                status_code = match.group(1)
                status_counts[status_code] += 1

    print("📊 HTTP Status Code Summary:")
    for code in sorted(status_counts.keys()):
        print(f"  {code}: {status_counts[code]} times")

    # Assert there are no 206 or other errors (anything not 200)
    non_200_responses = {code: count for code, count in status_counts.items() if code != '200'}

    if non_200_responses:
        print("\n❌ Detected invalid status codes:")
        for code, count in non_200_responses.items():
            print(f"  {code}: {count} times")

        assert '206' not in status_counts, "Partial responses (206) detected — this is considered a failure."
        assert all(code == '200' for code in status_counts), "One or more HTTP responses are not 200."

    print("\n✅ All requests returned 200 OK.")

# Run it
if __name__ == "__main__":
    try:
        analyze_http_logs("http_logs.txt")
    except AssertionError as e:
        print(f"\n❗ Assertion failed: {e}")
        sys.exit(1)