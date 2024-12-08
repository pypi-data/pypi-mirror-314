from amsdal_data.aliases.using import LAKEHOUSE_DB_ALIAS
from amsdal_models.classes.manager import ClassManager
from amsdal_models.classes.model import Model
from amsdal_models.querysets.base_queryset import QuerySet
from amsdal_utils.models.data_models.enums import MetaClasses
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.models.enums import Versions
from amsdal_utils.query.utils import Q

from amsdal_server.apps.classes.errors import ClassNotFoundError


class ModelClassMixin:
    @classmethod
    def get_model_class_by_name(cls, class_name: str) -> type[Model]:
        class_item: Model | None = (
            cls.get_class_objects_qs().latest().filter(_address__object_id=class_name).first().execute()
        )

        if not class_item:
            msg = f'Class not found: {class_name}'
            raise ClassNotFoundError(class_name, msg)

        return cls.get_model_class(class_item)

    @classmethod
    async def async_get_model_class_by_name(cls, class_name: str) -> type[Model]:
        class_item: Model | None = (
            await cls.get_class_objects_qs().latest().filter(_address__object_id=class_name).first().aexecute()
        )

        if not class_item:
            msg = f'Class not found: {class_name}'
            raise ClassNotFoundError(class_name, msg)

        return cls.get_model_class(class_item)

    @classmethod
    def get_model_class(cls, class_item: Model) -> type[Model]:
        class_manager = ClassManager()
        model_class = class_manager.import_model_class(
            class_item.object_id,  # type: ignore[arg-type]
            class_manager.resolve_schema_type(class_item.object_id),  # type: ignore[arg-type]
        )

        return model_class

    @classmethod
    def get_class_objects_qs(cls) -> QuerySet:  # type: ignore[type-arg]
        class_manager = ClassManager()
        class_object: type[Model] = class_manager.import_model_class('ClassObject', SchemaTypes.CORE)

        return class_object.objects.using(LAKEHOUSE_DB_ALIAS).filter(
            meta_class=MetaClasses.CLASS_OBJECT,
            _metadata__is_deleted=False,
            _address__object_version=Versions.LATEST,
        )

    @classmethod
    def get_class_object_metas_qs(cls, class_objects: list[Model] | None = None) -> QuerySet:  # type: ignore[type-arg]
        class_manager = ClassManager()
        class_object: type[Model] = class_manager.import_model_class('ClassObjectMeta', SchemaTypes.CORE)
        qs = class_object.objects.using(LAKEHOUSE_DB_ALIAS).filter(
            (
                Q(class_schema_type=SchemaTypes.CONTRIB)
                | Q(class_schema_type=SchemaTypes.USER)
                | Q(_address__object_id='File')  # ugly hack
            ),
            _metadata__is_deleted=False,
            _address__object_version=Versions.LATEST,
        )

        if class_objects:
            qs = qs.filter(
                _address__object_id__in=[class_object.object_id for class_object in class_objects],
            )

        return qs
