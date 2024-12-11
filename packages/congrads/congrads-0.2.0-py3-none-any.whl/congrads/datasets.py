import os
from urllib.error import URLError
import numpy as np
from pathlib import Path
from typing import Callable, Union
import pandas as pd
from torch.utils.data import Dataset
import torch

from torchvision.datasets.utils import check_integrity, download_and_extract_archive


class BiasCorrection(Dataset):

    mirrors = [
        "https://archive.ics.uci.edu/static/public/514/",
    ]

    resources = [
        (
            "bias+correction+of+numerical+prediction+model+temperature+forecast.zip",
            "3deee56d461a2686887c4ae38fe3ccf3",
        ),
    ]

    def __init__(
        self,
        root: Union[str, Path],
        transform: Callable,
        download: bool = False,
    ) -> None:

        super().__init__()
        self.root = root
        self.transform = transform

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError(
                "Dataset not found. You can use download=True to download it"
            )

        self.data_input, self.data_output = self._load_data()

    def _load_data(self):

        data: pd.DataFrame = pd.read_csv(
            os.path.join(self.data_folder, "Bias_correction_ucl.csv")
        ).pipe(self.transform)

        data_input = data["Input"].to_numpy(dtype=np.float32)
        data_output = data["Output"].to_numpy(dtype=np.float32)

        return data_input, data_output

    def __len__(self):

        return self.data_input.shape[0]

    def __getitem__(self, idx):

        example = self.data_input[idx, :]
        target = self.data_output[idx, :]
        example = torch.tensor(example)
        target = torch.tensor(target)
        return example, target

    @property
    def data_folder(self) -> str:

        return os.path.join(self.root, self.__class__.__name__)

    def _check_exists(self) -> bool:
        return all(
            check_integrity(os.path.join(self.data_folder, file_path), checksum)
            for file_path, checksum in self.resources
        )

    def download(self) -> None:
        if self._check_exists():
            return

        os.makedirs(self.data_folder, exist_ok=True)

        # download files
        for filename, md5 in self.resources:
            errors = []
            for mirror in self.mirrors:
                url = f"{mirror}{filename}"
                try:
                    download_and_extract_archive(
                        url, download_root=self.data_folder, filename=filename, md5=md5
                    )
                except URLError as e:
                    errors.append(e)
                    continue
                break
            else:
                s = f"Error downloading {filename}:\n"
                for mirror, err in zip(self.mirrors, errors):
                    s += f"Tried {mirror}, got:\n{str(err)}\n"
                raise RuntimeError(s)


class FiniteIncome(Dataset):

    mirrors = [
        "https://www.kaggle.com/api/v1/datasets/download/grosvenpaul/",
    ]

    resources = [
        (
            "family-income-and-expenditure",
            "7d74bc7facc3d7c07c4df1c1c6ac563e",
        ),
    ]

    def __init__(
        self,
        root: Union[str, Path],
        transform: Callable,
        download: bool = False,
    ) -> None:
        super().__init__()
        self.root = root
        self.transform = transform

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError(
                "Dataset not found. You can use download=True to download it."
            )

        self.data_input, self.data_output = self._load_data()

    def _load_data(self):

        data: pd.DataFrame = pd.read_csv(
            os.path.join(self.data_folder, "Family Income and Expenditure.csv")
        ).pipe(self.transform)

        data_input = data["Input"].to_numpy(dtype=np.float32)
        data_output = data["Output"].to_numpy(dtype=np.float32)

        return data_input, data_output

    def __len__(self):
        return self.data_input.shape[0]

    def __getitem__(self, idx):
        example = self.data_input[idx, :]
        target = self.data_output[idx, :]
        example = torch.tensor(example)
        target = torch.tensor(target)
        return example, target

    @property
    def data_folder(self) -> str:
        return os.path.join(self.root, self.__class__.__name__)

    def _check_exists(self) -> bool:
        return all(
            check_integrity(os.path.join(self.data_folder, file_path), checksum)
            for file_path, checksum in self.resources
        )

    def download(self) -> None:

        if self._check_exists():
            return

        os.makedirs(self.data_folder, exist_ok=True)

        # download files
        for filename, md5 in self.resources:
            errors = []
            for mirror in self.mirrors:
                url = f"{mirror}{filename}"
                try:
                    download_and_extract_archive(
                        url, download_root=self.data_folder, filename=filename, md5=md5
                    )
                except URLError as e:
                    errors.append(e)
                    continue
                break
            else:
                s = f"Error downloading {filename}:\n"
                for mirror, err in zip(self.mirrors, errors):
                    s += f"Tried {mirror}, got:\n{str(err)}\n"
                raise RuntimeError(s)
