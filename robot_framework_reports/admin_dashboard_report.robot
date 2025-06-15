*** Settings ***
Documentation     Robot Framework RPA script to generate reports from Admin Dashboard
Library           RPA.Browser.Selenium
Library           RPA.Excel.Files
Library           RPA.PDF
Library           RPA.FileSystem
Library           DateTime
Library           Collections
Library           String

*** Variables ***
${BASE_URL}       http://localhost:8000
${ADMIN_USERNAME} admin@example.com
${ADMIN_PASSWORD} admin123
${REPORT_FOLDER}  ${CURDIR}/reports
${TIMESTAMP}      ${EMPTY}

*** Tasks ***
Generate Admin Dashboard Report
    [Documentation]    Main task to generate comprehensive admin dashboard report
    Set Timestamp
    Create Report Directory
    Login To Admin Panel
    Navigate To Admin Dashboard
    Extract Dashboard Data
    Generate Excel Report
    Generate PDF Report
    Generate Summary Report
    [Teardown]    Close All Browsers

*** Keywords ***
Set Timestamp
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    Set Global Variable    ${TIMESTAMP}    ${timestamp}

Create Report Directory
    Create Directory    ${REPORT_FOLDER}
    Create Directory    ${REPORT_FOLDER}/excel
    Create Directory    ${REPORT_FOLDER}/pdf
    Create Directory    ${REPORT_FOLDER}/summary

Login To Admin Panel
    [Documentation]    Login to the admin panel
    Open Available Browser    ${BASE_URL}/administrator/
    Wait Until Element Is Visible    name=email    timeout=10s
    Input Text    name=email    ${ADMIN_USERNAME}
    Input Password    name=password    ${ADMIN_PASSWORD}
    Click Button    type=submit
    Wait Until Element Is Visible    xpath=//h1[contains(text(),'Admin Dashboard')]    timeout=10s

Navigate To Admin Dashboard
    [Documentation]    Navigate to the admin dashboard page
    Go To    ${BASE_URL}/administrator/dashboard/
    Wait Until Element Is Visible    xpath=//h1[contains(text(),'Admin Dashboard')]    timeout=10s

Extract Dashboard Data
    [Documentation]    Extract all relevant data from the dashboard
    Extract Category Distribution Data
    Extract Status Distribution Data
    Extract Monthly Statistics Data
    Extract Complaint Details Data

Extract Category Distribution Data
    [Documentation]    Extract category distribution from pie chart data
    Wait Until Element Is Visible    id=categoryPieChart    timeout=10s
    ${category_data}=    Execute JavaScript
    ...    return {{ category_data|safe }}.map(item => ({category: item.category__name, count: item.count}));
    Set Global Variable    ${CATEGORY_DATA}    ${category_data}
    Log    Category Data: ${category_data}

Extract Status Distribution Data
    [Documentation]    Extract status distribution from pie chart data
    Wait Until Element Is Visible    id=statusPieChart    timeout=10s
    ${status_data}=    Execute JavaScript
    ...    return {{ status_data|safe }}.map(item => ({status: item.status, count: item.count}));
    Set Global Variable    ${STATUS_DATA}    ${status_data}
    Log    Status Data: ${status_data}

Extract Monthly Statistics Data
    [Documentation]    Extract monthly statistics for each year level
    Wait Until Element Is Visible    xpath=//canvas[contains(@id,'monthlyChart')]    timeout=10s
    ${monthly_data}=    Execute JavaScript
    ...    return {{ monthly_stats|safe }}.map(item => ({year_level: item.year_level, data: item.data}));
    Set Global Variable    ${MONTHLY_DATA}    ${monthly_data}
    Log    Monthly Data: ${monthly_data}

Extract Complaint Details Data
    [Documentation]    Navigate to manage complaints and extract detailed data
    Go To    ${BASE_URL}/administrator/manage-complaints/
    Wait Until Element Is Visible    id=complaintsTable    timeout=10s
    
    ${complaints}=    Create List
    ${rows}=    Get Element Count    xpath=//table[@id='complaintsTable']//tbody/tr
    
    FOR    ${i}    IN RANGE    1    ${rows}+1
        ${category}=    Get Text    xpath=//table[@id='complaintsTable']//tbody/tr[${i}]/td[1]
        ${full_name}=    Get Text    xpath=//table[@id='complaintsTable']//tbody/tr[${i}]/td[2]
        ${course_title}=    Get Text    xpath=//table[@id='complaintsTable']//tbody/tr[${i}]/td[3]
        ${course_lecturer}=    Get Text    xpath=//table[@id='complaintsTable']//tbody/tr[${i}]/td[4]
        ${status}=    Get Text    xpath=//table[@id='complaintsTable']//tbody/tr[${i}]/td[5]
        ${submitted_date}=    Get Text    xpath=//table[@id='complaintsTable']//tbody/tr[${i}]/td[6]
        
        ${complaint}=    Create Dictionary
        ...    category=${category}
        ...    full_name=${full_name}
        ...    course_title=${course_title}
        ...    course_lecturer=${course_lecturer}
        ...    status=${status}
        ...    submitted_date=${submitted_date}
        
        Append To List    ${complaints}    ${complaint}
    END
    
    Set Global Variable    ${COMPLAINTS_DATA}    ${complaints}
    Log    Extracted ${rows} complaints

