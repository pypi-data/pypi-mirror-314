"""
The component that uses LLM to analyze the data
"""

__all__=['TextAnalyzer']

import ast

from openai import OpenAI
import pandas as pd


class TextAnalyzer:
    def __init__(self, api_key):
        """
        Instantiates a TextAnalyzer object. Basically, connects to Openai API.
        Instead of directly using OpenaiAPI, we can use 'aisuite' package
        and try multiple LLM models.
        :param api_key: OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        print('**** Textanalyzer is connected to openai')
        #todo: add location in the input command.
        # In notes, add that two chargers with close locations can have better ranks.
        self.system_content = ("Act as an electric vehicle owner who wants to charge their EV based"
                               " on data provided for each EV charging station.\n\n# Steps\n\n1. Read "
                               "the input data that is provided for a number of EV charging stations."
                               "\n2. Assess each charging station's available data\n"
                               "3. Offer the rankings of given charging stations. "
                               "\n\n\n# Inupt\n\nThe input is formatted as a JSON file with key-value pairs."
                               " The key for each pair is the index of the entry, and the entry data is "
                               "the value of the pair."
                               "\nEach data entry has the following attributes for one EV charging station:"
                               "\n\"Review score\": "
                               "Average score of reviewers on Google Maps. If no review is submitted, "
                               "it is zero."
                               "\n\"Rating count\": Number of reviews submitted on Google Maps"
                               "\n\"Reviews\": shows user reviews on Google Maps with their writer Names "
                               "\n\"Travel_Time\": travel time from our current location to this entry in minutes"
                               "\n\n# Output Format"
                               "\n\nProvide a dictionary with same keys as the input and values show their ranking. "
                               "The value of each key is an integer between 1 and number of input EV charging stations."
                               " No two values should be identical. The lower the value, the more desirable the "
                               "corresponding EV charging station is.  "
                               "\n\n# Example"
                               "\ninput: "
                               "\n'{\"0\":{\"Review score\":0.0,\"Rating count\":0,\"Reviews\":\"[\\'No reviews found."
                               "\\']\",\"Travel_Time\":\"6 mins\"},\"1\":{\"Review score\":1.0,\"Rating count\":1,"
                               "\"Reviews\":\"[\\'William Gibbs: One star because ALL chargers at this location are out"
                               " of service (as of mid-May 2023)\\']\",\"Travel_Time\":\"7 mins\"},"
                               "\"2\":{\"Review score\":3.0,\"Rating count\":4,\"Reviews\":\"[\\'Benjamin Lin: "
                               "Charging here multiple times, no issue until today found a gas car occupied the spot "
                               "and there are plenty of open lots. I heard some people doing this on purpose. "
                               "I don\\\\u2019t know why?\\', \\'Nick Corcimiglia: Finally working! "
                               "Volta app is showing \\\\u201cunknown\\\\u201d status, station 02 is properly working."
                               " It\\\\u2019s FREE!!\\', \\'Eric and Laura Sager: One of the chargers at Safeway has "
                               "been removed, the other is non-functional\\', \\\\\"Mariann K. Smith: Charger at Safeway"
                               " parking lot doesn\\'t work.\\\\\"]\",\"Travel_Time\":\"4 mins\"}}"
                               "'\n\noutput:"
                               "\n'{0:2, 1:3, 2:1}'\nThis output means that the input with the index of 2 is "
                               "the first EV charging station to go. It makes sense because it has better travel time,"
                               " reviews, and review scores than other charging stations. On the other hand, index 1 "
                               "corresponds to the least desirable charging station where the travel time is greater"
                               " than other stations and it has only one negative review which is worse than having "
                               "no review at all (the case for the first charger).\n\n# Notes\n\n- The review score "
                               "for a station with a rating count of zero can be estimated as the average score of"
                               " all inputs with valid reviews.\n- a station with no review is better than a station"
                               " with only negative reviews and a very low review score.\n- if a station has many "
                               "reviews, the review score is more reliable than a station with only a few reviews. \n"
                               " \n- only output the suggestion dictionary, with no additional explanation.\n"
                               )

    def LLM_analyze(self, data:pd.DataFrame):
        """
        Gets recommendations from openAI API.
        :param data:
        :return: updated data with a new column 'LLM rank'. Best suggestion has a value of one under this column
        """
        cols = ['Location', 'Review score', 'Rating count', 'Reviews', 'Travel_Time']
        data_sliced = data[cols]
        json_data = data_sliced.to_json(orient='index')

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": [{"type": "text", "text": self.system_content}]},
                {"role": "user", "content": [{"type": "text", "text": json_data}]}
            ],
            temperature=0.05,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Parse response into a dictionary
        response = response.choices[0].message.content.strip()
        response = ast.literal_eval(response)
        data['LLM rank'] = data.index.map(response)
        return data







