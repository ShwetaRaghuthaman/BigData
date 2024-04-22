import json, falcon, sys
import csv
import pandas as pd
import traceback
import io

import random
from google.cloud import storage
from google.cloud import bigquery
from google.oauth2 import service_account
from falcon_cors import CORS

class UploadTestGCPClass:
	def on_post(self, req, resp):	
		# Authenticate with GCP (Google Cloud Platform)
		storage_client = storage.Client.from_service_account_json('big-data-analytics-419312-12918a01efc2.json')
		# Get the bucket
		bucket_name = 'bigdata-liya'
		bucket = storage_client.get_bucket(bucket_name)

		
		# # Upload the file
		
		 # Upload the first file
		folder_name = 'incoming/'
		filename1 = 'crimeData.csv'
		full_filename1 = folder_name + filename1
		blob1 = bucket.blob(filename1)
		blob1.upload_from_filename('crimeData.csv', content_type='text/csv')

			# Upload the second file
		filename2 = 'US_unemploymentRate.csv'
		full_filename2 = folder_name + filename2
		blob2 = bucket.blob(filename2)
		blob2.upload_from_filename('US_unemploymentRate.csv', content_type='text/csv')


	

		resp.status = falcon.HTTP_201  # Created
		resp.body = 'File uploaded successfully'

class getTestGCPClass:
	def on_get(self, req, resp):
		# Specify the path to your service account JSON key file
		key_file_path = 'big-data-analytics-419312-12918a01efc2.json'

		# Create a client using the JSON key file for authentication
		storage_client = storage.Client.from_service_account_json(key_file_path)

		# Specify the bucket name and file name
		bucket_name = 'bigdata-liya'
		file_name = 'combined_results.csv'

		# Get the bucket
		bucket = storage_client.bucket(bucket_name)

		# Get the blob (file) from the bucket
		blob = bucket.blob(file_name)

		# Open the file for reading its content
		content = blob.download_as_string().decode('utf-8').splitlines()

		# Parse the CSV content
		csv_reader = csv.DictReader(content)
		csv_data = [row for row in csv_reader]

		# Convert CSV data to JSON
		json_data = json.dumps(csv_data)

		# Set response content type to JSON
		resp.content_type = falcon.MEDIA_JSON

		# Send JSON data as response
		resp.body = json_data
		
api = falcon.API()
# Initialize CORS middleware
cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)  # Allow requests from any origin

# Add CORS middleware to the middleware stack
api.add_middleware(cors.middleware)

api.add_route("/uploadTest",UploadTestGCPClass())
api.add_route("/getTest",getTestGCPClass())