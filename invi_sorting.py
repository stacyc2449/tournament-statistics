import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# larger file was separated in smaller ones through Excel equations, 
# then read and converted into pandas dataframes to work with.
# Within each file, events were separated into separate cells
initial_diag = pd.read_csv("initial_diagnostic.csv")
rickards = pd.read_csv("rickards.csv")
boyceville = pd.read_csv("boyceville.csv")
regionals_diag = pd.read_csv("regionals_diagnostic.csv")
regionals = pd.read_csv("regionals.csv")
yuso = pd.read_csv("yuso.csv")
birdso = pd.read_csv("birdso.csv")
states = pd.read_csv("states.csv")

# Calculates the average and standard deviation of percentiles in each tournament
# Using stdev because the files contain the population
# takes in one of the tournament dataframes above (e.g. initial_diag, rickards, etc.) as a parameter
def tournament_distribution(tournament):
    placements = []
    for ind in range(len(tournament)):
        for num in range(len(tournament.columns) - 1):
            event = str(tournament.iloc[ind, num + 1])
            ranking = re.findall(r'[\d]*[.][\d]+|[\d]+', event)
            if '%' in event:
                ranking.append(100)
            if len(ranking) > 1:
                if "score" in event:
                    # converting given scores to be percentiles, though it may be slightly biased
                    ranking[0] = float(ranking[1]) - float(ranking[0])
                placements.append(1 - float(float(ranking[0]) / float(ranking[1])))
    # Commented out to be less problematic when running get_individual_stats(), but distribution of scores can be viewed by uncommenting this
    # plt.hist(placements)
    # plt.show() 
    return [np.mean(placements), np.std(placements)]

# These lists contain the avg and stdev of each tournament
initial_dist = tournament_distribution(initial_diag)
rickards_dist = tournament_distribution(rickards)
boyceville_dist = tournament_distribution(boyceville)
regionalsdiag_dist = tournament_distribution(regionals_diag)
regionals_dist = tournament_distribution(regionals)
yuso_dist = tournament_distribution(yuso)
birdso_dist = tournament_distribution(birdso)
states_dist = tournament_distribution(states)


# Calculates team performance breakdown.
# Calculates team averages in different subjects, and "strategies"
# Subjects: Biology, Build, Chemistry & Inquiry, Earth Science, and Math & Physics
# "Strategies": Biology w/ cheatsheet (A&P, DD, Ecology, MM); ID (Forestry, Fossils); Lab (Chem Lab, Forensics); Earthsci w/ calculations (Astro, GM); Earthsci w/ cheatsheet (DP); No cheatsheet math (CB, Fermi); Math w/ build (DB, Optics, WP); Inquiry (Experimental Design, WIDI); Impounded build (Air trajectory, Scrambler, Robot Tour); Nonimpounded build (Flight, Towers)
# Applies better for one-team tournaments, but for some there was not enough information about what team they were on
# Returns average rankings based on type of event, and displayed in bar graph
# Takes in a tournament dataframe (e.g. rickards, boyceville, etc)
def team_breakdown(tournament):
    bio_rank, math_rank, earth_rank, chem_rank, build_rank =([] for i in range(5))
    bio_strat, id_strat, earthmath_strat, earth_strat, lab_strat, math_strat, eng_strat, inq_strat, impound_strat, nonimpound_strat = ([] for i in range(10))
    for ind in range(len(tournament)):
        for num in range(len(tournament.columns) - 1):
            event = str(tournament.iloc[ind, num + 1]).casefold()
            ranking = re.findall(r'[\d]*[.][\d]+|[\d]+', event)
            if len(ranking) > 1:
                if '%' in event:
                    ranking.append[100]
                if "score" in event:
                    ranking[0] = float(ranking[1]) - float(ranking[0])
                percentile = 1 - float(ranking[0]) / float(ranking[1])
                match event:
                    case event if "trajectory" in event:
                        build_rank.append(percentile)
                        impound_strat.append(percentile)
                    case event if "anatomy" in event:
                        bio_rank.append(percentile)
                        bio_strat.append(percentile)
                    case event if "astronomy" in event:
                        earth_rank.append(percentile)
                        earthmath_strat.append(percentile)
                    case event if "chemistry" in event:
                        chem_rank.append(percentile)
                        lab_strat.append(percentile)
                    case event if "codebusters" in event:
                        math_rank.append(percentile)
                        math_strat.append(percentile)
                    case event if "detector" in event:
                        math_rank.append(percentile)
                        eng_strat.append(percentile)
                    case event if "disease" in event:
                        bio_rank.append(percentile)
                        bio_strat.append(percentile)
                    case event if "dynamic" in event:
                        earth_rank.append(percentile)
                        earth_strat.append(percentile)
                    case event if "ecology" in event:
                        bio_rank.append(percentile)
                        bio_strat.append(percentile)
                    case event if "experimental" in event:
                        chem_rank.append(percentile)
                        inq_strat.append(percentile)
                    case event if "fermi" in event:
                        chem_rank.append(percentile)
                        math_strat.append(percentile)
                    case event if "flight" in event:
                        build_rank.append(percentile)
                        nonimpound_strat.append(percentile)
                    case event if "forensics" in event:
                        chem_rank.append(percentile)
                        lab_strat.append(percentile)
                    case event if "forestry" in event:
                        bio_rank.append(percentile)
                        id_strat.append(percentile)
                    case event if "fossils" in event:
                        earth_rank.append(percentile)
                        id_strat.append(percentile)
                    case event if "geologic" in event:
                        earth_rank.append(percentile)
                        earthmath_strat.append(percentile)
                    case event if "microbe" in event:
                        bio_rank.append(percentile)
                        bio_strat.append(percentile)
                    case event if "optics" in event:
                        math_rank.append(percentile)
                        eng_strat.append(percentile)
                    case event if "robot" in event:
                        build_rank.append(percentile)
                        impound_strat.append(percentile)
                    case event if "scrambler" in event:
                        build_rank.append(percentile)
                        impound_strat.append(percentile)
                    case event if "tower" in event:
                        build_rank.append(percentile)
                        nonimpound_strat.append(percentile)
                    case event if "wind" in event:
                        math_rank.append(percentile)
                        eng_strat.append(percentile)
                    case event if "write" in event:
                        chem_rank.append(percentile)
                        inq_strat.append(percentile)
                    case _:
                        continue
    rank = plt.subplot()
    strat = plt.subplot()
    avg_ranks = [np.mean(bio_rank), np.mean(chem_rank), np.mean(earth_rank), np.mean(math_rank), np.mean(build_rank)]
    avg_strat = [np.mean(bio_strat), np.mean(id_strat), np.mean(lab_strat), np.mean(earthmath_strat), np.mean(earth_strat), np.mean(math_strat), np.mean(eng_strat), np.mean(inq_strat), np.mean(impound_strat), np.mean(nonimpound_strat)]
    rank_names = ["Biology", "Chemistry & Inquiry", "Earth Science", "Math & Physics", "Build"]
    strat_names = ["Bio w/ Cheatsheet", "ID", "Lab", "Earth Sci w/ Calculations", "Earth Sci w/ Cheatsheet", "Math w/o Cheatsheet", "Math w/ Build", "Inquiry", "Impounded Build", "Non-Impounded Build"]
    rank.bar(rank_names, avg_ranks, label="Subjects")
    strat.bar(strat_names, avg_strat, label="Strategies")
    plt.show()

