import typer
from camel_converter import to_snake
from validio_sdk.config import ValidioConfig
from validio_sdk.exception import ValidioError
from validio_sdk.validio_client import ValidioAPIClient

import validio_cli
from validio_cli import (
    AsyncTyper,
    ConfigDir,
    Identifier,
    Namespace,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    get_client,
    output_json,
    output_text,
)
from validio_cli.namespace import get_namespace

app = AsyncTyper(help="Windows used to group data for calculations")


@app.async_command(help="Get windows")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace(),
    identifier: str = Identifier,
    source: str = typer.Option(None, help="List Windows for this source (ID or name)"),
) -> None:
    if identifier and source:
        raise ValidioError("--source can't be used together with an identifier")

    vc, cfg = get_client(config_dir)

    windows = await vc.get_windows(
        window_id=identifier, namespace_id=get_namespace(namespace, cfg)
    )

    if source:
        if not isinstance(windows, list):
            raise ValidioError("failed to get windows")

        windows = [
            window
            for window in windows
            if window is not None
            and validio_cli._resource_filter(window, ["source"], source)
        ]

    if output_format == OutputFormat.JSON:
        return output_json(windows, identifier)

    return output_text(
        windows,
        fields={
            "name": OutputSettings(attribute_name="resourceName"),
            "source": OutputSettings(reformat=lambda source: source["resourceName"]),
            "type": OutputSettings(
                attribute_name="__typename",
                reformat=lambda x: to_snake(
                    x.removesuffix("Window").removesuffix("Batch")
                ).upper(),
            ),
            "age": OutputSettings.string_as_datetime(attribute_name="createdAt"),
        },
    )


async def get_window_id(
    vc: ValidioAPIClient, cfg: ValidioConfig, identifier: str, namespace: str
) -> str | None:
    """
    Ensure the identifier is a resource id.

    If it doesn't have the expected prefix, do a resource lookup by name.
    """
    identifier_type = "window"
    prefix = "WDW_"

    if identifier is None:
        print(f"Missing {identifier_type} id or name")
        return None

    if identifier.startswith(prefix):
        return identifier

    resource = await vc.get_window_by_resource_name(
        resource_name=identifier,
        namespace_id=get_namespace(namespace, cfg),
    )

    if resource is None:
        print(f"No {identifier_type} with name or id {identifier} found")
        return None

    return resource.id


if __name__ == "__main__":
    typer.run(app())
