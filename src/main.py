from typing import List, Dict, Any
import os
from .file_reader import read_csv_file, read_excel_file


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Download of transactions from a file (JSON, CSV or XLSX)"""
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.json':
        return load_json_file(file_path)
    elif file_extension == '.csv':
        return read_csv_file(file_path)
    elif file_extension in ['.xlsx', '.xls']:
        return read_excel_file(file_path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_extension}")