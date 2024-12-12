"""Functions for handling reading the config file."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, cast

if TYPE_CHECKING:
    import pathlib

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

if sys.version_info >= (3, 11):
    import tomllib as toml
else:
    import toml

AnyDict = Dict[str, Any]
ConfigDict = AnyDict  # TODO: can this type be better?


class Config:
    """Class to handle reading a config file."""

    class MigrationStrategy:
        """Class containing the migration strategies to apply to a given file type."""

        TranslateStrategy = Tuple[str, Tuple[str, str]]

        file_type: str
        file_identifiers_to_delete: list[str]
        file_identifiers_to_translate: list[TranslateStrategy]

        @classmethod
        def from_dict(
            cls,
            file_type: str,
            dct: dict[str, list[str] | str],
        ) -> Self:
            """Create a MigrationStrategy from a dictionary."""
            delete = []
            translate = []
            for file_identifier, migrate_strategy in dct.items():
                if isinstance(migrate_strategy, str):
                    strategy = migrate_strategy
                elif isinstance(migrate_strategy, list) and len(migrate_strategy) != 0:
                    strategy = migrate_strategy[0]
                else:
                    message = (
                        f"Config has an invalid migration strategy for "
                        f"'{file_identifier}': {migrate_strategy}"
                    )
                    raise RuntimeError(message)

                if strategy == "delete":
                    delete.append(file_identifier)
                elif strategy == "translate-to":
                    if len(migrate_strategy) != 3:
                        message = (
                            f"Config has an invalid 'translate-to' migration "
                            f"strategy: {migrate_strategy}"
                        )
                        raise RuntimeError(message)
                    to_file_type = migrate_strategy[1]
                    to_file_identifier = migrate_strategy[2]
                    translate.append(
                        (file_identifier, (to_file_type, to_file_identifier)),
                    )
            return cls(file_type, delete, translate)

        def __init__(
            self,
            file_type: str,
            file_identifiers_to_delete: list[str],
            file_identifiers_to_translate: list[TranslateStrategy],
        ) -> None:
            """Construct."""
            self.file_type = file_type
            self.file_identifiers_to_delete = file_identifiers_to_delete
            self.file_identifiers_to_translate = file_identifiers_to_translate

    _config_dict: ConfigDict

    @classmethod
    def from_file(cls, file_path: pathlib.Path) -> Self:
        """Read a config from a file."""
        if not file_path.exists():
            message = f"File '{file_path}' not found"
            raise FileNotFoundError(message)
        ocpiupdate_config_dict = toml.load(file_path)
        config_dict = ocpiupdate_config_dict.get("ocpiupdate")
        if config_dict is None:
            message = f"Config file '{file_path}' does not contain '[ocpiupdate]'"
            raise RuntimeError(message)
        return cls(config_dict)

    def __init__(self, config_dict: ConfigDict) -> None:
        """Construct."""
        self._config_dict = config_dict

    def __repr__(self) -> str:
        """Dunder method: Convert to string evaluating to class constructor."""
        return f"{self.__class__.__name__}({self._config_dict!r})"

    def __str__(self) -> str:
        """Dunder method: Convert to string."""
        return str(self._config_dict)

    def get_dict_setting_for_parse(
        self,
        file_type: str,
        file_identifier: str,
        setting: str,
    ) -> AnyDict:
        """Get a setting of type dict from the `parse` category of the config."""
        # Get the `ocpiupdate.parse` category
        # or fail
        parse_config = self._config_dict.get("parse")
        if parse_config is None:
            return {}
        # Get the `ocpiupdate.parse.$file_type` category
        # or fail
        filetype_config = parse_config.get(file_type)
        if filetype_config is None:
            return {}
        # Get the `ocpiupdate.parse.$file_type.$file_identifier` category,
        # or try `ocpiupdate.parse.$file_type.$setting`
        # or fail
        subcategory_config = filetype_config.get(file_identifier)
        if subcategory_config is None:
            setting_config = filetype_config.get(setting)
            if setting_config is not None:
                return cast("AnyDict", setting_config)
            return {}
        # Get settings from `ocpiupdate.parse.$file_type.$file_identifier.inherit`
        # or try `ocpiupdate.parse.$file_type.$setting`
        ret: AnyDict = {}
        inherit_config = subcategory_config.get("inherit")
        if inherit_config is not None:
            ret.update(
                self.get_dict_setting_for_parse(
                    file_type,
                    inherit_config,
                    setting,
                ),
            )
        else:
            setting_config = filetype_config.get(setting)
            if setting_config is not None:
                ret.update(setting_config)
        # Get settings from `ocpiupdate.parse.$file_type.$file_identifier.$setting`
        setting_config = subcategory_config.get(setting)
        if setting_config is not None:
            ret.update(setting_config)
        return ret

    def get_list_setting_for_parse(
        self,
        file_type: str,
        file_identifier: str,
        setting: str,
    ) -> list[str]:
        """Get a setting of type list from the `parse` category of the config."""
        # Get the `ocpiupdate.parse` category
        # or fail
        parse_config = self._config_dict.get("parse")
        if parse_config is None:
            return []
        # Get the `ocpiupdate.parse.$file_type` category
        # or fail
        filetype_config = parse_config.get(file_type)
        if filetype_config is None:
            return []
        # Get the `ocpiupdate.parse.$file_type.$file_identifier` category,
        # or try `ocpiupdate.parse.$file_type.$setting`
        # or fail
        subcategory_config = filetype_config.get(file_identifier)
        if subcategory_config is None:
            setting_config = filetype_config.get(setting)
            if setting_config is not None:
                return cast("List[str]", setting_config)
            return []
        # Get settings from `ocpiupdate.parse.$file_type.$file_identifier.inherit`
        # or try `ocpiupdate.parse.$file_type.$setting`
        ret: list[str] = []
        inherit_config = subcategory_config.get("inherit")
        if inherit_config is not None:
            ret.extend(
                self.get_list_setting_for_parse(
                    file_type,
                    inherit_config,
                    setting,
                ),
            )
        else:
            setting_config = filetype_config.get(setting)
            if setting_config is not None:
                ret.extend(setting_config)
        # Get settings from `ocpiupdate.parse.$file_type.$file_identifier.$setting`
        setting_config = subcategory_config.get(setting)
        if setting_config is not None:
            ret.extend(setting_config)
        return ret

    def get_migration_strategies(self) -> list[MigrationStrategy]:
        """Get all migration strategies from the config file."""
        # Get the `ocpiupdate.migrate` category, or fail
        migrate_config = self._config_dict.get("migrate")
        if migrate_config is None:
            return []
        ret = []
        # Create the list of all migration strategies
        for file_type, file_type_migration_table in migrate_config.items():
            ret.append(
                self.MigrationStrategy.from_dict(
                    file_type,
                    file_type_migration_table,
                ),
            )
        return ret

    def get_setting_for_parse(
        self,
        file_type: str,
        file_identifier: str,
        setting: str,
    ) -> str | None:
        """Get a setting of type string from the `parse` category of the config."""
        # Get the `ocpiupdate.parse` category
        # or fail
        parse_config = self._config_dict.get("parse")
        if parse_config is None:
            return None
        # Get the `ocpiupdate.parse.$file_type` category
        # or fail
        filetype_config = parse_config.get(file_type)
        if filetype_config is None:
            return None
        # Get the `ocpiupdate.parse.$file_type.$file_identifier` category,
        # or try `ocpiupdate.parse.$file_type.$setting`
        # or fail
        subcategory_config = filetype_config.get(file_identifier)
        if subcategory_config is None:
            return cast("Optional[str]", filetype_config.get(setting))
        # Get setting from `ocpiupdate.parse.$file_type.$file_identifier.inherit`
        # or try `ocpiupdate.parse.$file_type.$setting`
        ret: str | None = None
        inherit_config = subcategory_config.get("inherit")
        if inherit_config is not None:
            ret = self.get_setting_for_parse(file_type, inherit_config, setting)
        else:
            ret = filetype_config.get(setting)
        # Get setting from `ocpiupdate.parse.$file_type.$file_identifier.$setting`
        setting_config = subcategory_config.get(setting)
        if setting_config is not None:
            ret = setting_config
        return ret
