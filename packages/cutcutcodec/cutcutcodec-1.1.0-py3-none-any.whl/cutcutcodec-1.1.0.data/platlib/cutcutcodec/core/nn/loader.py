#!/usr/bin/env python3

"""Implement some data-loader."""

import logging
import numbers
import pathlib
import typing

import torch

from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.filter.mix.video_cast import to_bgr
from cutcutcodec.core.filter.video.resize import resize
from cutcutcodec.core.io import IMAGE_EXTENSION
from cutcutcodec.core.io.read_image import read_image


class Dataset(torch.utils.data.Dataset):
    """Select files managing the probability.

    Examples
    --------
    >>> from cutcutcodec.core.nn.loader import Dataset
    >>> from cutcutcodec.utils import get_project_root
    >>> def selector(path):
    ...     return path.suffix == ".py"
    ...
    >>> dataset = Dataset(get_project_root(), selector, max_size=128)
    >>> len(dataset)
    128
    >>> dataset[0].relative_to(get_project_root())
    PosixPath('__init__.py')
    >>> dataset[1].relative_to(get_project_root())
    PosixPath('__main__.py')
    >>> dataset[2].relative_to(get_project_root())
    PosixPath('utils.py')
    >>> dataset[3].relative_to(get_project_root())
    PosixPath('core/__init__.py')
    >>> dataset[4].relative_to(get_project_root())
    PosixPath('gui/__init__.py')
    >>> dataset[5].relative_to(get_project_root())
    PosixPath('testing/__init__.py')
    >>> dataset[6].relative_to(get_project_root())
    PosixPath('core/exceptions.py')
    >>>
    """

    def __init__(
        self,
        root: typing.Union[str, bytes, pathlib.Path],
        selector: typing.Callable[[pathlib.Path], bool],
        **kwargs,
    ):
        """Initialise and create the class.

        Parameters
        ----------
        root : pathlike
            The root folder containing all the files of the dataset.
        selector : callable
            Function that take a file pathlib.Path and return True to keep it or False to reject.
        follow_symlinks : bool, default=False
            Follow the symbolink links if set to True.
        max_size : int, optional
            The maximum number of files contained in the dataset.
        decision_depth : int, default=1
            The thresold level befor to flatten the tree.
            If 0, all the file have the same proba to be drawn.
            If 1, the decision tree has only one root node
            If n, the decision tree has a maximum of n decks.
        """
        root = pathlib.Path(root).expanduser().resolve()
        assert root.is_dir(), root
        assert callable(selector), selector.__class__.__name__
        assert isinstance(kwargs.get("follow_symlinks", False), bool), \
            kwargs["follow_symlinks"].__class__.__name__
        if kwargs.get("max_size", None) is not None:
            assert isinstance(kwargs["max_size"], numbers.Integral), \
                kwargs["max_size"].__class__.__name__
            assert kwargs["max_size"] > 0, kwargs["max_size"]
        assert isinstance(kwargs.get("decision_depth", 1), numbers.Integral), \
            kwargs["decision_depth"].__class__.__name__
        assert kwargs.get("decision_depth", 1) >= 0, kwargs["decision_depth"]
        self._root = root
        self._selector = selector
        self._follow_symlinks = kwargs.get("follow_symlinks", False)
        self._max_size = None if kwargs.get("max_size", None) is None else int(kwargs["max_size"])
        self._decision_depth = int(kwargs.get("decision_depth", 1))
        self._tree: list[typing.Union[pathlib.Path, list]] = self.scan()

    def __getitem__(self, idx: int, *, _tree=None) -> pathlib.Path:
        """Pick out a file from the dataset.

        Parameters
        ----------
        idx : int
            The index of the file, has to be in [0, len(self)[.

        Returns
        -------
        file : pathlib.Path
            The absolute path of the file.

        Notes
        -----
        This method should be overwritten.
        """
        assert isinstance(idx, int), idx.__class__.__name__
        tree = _tree or self._tree
        files = [f for f in tree if isinstance(f, pathlib.Path)]
        dirs_len = len(tree) - len(files)  # assume sorted files then dirs
        if not dirs_len:
            file = files[idx % len(files)]
            logging.info("the file %s if yield twice", file)
            return file
        if idx < len(files):
            return files[idx]
        idx, dir_idx = divmod(idx-len(files), dirs_len)
        return Dataset.__getitem__(self, idx, _tree=tree[dir_idx+len(files)])

    def __len__(self, *, _tree=None) -> int:
        """Return the number of images contained in the dataset."""
        tree = _tree or self._tree
        size = sum(1 if isinstance(e, pathlib.Path) else self.__len__(_tree=e) for e in tree)
        if self._max_size:
            size = min(self._max_size, size)
        return size

    def scan(self, *, _root=None, _depth=0) -> list[typing.Union[pathlib.Path, list]]:
        """Rescan the dataset to update the properties."""
        if _root is None:
            self._tree = []
            tree = self._tree  # reference
            root = _root or self._root
        else:
            tree = []
            root = _root

        # scan
        items = sorted(root.iterdir())
        tree.extend(f for f in items if f.is_file() and self._selector(f))
        dirs = [
            self.scan(_root=d, _depth=_depth+1) for d in items
            if d.is_dir() or (self._follow_symlinks and d.is_symlink())
        ]

        # filter and flatten
        if _depth >= self._decision_depth:
            tree.extend(f for d in dirs if d for f in d)
        else:
            tree.extend(d for d in dirs if d)

        return tree


