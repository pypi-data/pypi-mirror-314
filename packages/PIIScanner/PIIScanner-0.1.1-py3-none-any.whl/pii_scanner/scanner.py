import os
import asyncio
from ner.ner_scanner import SpacyNERScanner
from constants.patterns_countries import Regions


class PIIScanner:
    def __init__(self):
        self.spacy_ner_scanner = SpacyNERScanner()  # Initialize NER Scanner for column data scanning

    async def scan(self, file_path: str = None, data: list = None, region: str = None):
        """
        Asynchronous method to scan data or file for PII.
        """
        if data is not None:
            print("Scanning provided data for PII asynchronously...")
            return await self.spacy_ner_scanner.scan_async(data, region)
        elif file_path:
            print(f"Scanning file asynchronously: {file_path}")
            return await self.files_data_pii_scanner_async(file_path, region)
        else:
            print("No data or file path provided for scanning.")
            return None



    # Placeholder for file processing methods
    async def files_data_pii_scanner_async(self, file_path: str, region: str):
        """
        Asynchronous method to process file data for PII.
        """
        print(f"Processing file asynchronously: {file_path}")
        # Add file reading and async chunk processing logic here
        return {"message": "File scanning not implemented yet"}

    def files_data_pii_scanner(self, file_path: str):
        """
        Synchronous method to process file data for PII.
        """
        print(f"Processing file: {file_path}")
        # Add file reading and chunk processing logic here
        return {"message": "File scanning not implemented yet"}


# Example usage:
if __name__ == "__main__":
    import asyncio

    pii_scanner = PIIScanner()
    data = ["Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian"]

  
    # Run asynchronous scan
    async def run_async_scan():
        data = ["Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian", "Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian","Ankit Gupta", "Lucknow", "+919140562195", "Indian", "Sofia Rossi", "Rome", "+390612345678", "Italian"]
        region = Regions.IN  # Replace with your region
        results_async = await pii_scanner.scan(data=data, region=region)
        print("Asynchronous Results:", results_async)

    asyncio.run(run_async_scan())
