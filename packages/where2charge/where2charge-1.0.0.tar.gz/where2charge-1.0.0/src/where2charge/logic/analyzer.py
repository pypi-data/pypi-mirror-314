"""
this code will use all the data to suggest the best EV charging stations.
implemented using OOP
"""

__all__=['Analyzer']

from .text_analyzer import TextAnalyzer


class Analyzer:
    """
    an analyzer object, uses data collected from Google and other data sources
    to find the best charging station. To do this, it also uses the help of
    ChatGPT
    """
    def __init__(self, openai_key):
        self.text_analyzer = TextAnalyzer(openai_key)
        print('*** Analyzer is ready to run.')


    def get_suggestions(self, data, n_recomm, charger_type):
        """
        The main method for finding suggestions.
        all data must be passed to this method to be evaluated
        :param data: pandas DataFrame object
        :return: an ordered pd.Dataframe
        """
        print(f'Analyzer input: given data, n_recom:{n_recomm}, connector type: {charger_type}')  # log
        if charger_type is not None:
            data = data[data['EV Connector Types'].str.contains(charger_type)]
        else:
            pass
        # use text analyzer to get suggestions
        data = self.text_analyzer.LLM_analyze(data)
        # sort data
        data = data.sort_values(by='LLM rank').reset_index(drop=True)
        if n_recomm < len(data):
            return data.iloc[:n_recomm]
        else:
            return data
