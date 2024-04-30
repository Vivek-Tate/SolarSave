# Imports
from solar_offset.db import get_db
from .carbon_offset_util import calculate_reduced_carbon_footprint

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64
from collections import defaultdict, Counter
from datetime import datetime


# Public Methods

def calculate_statistics():
    return (get_total_users(),
            get_total_countries(),
            get_number_of_donations(),
            get_total_donations(),
            get_reduced_carbon_emissions())


def get_total_users() -> int:
    # Stored Properties
    db = get_db()
    # Fetching all the user from database
    users = db.execute('SELECT * FROM user').fetchall()
    return len(users) or 0


def get_total_countries() -> int:
    # Stored Properties
    db = get_db()
    # Fetching all the countries listed
    countries = db.execute('SELECT * FROM country').fetchall()
    return len(countries) or 0


def get_number_of_donations() -> int:
    # Stored Properties
    db = get_db()
    # Fetching all the donations made
    donations = db.execute('SELECT * FROM donation').fetchall()
    return len(donations) or 0


def get_total_donations() -> int:
    # Stored Properties
    db = get_db()
    # Fetching all the donations made
    donations = db.execute('SELECT * FROM donation').fetchall()
    # Calculate and returns the total donations made
    return sum(int(donation['donation_amount']) for donation in donations) or 0


def get_reduced_carbon_emissions():
    # Calculate the reduced carbon emission based on total donations made
    return calculate_reduced_carbon_footprint(get_total_donations()) or "0 kg"


def countries_stats(countries):
    # Create the graphs
    solar_hours_chart = create_solar_hours_chart(countries)
    carbon_emissions_chart = create_carbon_emissions_chart(countries)
    solar_panel_price_chart = create_solar_panel_price_chart(countries)
    electricity_mix_chart = create_electricity_mix_chart(countries)
    return solar_hours_chart, carbon_emissions_chart, solar_panel_price_chart, electricity_mix_chart


# Charts - Countries
def create_solar_hours_chart(countries):
    # Create a bar chart for solar hours
    country_names = [country['name'] for country in countries]
    solar_hours = [country['solar_hours'] for country in countries]

    fig = plt.figure(figsize=(10, 6), facecolor='#f5f5f5')
    plt.bar(country_names, solar_hours, color='#4CAF50')
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Solar Hours', fontsize=12)
    plt.title('Solar Hours by Country', fontsize=16, fontweight='bold')
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Convert the chart to an image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    solar_hours_chart = base64.b64encode(img.getvalue()).decode('utf-8')

    return solar_hours_chart


def create_carbon_emissions_chart(countries):
    # Create a bar chart for carbon emissions
    country_names = [country['name'] for country in countries]
    carbon_emissions = [country['carbon_emissions'] for country in countries]

    fig = plt.figure(figsize=(10, 6), facecolor='#f5f5f5')
    plt.bar(country_names, carbon_emissions, color='#E53935')
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Carbon Emissions', fontsize=12)
    plt.title('Carbon Emissions by Country', fontsize=16, fontweight='bold')
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Convert the chart to an image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    carbon_emissions_chart = base64.b64encode(img.getvalue()).decode('utf-8')

    return carbon_emissions_chart


