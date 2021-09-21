import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 14100)
pd.set_option('display.width', 1000)
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import dateutil
import warnings

warnings.filterwarnings("ignore")
import plotly.express as px

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import math

#Data Import, Preprocessing
covid_data = pd.read_csv(r"C:\Users\aruna\OneDrive\Desktop\UCD_Project_Final\UCDPA_Aruna\data.csv")
# print (covid_data)

print (covid_data.shape)   #number of rows and columns in this dataset
covid_data.info()         # print columns names and dataType.There's no null value in this dataset

#Since the dateRep is in object will convert this to datetime
covid_data["dateRep"] = pd.to_datetime(covid_data["dateRep"])
print (covid_data.dtypes)

print (covid_data.describe())      #key feature in this dataset

# # Heatmap
# plt.figure(figsize=(10,8))
# sns.heatmap(data = covid_data.corr(), annot = True, cmap = 'inferno')
# plt.show()

covid_data["countriesAndTerritories"].unique()  #list of all countries in EU

#data_date = covid_data.groupby("dateRep", as_index=False).cases.max()
data_date = covid_data.groupby('dateRep').sum()['cases'].reset_index()  #creating a dataframe to see number of cases based on the date reported

data_date['dateRep'] = pd.to_datetime(data_date['dateRep'])
print (data_date)
# ----------------

# finding number of Cases in EU
group_eu = covid_data.groupby('countriesAndTerritories')['cases', 'deaths'].sum().reset_index()  # Using groupby to display the sum of cases.deaths in EU
print (group_eu)
#

# #Plotline cases based on date reported
plt.figure(figsize=(17,20))
sns.lineplot(x=data_date['dateRep'], y=data_date['cases'])
plt.title("No of Reported Cases Based On Date Reported.")
plt.xticks(rotation=45)
plt.show()
#

# #Covid cases based on countries"
covid_data['cases']=covid_data.groupby('countriesAndTerritories').cases.tail(1)
x=covid_data.groupby('countriesAndTerritories')['cases'].mean().sort_values(ascending=False)
plt.figure(figsize=(10,8))
ax=sns.barplot(x.values,x.index)
ax.set_xlabel("Covid cases based on countries")
ax.set_ylabel("countriesAndTerritories")
plt.show()
#

# #Top 5 reported cases by countries
countries = covid_data.groupby('countriesAndTerritories')['cases'].max().sort_values(ascending= False)[:5].index
top_countries = pd.DataFrame(columns=covid_data.columns)
for country in countries:
  top_countries = top_countries.append(covid_data.loc[covid_data['countriesAndTerritories'] == country])
print (top_countries.sort_values(by="dateRep"))
#

# using plt line to display the countries
plt.figure(figsize=(15,8))
sns.lineplot(top_countries['dateRep'],
             top_countries['cases'],
             hue = top_countries['countriesAndTerritories'], ci= False)
plt.title("Top cases based on countries in Europe");
plt.show()
#

#Map of EU - covid cases
fig = px.choropleth(group_eu, locations="countriesAndTerritories",
                    locationmode='country names', color="cases", scope='europe',
                    hover_name="countriesAndTerritories", range_color=[1,8777999],height=800, width=750,
                    color_continuous_scale="sunset",
                    title='Cases Reported in EU')

fig.show()

#
# Finding Ratio Cases over Population
#data_population = covid_data.groupby("countriesAndTerritories")[['popData2020','cases', 'deaths']].sum().reset_index()
data_population= covid_data.groupby(['popData2020', 'countriesAndTerritories'])['cases','deaths'].sum().reset_index()
data_population.sort_values('popData2020', ascending=True)

#Calculate Ratio Cases over Population
data_cases = covid_data.groupby("countriesAndTerritories", as_index=False).cases.sum()

ratio = data_cases["cases"]/data_population["popData2020"] * 1000
ratio

data_cases ["Ratio"] = ratio
data_cases


# Top 20 Ratio Cases over Population
data_top20 = data_cases.sort_values(by="Ratio", ascending=True)
data_top20 = data_top20.head(20)

plt.figure(figsize=(10,10))
sns.barplot(x=data_top20["countriesAndTerritories"], y=data_top20["Ratio"])
plt.title("Ratio of cases over population")
plt.xticks(rotation=90)
plt.show()






# #Covid:Deaths reported in EU
data_death=covid_data.groupby("countriesAndTerritories")[['deaths']].sum().reset_index()
#print (data_death)

plt.figure(figsize=(15,40))
sns.barplot(x=data_death["countriesAndTerritories"], y=data_death["deaths"])
plt.yticks(size=10)
plt.xticks(size=20)
plt.title("Death cases in Europe");
plt.xticks(rotation=90)
plt.show()
#

# #Top 20 Deaths
death = data_death.sort_values(by="deaths", ascending=False)       # Creating a dataframe of top 20 countries.
death_top20 = death.head(20)
death_top20
#
plt.figure(figsize=(10,5))
sns.barplot(x=death_top20["deaths"], y=death_top20["countriesAndTerritories"])
plt.title("Top 20 countries with the most death cases")
plt.show()
#

# Covid 19 :EU Visualize Timeseries ()
group_eu1 = covid_data.groupby(['dateRep', 'countriesAndTerritories'])['cases','deaths'].sum().reset_index()
#group_eu1['dateRep'] = pd.to_datetime(covid_data['dateRep'])
group_eu1 = covid_data.sort_values('dateRep', ascending=True)
group_eu1['dateRep'] = group_eu1['dateRep'].dt.strftime('%m-%d-%Y')
#group_eu1['dateRep'] = group_eu1['dateRep'].dt.strftime('%Y-%m-%d')
#
eu_copy = group_eu1.copy()
fig = px.scatter_geo(eu_copy, locations="countriesAndTerritories", locationmode='country names',
                     color="cases", hover_data=["countriesAndTerritories",'deaths'],
                     range_color= [0, 2000],
                     projection="natural earth", animation_frame="dateRep", scope="europe",
                     title='COVID-19: Cases and Deaths Over Time in Europe', color_continuous_scale="spectral", height=750)
