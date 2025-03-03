# Data Collector and Player Ranker for "Super Smash Brothers Ultimate" Tournaments
Within the community of Super Smash Brothers, ranking of players through tournament data is a regular occurence on multiple scales such as the state level, country level, or even a world-wide level. Despite ranking being a frequent activity, a lot of manual labor in data aggregation and organization is performed with a lack of a software-based framework to speed up and automate the process. This tool aims to be just that by querying the database of the standard tournament hosting website, start.gg. Once these events are queried, every participating player and their matches played are processed and stored in a manner that is easily digestible for a ranker to use manually, or do further computational processing. An example of this further computation is provided, being the creation of a player ranking within Northern California over the span of 3 months.

## queries.py
This contains all of the necesarry API queries, and the functions that use them, in order to properly retreive data in accordance with rate limits. These queries include getting the unique IDs of each event, retrieving every set (the unit of game used in tournaments) within an event, and getting the participants and score of a given set.

## processing.py
This file contains methods revolving around both the flow of incoming queries and also what to do with the data after it is queried. This concerns 2 main actions: creating and initializing 2D arrays that contains the set and game records for every combination of players (a set can consist of anywhere between 2 and 5 games), and also maintaining an ELO ranking based off of this data.

## the_project.py (rename this to something else)
A lightweight example usage of the general pipeline to be employed

## pr-generator.ipynb
A more robust example usage that includes lots of extra post-processing that is used to generate the Nothern California player rankings. Extra functionality includes automatic tournament link scraping based off of location, extracting "notable" wins and losses for given players (based off of rankings), and a more robust AI produced ranking using agentic reasoning. Eventually, this pipeline will be available to anyone who wants to create their own ranking whether it be for their state, country, or even worldwide.