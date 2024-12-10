import contextlib
from collections.abc import Iterator

from amsdal.configs.main import settings
from amsdal.schemas.manager import SchemaManager
from amsdal_models.classes.constants import USER_MODELS_MODULE
from amsdal_models.classes.data_models.dependencies import DependencyModelNames
from amsdal_models.classes.errors import AmsdalClassNotFoundError
from amsdal_models.classes.helpers.reference_loader import ReferenceLoader
from amsdal_models.classes.manager import ClassManager
from amsdal_models.classes.model import Model
from amsdal_models.classes.utils import resolve_base_class_for_schema
from amsdal_models.classes.writer import ClassWriter
from amsdal_models.querysets.executor import LAKEHOUSE_DB_ALIAS
from amsdal_utils.models.base import ModelBase
from amsdal_utils.models.data_models.schema import ObjectSchema
from amsdal_utils.models.enums import SchemaTypes


def build_missing_models() -> list[str]:
    class_manager = ClassManager()
    class_writer = ClassWriter(settings.models_root_path)
    ClassObjectMeta = class_manager.import_class('ClassObjectMeta', SchemaTypes.CORE)  # noqa: N806
    model_names = DependencyModelNames.build_from_database()

    missed_models = []

    for object_meta in (
        ClassObjectMeta.objects.latest()  # type: ignore[attr-defined]
        .using(LAKEHOUSE_DB_ALIAS)
        .filter(
            _metadata__is_deleted=False,
        )
        .execute()
    ):
        class_object_object = ReferenceLoader(object_meta.get_metadata().class_meta_schema_reference).load_reference(
            using=LAKEHOUSE_DB_ALIAS
        )

        model = None
        with contextlib.suppress(AmsdalClassNotFoundError):
            model = import_class_model(object_meta.title)

        if not model:
            missed_models.append(object_meta.title)

            dump = object_meta.model_dump()
            dump.update(class_object_object.model_dump())
            object_schema = ObjectSchema(**dump)

            class_writer.generate_model(
                schema=object_schema,
                schema_type=SchemaTypes.USER,
                base_class=resolve_base_class_for_schema(object_schema),
                model_names=model_names,
                sub_models_directory=USER_MODELS_MODULE,
            )

    return missed_models


async def async_build_missing_models() -> list[str]:
    class_manager = ClassManager()
    class_writer = ClassWriter(settings.models_root_path)
    ClassObjectMeta = class_manager.import_class('ClassObjectMeta', SchemaTypes.CORE)  # noqa: N806
    model_names = await DependencyModelNames.async_build_from_database()

    missed_models = []

    for object_meta in (
        await ClassObjectMeta.objects.latest()  # type: ignore[attr-defined]
        .using(LAKEHOUSE_DB_ALIAS)
        .filter(
            _metadata__is_deleted=False,
        )
        .aexecute()
    ):
        class_object_object = await ReferenceLoader(
            (await object_meta.aget_metadata()).class_meta_schema_reference
        ).aload_reference(using=LAKEHOUSE_DB_ALIAS)

        model = None
        with contextlib.suppress(AmsdalClassNotFoundError):
            model = import_class_model(object_meta.title)

        if not model:
            missed_models.append(object_meta.title)

            dump = object_meta.model_dump()
            dump.update(class_object_object.model_dump())
            object_schema = ObjectSchema(**dump)

            class_writer.generate_model(
                schema=object_schema,
                schema_type=SchemaTypes.USER,
                base_class=resolve_base_class_for_schema(object_schema),
                model_names=model_names,
                sub_models_directory=USER_MODELS_MODULE,
            )

    return missed_models


def _build_schema_tree() -> dict[str, list[tuple[str, SchemaTypes]]]:
    schema_tree: dict[str, list[tuple[str, SchemaTypes]]] = {}
    schemas: list[tuple[ObjectSchema, SchemaTypes]] = SchemaManager().class_schemas()

    for schema, schema_type in schemas:
        schema_tree.setdefault(schema.title, [])
        schema_tree.setdefault(schema.type, [])
        schema_tree[schema.type].append((schema.title, schema_type))

    return schema_tree


def get_subclasses(class_item: type[ModelBase] | None) -> Iterator[type[ModelBase]]:
    if class_item is not None:
        class_manager = ClassManager()
        schema_tree = _build_schema_tree()
        subclasses_names = schema_tree.get(class_item.__name__, [])

        for subclass_name, schema_type in subclasses_names:
            yield class_manager.import_model_class(
                subclass_name,
                schema_type,
            )


def import_class_model(class_name: str) -> type[Model]:
    class_manager = ClassManager()

    for _schema_type in [SchemaTypes.USER, SchemaTypes.CONTRIB]:
        with contextlib.suppress(AmsdalClassNotFoundError):
            return class_manager.import_model_class(class_name, _schema_type)

    return class_manager.import_model_class(class_name, SchemaTypes.CORE)
