import warnings

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.exceptions import ConvergenceWarning

from cumulative.opts import options
from cumulative.transforms.transform import Transform


class Cluster(Transform):
    def apply(self, src: str, k: int = 2) -> pd.DataFrame:
        """
        At each `x` position, cluster `y` values with k-means.
        """

        # Seed the random number generator for reproducibility
        seed = options().get("reproducibility.random_seed")

        y = np.dstack(self.c.df[f"{src}.y"].values).squeeze()
        # `y`: first row contains y values for all series at idx=0

        y_hat = []

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ConvergenceWarning)

            for i in range(y.shape[0]):
                yi = y[i].reshape(-1, 1)
                kmeans = KMeans(n_clusters=k, random_state=seed, n_init="auto").fit(yi)
                yi_hat = kmeans.cluster_centers_[kmeans.predict(yi)].squeeze()
                y_hat.append(yi_hat)

        y_hat = np.array(y_hat)
        # `y`: first row contains clustered y values

        return pd.DataFrame(
            {"x": self.c.df[f"{src}.x"], "y": pd.Series(y_hat.T.tolist(), index=self.c.df.index)}, copy=True
        )