fig.show()
#
#
#



#Covid19 - Ireland
data_Ireland=covid_data[(covid_data['countriesAndTerritories'] == "Ireland")][['countriesAndTerritories', 'dateRep', 'cases', 'deaths']].sort_values('dateRep', ascending=True)
data_Ireland['dateRep'] = data_Ireland['dateRep'].dt.strftime('%m-%d-%Y')

data_Ireland.info()
#print(data_Ireland)

#Cases Reported in Ireland
Ireland_cases = data_Ireland['cases'].groupby(data_Ireland['dateRep']).sum().sort_values(ascending=True)
#print(Ireland_cases)

#Cases In Irelnas based in date reported
plt.figure(figsize=(15,13))
sns.lineplot(x=data_Ireland.dateRep, y=data_Ireland.cases)
plt.xlabel("dateRep")
plt.ylabel("cases")
plt.title('Daily cases in Ireland');
plt.show()

#

# Death Reported in Ireland
Ireland_deaths = data_Ireland['deaths'].groupby(data_Ireland['dateRep']).sum().sort_values(ascending=True)
print(Ireland_deaths)

plt.figure(figsize=(15,13))
sns.lineplot(x=data_Ireland.dateRep, y=data_Ireland.deaths)
plt.xlabel("dateRep")
plt.ylabel("deaths")
plt.title('Daily Deaths in Ireland');
plt.show()
#

# Covid 19 Ire: Cases & Deaths
fig = go.Figure()
fig.add_trace(go.Scatter(x=data_Ireland['dateRep'],
                         y=data_Ireland['cases'],
                         mode='lines+markers',
                         name='Cases',
                         line=dict(color='blue', width=2)
                        ))
fig.add_trace(go.Scatter(x=data_Ireland['dateRep'],
                         y=data_Ireland['deaths'],
                         mode='lines+markers',
                         name='Deaths',
                         line=dict(color='Red', width=2)
                        ))

fig.update_layout(
    title=' Covid-19 Ireland - Cases And Deaths ',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    )
)
fig.show()
#



# reland mortality_over_time
mortality_over_time = round((Ireland_cases / Ireland_deaths) * 100, 2)

index = mortality_over_time.index
data = mortality_over_time

fig = go.Figure(data=[

    go.Line(name='Mortality in %'
    ,x=index
    ,y=data
    ,mode="lines+markers")

])

fig['layout'].update(
    title="Covid-19:Ireland Mortality rate over the time"
    , title_x=0.5
    , xaxis_title='month'
    , yaxis_title='Mortality rate (deaths/cases) in Percentage'
)

fig.show()

#

#Spain mortality
data_Spain=covid_data[(covid_data['countriesAndTerritories'] == "Spain")][['countriesAndTerritories', 'dateRep', 'cases', 'deaths']].sort_values('dateRep', ascending=True)
data_Spain['dateRep'] = data_Spain['dateRep'].dt.strftime('%m-%d-%Y')
Spain_cases = data_Spain['cases'].groupby(data_Spain['dateRep']).sum().sort_values(ascending=True)
Spain_deaths = data_Spain['deaths'].groupby(data_Spain['dateRep']).sum().sort_values(ascending=True)

mortality_over_time = round((Spain_cases / Spain_deaths) * 100, 2)

index = mortality_over_time.index
data = mortality_over_time

fig = go.Figure(data=[

    go.Line(name='Mortality in %'
    ,x=index
    ,y=data
    ,mode="lines+markers")

])

fig['layout'].update(
    title="Covid 19: Spain Mortality rate over the time"
    , title_x=0.5
    , xaxis_title='month'
    , yaxis_title='Spain - Mortality rate (deaths/cases) in Percentage')

fig.show()

#
# #Covid 19: Ireland and Spain Cases
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{}, {}],
           [{"colspan": 2}, None]],
    subplot_titles=("Ireland", "Spain"))

fig.add_trace(go.Scatter(x=data_Ireland['dateRep'], y=data_Ireland['cases'],
                    marker=dict(color=data_Ireland['cases'], coloraxis="coloraxis")),
              1, 1)

fig.add_trace(go.Scatter(x=data_Spain['dateRep'], y=data_Spain['cases'],
                    marker=dict(color=data_Spain['cases'], coloraxis="coloraxis")),
              1, 2)

#Covid 19: Ireland and Spain Deaths
fig.update_layout(coloraxis=dict(colorscale='RdBu'), showlegend=False,title_text="Trend of Covid-19 Cases In Ireland and Spain ")
fig.update_layout(plot_bgcolor='rgb(254,224,144)')
fig.show()

#Covid 19: Ireland and Spain Cases
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{}, {}],
           [{"colspan": 2}, None]],
    subplot_titles=("Ireland", "Spain"))

fig.add_trace(go.Scatter(x=data_Ireland['dateRep'], y=data_Ireland['deaths'],
                    marker=dict(color=data_Ireland['deaths'], coloraxis="coloraxis")),
              1, 1)

fig.add_trace(go.Scatter(x=data_Spain['dateRep'], y=data_Spain['deaths'],
                    marker=dict(color=data_Spain['deaths'], coloraxis="coloraxis")),
              1, 2)


fig.update_layout(coloraxis=dict(colorscale='RdBu'), showlegend=False,title_text="Trend of Covid-19 Deaths in Ireland and Spain")
fig.update_layout(plot_bgcolor='rgb(253,174,97)')
fig.show()
