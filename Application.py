from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the CSV data
data = pd.read_excel('visit.xlsx')


# Extract unique territories from the data
territories = data['Territory'].unique()

# Define a route to display customer names for a selected designation
@app.route('/')
def index():
    designations = data.columns[3:]  # Assuming designations start from the third column
    return render_template('index.html', designations=designations, territories=territories)

# Define a route to handle the form submission and display results
@app.route('/results', methods=['POST'])
def results():
    designation = request.form.get('designation')
    territory = request.form.get('territory')

    # Filter the data based on the selected designation and territory for no visits
    filtered_data_no_visit = data[(data[designation] == 'No Visits')]

    if territory:
        filtered_data_no_visit = filtered_data_no_visit[filtered_data_no_visit['Territory'] == territory]

    customers_no_visit = filtered_data_no_visit['Customer'].tolist()

    # Filter the data based on the selected designation and territory for visits
    filtered_data_with_visit = data[(data[designation] != 'No Visits')]

    if territory:
        filtered_data_with_visit = filtered_data_with_visit[filtered_data_with_visit['Territory'] == territory]

    # Create a list of dictionaries for customers with visit dates
    customers_with_visit = []
    for index, row in filtered_data_with_visit.iterrows():
        customers_with_visit.append({
            'customer': row['Customer'],
            'visit_date': row[designation]
        })

    return render_template('results.html', designation=designation, territory=territory,
                           customers_no_visit=customers_no_visit, customers_with_visit=customers_with_visit)


if __name__ == '__main__':
    app.run(debug=True)
