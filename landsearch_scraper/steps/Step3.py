import pandas as pd

class Step3:
    def save_to_excel(self, data, file_path):
        # Create a DataFrame
        df = pd.DataFrame(data)

        # Save to Excel
        df.to_excel(file_path, index=False)
        print(f"\nData saved to {file_path}")
