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
    Sleep    5s
    ${title}=    Get Title
    Log    Current page title: ${title}
    ${url}=    Get Location
    Log    Current URL: ${url}
    Capture Page Screenshot
    Wait Until Element Is Visible    xpath=//h1[contains(text(),'Admin Dashboard')]    timeout=20s
    Log    Successfully logged in to admin panel 