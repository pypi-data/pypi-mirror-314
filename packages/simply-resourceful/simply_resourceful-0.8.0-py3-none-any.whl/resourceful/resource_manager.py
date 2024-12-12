from __future__ import annotations

import difflib
from pathlib import Path
from typing import Any, Callable, Optional, Type, TypeVar


T = TypeVar("T")


class ResourceManager[T]:
    _instances: dict[Type[T], dict[str, ResourceManager]] = {}

    def __init__(self, handle: str) -> None:
        self.handle = handle
        self.resources: dict[str, T] = {}
        self.resource_locations: dict[str, Path] = {}

    def config(self, loader_helper: Optional[Callable] = None) -> None:
        """
        Modifies the resource manager's behavior per the specified parameters.

        :param loader_helper: Loader function for the resource. Must take the location
        data its parameter, and return an instance of the resource.
        """
        if loader_helper:
            self._asset_loader = loader_helper

    def preload(self, asset_handle: str, resource_location: Any) -> None:
        """
        Prepares the resource manager to load a resource.

        The asset handle is how users of the resource will ask for it.

        The resource location is data that describes how the asset loader can locate
        the resource. It may be a path, or a download site, or anything else, so long
        as the asset loader can handle the parameters.

        :param asset_handle: The name of the resource
        :param resource_location: The data the asset loader needs to produce the
        resource.
        """
        self.resource_locations.update({asset_handle: resource_location})

    def force_load(self, asset_handle: str, resource_location: Any) -> None:
        """
        Establishes the resource in the database, and loads it immediately instead of
        deferring to when the asset is requested.

        :param asset_handle: The name of the resource
        :param resource_location: The data the asset loader needs to produce the
        resource.
        """
        self.preload(asset_handle, resource_location)
        asset: T = self._asset_loader(resource_location)
        self.resources.setdefault(asset_handle, asset)

    def force_update(self, asset_handle: str, asset: T) -> T | None:
        """
        Changes the loaded resource of the given handle to that of the given asset.

        :param asset_handle: The name of the resource
        :param asset: The new asset replacing the old asset.
        :return: The old asset, or None if the asset wasn't loaded.
        """
        old_asset = self.resources.get(asset_handle, None)
        self.resources[asset_handle] = asset
        return old_asset

    def get(self, asset_handle: str, default: Optional[T] = None) -> T:
        """
        Gets the asset of the requested handle. Loads the asset if it isn't already.
        If the asset can't be loaded and a default is given, pass along that instead.
        The default is not added to the loaded dict.

        :param asset_handle: Name of the asset to be gotten
        :param default: Item returned if the asset is unavailable
        :raises KeyError: Raised if handle is not found or fails to load,
        and no default is given
        :return: The (loaded) instance of the asset.
        """
        if asset_handle not in self.resource_locations:
            if default is None:
                closest = difflib.get_close_matches(
                    asset_handle, self.resource_locations.keys(), n=1
                )
                error_msg = f"Resource '{asset_handle}' is not handled by {self}."
                if len(closest) > 0:
                    error_msg += f" Did you mean '{closest[0]}'?"
                raise KeyError(error_msg)
            return default
        asset = self.resources.get(asset_handle, None)
        if asset is None:
            asset = self._asset_loader(self.resource_locations.get(asset_handle))
            if asset is None:
                # Last chance to get an asset
                if default is None:
                    raise KeyError(f"Resource '{asset_handle}' failed to load.")
                asset = default
            self.resources[asset_handle] = asset
        return asset

    def dump(self, asset_handle: str) -> T | None:
        """
        Unloads the specified asset from the manager. Existing copies of the resource
        being used by objects will keep it in memory until they cease using it.

        If the asset is requested again, it will be reloaded.

        :param asset_handle: The name of the resource
        :return: The resource being unloaded, or None if it does not exist.
        """
        return self.resources.pop(asset_handle, None)

    def forget(self, asset_handle: str) -> tuple[T | None, Any]:
        """
        Unloads the asset, and removes it from the load dictionary.

        If the resource is requested again, it will fail to load.

        :param asset_handle: _description_
        :return: A tuple containing the old asset and its location data, or None if
        none exists.
        """
        old_asset = self.dump(asset_handle)
        old_location = self.resource_locations.pop(asset_handle, None)
        return (old_asset, old_location)

    @staticmethod
    def _asset_loader(*args, **kwds):
        """
        This is overwritten by self.config

        :raises AttributeError: If asset_loader is not supplied via config.
        """
        raise AttributeError(
            "No loader function assigned. You must assign a loader to run."
        )


def getResourceManager(asset_type: Type[T], handle: str = "") -> ResourceManager[T]:
    """
    Provides a Resource Manager of the specified type and handle.
    If the asset type or handle do not match an existing one, it will be created.

    :param asset_type: The Type of the resource being managed.
    :param handle: The name of the manager, defaults to ""
    :return: The resource manager of the type and handle specified.
    """
    manager_set = ResourceManager._instances.setdefault(asset_type, {})
    return manager_set.setdefault(handle, ResourceManager[asset_type](handle))
