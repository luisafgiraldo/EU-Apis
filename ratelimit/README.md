# Rate Limit Test Script

This script tests the rate limiting functionality of the Agentic Document Analysis API by sending requests.

## Usage

At root of the repo
```bash
node ratelimit-test.js [--tier environment] [--apikey key] [--rpm number]
```
 
### Parameters

- `--tier` (optional): Environment tier to test. Options: staging|dev|production. Default: staging
- `--apikey` (optional): API key for authentication. Default: staging test key
- `--rpm` (optional): Requests per minute. Default: 60

### Examples

```bash
# Test with default settings (staging tier, 60 rpm)
node ratelimit-test.js

# Test with your api key
node ratelimit-test.js --apikey "your-api-key"

# Test in production at 120 rpm
node ratelimit-test.js --tier production --rpm 120

# Test with custom API key and 90 rpm
node ratelimit-test.js --tier staging --apikey "your-api-key" --rpm 90
```

## Features

- Sends 100 total requests by default
- Configurable requests per minute (RPM)
- Shows response status codes and request timing
- Graceful cleanup on Ctrl+C
- Configurable for different environments (staging/dev/production)
- Uses native fetch API (no external dependencies)

## Notes

- The script uses a test PDF file located at `./public/pdfs/Loan+Form.pdf`
- Each request includes an `X-Ratelimit-Test: true` header
- The delay between requests is automatically calculated based on the RPM setting 