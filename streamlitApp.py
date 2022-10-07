import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from readExcelFiles import *

st.set_page_config(layout="wide")
col8, col9, col10 = st.columns([1, 5, 1])
col9.title('PCOC Shifts Data Visualization')


# Creating a new data frame filtered by employee name
def create_employee_df(employee_name, df):
    employee_df = df.loc[df['employee'] == employee_name]
    return employee_df


# Calculating weekend shifts
def weekend_counts(employee_df):
    saturdays_df = employee_df.loc[employee_df['day'] == 'Saturday']
    fridays_df = employee_df.loc[employee_df['day'] == 'Friday']
    weekend_df = pd.concat([fridays_df, saturdays_df])
    return weekend_df


# Calculating morning evening and night shifts
def morning_counts(employee_df):
    morning_df = employee_df.loc[employee_df['hours'] == '09:00 - 17:00']
    return morning_df


def eve_counts(employee_df):
    eve_df = employee_df.loc[employee_df['hours'] == '17:00 - 01:00']
    return eve_df


def night_counts(employee_df):
    night_df = employee_df.loc[employee_df['hours'] == '01:00 - 09:00']
    return night_df


def get_employees(mdf):
    working_employees = []
    for x in range(len(mdf)):
        e = (mdf.loc[x, "employee"])
        if e not in working_employees:
            working_employees.append(e)
    return working_employees


# getting a list of monthly dataframes from a specific directory that contains all excel sheets
monthly_df_list = get_monthly_df()


def plot_monthly_stats(filename):
    primary_df = monthly_df_list[filename]
    # returns a list of employees working this month
    employees = get_employees(primary_df)
    employee_df_list = []
    for i in range(len(employees)):
        employee_df_list.append(create_employee_df(employees[i], primary_df))

    # Visualizing the data with matplotlib

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    fig5, ax5 = plt.subplots()
    fig6, ax6 = plt.subplots()

    # plot morning shifts distribution
    morning_count = []
    for i in range(len(employees)):
        count = morning_counts(employee_df_list[i]).shape[0]
        morning_count.append(count)
        ax1.text(i - 0.075, count + 0.075, count)
    ax1.bar(employees, morning_count)

    # plot eve shifts distribution
    evening_counts = []
    for i in range(len(employees)):
        count = eve_counts(employee_df_list[i]).shape[0]
        evening_counts.append(count)
        ax2.text(i - 0.075, count + 0.075, count)
    ax2.bar(employees, evening_counts)

    # plot night shifts distribution
    night_count = []
    for i in range(len(employees)):
        count = night_counts(employee_df_list[i]).shape[0]
        night_count.append(count)
        ax3.text(i - 0.075, count + 0.075, count)
    ax3.bar(employees, night_count)

    # plot weekend shifts distribution
    weekend_shift_counts = []
    for i in range(len(employees)):
        count = weekend_counts(employee_df_list[i]).shape[0]
        weekend_shift_counts.append(count)
        ax4.text(i - 0.075, count + 0.045, count)
    ax4.bar(employees, weekend_shift_counts)

    # plot all employees shift count
    shift_counts = []
    for i in range(len(employees)):
        count = employee_df_list[i].shape[0]
        shift_counts.append(count)
        ax5.text(i - 0.075, count + 0.075, count)
    ax5.bar(employees, shift_counts)

    # plot all employees salaries
    salaries = []
    max_salary = 0
    for i in range(len(employees)):
        count = employee_df_list[i].shape[0] * 8 * 80
        if count > max_salary:
            max_salary = count
            highest_paid = employees[i]
        salaries.append(count)
        ax6.text(i - 0.25, count + 75, count)

    ax6.bar(employees, salaries)

    # setting plots labels and titles
    fig1.suptitle(filename.split()[1] + " " + filename.split()[2])
    fig2.suptitle(filename.split()[1] + " " + filename.split()[2])
    fig3.suptitle(filename.split()[1] + " " + filename.split()[2])
    fig4.suptitle(filename.split()[1] + " " + filename.split()[2])
    fig5.suptitle(filename.split()[1] + " " + filename.split()[2])
    fig6.suptitle(filename.split()[1] + " " + filename.split()[2])

    ax1.set_title('Morning Shifts distribution')
    ax2.set_title('evening Shifts distribution')
    ax3.set_title('night Shifts distribution')
    ax4.set_title('weekend Shifts distribution')
    ax5.set_title('genral Shifts distribution')
    ax6.set_title('Expected salaries')

    for label in ax1.get_xticklabels() + ax2.get_xticklabels() + ax3.get_xticklabels() + ax4.get_xticklabels() + ax5.get_xticklabels() + ax6.get_xticklabels():
        label.set_rotation(30)
        label.set_ha('right')

    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])

    col2.pyplot(fig1)
    col3.pyplot(fig2)
    col2.pyplot(fig3)
    col3.pyplot(fig4)
    col2.pyplot(fig5)
    col3.pyplot(fig6)


