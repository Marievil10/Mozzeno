Hi all

I am one of the many users of the Mozzeno investing platform and also one of many who use Google Sheets to keep track of their investments. Mozzeno offers a CSV file containing an overview of your investments. However, it became clear very quickly that the manual editing, copying, and pasting of my sheet would take a lot of time. So I decided to create a little Python project to make the process go quicker. I made this project so that it can be uploaded in an empty sheet, as well as update an existing sheet. Do take into account that the CSV file should include **ALL** your nodes, including the ones that are already paid, sold, etc.

> [!NOTE]
> It does still require the manual starting of the project in your program of choice (e.g. PyCharm, VSCode,...).

## General information

### Version, language, packages and functions

The Python version of this project is 3.10.

This project uses both well-known packages as well as some custom functions and fixed values. They can be found in the following files:
- main.py: the main file where everything happens, of course
- functions.py: custom functions made for this project
- fixed_values.py: fixed values for me personally, but can be adjusted to your situation. This also includes a dataframe of the gross and net percentages of Mozzeno which will be used in one of the dataframes

> [!CAUTION]
> Only Dutch is supported (for now).

### Connection to Google Sheets

To be able to perform changes in your sheet, I had to make a connection between my Python project and the sheet. This is done through a credentials file and a JSON file. The credentials file itself is available in my project, but here is the video I used to create the .json file for accessing and editing my Google Sheets-sheet: https://www.youtube.com/watch?v=w533wJuilao&t=109s. Don't forget to fill in your .json file name in your credentials file here:

    creds = ServiceAccountCredentials.from_json_keyfile_name('.json file name', scope)

The import of the credentials is already done within main.py, what you still need to do is fill in the name of your file and sheet right here: 

    sheet = get_credentials('name of file', 'name of sheet')

When that's done, you should be able to connect to your Google Sheet and perform updates.

### Connection to the correct folder and file

> [!NOTE]
> When downloading the CSV file from Mozzeno, the filename looks like this: **notes_900100001860_20240919_100946.xlsx**

To be able to use the information from the CSV file for this project, I had to:
- fill in the path to the folder in which to find the file
- define the correct file extension 
- find the most recent file

First of all, find the file to which the CSV file gets saved when downloading it from Mozzeno and fill it in here:

    folder_path = r'your_path'

Secondly, be specific with your file extension:

    file_type = r'/*xlsx'

Next, the function get_max_mozzeno_file is used to determine all files that contain the word 'notes' in the filename (see filename structure in the note above), put them in a list, and sort them based on time. It will determine the most recent folder in that list. In case there are no files found, an error will be shown and the project will not continue. 

Lastly, it will make a dataframe based on the newly determined CSV file and clear the current Google sheet of its contents to not have overlapping fields and incoherent tables.

At the end of the script you will find the delete_file function. This will automatically delete the used file from your folder. I added this to make sure my folder does not get overflown with files by Mozzeno, however this is completely optional. 

### To be done in Google Sheets

The project includes a complete emptying of the sheet so that the new information does not interfere with the old information (headers don't mix with the numbers,...). However, adjustments of font, layout,... in Google Sheets are not included in this project, this will have to be done separately. 

## Dataframes
There are three dataframes used within this project.

### Detailed overview of the notes
This includes:
- Renewal date of the notes
- How much you invested in each node
- How much of the node is already paid back
- How much interest you have already received
- The status of the node (on time, too late, etc.)
- How much of the node still needs to be paid back
- When the node has been fully paid back

The dataframe also includes a summarizing row right under the header:

<img width="650" alt="image" src="https://github.com/user-attachments/assets/2d73adab-97ff-4a2b-8df8-87be67540d09">


The status summary can contain three different words:
1. Good: all payments are on time
2. Anticipating: the borrower promised to pay
3. Panic: one of the payments are not being made

### Detailed overview of gains
This includes:
- Your start capital, this increases when you deposit money
- Total of interests and bonuses minus the taxes
- Current worth of your portfolio
- The still available, not invested, amount
- Your gain percentage based on your start capital
- The last time you updated the sheet/ran the script
- How much you have already withdrawn


<img width="571" alt="image" src="https://github.com/user-attachments/assets/2a545d43-09de-417e-80f1-385c66db9939">

> [!WARNING]
> In case you have done some withdrawing and depositing already, you will have to go through the script multiple times to start:
> - First time to fill in the sheet with its dataframe headers and the initial information regarding the nodes
> - Second time to add and/or subtract the summation of the withdrawn and deposited money to take into account all the changes already done, to have an accurate view of the current state of your notes

### Detailed overview of the (future) gain
This includes:
- Value of the running nodes
- Estimated average gross gain percentage of the running nodes
- Estimated average net gain percentage of the running nodes
- Total projected interest on these nodes
- Remaining interest on these nodes
- Gain of the current year

<img width="648" alt="image" src="https://github.com/user-attachments/assets/93144da3-19b1-4cb2-ba8a-b659780e15db">

## More
When running the script, there will always be the question of whether or not you changed something to the amount of money. These are actions that are different from investing or receiving money. More specifically, I mean depositing or withdrawing money.

As I said, this project can be uploaded in an empty sheet, as well as update an existing sheet. To have the correct calculations, it will start with checking if certain fields/columns already exist, namely 'Withdrawn' and 'Start capital'. If these fields are not found, or these fields contain value that cannot be used within the calculations, they will be retrieved from the fixed_values.py file. 
