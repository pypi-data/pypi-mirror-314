# where2charge
This document explains user stories and component design behind this project




## User stories:


- Suzi is an EV owner. She wants to charge her car every morning before
 showing up at work. She wants to use this tool to quickly navigate herself
 to an available charging station in middle of her commute route. 

- Brandon: Brandon is an EV owner who wants to look at different charging stations on the map and review their main attributes of reliability. Specifically, he wants to understand their reviews in just few words.

- Susan: Susan is an EV owner who wants to drive to a shopping mall with a EV charger close to her. She wants to get the best suggestion based on the location she wants to go. 

- Leo: Leo is a researcher who wants to analyse trip information of the users (anonymous), and check differences between travel time and see how travel time would be different based on different attributes and investigate equity.

- Joe is an employee in SDOT. He want to see number of EV trips from each traffic analysis zone (TAZ) to better understand the generated demand. He wants to see a summary and a csv file for trips generated. 

- Dave is the system admin. He wants to communicate with app users. He needs a specific interface where he
can see each user usage, subscription, feedbacks, etc., and send notification to all or a group of users.

- Rob is a hacker. He wants to access location information of users. 
He made a bot to decode admin credentials. 

* The user's data in this app should be encrypted and the location information needs to be masked in
 a more aggregated level.
This will be clearly indicated to users. 
The application should assure users that there is no way for use of their accurate information and all analysis will be used anonymously.
 This is necessary to meet the criteria for data ethics.


## Components:

1. User interface (app.py)
- Gets the input from the user and provide the requested task and visualize them. The main goal is to provide user-friendly 
environment for EV riders to be able to benefit from the provided analysis.
- Input: Type of plug, origin/destination locations, and other user preferences for selecting EV charging station
- Output: Visualization of the suggested route and their differences (e.g., review summary, time, distance, etc.)
- It should be connected to the control logic and get instructinos, including map, from it.
- side effects: 

2. Server handler (server.py)
- runs the server and gets connected to the user and establishes a connection between user and the logic. Also, it encapsulates the logic package and makes an API.
- input comes from the UI and output comes from the recommendation system
- bridges the gap between the backend and the frontend

3. Control logic (recommender.py)
- It provides the calculation of the input data for the interface.
- The input is one to multiple origin/destination locations that user specifies, type of plugs and other preferences that user determine.
- Time, distance, and other trip components for the suggested routes.
- It uses user navigation system, database, analysis component
- Side effect: risk of data leakage, crashing risk as it need to handle multiple users, it needs maintenance
- it has the following four components:


     3.1. geographic information collector (googleAPI_handler.py)
     - It provides EV charging station locations, their details and reviews, and routes
     - The input is user address and the output is possible options for EV charging
     - It is called by the control logic

     3.2. Database (data_handler.py)
     - download the data, clean and merge them to have necessary variables for analysis
     - This will include getting EV charging station dataset and merging supplementary datasets such as EV registration, socio demographics, etc.
     - It is called by the control logic

     3.3. analysis component (analyzer.py)
     - Gets the information from database and geographic information collector and analyze them to allocate a score to each charging alternative.
     - It sorts the scores and mark the one with the most appropriate score.
     - It is called by the control logic 

     3.4. LLM component (text_analyzer.py)
     - Gets all the processed data from analyzer object to perform additional analysis on data using strength of Large Language Models (LLM).
     - It is called by the analyzer object

4. Test directory
- Files in this directory will test logic components.
- These tests include smoke test, one-shot test, edge test, and logic test.


### here is the tree of this project:
```
where2charge
|--doc dir
|--src dir
|--|--app.py
|--|--config.yaml         # includes app and server ports as well as API keys
|--|--main.py             # runs app.py and server.py and connects them
|--|--server.py           # before responding to client, establishes a connection with recommender.py
|--|--where2charge dir 
|--|--|--logic dir        # contains .py files imported by recommender.py
|--|--|--recommender.py   
|--test dir               # inclueds unit tests
|--environment.yml        # can be used to make a conda environment
|--pyproject.toml         # used to create a package
|--LICENCE
|--README.md
```