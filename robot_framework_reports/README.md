# Admin Dashboard Report Bot

This Robot Framework bot automatically extracts data from your admin dashboard and generates comprehensive reports.

## Prerequisites

1. **Python 3.8+** installed
2. **Chrome browser** installed
3. **ChromeDriver** installed and in PATH (download from https://chromedriver.chromium.org/)
4. **Django server** running on http://localhost:8000

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Download ChromeDriver:
   - Go to https://chromedriver.chromium.org/downloads
   - Download the version that matches your Chrome browser
   - Extract and add to your system PATH

## Configuration

Edit `simple_admin_report.robot` and update these variables if needed:
```robot
${BASE_URL}       http://localhost:8000
${ADMIN_USERNAME} admin@example.com
${ADMIN_PASSWORD} admin123
```

## Usage

### Method 1: Using the Batch File (Windows)
```bash
run_report.bat
```

### Method 2: Using Robot Framework Directly
```bash
robot simple_admin_report.robot
```

### Method 3: Using Python
```bash
python -m robot simple_admin_report.robot
```

## What the Bot Does

1. **Opens browser** and logs into admin panel
2. **Navigates** to admin dashboard
3. **Extracts** dashboard statistics (charts data)
4. **Navigates** to manage complaints page
5. **Extracts** detailed complaints data
6. **Generates** a summary report in text format
7. **Saves** the report with timestamp

## Output

The bot generates:
- **Console logs** with detailed information
- **Text report file** named `admin_report_YYYY-MM-DD_HH-MM-SS.txt`
- **Robot Framework log files** (log.html, report.html, output.xml)

## Troubleshooting

### Common Issues:

1. **"ChromeDriver not found"**
   - Download ChromeDriver and add to PATH
   - Or specify the path in the script

2. **"Django server not accessible"**
   - Make sure Django server is running: `python manage.py runserver`
   - Check if it's running on http://localhost:8000

3. **"Login failed"**
   - Check admin credentials in the script
   - Make sure admin account exists

4. **"Element not found"**
   - Check if the page structure has changed
   - Update XPath selectors if needed

### Debug Mode:
Run with verbose logging:
```bash
robot --loglevel DEBUG simple_admin_report.robot
```

## Customization

You can modify the script to:
- Extract different data
- Generate different report formats
- Add more pages to scrape
- Change the output format

## Scheduling

To run automatically:
- **Windows**: Use Task Scheduler
- **Linux/Mac**: Use cron jobs
- **Example cron job** (daily at 9 AM):
  ```bash
  0 9 * * * cd /path/to/robot_framework_reports && robot simple_admin_report.robot
  ``` 