# Provide member number, get statistics from them
# Percentiles are relative to the placements of other members on the team 
# (e.g. 90th percentile is above 90% of the placements obtained by members on the team)
# Used a normal distribution to obtain percentiles, though that can be changed

# Prints out the average percentile for each event, the standard dev of percentile for each event, linear regression slope (to show improvement over time), and the number of times they've competed in each event
# Linear Regression slope of "nan" means that there is not enough data available, e.g. member only participated in that event once
# Also displays a graph, showing events and the percentile changes over time
# Note that the graph does not display events that members have only participated in once
# Takes in a number corresponding to the member's name
def get_individual_stats(member):
    member -= 1 #offset by 1 in the csv files

    i = 0 #iterative variable, for linear regression x axis. Supposed to be time, so an approximation that all tournaments were about evenly spaced apart
    event_list = []
    percentiles_list = []
    lin_regress_x = []
    comp = [initial_diag.iloc[member], rickards.iloc[member], boyceville.iloc[member], regionals_diag.iloc[member], regionals.iloc[member], yuso.iloc[member], birdso.iloc[member], states.iloc[member]]
    distributions = [initial_dist, rickards_dist, boyceville_dist, regionalsdiag_dist, regionals_dist, yuso_dist, birdso_dist, states_dist]
    for tourn in comp:
        for event in tourn:
            eventname = re.sub(r'[0-9]+|[/]|[*]|[.]', '', str(event))
            ranking = re.findall(r'[\d]*[.][\d]+|[\d]+', str(event))
            if '%' in eventname:
                ranking.append(100)
                eventname = re.sub('%', '', eventname)
            if "score" in eventname:
                ranking[0] = int(float(ranking[1])) - int(float(ranking[0]))
            eventname = re.sub("(rank)|(score)|[()]", '', str(eventname))
            eventname = eventname.strip()
            if len(ranking) > 1:
                percentile = 1 - float(ranking[0]) / float(ranking[1])
                z_score = (percentile - distributions[i][0]) / distributions[i][1]
                norm_percentile = stats.norm.cdf(z_score)
                if eventname.casefold() not in event_list and len(eventname) > 4: 
                    event_list.append(eventname.casefold())
                    percentiles_list.append([norm_percentile])
                    lin_regress_x.append([i])
                elif eventname.casefold() in event_list:
                    index = event_list.index(eventname.casefold())
                    percentiles_list[index].append(norm_percentile)
                    lin_regress_x[index].append(i)
        i = i + 1
    averaged_percentiles = []
    print(f'Name: {member + 1}')
    for event in range(len(percentiles_list)):
        lin_reg = 0
        if len(percentiles_list[event]) > 1:
            lin_regress = stats.linregress(lin_regress_x[event], percentiles_list[event])
            lin_reg = lin_regress.slope
        averaged_percentiles.append([np.mean(percentiles_list[event]), np.std(percentiles_list[event])])
        print(f'Event: {event_list[event].capitalize()}\nAverage Percentile: {averaged_percentiles[event][0]}; \nStandard Deviation: {averaged_percentiles[event][1]}; \nLinear Regression Slope: {lin_reg}\nNumber of times competed: {len(percentiles_list[event])}')
        plt.plot(lin_regress_x[event], percentiles_list[event], label=event_list[event])
    plt.legend(loc='best')
    plt.title("Member" + str(member+1))
    plt.show()

#### RUN CODE HERE ####
# Example:
for i in range(3):
    get_individual_stats(i+1)
    


        