def create_solar_panel_price_chart(countries):
    # Create a scatter plot for solar panel price
    country_names = [country['name'] for country in countries]
    solar_panel_price = [country['solar_panel_price_per_kw'] for country in countries]

    fig = plt.figure(figsize=(10, 6), facecolor='#f5f5f5')
    plt.scatter(country_names, solar_panel_price, color='#1E88E5')
    plt.xlabel('Country', fontsize=12)
    plt.ylabel('Solar Panel Price (per kW)', fontsize=12)
    plt.title('Solar Panel Price by Country', fontsize=16, fontweight='bold')
    plt.xticks(rotation=90, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(linestyle='--', alpha=0.5)

    # Convert the chart to an image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    solar_panel_price_chart = base64.b64encode(img.getvalue()).decode('utf-8')

    return solar_panel_price_chart


def create_electricity_mix_chart(countries):
    # Create a pie chart for electricity mix percentage
    country_names = [country['name'] for country in countries]
    electricity_mix_percentage = [country['electricity_mix_percentage'] for country in countries]

    fig = plt.figure(figsize=(8, 8), facecolor='#f5f5f5')
    plt.pie(electricity_mix_percentage, labels=country_names, autopct='%1.1f%%',
            colors=['#FFA726', '#66BB6A', '#42A5F5', '#EF5350', '#AB47BC'])
    plt.axis('equal')
    plt.title('Electricity Mix Percentage by Country', fontsize=16, fontweight='bold')
    plt.legend(country_names, loc='upper left', fontsize=10)

    # Convert the chart to an image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    electricity_mix_chart = base64.b64encode(img.getvalue()).decode('utf-8')

    return electricity_mix_chart


# Charts - Staff & Admin Dashboard

def staff_dashboard_statistics(donations):
    # Create the graphs
    total_donations_chart = create_total_donations_chart(donations)
    donation_frequency_chart = create_donation_frequency_chart(donations)
    avg_donation_chart = create_avg_donation_chart(donations)

    return total_donations_chart, donation_frequency_chart, avg_donation_chart


def create_total_donations_chart(donations):
    # Create a stacked bar chart for total donations by country and organization
    country_org_donations = defaultdict(lambda: defaultdict(int))
    for donation in donations:
        country_name = donation['country_name']
        organization_name = donation['organization_name']
        amount = donation['amount']
        country_org_donations[country_name][organization_name] += amount

    fig = plt.figure(figsize=(10, 6), facecolor='#f5f5f5')
    ax = fig.add_subplot(111)
    bottom = [0] * len(country_org_donations)
    for organization_name in sorted(set(d['organization_name'] for d in donations)):
        amounts = [country_org_donations[country_name][organization_name] for country_name in
                   sorted(country_org_donations)]
        ax.bar(sorted(country_org_donations), amounts, bottom=bottom, label=organization_name)
        bottom = [x + y for x, y in zip(bottom, amounts)]
    ax.set_xlabel('Country')
    ax.set_ylabel('Total Donations')
    ax.set_title('Total Donations by Country and Organisation')
    ax.legend()
    plt.xticks(rotation=0)

    # Convert the chart to an image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    total_donations_chart = base64.b64encode(img.getvalue()).decode('utf-8')

    return total_donations_chart


import datetime

def create_donation_frequency_chart(donations):
    # Get the last 12 months
    today = datetime.datetime.now()
    last_12_months = [today - datetime.timedelta(days=x) for x in range(0, 365, 30)][:12]

    # Count the donations for each month
    donation_counts = [0] * 12
    for donation in donations:
        donation_date = datetime.datetime.strptime(donation['created'], '%Y-%m-%d %H:%M')
        for i, month_date in enumerate(last_12_months):
            if donation_date.year == month_date.year and donation_date.month == month_date.month:
                donation_counts[i] += 1
                break

    # Create the line chart
    fig = plt.figure(figsize=(10, 6), facecolor='#f5f5f5')
    plt.plot(last_12_months, donation_counts)
    plt.xlabel('Date')
    plt.ylabel('Donation Count')
    plt.title('Donation Frequency over the Last 12 Months')
    plt.xticks(last_12_months, [month.strftime('%b %Y') for month in last_12_months], rotation=45)

    # Convert the chart to an image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    donation_frequency_chart = base64.b64encode(img.getvalue()).decode('utf-8')

    return donation_frequency_chart


def create_avg_donation_chart(donations):
    # Create a bar chart for average donation amount by country and organization
    country_org_donations = defaultdict(lambda: defaultdict(list))
    for donation in donations:
        country_name = donation['country_name']
        organization_name = donation['organization_name']
        amount = donation['amount']
        country_org_donations[country_name][organization_name].append(amount)

    fig = plt.figure(figsize=(10, 6), facecolor='#f5f5f5')
    ax = fig.add_subplot(111)
    x = []
    for country_name in sorted(country_org_donations):
        for organization_name in sorted(country_org_donations[country_name]):
            avg_amount = sum(country_org_donations[country_name][organization_name]) / len(
                country_org_donations[country_name][organization_name])
            ax.bar(f"{country_name} - {organization_name}", avg_amount)
            x.append(f"{country_name} - {organization_name}")
    ax.set_xlabel('Country - Organisation')
    ax.set_ylabel('Average Donation Amount')
    ax.set_title('Average Donation Amount by Country and Organisation')
    plt.xticks(rotation=0)

    # Convert the chart to an image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    avg_donation_chart = base64.b64encode(img.getvalue()).decode('utf-8')

    return avg_donation_chart


# Charts - Admin Dashboard

def admin_dashboard_statistics(donations, users):
    # Create the graphs
    total_donations_chart = create_total_donations_chart(donations)
    donation_frequency_chart = create_donation_frequency_chart(donations)
    avg_donation_chart = create_avg_donation_chart(donations)
    user_type_chart = create_user_type_chart(users)

    return total_donations_chart, donation_frequency_chart, avg_donation_chart, user_type_chart


def create_user_type_chart(users):
    # Create a pie chart for user type distribution
    user_types = [user['user_type'] for user in users]
    user_type_counts = Counter(user_types)

    fig = plt.figure(figsize=(8, 8), facecolor='#f5f5f5')
    colors = ['#4CAF50', '#E53935', '#1E88E5']
    explode = (0.1, 0.1, 0.1)
    plt.pie(user_type_counts.values(), labels=user_type_counts.keys(), colors=colors, explode=explode, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('User Type Distribution', fontsize=16, fontweight='bold')
    plt.legend(user_type_counts.keys(), loc='upper left', fontsize=12)

    # Convert the chart to an image
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    user_type_chart = base64.b64encode(img.getvalue()).decode('utf-8')

    return user_type_chart
