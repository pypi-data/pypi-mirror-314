import typer
from camel_converter import to_snake

from validio_cli import (
    AsyncTyper,
    ConfigDir,
    Identifier,
    Namespace,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    _single_resource_if_specified,
    get_client,
    output_json,
    output_text,
)
from validio_cli.namespace import get_namespace

app = AsyncTyper(help="Channels used for notifications")


@app.async_command(help="Get channels")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace(),
    identifier: str = Identifier,
) -> None:
    client, cfg = get_client(config_dir)

    channels = await client.get_channels(
        channel_id=identifier,
        namespace_id=get_namespace(namespace, cfg),
    )

    # TODO(UI-2311): Fully support list/get/get_by_resource_name
    if isinstance(channels, list):
        channels = _single_resource_if_specified(channels, identifier)

    if output_format == OutputFormat.JSON:
        return output_json(channels, identifier)

    return output_text(
        channels,
        fields={
            "name": OutputSettings(attribute_name="resourceName"),
            "type": OutputSettings(
                attribute_name="__typename",
                reformat=lambda x: to_snake(x.removesuffix("Channel")).upper(),
            ),
            "age": OutputSettings.string_as_datetime("createdAt"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
