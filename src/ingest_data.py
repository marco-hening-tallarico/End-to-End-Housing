import os
import zipfile
from abc import ABC, abstractmethod

# Define the abstract base class for data ingestion
class DataIngestor(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        """Abstract method to ingest data given a given file"""
        pass
# implement a concrete class for ZIP Ingestion
class ZipDataIngestor(DataIngestor):
    def ingest(self, file_path: str) -> pd.DataFrame:
        """Extracts a .zip file and returns the contents as a pandas DataFrame"""
        # Ensure file is a zip file
        if not file_path.endswith('.zip'):
            raise ValueError("Provided file is not a .zip file")
        # extract the zip file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall("extracted_data")

        # Find the extracted CSV file (assuming there's only one CSV in the zip)
        extracted_files = os.listdir("extracted_data")
        csv_files = [f for f in extracted_files if f.endswith('.csv')]

        if len(csv_files) == 0:
            raise FileNotFoundError("No csv file found in the extracted zip")
        if len(csv_files) > 1:
            raise ValueError("Multiple csv files found in the extracted zip. Please ensure there's only one csv file.")

        # Read the CSV file into a DataFrame
        csv_file_path = os.path.join("extracted_data", csv_files[0])
        df = pd.read_csv(csv_file_path)

        return df