Generate Excel Report
    [Documentation]    Generate comprehensive Excel report with multiple sheets
    ${excel_file}=    Set Variable    ${REPORT_FOLDER}/excel/admin_dashboard_report_${TIMESTAMP}.xlsx
    
    Create Workbook    ${excel_file}
    
    # Summary Sheet
    Create Worksheet    Summary
    Add Summary Data
    
    # Category Distribution Sheet
    Create Worksheet    Category Distribution
    Add Category Data
    
    # Status Distribution Sheet
    Create Worksheet    Status Distribution
    Add Status Data
    
    # Monthly Statistics Sheet
    Create Worksheet    Monthly Statistics
    Add Monthly Data
    
    # Detailed Complaints Sheet
    Create Worksheet    Detailed Complaints
    Add Complaints Data
    
    Save Workbook
    Log    Excel report generated: ${excel_file}

Add Summary Data
    [Documentation]    Add summary statistics to the Summary sheet
    ${total_complaints}=    Get Length    ${COMPLAINTS_DATA}
    
    Set Cell Value    1    1    Admin Dashboard Report Summary
    Set Cell Value    1    2    Generated on: ${TIMESTAMP}
    
    Set Cell Value    3    1    Total Complaints
    Set Cell Value    3    2    ${total_complaints}
    
    # Calculate status breakdown
    ${pending_count}=    Set Variable    0
    ${ongoing_count}=    Set Variable    0
    ${resolved_count}=    Set Variable    0
    
    FOR    ${complaint}    IN    @{COMPLAINTS_DATA}
        ${status}=    Get From Dictionary    ${complaint}    status
        Run Keyword If    '${status}' == 'Pending'    ${pending_count}=    Evaluate    ${pending_count} + 1
        Run Keyword If    '${status}' == 'On-going'    ${ongoing_count}=    Evaluate    ${ongoing_count} + 1
        Run Keyword If    '${status}' == 'Resolved'    ${resolved_count}=    Evaluate    ${resolved_count} + 1
    END
    
    Set Cell Value    5    1    Pending Complaints
    Set Cell Value    5    2    ${pending_count}
    Set Cell Value    6    1    On-going Complaints
    Set Cell Value    6    2    ${ongoing_count}
    Set Cell Value    7    1    Resolved Complaints
    Set Cell Value    7    2    ${resolved_count}

Add Category Data
    [Documentation]    Add category distribution data
    Set Cell Value    1    1    Category
    Set Cell Value    1    2    Count
    Set Cell Value    1    3    Percentage
    
    ${row}=    Set Variable    2
    ${total}=    Set Variable    0
    
    FOR    ${category}    IN    @{CATEGORY_DATA}
        ${total}=    Evaluate    ${total} + ${category.count}
    END
    
    FOR    ${category}    IN    @{CATEGORY_DATA}
        ${percentage}=    Evaluate    round((${category.count} / ${total}) * 100, 2)
        Set Cell Value    ${row}    1    ${category.category}
        Set Cell Value    ${row}    2    ${category.count}
        Set Cell Value    ${row}    3    ${percentage}%
        ${row}=    Evaluate    ${row} + 1
    END

Add Status Data
    [Documentation]    Add status distribution data
    Set Cell Value    1    1    Status
    Set Cell Value    1    2    Count
    Set Cell Value    1    3    Percentage
    
    ${row}=    Set Variable    2
    ${total}=    Set Variable    0
    
    FOR    ${status}    IN    @{STATUS_DATA}
        ${total}=    Evaluate    ${total} + ${status.count}
    END
    
    FOR    ${status}    IN    @{STATUS_DATA}
        ${percentage}=    Evaluate    round((${status.count} / ${total}) * 100, 2)
        Set Cell Value    ${row}    1    ${status.status}
        Set Cell Value    ${row}    2    ${status.count}
        Set Cell Value    ${row}    3    ${percentage}%
        ${row}=    Evaluate    ${row} + 1
    END

