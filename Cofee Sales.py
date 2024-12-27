import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset (update the path to your actual dataset location)
data = pd.read_csv('coffee_sales.csv')

# Data Preprocessing
data['date'] = pd.to_datetime(data['date'])
data['hour'] = pd.to_datetime(data['datetime']).dt.hour
data['weekday'] = data['date'].dt.day_name()
data['month'] = data['date'].dt.to_period('M').astype(str)

# Aggregated Metrics
sales_by_product = data.groupby('coffee_name')['money'].sum().sort_values(ascending=False)
monthly_sales = data.groupby('month')['money'].sum()
weekday_sales = data.groupby('weekday')['money'].sum().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
hourly_sales = data.groupby('hour')['money'].sum()

# Visualization 1: Sales Distribution by Coffee Type
fig1 = px.bar(sales_by_product, x=sales_by_product.index, y=sales_by_product.values,
              labels={'x': 'Coffee Type', 'y': 'Total Revenue'},
              title='Total Revenue by Coffee Type', color=sales_by_product.values,
              color_continuous_scale='Viridis')
fig1.show()

# Visualization 2: Monthly Sales Trends
fig2 = px.line(monthly_sales, x=monthly_sales.index, y=monthly_sales.values,
               labels={'x': 'Month', 'y': 'Total Revenue'},
               title='Monthly Sales Trends', markers=True)
fig2.show()

# Visualization 3: Weekly Sales Distribution
fig3 = px.bar(weekday_sales, x=weekday_sales.index, y=weekday_sales.values,
              labels={'x': 'Day of the Week', 'y': 'Total Revenue'},
              title='Weekly Sales Distribution', color=weekday_sales.values,
              color_continuous_scale='Plasma')
fig3.show()

# Visualization 4: Hourly Sales Pattern
fig4 = px.bar(hourly_sales, x=hourly_sales.index, y=hourly_sales.values,
              labels={'x': 'Hour of the Day', 'y': 'Total Revenue'},
              title='Hourly Sales Pattern', color=hourly_sales.values,
              color_continuous_scale='Cividis')
fig4.show()

# Visualization 5: Coffee Type Popularity During Peak Hours
peak_hour_sales = data.groupby(['hour', 'coffee_name'])['money'].sum().reset_index()
fig5 = px.line(peak_hour_sales, x='hour', y='money', color='coffee_name',
               labels={'hour': 'Hour of the Day', 'money': 'Revenue', 'coffee_name': 'Coffee Type'},
               title='Coffee Type Popularity During Peak Hours')
fig5.show()

# Save figures if needed
fig1.write_html("total_revenue_by_coffee_type.html")
fig2.write_html("monthly_sales_trends.html")
fig3.write_html("weekly_sales_distribution.html")
fig4.write_html("hourly_sales_pattern.html")
fig5.write_html("coffee_type_peak_hours.html")

print("Dashboard visualizations are complete. Check saved HTML files for interactive plots.")
