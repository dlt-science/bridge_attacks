import pandas as pd
import matplotlib.pyplot as plt

# Process the raw data and save the processed data as a CSV file
def process_and_save_data():
    # Read the raw data
    df = pd.read_csv('./data/Bridge_Real_Life_Attack_Incidents_Info.csv',encoding='utf-8')

    # Convert the date column to a date type
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')

    # Extract year and month information
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month

    # Get the minimum year and month from the raw data
    min_year = df['Year'].min()
    min_month = df[df['Year'] == min_year]['Month'].min()

    # Get the maximum year and month from the raw data
    max_year = df['Year'].max()
    max_month = df[df['Year'] == max_year]['Month'].max()

    # Create a date range with all months
    date_range = pd.date_range(start=f'{int(min_year)}-{int(min_month):02d}-01', 
                              end=f'{int(max_year)}-{int(max_month):02d}-01', 
                              freq='MS')
    all_months = pd.DataFrame({'Year': date_range.year, 'Month': date_range.month})

    # Merge the raw data with the data containing all months
    df = pd.merge(all_months, df, on=['Year', 'Month'], how='left')

    # Fill missing values with 0
    df['Amount lost (in Million USD)'] = df['Amount lost (in Million USD)'].fillna(0)

    # Summarize data by year and month
    monthly_summary = df.groupby(['Year', 'Month']).agg({'Amount lost (in Million USD)': 'sum', 'Date': 'count'}).reset_index()
    monthly_summary.rename(columns={'Amount lost (in Million USD)': 'Total Loss (Million USD)', 'Date': 'Number of Incidents'}, inplace=True)

    # Save the processed data as a CSV file
    monthly_summary.to_csv('Data/Bridge_Attack_monthly_summary.csv', index=False)

#  Plot the chart
def plot_chart():
    # Read the processed CSV file
    df = pd.read_csv('Data/Bridge_Attack_monthly_summary.csv')

    # Create a figure and axis object
    fig, ax1 = plt.subplots()

    # Plot a line chart representing the number of incidents
    ax1.plot(df['Year'].astype(str) + '-' + df['Month'].astype(str), df['Number of Incidents'], color=(117/255, 157/255, 219/255), label='Number of Incidents')
    ax1.set_xlabel('Year-Month')
    ax1.set_ylabel('Number of Incidents', color='black')
    ax1.tick_params('y', colors='black')

    # Create a second y-axis with a shared x-axis
    ax2 = ax1.twinx()

    # Plot a bar chart representing the total loss amount, and set the legend label as "Total Loss"
    ax2.bar(df['Year'].astype(str) + '-' + df['Month'].astype(str), df['Total Loss (Million USD)'], color=(236/255, 164/255, 124/255), alpha=0.7, label='Total Loss (Million USD)')
    ax2.set_ylabel('Total Loss (Million USD)', color='black')

    # Add legends for the line chart and bar chart, placing them in the upper right corner, vertically stacked, with shorter legend item length
    legend1 = ax1.legend(loc='upper right', bbox_to_anchor=(1.01, 0.91), handlelength=0.5)
    legend2 = ax2.legend(loc='upper right', bbox_to_anchor=(1.01, 1.01), handlelength=0.5)

    # Automatically adjust x-axis labels to avoid overlap
    fig.autofmt_xdate()

    # Rotate x-axis labels by 90 degrees
    ax1.tick_params(axis='x', rotation=90)

    # Save the chart as a PDF file
    plt.savefig('./figures/Fig_Incident_time_num_loss.pdf', format='pdf', bbox_inches='tight')

    # Show the chart
    plt.show()

if __name__ == "__main__":
    process_and_save_data()
    plot_chart()