class ImageDataset(Dataset):
    """A specific dataset for managing images."""

    def __init__(
        self,
        root: typing.Union[str, bytes, pathlib.Path],
        shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]],
        *,
        dataaug: typing.Optional[typing.Callable[[FrameVideo], FrameVideo]] = None,
        **kwargs,
    ):
        """Initialise and create the class.

        Parameters
        ----------
        root : pathlike
            Transmitted to ``Dataset`` initialisator.
        shape : int and int
            The pixel dimensions of the returned image.
            The image will be random reshaped and random cropped to reach this final shape.
            The convention adopted is the numpy convention (height, width).
        dataaug : callable, optional
            If provided, the function is called for each brut readed image before normalization.
        **kwargs : dict
            Transmitted to ``Datset`` initialisator.
        """
        assert isinstance(shape, (tuple, list)), shape.__class__.__name__
        assert len(shape) == 2, len(shape)
        assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape
        assert dataaug is None or callable(dataaug), dataaug.__class__.__name__

        def _selector(file: pathlib.Path) -> bool:
            if file.suffix.lower() not in IMAGE_EXTENSION:
                return False
            return kwargs.get("selector", lambda p: True)(file)

        super().__init__(root, **kwargs, selector=_selector)
        self.shape = (int(shape[0]), int(shape[1]))
        self.dataaug = dataaug

    def __getitem__(self, idx: int) -> torch.Tensor:
        """Read the image of index ``idx``.

        Parameters
        ----------
        idx : int
            Transmitted to ``Datset.__getitem__``.

        Returns
        -------
        image : torch.Tensor
            The readed augmented and converted throw the method ``ImageDataset.normalize``.
        """
        file = super().__getitem__(idx)
        img = FrameVideo(0, read_image(file))
        if self.dataaug is not None:
            img = self.dataaug(img)
        img = self.normalize(img)
        return img

    def normalize(self, image: FrameVideo) -> torch.Tensor:
        """Pipeline to normalize any image for batching.

        The normalization consists in:
            * Resize with deformation to reach the final size.
            * Convertion into torch float32 with good dynamic.
            * Convert into torch tensor.
            * Convert into BGR.
            * Depth channel first: (H, W, C) -> (C, H, W)

        Parameters
        ----------
        image : cutcutcodec.core.classes.frame_video.FrameVideo
            The input brut image of any shape, channels and dtype.

        Returns
        -------
        normlized_image : torch.Tensor
            The normalized float32 image of shape (3, final_height, final_width).
        """
        assert isinstance(image, FrameVideo), image.__class__.__name__

        img = torch.as_tensor(image)

        resize_after = self.shape[0]*self.shape[1] > img.shape[0]*img.shape[1]
        bgr_after = image.shape[2] > 3

        # shape normalization
        if not resize_after:
            img = resize(img, self.shape, copy=False)
        if not bgr_after:
            img = to_bgr(img)
        if resize_after:
            img = resize(img, self.shape, copy=False)
        if bgr_after:
            img = to_bgr(img)

        # convert into float32
        if img.dtype == torch.uint8:
            img = img.to(torch.float32)
            img /= 255.0
        elif img.dtype != torch.float32:
            img = img.to(torch.float32)

        # convert into bgr (C, H, W)
        img = torch.moveaxis(img, 2, 0)

        return img
