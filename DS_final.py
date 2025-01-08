#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 21:17:02 2024

@author: bridgetcrampton
"""

# import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the dataset
df = pd.read_csv('data_science_job.csv')


# Section 1: Average Salary Trends
# ----------------------------------
# Average Salary by Year
salary_trend = df.groupby('work_year')['salary_in_usd'].mean()
salary_trend_by_job = df.groupby(['work_year', 'job_category'])['salary_in_usd'].mean().unstack()  


plt.figure(figsize=(10, 6))
plt.plot(salary_trend.index, salary_trend, marker='o', label='Average Salary', color='blue')


# Plot the average salary by job category
for job_category in salary_trend_by_job.columns:
    plt.plot(salary_trend_by_job.index, salary_trend_by_job[job_category], marker='x', label=f'{job_category} Salary')


plt.title('Salary Trends Over Time by Job Category')
plt.xlabel('Year')
plt.ylabel('Salary (USD)')
plt.xticks([2020, 2021, 2022])
plt.legend(loc='best')
plt.grid()
plt.savefig('salary_trends_multiple_dimensions.png')
plt.show()


# Section 2: Salary Distributions
# ---------------------------------
# Distribution of salaries by year
sns.set(style='whitegrid')
plt.figure(figsize=(8, 5))
sns.boxplot(x='work_year', y='salary_in_usd', data=df)
plt.title('Salaries by Work Year', fontsize=14)
plt.xlabel('Work Year', fontsize=12)
plt.ylabel('Salary in USD', fontsize=12)
plt.savefig('salary_by_work_year_boxplot.png')
plt.show()

# Section 3: Filter Data by Experience Level
# -------------------------------------------
df_EN = df[df['experience_level'].isin(['EN'])]
df_SE = df[df['experience_level'].isin(['SE'])]
df_MI = df[df['experience_level'].isin(['MI'])]

# Section 4: Salary Distributions by Company Location
# ----------------------------------------------------
def plot_salary_distribution_by_location(data,title,filename):
    sns.set(style='whitegrid')
    plt.figure(figsize=(8,5))
    sns.boxplot(x = 'company_location', y = 'salary_in_usd', hue = 'company_location', data=data)
    plt.title(title, fontsize=14)
    plt.xlabel('Company Location', fontsize=12)
    plt.ylabel('Salary in USD', fontsize=12)
    plt.savefig(filename,bbox_inches = 'tight')
    plt.show()

plot_salary_distribution_by_location(df_EN, 'Salaries by Company Location (EN)', 'salaries_by_company_location_EN.png')
plot_salary_distribution_by_location(df_SE, 'Salaries by Company Location (SE)', 'salaries_by_company_location_SE.png')


# Section 5: Salary Distrubtion by Job Category
# ----------------------------------------------

def plot_salary_distribution_by_job_category(data, title, filename):
    sns.set(style='whitegrid')
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='salary_in_usd', y='job_category', hue='job_category', data=data)
    plt.title(title, fontsize=14)
    plt.xlabel('Salary in USD', fontsize=12)
    plt.ylabel('Job Category', fontsize=12)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

plot_salary_distribution_by_job_category(df_EN, 'Salaries by Job Category (EN)', 'salaries_by_job_category_EN.png')
plot_salary_distribution_by_job_category(df_SE, 'Salaries by Job Category (SE)', 'salaries_by_job_category_SE.png')


# Section 6: Salary by Job Title
# --------------------------------
salary_by_title = df_EN.groupby('job_title')['salary_in_usd'].mean().reset_index()
salary_by_title_sorted = salary_by_title.sort_values(by='salary_in_usd', ascending=False).reset_index(drop=True)

sns.barplot(x='salary_in_usd', y='job_title', data=salary_by_title_sorted, hue = 'job_title', palette='pastel', legend = False)
plt.title('Average Salary by Job Title (EN)')
plt.xlabel('Salary in USD')
plt.ylabel('Job Title')
plt.savefig('salaries_by_job_title_EN.png',bbox_inches = 'tight')
plt.show()

# Section 7: Wage Premium Calculations
# --------------------------------------
salary_by_title_EN = df_EN.groupby('job_title')['salary_in_usd'].mean().reset_index()
salary_by_title_MI = df_MI.groupby('job_title')['salary_in_usd'].mean().reset_index()
salary_by_title_SE = df_SE.groupby('job_title')['salary_in_usd'].mean().reset_index()

merged_salary = salary_by_title_EN.merge(salary_by_title_MI, on='job_title', how='outer', suffixes=('_EN', '_MI'))
merged_salary = merged_salary.merge(salary_by_title_SE, on='job_title', how='outer', suffixes=('', '_SE'))

print(merged_salary.head())
print()

merged_salary['wage_premium_MI'] = merged_salary['salary_in_usd_MI']/merged_salary['salary_in_usd_EN']
print(merged_salary.head())

# Bar Graph of Wage Premium (MI) by Job Title / difference between MI and EN Salary

merged_salary_sorted = merged_salary.sort_values(by='wage_premium_MI', ascending=False).reset_index(drop=True)

sns.barplot(x='wage_premium_MI', y='job_title', data=merged_salary_sorted, hue = 'job_title', palette='pastel', legend = False)
plt.title('Wage Premium (MI) by Job Title')
plt.xlabel('Wage Premium (MI)')
plt.ylabel('Job Title')

plt.savefig('wage_premium_MI_title_mean.png',bbox_inches = 'tight')
plt.show()

# Calculating Job Category Wage Premium

salary_by_category_EN = df_EN.groupby('job_category')['salary_in_usd'].median().reset_index()
salary_by_category_MI = df_MI.groupby('job_category')['salary_in_usd'].median().reset_index()
salary_by_category_SE = df_SE.groupby('job_category')['salary_in_usd'].median().reset_index()

merged_salary = salary_by_category_EN.merge(salary_by_category_MI, on='job_category', how='outer', suffixes=('_EN', '_MI'))
merged_salary = merged_salary.merge(salary_by_category_SE, on='job_category', how='outer', suffixes=('', '_SE'))

print(merged_salary.head())
print()

merged_salary['wage_premium_MI'] = merged_salary['salary_in_usd_MI']/merged_salary['salary_in_usd_EN']
print(merged_salary.head())

# Bar Graph of Wage Premium (MI) by Job Category / difference between MI and EN Salary

merged_salary_sorted = merged_salary.sort_values(by='wage_premium_MI', ascending=False).reset_index(drop=True)

sns.barplot(x='wage_premium_MI', y='job_category', data=merged_salary_sorted, hue = 'job_category', palette='pastel', legend = False)
plt.title('Wage Premium (MI) by Job Category')
plt.xlabel('Wage Premium (MI)')
plt.ylabel('Job Category')

plt.savefig('wage_premium_MI_category_median.png',bbox_inches = 'tight')
plt.show()

# Section 8: Job Category and Location Distributions
# ----------------------------------------------------
# Job category distribution
job_category_counts = df['job_category'].value_counts()
job_category_counts.plot(kind='pie', autopct='%1.1f%%', figsize=(6, 6), startangle=90, colors=plt.cm.Paired.colors)
plt.title('Job Category Distribution')
plt.ylabel('')  # Removes the default ylabel
plt.savefig("job_category_distribution.png") 
plt.show()


#Job location distribution


# Calculate the average salary in USD by job title
average_salary_by_job_title = df.groupby('job_title')['salary_in_usd'].mean()

# Display the results
print(average_salary_by_job_title)
average_salary_by_job_title = average_salary_by_job_title.sort_values(ascending=False)
print(average_salary_by_job_title)


#Job location distribution
employee_residence_counts = df['employee_residence'].value_counts()
employee_residence_counts.plot(kind='pie', autopct='%1.1f%%', figsize=(6, 6), startangle=90, colors=plt.cm.Paired.colors)
plt.title('Job Location Distribution')
plt.ylabel('')  # Removes the default ylabel
plt.savefig("employee_residence_coun.png") 
plt.show()
#This shows that Data Science jobs are most prominent in Japan, India, US and Denmark. 


"""
    Creates a custom graph based on user input.
    
    Parameters:
    - data: DataFrame containing the data.
    - x_column: Column name for the x-axis.
    - y_column: Column name for the y-axis (optional for some graphs).
    - graph_type: Type of graph to create ('boxplot', 'barplot', 'scatter', 'line').
    - figsize: Tuple specifying the figure size (width, height).
