import pandas as pd

# Read input CSV file
input_csv = "input.csv"
df = pd.read_csv(input_csv)

# Define the columns expected by ADO
ado_columns = [
    'ID',
    'Work Item Type',
    'Title',
    'Test Step',
    'Step Action',
    'Step Expected',
    'Area Path',
    'Assigned To',
    'State'
]

# Create a new DataFrame with columns in the expected order
ado_df = pd.DataFrame(columns=ado_columns)

# Map existing columns to ADO columns
ado_df['Title'] = df['name']
ado_df['Step Action'] = df['step_description']

#TODO: make the values inputable
# Fill 'Area Path', 'Assigned To', 'State', and 'Work Item Type' to 'Test Case' for non-null/non-empty 'Title'
ado_df['Work Item Type'] = ado_df['Title'].apply(lambda x: '' if pd.notna(x) and x.strip() else '')
ado_df['Area Path'] = ado_df['Title'].apply(lambda x: '' if pd.notna(x) and x.strip() else '')
ado_df['Assigned To'] = ado_df['Title'].apply(lambda x: '' if pd.notna(x) and x.strip() else '')
ado_df['State'] = ado_df['Title'].apply(lambda x: '' if pd.notna(x) and x.strip() else '')

# Fill 'Test Step' with incremental numbers as strings for 'Step Action', resetting for each 'Title'
current_test_step = 0
test_steps = []

for index, row in ado_df.iterrows():
    if pd.notna(row['Title']) and row['Title'].strip():
        current_test_step = 0  # Reset count when a new Title is found
    if pd.notna(row['Step Action']) and row['Step Action'].strip():
        current_test_step += 1
        test_steps.append(str(current_test_step))
    else:
        test_steps.append('')  # Empty if no Step Action

ado_df['Test Step'] = test_steps

# Save the rearranged DataFrame to a new CSV file
output_csv = 'ado_formatted_test_cases.csv'
ado_df.to_csv(output_csv, index=False)

print(f"CSV file has been converted and saved as '{output_csv}'")