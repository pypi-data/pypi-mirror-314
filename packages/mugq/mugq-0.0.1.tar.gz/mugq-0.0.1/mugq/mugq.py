
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def mugq():
  print("**********************************************************")
  print("Welcome to use mugq: multi purposes guage and quantifier")
  print("**********************************************************")
  print()
  print("Contacts:")
  print()
  print("Dr Anna Sung - email: a.sung@chester.ac.uk")
  print("Prof Kelvin Leong - email: k.leong@chester.ac.uk")
  print("subpackage: tc, functions: tcexp01, tcexp02, tcfb")
  # print()
  # print("mugq includes following subpackages")
  # print("tc: text classification")
  # print()
  print("**********************************************************")

#SUBPACKAGE: tc---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions include:
# tcexp01 (allows user to experience zero shot classification)
# tcexp02 (allows user to experience zero shot classification and assign own selected labels)
# tcfb (allows user to upload a csv, specify the column to analyse, provide label set, generate result to csv)
#      (using zero-shot classification, model: facebook/bart-large-mnli)
#
#***********************************************************************************************************
def tcexp01():
  from transformers import pipeline
  from tabulate import tabulate  # Import tabulate library
  
  classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

  # Allow the user to enter the text for classification
  text = input("Enter the text to classify: ")
  candidate_labels = ["positive", "negative", "neutral"]

  # Perform classification
  output = classifier(text, candidate_labels, multi_label=False)

  # Create a table from the output
  table_data = []
  for label, score in zip(output['labels'], output['scores']):
      table_data.append([label, score])

  # Print the table
  print(tabulate(table_data, headers=["Label", "Score"], tablefmt="grid"))
  print("*Notes: The 'score' in the code represents a numerical value that indicates how confident the classifier is that a given label is the correct classification for the input text. Higher scores suggest a higher level of confidence in the classification choice, while lower scores suggest less confidence.")
  print("for more detail, contacts: Dr Anna Sung / Prof Kelvin Leong")
  
#***********************************************************************************************************
def tcexp02():
  from transformers import pipeline
  from tabulate import tabulate  # Import tabulate library

  # ------- Select label
  input_labels = input('Suggest your label set - using the format "label 1", "label 2"... "label n": ')
  print(f'You suggested the following labels: {input_labels}')

  # ------- Start running and enter text
  classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

  # Allow the user to enter the text for classification
  text = input("Enter the text to classify: ")
  candidate_labels = input_labels

  # Perform classification
  output = classifier(text, candidate_labels, multi_label=False)

  # Create a table from the output
  table_data = []
  for label, score in zip(output['labels'], output['scores']):
      table_data.append([label, score])

  # Print the table
  print(tabulate(table_data, headers=["Label", "Score"], tablefmt="grid"))
  print(f'You selected the model: facebook/bart-large-mnli')
  print("*Notes: The 'score' in the code represents a numerical value that indicates how confident the classifier is that a given label is the correct classification for the input text. Higher scores suggest a higher level of confidence in the classification choice, while lower scores suggest less confidence.")
  print("for more detail, contacts: Dr Anna Sung / Prof Kelvin Leong")

#***********************************************************************************************************
def tcfb():
  from transformers import pipeline
  from tabulate import tabulate
  import pandas as pd
  from google.colab import files

  # Use Colab file upload to upload the CSV file
  uploaded = files.upload()

  # Check if a file was uploaded
  if len(uploaded) == 0:
     print("No CSV file uploaded. Exiting.")
     exit(0)

  # Assuming you uploaded a single CSV file, get its name
  csv_file_name = list(uploaded.keys())[0]

  # Read the uploaded CSV file
  try:
     df = pd.read_csv(csv_file_name)
  except FileNotFoundError:
     print("File not found. Please provide a valid CSV file.")
     exit(1)

  # Ask the user to input the name of the column to analyze
  column_name = input("Enter the name of the column to analyze: \n")

  # Check if the specified column exists in the DataFrame
  if column_name not in df.columns:
     print(f"Column '{column_name}' not found in the CSV file.")
     exit(1)

  # Ask the user to specify the labels
  input_labels = input('Suggest your label set - using the format "label 1", "label 2", ... "label n": \n')
  print(f'You suggested the following labels: {input_labels}')

  # Initialize the text classifier
  classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

  # Create an empty DataFrame to store the classification results
  output_df = pd.DataFrame(columns=["Content", "Label", "Score"])

  # Iterate through each cell in the specified column
  for index, row in df.iterrows():
     text = row[column_name]
     # Perform classification
     output = classifier(text, input_labels, multi_label=False)
     # Append the classification results to the output DataFrame
     for label, score in zip(output['labels'], output['scores']):
         output_df = output_df.append({"Content": text, "Label": label, "Score": score}, ignore_index=True)

  # Specify the output CSV file path
  output_csv_path = "output_classification.csv"
   
  # Save the output DataFrame to a CSV file
  output_df.to_csv(output_csv_path, index=False)

  # Print the table of classification results
  print(tabulate(output_df, headers=["Content", "Label", "Score"], tablefmt="grid"))
  print(f'Classification results saved to {output_csv_path}')
  print("Notes: The 'Score' represents a numerical value that indicates the confidence of the classification for each label.")
  print("for more detail, contacts: Dr Anna Sung / Prof Kelvin Leong")

#***********************************************************************************************************
