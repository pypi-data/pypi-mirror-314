from bs4 import BeautifulSoup
from base64 import b64decode
from typing import Tuple, List
import pandas as pd
from datetime import datetime


class RequestResponseHandler:
	def __init__(self, file_path: str, output_format: str):
		self.file_path = file_path
		self.items = []
		self.output_format = output_format

	def load_file(self):
		""" Reads the content from the specified log file. """
		with open(self.file_path, 'r', encoding='utf-8') as file:
			content = file.read()
		self.parse_xml(content)

	def parse_xml(self, content: str):
		""" Parses XML content and finds all 'item' elements. """
		xml_content = BeautifulSoup(content, 'xml')
		self.items = xml_content.find_all('item')

	def date_to_epoch(self, date_string: str):
		# date_string = "Fri Dec 06 09:33:44 EET 2024"
		date_string = date_string.replace(" EET", "")
		date_format = "%a %b %d %H:%M:%S %Y"
		dt = datetime.strptime(date_string, date_format)
		return int(dt.timestamp())

	def breakdown_structure(self, r: str) -> Tuple[str, List[str], str]:
		""" Breaks down the structure of the response or request string into:
			1. HTTP Start Line
			2. List of Headers
			3. Body of the message
		"""
		r_lines = r.split("\n")
		headers = []
		for line in r_lines[1:]:
			if line.strip() == "":
				break  # Stop when an empty line is encountered
			headers.append(line.strip())

		body = "\n".join(r_lines[len(headers) + 1:]).strip()
		start_line = r_lines[0].strip()
		body = "\n".join(r_lines[len(headers) + 1:]).strip()
		return start_line, headers, body

	def process_items(self):
		""" Processes each item, decoding requests and responses. """
		output_dict = {"Time":[], "Request Start Line":[], "Request Headers":[], "Request Body":[],
					   "Response Start Line":[], "Response Headers":[], "Response Body":[], "Timestamp":[]}

		for item in self.items:
			time_string = item.time.string if item.time.string else "N/A"
			request = b64decode(item.request.string).decode("utf-8") if item.request.string else "N/A"
			response = b64decode(item.response.string).decode("utf-8") if item.response.string else "N/A"
			# Breakdown and print response structure
			start_line, headers, body = self.breakdown_structure(request)
			output_dict["Time"].append(time_string)
			output_dict["Request Start Line"].append(start_line)
			output_dict["Request Headers"].append("\n".join(headers))
			output_dict["Request Body"].append(body)

			start_line, headers, body = self.breakdown_structure(response)
			output_dict["Response Start Line"].append(start_line)
			output_dict["Response Headers"].append("\n".join(headers))
			output_dict["Response Body"].append(body)

			output_dict["Timestamp"].append(self.date_to_epoch(time_string))

		if self.output_format == 'xlsx':
			pd.DataFrame.from_dict(output_dict).to_excel("burp_logs.xlsx")
		if self.output_format == 'csv':
			pd.DataFrame.from_dict(output_dict).to_csv("burp_logs.csv")
		if self.output_format == 'json':
			with open("burp_logs.json", "w") as f:
				f.write(pd.DataFrame.from_dict(output_dict).to_json(orient='records'))

def log_analysis(file_path: str = r"burp_logs", output_format: str = r"xlsx"):
	handler = RequestResponseHandler(file_path, output_format)
	handler.load_file()
	handler.process_items()


if __name__ == "__main__":
	log_analysis(output_format='json')