Add Monthly Data
    [Documentation]    Add monthly statistics data
    Set Cell Value    1    1    Year Level
    Set Cell Value    1    2    January
    Set Cell Value    1    3    February
    Set Cell Value    1    4    March
    Set Cell Value    1    5    April
    Set Cell Value    1    6    May
    Set Cell Value    1    7    June
    Set Cell Value    1    8    July
    Set Cell Value    1    9    August
    Set Cell Value    1    10    September
    Set Cell Value    1    11    October
    Set Cell Value    1    12    November
    Set Cell Value    1    13    December
    
    ${row}=    Set Variable    2
    FOR    ${year_data}    IN    @{MONTHLY_DATA}
        Set Cell Value    ${row}    1    ${year_data.year_level}
        ${col}=    Set Variable    2
        FOR    ${month_count}    IN    @{year_data.data}
            Set Cell Value    ${row}    ${col}    ${month_count}
            ${col}=    Evaluate    ${col} + 1
        END
        ${row}=    Evaluate    ${row} + 1
    END

Add Complaints Data
    [Documentation]    Add detailed complaints data
    Set Cell Value    1    1    Category
    Set Cell Value    1    2    Full Name
    Set Cell Value    1    3    Course Title
    Set Cell Value    1    4    Course Lecturer
    Set Cell Value    1    5    Status
    Set Cell Value    1    6    Submitted Date
    
    ${row}=    Set Variable    2
    FOR    ${complaint}    IN    @{COMPLAINTS_DATA}
        Set Cell Value    ${row}    1    ${complaint.category}
        Set Cell Value    ${row}    2    ${complaint.full_name}
        Set Cell Value    ${row}    3    ${complaint.course_title}
        Set Cell Value    ${row}    4    ${complaint.course_lecturer}
        Set Cell Value    ${row}    5    ${complaint.status}
        Set Cell Value    ${row}    6    ${complaint.submitted_date}
        ${row}=    Evaluate    ${row} + 1
    END

Generate PDF Report
    [Documentation]    Generate PDF summary report
    ${pdf_file}=    Set Variable    ${REPORT_FOLDER}/pdf/admin_dashboard_summary_${TIMESTAMP}.pdf
    
    ${html_content}=    Create Summary HTML
    Html To Pdf    ${html_content}    ${pdf_file}
    Log    PDF report generated: ${pdf_file}

Create Summary HTML
    [Documentation]    Create HTML content for PDF report
    ${html}=    Set Variable
    ...    <html><head><style>body{font-family:Arial,sans-serif;margin:20px;}table{border-collapse:collapse;width:100%;}th,td{border:1px solid #ddd;padding:8px;text-align:left;}th{background-color:#f2f2f2;}</style></head><body>
    ...    <h1>Admin Dashboard Report</h1>
    ...    <p><strong>Generated on:</strong> ${TIMESTAMP}</p>
    ...    <h2>Summary Statistics</h2>
    ...    <table>
    ...    <tr><th>Metric</th><th>Value</th></tr>
    ...    <tr><td>Total Complaints</td><td>${COMPLAINTS_DATA.__len__()}</td></tr>
    ...    </table>
    ...    <h2>Category Distribution</h2>
    ...    <table>
    ...    <tr><th>Category</th><th>Count</th></tr>
    
    FOR    ${category}    IN    @{CATEGORY_DATA}
        ${html}=    Set Variable    ${html}<tr><td>${category.category}</td><td>${category.count}</td></tr>
    END
    
    ${html}=    Set Variable    ${html}</table></body></html>
    [Return]    ${html}

Generate Summary Report
    [Documentation]    Generate text summary report
    ${summary_file}=    Set Variable    ${REPORT_FOLDER}/summary/report_summary_${TIMESTAMP}.txt
    
    ${content}=    Set Variable
    ...    ADMIN DASHBOARD REPORT SUMMARY\n
    ...    Generated on: ${TIMESTAMP}\n\n
    ...    SUMMARY STATISTICS:\n
    ...    - Total Complaints: ${COMPLAINTS_DATA.__len__()}\n\n
    ...    CATEGORY DISTRIBUTION:\n
    
    FOR    ${category}    IN    @{CATEGORY_DATA}
        ${content}=    Set Variable    ${content}- ${category.category}: ${category.count}\n
    END
    
    ${content}=    Set Variable    ${content}\nSTATUS DISTRIBUTION:\n
    
    FOR    ${status}    IN    @{STATUS_DATA}
        ${content}=    Set Variable    ${content}- ${status.status}: ${status.count}\n
    END
    
    Create File    ${summary_file}    ${content}
    Log    Summary report generated: ${summary_file} 