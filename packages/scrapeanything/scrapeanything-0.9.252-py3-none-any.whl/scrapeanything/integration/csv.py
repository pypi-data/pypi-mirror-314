import pandas as pd

class Csv:
    
    def __init__(self) -> None:
        pass

    def import_data(self, filename: str) -> None:
        results = []

        data = pd.read_csv(filename)
        for i, row in data.iterrows():
            results.append({col: row[col] for col in row.index})

        return results

    def export_data(self, data: any, filename: str, separator: str) -> None:
        df = pd.DataFrame(data)
        df.to_csv(filename, sep=',', encoding='utf-8')