# where2charge
_Course project for 'CSE583 Software Development for Data Scientists' during the autumn 2024 quarter at the University of Washington._

_Team members: Arsalan Esmaili, Soheil Keshavarz_

## Description: 

`where2charge` is a platform that is aimed to suggest reliable charging station options to EV owners.

This repository contains four main components as below:
- User interface (app.py) 

- Server handler (server.py)

- Control logic (recommender.py)

- Unit tests 

More information on user requirements, component design, structure of this work, and future work
can be seen at `doc/README.md` and `doc/CSE583 where2charge presentation.pptx`



## How to use
This project can be used in three ways: as a web application, as an API, and as a python package. 

Before using our codes, you need to have:

1. A valid Google API key (https://developers.google.com/maps) with access to Places, Distance Matrix, 
and Directions APIs.
2. A valid OpenAI API key (https://platform.openai.com/api-keys)
### Streamlit based web app
1. Update `config.yaml` file with your api keys
```angular2html
GOOGLE_API_KEY: "your_google_api_key"
OpenAI_API_KEY: "your_openai_api_key"
```
2. run `src/main.py` from root directory of this repo.

![app screenshot](https://github.com/BlueSoheil99/where2charge/blob/main/doc/recording.gif?raw=true)

Please do not click or drag on the map when you see the message below on the app:
<img src="https://github.com/BlueSoheil99/where2charge/blob/main/doc/running_screenshot.png?raw=true" width=300>
### API
in case you want to use this work directly as an api instead of a UI, you can get connected to the server. 
Since this project is deployed on cloud yet, server address is you localhost. To run the server individually,
run `uvicorn src.server:app --reload --port {selected-port}` on terminal and on the root directory. Then open a browser and type `http://localhost:{selected-port}/docs
` in the address bar. `selected-port`, `8000` for example, is determined by the user.


![api_screenshot](https://github.com/BlueSoheil99/where2charge/blob/main/doc/api_screenshot.png?raw=true)
### a Python package

```angular2html
pip install where2charge
```
Sample code:
```angular2html
import where2charge

google_key = 'your_google_api_key'
openai_key = 'your_openai_api_key'

lat, lng = selected_latitude, selected_longitude
connector_type = 'Tesla'
number_of_suggestions = 3

recommender = where2charge.Recommender(google_key, openai_key)
suggestions = recommender.get_suggestions(lat, lng, number_of_suggestions, connector_type)
```