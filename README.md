# football_league
A league creator

Just navigate to project directory and run command:

> uvicorn league:app --port 8080

Then you can send a POST request from any source to:

> localhost:8080/fixture/{number_of_teams_you_want}