filenames = []
for filename in monthly_df_list:
    filenames.append(filename)
shifts_filename = col9.selectbox('Select a File to display', filenames)

plot_monthly_stats(shifts_filename)

col8, col9, col10 = st.columns([1, 5, 1])

alltimeEmployees = []
for x in monthly_df_list:
    employees = get_employees(monthly_df_list[x])
    for employ in employees:
        if employ not in alltimeEmployees:
            alltimeEmployees.append(employ)

EMPLOYEE_NAME = col9.selectbox('Select an Employee to display', alltimeEmployees)

col1, col5, col6, col4 = st.columns([1, 2, 2, 1])


def plot_annual_salary(employee):
    # show annual salary progression
    annual_employee_salaries = []
    months = []
    fig7, ax7 = plt.subplots()
    x = 0
    for monthly_df in monthly_df_list:
        curr_employee_df = create_employee_df(employee, monthly_df_list[monthly_df])
        count = int(curr_employee_df.shape[0] * 8 * 80)
        annual_employee_salaries.append(count)
        months.append(monthly_df.split()[1])
        ax7.text(x - 0.4, count + 75, count)
        x = x + 1

    ax7.bar(months, annual_employee_salaries)
    ax7.set_title(f'{employee} annual salaries 2022')

    for label in ax7.get_xticklabels():
        label.set_rotation(30)
        label.set_ha('right')

    col5.pyplot(fig7)


def plot_annual_salaries_distribution():
    fig8, ax8 = plt.subplots()
    months = []
    monthly_salaries = []
    x = 0

    for monthly_df in monthly_df_list:
        total_salaries = 0
        average = 0
        primary_df = monthly_df_list[monthly_df]
        employees = get_employees(primary_df)

        for i in range(len(employees)):
            cur_employee_df = create_employee_df(employees[i], primary_df)
            total_salaries += cur_employee_df.shape[0] * 8 * 80
        average = int(total_salaries / len(employees))
        months.append(monthly_df.split()[1])
        monthly_salaries.append(average)

        ax8.text(x - 0.4, average + 75, average)
        x = x + 1

    for label in ax8.get_xticklabels():
        label.set_rotation(30)
        label.set_ha('right')

    ax8.bar(months, monthly_salaries)
    ax8.set_title('Salary Distribution By Month 2022')

    col6.pyplot(fig8)


plot_annual_salary(EMPLOYEE_NAME)
plot_annual_salaries_distribution()


def plot_annual_shifts_distribution():
    # creating for every employee a list that holds shift counts '[morning,eve,night,weekend]'
    employees_shifts_dist = {}
    for em in alltimeEmployees:
        employees_shifts_dist[em] = [0, 0, 0, 0]  # {'Tamir Padlad': [],..}
    # iterating each month to accumulate employees shift count dist
    for monthly_df in monthly_df_list:
        primary_df = monthly_df_list[monthly_df]
        employees = get_employees(primary_df)

        for i in range(len(employees)):
            cur_employee_df = create_employee_df(employees[i], primary_df)

            employees_shifts_dist[employees[i]][0] += morning_counts(cur_employee_df).shape[0]
            employees_shifts_dist[employees[i]][1] += eve_counts(cur_employee_df).shape[0]
            employees_shifts_dist[employees[i]][2] += night_counts(cur_employee_df).shape[0]
            employees_shifts_dist[employees[i]][3] += weekend_counts(cur_employee_df).shape[0]

    category_names = ['Morning Shifts', 'Evening shifts', 'Night shifts',
                      'Weekend shifts']

    labels = list(employees_shifts_dist.keys())
    data = np.array(list(employees_shifts_dist.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig9, ax9 = plt.subplots(figsize=(9.2, 5))
    ax9.invert_yaxis()
    ax9.xaxis.set_visible(False)
    ax9.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax9.barh(labels, widths, left=starts, height=0.5,
                         label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax9.bar_label(rects, label_type='center', color=text_color)

    ax9.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
               loc='lower left', fontsize='small')
    col8, col11, col10 = st.columns([1, 4, 1])
    col8, col9, col10 = st.columns([1, 4, 1])

    col9.pyplot(fig9)
    col11.header('Annual Shifts Distribution By Employee 2022')


plot_annual_shifts_distribution()
