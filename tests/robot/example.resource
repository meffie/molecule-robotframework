| *** Settings ***   |
| Documentation      |  An example resource file

| *** Variables ***  |
| ${HOST}            | www.example.com

| *** Keywords ***   |                        |         |
| My Keyword         | [Arguments]            | ${path} |
|                    | Directory Should Exist | ${path} |
