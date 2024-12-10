"""ncdataset.py - This module contains the NCDataset class to make working with NetCDF
Datasets a little nicer.

Module-level variables
----------------------
auto_mask
    Sets the default value of the `auto_mask` parameter for every dataset opened or
    created with `NCDataset`. Default is False.

Classes
-------
NCDataset
    Wrapper for `netCDF4.Dataset` that keeps track of the filename and keyword arguments,
    even when it closes.
NCDatasetError
    Raised when trying to change dataset calling arguments and the dataset is open.
NonScalarVariableError
    Raised when trying to use NCDataset.get_scalar_var() on a non-scalar variable
DatasetClosedError
    Raised when trying to access data in a closed dataset.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TypedDict, Union

import netCDF4
from typing_extensions import Buffer, Unpack

if TYPE_CHECKING:
    from netCDF4 import AccessMode, Format
else:
    AccessMode = str
    Format = str


class NCDatasetError(Exception):
    pass


class NonScalarVariableError(NCDatasetError):
    pass


class DatasetClosedError(NCDatasetError):
    def __init__(self, *args):
        if not args:
            args = ("The dataset is not open and thus its contents are not accessible.",)
        super().__init__(*args)


auto_mask: bool = False


class _NC4DsKwargs(TypedDict, total=False):
    """Extra keyword arguments available for netCDF4.Dataset.__init__ (as of 1.7.2)
    Note: Technially additional kwargs are allowed by __init__, but they are not
    used.
    """

    clobber: bool
    format: Format
    diskless: bool
    persist: bool
    keepweakref: bool
    memory: Union[Buffer, int, None]
    encoding: Optional[str]
    parallel: bool
    comm: Any
    info: Any
    auto_complex: bool


class NCDataset(netCDF4.Dataset):
    """Wrapper for `netCDF4.Dataset` that keeps track of the filename and keyword
    arguments, even when it closes.

    Examples
    --------
    >>> ds = NCDataset("example.nc", mode="w", keepopen=False, diskless=True, persist=True)
    >>> print(ds)
    NCDataset[netCDF4.Dataset]
    nc_path: example.nc
    nc_kwargs: {'diskless': True, 'persist': True, 'mode': 'w', 'clobber': False}
    (closed)
    >>> # Since mode was "w", mode is now automatically "a" (unless we set clobber=False)
    >>> # Changes to the kwargs can be made with update_params or just __call__
    >>> with ds(diskless=False):
    ...     # Can augment the netCDF4.Dataset here, just like netCDF4.Dataset
    ...     ds.createDimension("time", 1024)
    ...     print(ds)
    ...
    NCDataset[netCDF4.Dataset]
    nc_path: example.nc
    nc_kwargs: {'diskless': False, 'persist': True, 'mode': 'a', 'clobber': False}
    <class 'hpx_radar_recorder.ncdataset.NCDataset'>
    root group (NETCDF4 data model, file format HDF5):
        dimensions(sizes): time(1024)
        variables(dimensions):
        groups:

    """

    _private_atts = (
        "nc_path",
        "nc_kwargs",
        "auto_mask",
        "failfast",
        "_ctxmgr_depth",
        "_closeval",
    )  # for __getattr__ and __setattr__
    nc_path: Path
    nc_kwargs: dict[str, Any]
    auto_mask: bool
    failfast: bool
    _ctxmgr_depth: int
    _closeval: memoryview

    def __init__(
        self,
        nc_path: Union[Path, str],
        mode: AccessMode = "r",
        *,
        keepopen: bool = True,
        failfast: bool = True,
        **nc_kwargs: Unpack[_NC4DsKwargs],
    ):
        """Initialize the NCDataset object.

        Opens or creates a netCDF4.Dataset and optionally leaves it open for modification.
        The file path and keyword arguments are retained for future use of the file.

        Parameters
        ----------
        nc_path
            Path to open or create the netCDF dataset.
        mode
            See `netCDF4.Dataset.__init__()`. For compatibility with `Dataset(path_to_ds,
            "r")` syntax.
        keepopen
            If True, the dataset is left open after creating/opening. (default) If False,
            the dataset file is created/opened (depending on mode) and closed again. This
            confirms that it exists and saves the keyword arguments for future
            interaction.
        failfast
            If true, accessing a variable or group in a closed dataset with
            `__getitem__()` (e.g. `dataset["myvar"]`) will fail immediately with a
            `DatasetClosedError`, rather than when something in the variable or group is
            used (and then only with `RuntimeError('NetCDF: Not a valid ID')`)
        **nc_kwargs
            Other arguments to pass to `netCDF4.Dataset.__init__()`. See the
            netCDF4-python docs for details.

        """
        self.nc_path = Path(nc_path)
        self.auto_mask = auto_mask  # use module-level default
        self.nc_kwargs = nc_kwargs | {"mode": mode}
        self.failfast = failfast
        self.open()
        if not keepopen:
            self.close()
        self._ctxmgr_depth = 0
        self._closeval = memoryview(
            b""
        )  # overriden when an open dataset is actually closed

    def get_scalar_var(self, varname: str, **kwargs) -> Any:
        """Get a variable, if it exists. If not and 'default' is provided, return default.
        otherwise allow the exception from netCDF4 to be raised (IndexError). A
        NonScalarVariableError will be raised if the variable is not scalar.
        """
        try:
            var_: netCDF4.Variable = self[varname]
        except IndexError:
            if "default" in kwargs:
                return kwargs["default"]
            raise
        try:
            return var_.getValue().item()
        except AttributeError:  # "scalar" strings don't have item()
            return var_.getValue()
        except IndexError:
            raise NonScalarVariableError(
                f"{varname} is not a scalar variable (dimensions are {var_.dimensions})"
            ) from None

    # Have to override __getattr__ and __setattr__ to allow access to this class's
    # attributes.
    def __getattr__(self, name: str) -> Any:
        if name in self._private_atts:
            return self.__dict__[name]
        if not self.isopen():
            raise DatasetClosedError
        return super().__getattr__(name)

    def __setattr__(self, name: str, value: Any):
        """Set an attribute, if possible

        If the attribute is a member of `NCDataset`, set it there. Then, check if the
        dataset is open and if not, raise a `DatasetClosedError`--otherwise set the
        attribute on the `netCDF4.Dataset`.
        """
        if name in self._private_atts:
            self.__dict__[name] = value
            return
        if not self.isopen():
            raise DatasetClosedError
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        """Get an attribute, if possible.

        If the attribute is a member of `NCDataset`, get it from there. Then, check if the
        dataset is open and if not, raise a `DatasetClosedError`--otherwise get the
        attribute from the `netCDF4.Dataset`.
        """
        try:
            return super().__getattribute__(name)
        except RuntimeError as rte:
            if "not a valid ID" in str(rte.args[0]).lower():
                raise DatasetClosedError from None
            raise

    def __getitem__(self, elem) -> Any:
        """Get a variable or group from a dataset.

        If `failfast` is set and the dataset is closed, raise a `DatasetClosedError`.
        Otherwise return the value from __getitem__ on the underlying netCDF4.Dataset.
        """
        if self.failfast and not self.isopen():
            raise DatasetClosedError
        return super().__getitem__(elem)

    def __enter__(self):
        self._ctxmgr_depth += 1
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ctxmgr_depth -= 1
        if self._ctxmgr_depth <= 0:
            self.close()

    def __call__(self, **kwargs):
        """If the dataset is closed, __call__ can be used to change the calling kwargs.

        Parameters
        ----------
        **kwargs
            Arguments to pass to `update_params()`.

        Returns
        -------
        NCDataset
            This NCDataset instance.

        """
        self.update_params(**kwargs)
        return self

    def __str__(self):
        if self.isopen():
            ds_repr = super().__str__()
        else:
            ds_repr = "(closed)"
        return (
            f"{self.__class__}[netCDF4.Dataset]"
            f"\nnc_path: {self.nc_path}"
            f"\nnc_kwargs: {self.nc_kwargs}"
            f"\n{ds_repr}"
        )

    def update_params(self, replace_kwargs=False, **kwargs):
        """Update keyword arguments passed to `netCDF4.Dataset.__init__()

        Parameters
        ----------
        replace_kwargs : bool, optional
            If True, the (k,v) pairs in `**kwargs` replace the previous keyword arguments.
            Otherwise, `**kwargs` amends the existing arguments. Default is False.
        **kwargs
            Keyword arguments for `netCDF4.Dataset.__init__()`.

        Raises
        ------
        NCDatasetError
            If called when the dataset is open.
        """
        if self.isopen():
            raise NCDatasetError("Cannot update calling parameters when dataset is open.")
        if replace_kwargs:
            self.nc_kwargs = kwargs
        else:
            self.nc_kwargs.update(kwargs)

    def open(self, **kwargs):
        """Reopen the dataset with the same or new arguments.

        By default `clobber=False` (see doc for `netCDF4.Dataset.__init__()`). If
        `clobber==True`, it will revert to default (`False`) after the dataset is closed.
        Other kwargs will update the default kwargs.

        Parameters
        ----------
        **kwargs
            Updates to kwargs to pass to `netCDF4.Dataset.__init__()`.
        """
        if kwargs:
            self.update_params(**kwargs)
        if not self.isopen():
            super().__init__(self.nc_path, **self.nc_kwargs)
            super().set_auto_mask(self.auto_mask)

    def close(self) -> memoryview:
        """Close the dataset.
        Calls netCDF4.Dataset.close() but only if the dataset it open.
        Resets clobber to False and mode to "a" if it was "w".
        """
        if self.isopen():
            self._closeval = super().close()
        self.nc_kwargs["clobber"] = False
        if self.nc_kwargs.get("mode", "r") == "w":
            self.nc_kwargs["mode"] = "a"
        return self._closeval

    def set_auto_mask(self, value: bool):
        """
        See netCDF4.Dataset.set_auto_mask().
        Value preserved across dataset close/open, and OK to set with closed dataset.
        """
        if self.isopen():
            super().set_auto_mask(value)
        self.auto_mask = value

    # ###
    # Override variables, dimensions, and groups properties to "fail fast" if desired.
    # ###
    @property
    def variables(self) -> dict[str, netCDF4.Variable]:
        if self.failfast and not self.isopen():
            raise DatasetClosedError
        # get the base class property
        return super().variables

    @property
    def dimensions(self) -> dict[str, netCDF4.Dimension]:
        if self.failfast and not self.isopen():
            raise DatasetClosedError
        # get the base class property
        return super().dimensions

    @property
    def groups(self) -> dict[str, netCDF4.Group]:
        if self.failfast and not self.isopen():
            raise DatasetClosedError
        # get the base class property
        return super().groups
