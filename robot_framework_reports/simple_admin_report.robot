*** Settings ***
Documentation     Simple Robot Framework script to generate admin dashboard reports
Library           SeleniumLibrary
Library           Collections
Library           DateTime
Library           String
Library           OperatingSystem
Library           docx_writer.py

*** Variables ***
${BASE_URL}       http://localhost:8000
${ADMIN_USERNAME}    aeron123456
${ADMIN_PASSWORD}    123456
${BROWSER}        chrome
${TIMEOUT}        10s

*** Test Cases ***
Generate Admin Dashboard Report
    [Documentation]    Generate dashboard-only admin report with chart images and data
    Open Browser And Login
    Extract Dashboard Statistics And Charts
    Generate Dashboard Report
    [Teardown]    Close All Browsers

*** Keywords ***
Open Browser And Login
    [Documentation]    Open browser and login to admin panel
    Open Browser    ${BASE_URL}/administrator/    ${BROWSER}
    Maximize Browser Window
    Sleep    2s
    Wait Until Element Is Visible    name=username    timeout=${TIMEOUT}
    Input Text    name=username    ${ADMIN_USERNAME}
    Input Password    name=password    ${ADMIN_PASSWORD}
    Click Button    Log in
    Sleep    3s
    Wait Until Element Is Visible    xpath=//h1[contains(text(),'Admin Dashboard')]    timeout=${TIMEOUT}
    Log    Successfully logged in to admin panel

Extract Dashboard Statistics And Charts
    [Documentation]    Extract visible dashboard data and capture chart images
    Sleep    3s
    ${heading}=    Get Text    xpath=//h1[contains(text(),'Admin Dashboard')]
    ${category_title}=    Get Text    xpath=//h2[contains(text(),'Category Distribution')]
    ${status_title}=    Get Text    xpath=//h2[contains(text(),'Status Distribution')]
    Set Suite Variable    ${heading}
    Set Suite Variable    ${category_title}
    Set Suite Variable    ${status_title}
    # Capture chart images
    Capture Element Screenshot    id=categoryPieChart    category_chart.png
    Capture Element Screenshot    id=statusPieChart      status_chart.png
    # Extract chart data from script tags (Django json_script)
    ${category_data}=    Get Element Attribute    xpath=//script[@id='category-data-json']    textContent
    ${status_data}=    Get Element Attribute    xpath=//script[@id='status-data-json']    textContent
    Set Suite Variable    ${category_data}
    Set Suite Variable    ${status_data}
    # List year levels and their corresponding canvas IDs
    ${year_levels}=    Create List    First Year    Second Year    Third Year    Fourth Year
    ${canvas_ids}=     Create List    monthlyChart1    monthlyChart2    monthlyChart3    monthlyChart4

    FOR    ${index}    IN RANGE    0    4
        Wait Until Element Is Visible    id=${canvas_ids[${index}]}    10s
        Sleep    1s
        Capture Element Screenshot    id=${canvas_ids[${index}]}    bar_graph_${index+1}.png
    END

Generate Dashboard Report
    [Documentation]    Fill template with dashboard data
    ${timestamp}=    Get Current Date    result_format=%Y-%m-%d_%H-%M-%S
    ${output_file}=    Set Variable    robot_framework_reports/admin_dashboard_report_${timestamp}.docx
    ${bar_graph_images}=    Create List    bar_graph_1.png    bar_graph_2.png    bar_graph_3.png    bar_graph_4.png
    ${year_level_names}=    Create List    First Year    Second Year    Third Year    Fourth Year
    Fill Report Template    robot_framework_reports/report.docx    ${output_file}    ${category_data}    ${status_data}    ${bar_graph_images}    ${year_level_names}
    Log    Word report saved to: ${output_file}
    Log    Chart images saved as category_chart.png, status_chart.png, and bar graphs (bar_graph_1.png, bar_graph_2.png, bar_graph_3.png, bar_graph_4.png) 