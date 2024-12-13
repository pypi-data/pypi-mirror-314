import typer
from validio_sdk.exception import ValidioError

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

app = AsyncTyper(help="Filters on sources")


@app.async_command(help="List filters")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    namespace: str = Namespace(),
    identifier: str = Identifier,
    source: str = typer.Option(None, help="List filters for this source (ID or name)"),
) -> None:
    if identifier and source:
        raise ValidioError("--source can't be used together with an identifier")

    vc, cfg = get_client(config_dir)

    filters = await vc.get_filters(
        filter_id=identifier, namespace_id=get_namespace(namespace, cfg)
    )

    if source:
        if not isinstance(filters, list):
            raise ValidioError("failed to get filters")

        filters = [
            f
            for f in filters
            if f is not None and validio_cli._resource_filter(f, ["source"], source)
        ]

    if output_format == OutputFormat.JSON:
        return output_json(filters, identifier)

    return output_text(
        filters,
        fields={
            "name": OutputSettings(attribute_name="resourceName"),
            "source": OutputSettings(reformat=lambda source: source["resourceName"]),
            "type": OutputSettings(
                attribute_name="__typename",
            ),
            "age": OutputSettings.string_as_datetime(attribute_name="createdAt"),
        },
    )


if __name__ == "__main__":
    typer.run(app())
