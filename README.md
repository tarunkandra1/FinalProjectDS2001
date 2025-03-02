# NFL Data Analysis Project

## Overview
This project analyzes NFL game results and team statistics to derive insights into team performance, specifically focusing on offensive and defensive ratings, net ratings, and the correlation between different statistical categories. The analysis is performed using Python, with libraries such as `pandas`, `numpy`, `scikit-learn`, `matplotlib`, and `seaborn`. The goal is to find out which factors have a high impact on the amount of wins a team gets and create a semi-accurate, unbiased rating system of the teams.

## Project Structure
The project is structured around several key functions that perform specific tasks:

1. **Data Loading and Preprocessing**:
   - The project starts by loading NFL game results and team statistics from CSV files.
   - The data is cleaned and preprocessed to remove unnecessary rows and columns.

2. **Team Wins Calculation**:
   - The `team_wins` function calculates the number of wins and losses for each team over a specified period.

3. **Defensive and Offensive Rating Calculation**:
   - The `rate_teamD` and `rate_teamO` functions calculate defensive and offensive ratings for each team based on yards allowed, points allowed, and turnover percentages.
   - These ratings are adjusted against league averages to provide a relative performance metric.

4. **Net Rating Calculation**:
   - The `net_rating` function calculates the net rating for each team by averaging the defensive and offensive ratings.

5. **Factor Analysis**:
   - The `graph_corr` function generates scatter plots with regression lines to visualize the correlation between different statistical categories (e.g., total yards vs. points allowed).
   - It also calculates and returns the correlation coefficient if requested.

6. **Mean Yards Calculation**:
   - The `mean_yardsW` and `mean_yardsL` functions calculate the mean yards gained in wins and losses, respectively.
