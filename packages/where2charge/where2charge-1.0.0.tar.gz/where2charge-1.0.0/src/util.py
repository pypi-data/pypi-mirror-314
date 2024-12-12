""" this file holds general functions that can be used by multiple files"""
import yaml


def read_config(file_path:str ='config.yaml')-> dict:
    """
    This function reads a yaml file which contains configuration details
    :param file_path:  path to the yaml file
    :return: dictionary with configuration details
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config
