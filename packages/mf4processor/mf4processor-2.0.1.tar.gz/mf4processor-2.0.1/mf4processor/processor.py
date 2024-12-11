from asammdf import MDF
import pandas as pd
import numpy as np

class MF4Processor:
    def __init__(self, mf4_file_path):
        """
        Initialize the MF4Processor with the specified MF4 file path.
        """
        self.mf4_file_path = mf4_file_path
        self.mdf = None
        self.data_groups = None
        self.load_mf4_file()

    def load_mf4_file(self):
        """
        Load the MF4 file and extract data groups.
        """
        try:
            self.mdf = MDF(self.mf4_file_path)
            self.data_groups = self.mdf.groups
            print(f"Successfully loaded MF4 file: {self.mf4_file_path}")
        except Exception as e:
            print(f"Error loading MF4 file: {e}")

    def save_channel_names_to_txt(self, output_txt_path):
        """
        Save all channel names from all groups to a text file.
        """
        try:
            if not self.data_groups:
                print("No data groups found in the MF4 file.")
                return

            all_channels = []
            for group_index, group in enumerate(self.data_groups):
                channel_names = [channel.name for channel in group.channels]
                all_channels.extend(channel_names)

            with open(output_txt_path, 'w') as file:
                for channel_name in all_channels:
                    file.write(f"{channel_name}\n")

            print(f"All channel names have been saved to: {output_txt_path}")
        except Exception as e:
            print(f"An error occurred while saving channel names: {e}")
    
    def get_signal_as_numpy(self, channel_name):
        """
        Get the specified channel's data as a numpy array.
        Returns:
            numpy.ndarray: The signal data as a numpy array.
        """
        try:
            if not self.data_groups:
                print("No data groups found in the MF4 file.")
                return None

            for idx, group in enumerate(self.data_groups):
                channel_names = [channel.name for channel in group.channels]
                if channel_name in channel_names:
                    signal_data = self.mdf.get(channel_name, group=idx)

                    samples = np.array(signal_data.samples)
                    if isinstance(samples[0], np.void):
                        samples = np.array([list(sample[0]) for sample in samples])
                    samples = np.nan_to_num(samples, nan=0)
                    return samples

            print(f"Channel '{channel_name}' not found in any group.")
            return None

        except Exception as e:
            print(f"An error occurred while retrieving signal data: {e}")
            return None

    def convert_channel_to_csv(self, channel_name, output_csv_path=None):
        """
        Convert the specified channel's data to a CSV file.
        If the channel is found, its data is saved to the specified CSV path.
        """
        try:
            if not self.data_groups:
                print("No data groups found in the MF4 file.")
                return

            selected_group = None
            group_index = None

            # Search for the group containing the specified channel
            for idx, group in enumerate(self.data_groups):
                channel_names = [channel.name for channel in group.channels]
                if channel_name in channel_names:
                    selected_group = group
                    group_index = idx
                    break

            if not selected_group:
                print(f"Channel '{channel_name}' not found in any group.")
                return

            signal_data = self.mdf.get(channel_name, group=group_index)

            samples = np.array(signal_data.samples)
            if isinstance(samples[0], np.void):
                samples = np.array([list(sample[0]) for sample in samples])

            samples = np.nan_to_num(samples, nan=0)

            if samples.ndim == 2:
                num_signals = samples.shape[1]
                columns = [f"Signal_{i+1}" for i in range(num_signals)]
                df = pd.DataFrame(samples, columns=columns)
            elif samples.ndim == 1:
                df = pd.DataFrame(samples, columns=["Signal_1"])
            else:
                print("Sample data is not in the expected format.")
                return

            if not output_csv_path:
                output_csv_path = f"{channel_name}.csv"

            df.to_csv(output_csv_path, index=False)
            print(f"CSV file created successfully: {output_csv_path}")

        except ValueError as ve:
            print(f"Data type conversion error: {ve}")
        except Exception as e:
            print(f"An error occurred during CSV conversion: {e}")