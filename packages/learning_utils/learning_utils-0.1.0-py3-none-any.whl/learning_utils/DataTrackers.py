"""
A way to track data in the training loop like rewards, losses, and other metrics
"""

import pandas as pd

class TrainingLoopTracker:
    """
    Easy way to track all of your metrics in the training loop like rewards, losses, etc.
    Enter the names of the metrics you want to track as strings.

    args:
        *metrics (str): Strings that contain the names of your metrics

    attr:
        names (list of strings): 
        num_metrics (int): Number of metrics you are tracking
        metrics (list of lists): Metrics you are tracking
    """
    def __init__(self, *metric_names: str) -> None:
        # Save metric names
        self.names = []
        for arg in metric_names:
            if not isinstance(arg, str):
                raise TypeError(f"Argument '{arg}' is not a string. Please make sure all of your metric names are strings")
            self.names.append(arg)

        self.num_metrics = len(self.names)
        self.metrics = [[] for n in range(self.num_metrics)]

    @classmethod
    def load_metrics(self, path: str) -> None:
        """
        Alternative constructor to load your metrics from a CSV file to continue training
        
        args:
            path (str): where to load your metrics from i.e. path/to/file.csv
        """
        ## TODO ## Check if this works
        df = pd.read_csv(path)
        self.names = df.columns.tolist()
        self.num_metrics = len(self.names)
        self.metrics = [df.iloc[:, i] for i in range(self.num_metrics)]

    def update(self, *metrics) -> None:
        """
        Update your metrics. Be sure to input your metrics in the same order that you defined them in.
        If you don't remember and don't want to look back in your code, use print_info() to see what order your metrics are in.

        args:
            metrics (any): Metrics that you want to track. Be sure to put them in the right order. Use print_info() to see the order to input them in.
        """
        # Check if we have the right amount of metrics
        if len(metrics) != self.num_metrics:
            raise NameError(f"The number of metrics you entered do not match the number of metrics you are tracking. You are tracking {self.num_metrics} metrics in this order: {self.names}")

        # Save metrics
        for i, metric in enumerate(metrics):
            self.metrics[i].append(metric)

    def print_info(self) -> None:
        """
        Prints the number of metrics you are tracking as well as the order to put in the update() function
        """
        print(f"\nYou are tracking {self.num_metrics} metrics: \n{self.names}\n")

    def get_metrics_df(self) -> pd.DataFrame:
        """
        Returns your metrics in a pandas dataframe
        """
        dictionary = {self.names[i]: self.metrics[i] for i in range(self.num_metrics)}
        return pd.DataFrame(dictionary)

    def save_metrics(self, path: str, index: bool = True) -> None:
        """
        Saves your metrics to a csv file in path.

        args:
            path (str): where to save your metrics i.e. path/to/file.csv
            index (bool): Whether to save with an index column or not
        """
        df = self.get_metrics_df()
        df.to_csv(path, index = index)

