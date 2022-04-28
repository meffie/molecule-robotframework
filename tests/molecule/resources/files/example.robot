| *** Settings ***   |
| Documentation      | Example using the pipe separated format.
| Resource           | example.resource

| *** Variables ***  |
| ${MESSAGE}         | Hello, world!

| *** Test Cases *** |                 |               |
| My Test            | [Documentation] | Example test. |
|                    | My Keyword      | ${MESSAGE}    | Hello, world!
