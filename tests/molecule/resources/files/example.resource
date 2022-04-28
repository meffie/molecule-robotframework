| *** Settings ***   |
| Documentation      | Example resource file

| *** Keywords   *** |
| My Keyword         | [Arguments]     | ${a} | ${b}
|                    | Should Be Equal | ${a} | ${b}
