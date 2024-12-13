from dataclasses import dataclass

import typer

from validio_cli import (
    AsyncTyper,
    ConfigDir,
    Namespace,
    OutputFormat,
    OutputFormatOption,
    OutputSettings,
    get_client,
    output_json,
    output_text,
)
from validio_cli.bin.entities import sources

app = AsyncTyper(help="Recommended validators for your Sources")

APPLY_RESULT_SUCCEEDED = "SUCCEEDED"
APPLY_RESULT_FAILED = "FAILED"


@dataclass
class ApplyResult:
    """Result from applying recommendation"""

    id: str
    state: str


@app.async_command(help="List all recommendations")
async def get(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    # ruff: noqa:  ARG001
    namespace: str = Namespace(),
    source: str = typer.Option(
        ..., help="List recommendations for this Source (ID or name)"
    ),
) -> None:
    vc, cfg = get_client(config_dir)

    source_id = await sources.get_source_id(vc, cfg, source, namespace)
    if source_id is None:
        return None

    recommendations = await vc.get_recommendations(source_id=source_id)

    if output_format == OutputFormat.JSON:
        return output_json(recommendations)

    return output_text(
        recommendations,
        fields={
            "id": None,
            "name": None,
            "type": OutputSettings.trimmed_upper_snake(
                attribute_name="__typename", trim="Validator"
            ),
            "age": OutputSettings.string_as_datetime(attribute_name="createdAt"),
        },
    )


@app.async_command(help="Apply recommendations")
async def apply(
    config_dir: str = ConfigDir,
    output_format: OutputFormat = OutputFormatOption,
    ids: list[str] = typer.Option(
        ..., "--id", help="Recommendations to apply (IDs), supports multiple values"
    ),
) -> None:
    vc, _ = get_client(config_dir)

    api_result = await vc.apply_recommendations(recommendation_ids=ids)

    result = []
    seen_ids = set()

    for r, state in [
        (api_result["failedIds"], APPLY_RESULT_FAILED),
        (api_result["successIds"], APPLY_RESULT_SUCCEEDED),
    ]:
        for id in r:
            seen_ids.add(id)
            result.append(ApplyResult(id=id, state=state))

    # TODO: The API silently accepts unknown ids but we want to add them as
    # failed in the output so the caller know they've not been applied.
    for id in ids:
        if id in seen_ids:
            continue

        result.append(ApplyResult(id=id, state=APPLY_RESULT_FAILED))

    if output_format == OutputFormat.JSON:
        return output_json(result)

    return output_text(
        result,
        fields={
            "id": None,
            "state": None,
        },
    )


if __name__ == "__main__":
    typer.run(app())
