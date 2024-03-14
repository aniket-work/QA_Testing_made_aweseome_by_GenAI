import pandas as pd

def generate_table(text):
    # Split the text into lines
    lines = text.strip().split('\n')

    # Extract table data
    data = [line.strip().split('|') for line in lines if line.strip()]

    # Remove empty strings and strip leading/trailing whitespaces from each cell
    data = [[cell.strip() for cell in row if cell.strip()] for row in data]

    # Initialize variables
    current_row = []
    combined_data = []

    # Iterate through the data
    for row in data:
        if row[0].startswith("TC_"):
            # Start a new row
            if current_row:
                combined_data.append(current_row)
            current_row = row[:4]
            current_row.append('')  # Initialize Actual Results
        else:
            # Append steps to perform
            if len(row) > 0 and len(current_row) > 2:
                current_row[2] += f"<br>{row[0]}"
            elif len(row) == 1:
                current_row.append(row[0])  # Populate Expected Result

    # Append the last row
    if current_row:
        combined_data.append(current_row)

    # Create DataFrame if data exists
    if combined_data:
        header_row = ["Test Case ID", "Description of the Test Case", "Steps to Perform the Test Case", "Expected Result", "Actual Results"]
        df = pd.DataFrame(combined_data[1:], columns=header_row[:len(combined_data[0])])  # Adjust the number of columns in the header row
        df["Actual Results"] = ''  # Add Actual Results column with empty values
        df["Expected Result"] = combined_data[0][3]  # Assign Expected Result value from TC_01
    else:
        return "No data available."

    # Convert DataFrame to HTML table
    return df.to_html(index=False, escape=False)

# Example usage:
example_text = """
| Test Case ID  |  Description of the Test Case  |  Steps to Perform the Test Case  |  Expected Result
| TC_01 | Verify if the contact form is visible and accessible | 1. Open the image with the contact form.
2. Check if the form is displayed properly.
3. Verify that all fields are functional and can be interacted with. | The contact form should be visible and accessible to users. All input fields should work as intended, and the form should display properly across different devices and screen sizes.
| TC_02 | Verify if the form fields have labels | 1. Check if each field has a corresponding label above it.
2. Ensure that the labels are aligned correctly with their respective input boxes.
3. Confirm that the labels are readable and visible. | The labels should be associated with the correct input fields, and they should be clearly visible to users.
| TC_03 | Verify if the form accepts valid email addresses | 1. Enter a valid email address in the "Email" field.
2. Click on the submit button.
3. Check if an error message or confirmation is displayed. | The form should accept valid email addresses, and upon submission, a message or confirmation should be displayed. Additionally, the user's input should be stored in the backend system.
"""

html_table = generate_table(example_text)
if html_table:
    # Adjust the width of the div containing the response
    max_width_str = "max-width: 1000px;"
    response_html = f"""
    <div style="background-color: #e6f7ff; padding: 16px; border-radius: 8px; {max_width_str}">
        <h3 style="margin-top: 0;">Response:</h3>
        {html_table}
    </div>
    """
    print(response_html)  # Print the HTML for the table
