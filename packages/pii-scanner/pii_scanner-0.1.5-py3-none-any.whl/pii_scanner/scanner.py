import re
from core.structured import ScannerForStructuredData

class PIIScanner:
    def __init__(self):
        self.structured_scanner = ScannerForStructuredData()  # Initialize NER Scanner for column data scanning

    def column_data_pii_scanner(self, data, column_name=None, chunk_size=10):
        """
        Scan the provided data for PII information using MLBasedNERScannerForStructuredData.

        :param data: List of strings to be scanned for PII.
        :param column_name: Column name to be used for sensitivity detection.
        :param chunk_size: The size of data chunks to process at a time.
        """
        # Process data in chunks
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            result = self.structured_scanner.scan(chunk)

            # Print results
            # json_result = format_result_as_json(result)
            # print("\nJSON Results:")
        return result
    
    # def files_data_pii_scanner(self, file_path, sample_size=0.2, chunk_size=1000):
    #     """
    #     Determine the file type based on its extension and call the appropriate PII detection function.

    #     :param file_path: Path to the file to be scanned.
    #     :param sample_size: Proportion of data to sample from the file.
    #     :param chunk_size: Number of rows or data units to process at once.
    #     """
    #     # Get the file extension
    #     file_extension = os.path.splitext(file_path)[1].lower()

    #     try:
    #         if file_extension == '.csv':
    #             column_name = None  # Set to None to process all columns
    #             result = csv_file_pii_detector(file_path, column_name, sample_size, chunk_size)
    #             print("CSV File PII Scanner Results:")
    #             return result
            
    #         elif file_extension in ['.jpg', '.jpeg', '.png']:
    #             result = process_file_octopii(file_path)
    #             print("Image File PII Scanner Results:")
    #             return result
                

    #         elif file_extension in ['.txt', '.pdf', '.docx']:
    #             result = file_pii_detector(file_path, sample_size)
    #             print("Text/PDF/Docx File PII Scanner Results:")
    #             return result
                

    #         elif file_extension == '.json':
    #             column_name = None  # Set to None to process all columns
    #             result = json_file_pii_detector(file_path, column_name, sample_size, chunk_size)
    #             print("JSON File PII Scanner Results:")
    #             return result

    #         elif file_extension == '.xlsx':
    #             print(file_path)
    #             column_name = None  # Specify column name or set to None to process all columns
    #             sheet_name = 'Sheet1'
    #             result = xlsx_file_pii_detector(file_path, sheet_name, column_name, sample_size, chunk_size)
    #             print("XLSX File PII Scanner Results:")
    #             return result

    #         else:
    #             print(f"Unsupported file type: {file_extension}")
    #             return

    #         # Process and print the results
    #         # print_entities_and_sensitivity(result)
    #         # json_result = format_result_as_json(result)
    #         # print("\nJSON Results:")

        # except Exception as e:
        #     print(f"Error processing file: {e}")

    def scan(self, file_path=None, data=None, sample_size=0.2, chunk_size=1000, column_name="password"):
        """
        Main function to call the appropriate PII scanner based on the provided inputs.

        :param file_path: Path to the file to be scanned (optional).
        :param data: List of strings to be scanned for PII (optional).
        :param sample_size: Proportion of data to sample from the file.
        :param chunk_size: Number of rows or data units to process at once.
        :param column_name: Column name to be used for sensitivity detection in data scanning.
        """
        if data is not None:
            print("Scanning provided data for PII...")
            return self.column_data_pii_scanner(data, column_name, chunk_size)
        elif file_path:
            print(f"Scanning file: {file_path}")
            return self.files_data_pii_scanner(file_path, sample_size, chunk_size)
        else:
            print("No data or file path provided for scanning.")

# # Example usage:
if __name__ == "__main__":
    pii_scanner = PIIScanner()
    data = ["Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian"]
    results = pii_scanner.scan(data=data, chunk_size=10, sample_size=1.0)
    print(results)
    
    # # Example 2: Scanning a file by specifying its path
    # file_path = 'dummy-pii/test.json'  # Example: 'dummy-pii/test.csv', 'dummy-pii/test.json', etc.
    # sample_size = None  # Adjust as needed
    # chunk_size = 500  # Adjust chunk size as needed
    # result = pii_scanner.scan_structured_data
    # print("====", result, "====")
                