"""

# Section 9: Custom Graph Function
# ----------------------------------
def create_custom_graph(data, x_column, y_column, graph_type, fig_size=(10, 6)):   
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=fig_size)
    title = f"{graph_type.capitalize()} of {y_column} by {x_column}" 
    plt.title(title, fontsize=16)
    plt.xlabel(x_column.replace("_", " ").capitalize(), fontsize=14)
    plt.ylabel(y_column.replace("_", " ").capitalize(), fontsize=14)


    if graph_type == 'boxplot':
        sns.boxplot(data=data, x=x_column, y=y_column, palette="muted")
    elif graph_type == 'barplot':
        sns.barplot(data=data, x=x_column, y=y_column, palette="muted")
    elif graph_type == 'scatter':
        sns.scatterplot(data=data, x=x_column, y=y_column, palette="muted")
    elif graph_type == 'line':
        sns.lineplot(data=data, x=x_column, y=y_column, marker="o")
    else:
        raise ValueError(f"Unsupported graph type: {graph_type}")
        
    filename = f"{graph_type}_{x_column}_vs_{y_column}.png"
    plt.savefig(filename)
    print(f"Graph saved as: {filename}")
    plt.tight_layout()
    plt.show()

# Prompt user for custom graph
print("Instructions:")
print("1. For boxplots and barplots, choose categorical variables for the x-axis and numerical ones for the y-axis.")
print("2. For scatterplots and lineplots, choose numerical variables on both axes (e.g., 'work_year' vs 'salary_in_usd').")
print("3. The graph type should correspond to the kind of data you're working with.")

# User inputs for the x and y variables and graph type
x_column = input("Choose your x variable from: 'work_year', 'job_title', 'job_category', 'salary_currency', 'salary', 'salary_in_usd', 'employee_residence', 'experience_level', 'employment_type', 'work_setting', 'company_location', 'company_size' : ")
y_column = input("Choose your y variable from: 'work_year', 'job_title', 'job_category', 'salary_currency', 'salary', 'salary_in_usd', 'employee_residence', 'experience_level', 'employment_type', 'work_setting', 'company_location', 'company_size' : ")
graph_type = input("Enter the graph type ('boxplot', 'scatter', 'barplot', 'line'): ")

# Create the graph with the inputs
create_custom_graph(df, x_column, y_column, graph_type)



  