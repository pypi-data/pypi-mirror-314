import contextlib
import logging

from amsdal.schemas.manager import SchemaManager
from amsdal_models.classes.errors import AmsdalClassNotFoundError
from amsdal_models.classes.manager import ClassManager
from amsdal_models.classes.model import Model
from amsdal_models.classes.utils import get_custom_properties
from amsdal_utils.models.data_models.enums import CoreTypes
from amsdal_utils.models.data_models.enums import MetaClasses
from amsdal_utils.models.data_models.schema import ObjectSchema
from amsdal_utils.models.data_models.schema import PropertyData
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.models.enums import Versions

from amsdal_server.apps.common.serializers.column_format import ColumnFormat
from amsdal_server.apps.common.serializers.column_response import ColumnFilter
from amsdal_server.apps.common.serializers.column_response import ColumnInfo
from amsdal_server.apps.common.serializers.column_response import FieldFilter
from amsdal_server.apps.common.serializers.column_response import FieldFilterControl
from amsdal_server.apps.common.serializers.column_response import FieldFilterInputType

logger = logging.getLogger(__name__)


class ColumnInfoMixin:
    @classmethod
    def get_object_object(cls, class_name: str) -> ObjectSchema | None:
        schema_manager = SchemaManager()
        schema: ObjectSchema | None = schema_manager.get_schema_by_name(
            class_name,
        )

        return schema

    @classmethod
    def get_class_properties_by_class_and_meta(
        cls,
        class_item: Model,
        class_meta_item: Model,
    ) -> list[ColumnInfo]:
        params = {**class_item.model_dump()}
        params.update(**class_meta_item.model_dump())

        for prop_name, prop in params['properties'].items():
            prop.update(class_item.properties[prop_name])

        schema = ObjectSchema(**params)
        return cls.get_class_properties(schema)

    @classmethod
    def get_default_filters(cls, property_name: str, property_item: PropertyData) -> list[FieldFilter]:
        label = property_item.title or property_name
        if property_item.options:
            return [
                FieldFilter(
                    type='EQ',
                    control=FieldFilterControl(
                        key=property_name,
                        type=FieldFilterInputType.SINGLE_SELECT,
                        label=f'{label} Equal',
                        options=[option.value for option in property_item.options],
                    ),
                )
            ]

        default_property_type = {
            'string': FieldFilterInputType.TEXT,
            'number': FieldFilterInputType.NUMBER,
            'date': FieldFilterInputType.DATE,
            'datetime': FieldFilterInputType.DATE_TIME,
        }

        default_filter = [
            FieldFilter(
                type='EQ',
                control=FieldFilterControl(
                    key=property_name,
                    type=default_property_type.get(property_item.type, FieldFilterInputType.TEXT),
                    label=f'{label} Equal',
                ),
            ),
            FieldFilter(
                type='NEQ',
                control=FieldFilterControl(
                    key=f'{property_name}__neq',
                    type=default_property_type.get(property_item.type, FieldFilterInputType.TEXT),
                    label=f'{label} Not Equal',
                ),
            ),
        ]

        if property_item.type == 'string':
            return [
                *default_filter,
                FieldFilter(
                    type='CONTAINS',
                    control=FieldFilterControl(
                        key=f'{property_name}__contains',
                        type=FieldFilterInputType.TEXT,
                        label=f'{label} Contains',
                    ),
                ),
                FieldFilter(
                    type='ICONTAINS',
                    control=FieldFilterControl(
                        key=f'{property_name}__icontains',
                        type=FieldFilterInputType.TEXT,
                        label=f'{label} Contains (case insensitive)',
                    ),
                ),
                FieldFilter(
                    type='STARTSWITH',
                    control=FieldFilterControl(
                        key=f'{property_name}__startswith',
                        type=FieldFilterInputType.TEXT,
                        label=f'{label} Starts With',
                    ),
                ),
                FieldFilter(
                    type='ISTARTSWITH',
                    control=FieldFilterControl(
                        key=f'{property_name}__istartswith',
                        type=FieldFilterInputType.TEXT,
                        label=f'{label} Starts With (case insensitive)',
                    ),
                ),
                FieldFilter(
                    type='ENDSWITH',
                    control=FieldFilterControl(
                        key=f'{property_name}__endswith',
                        type=FieldFilterInputType.TEXT,
                        label=f'{label} Ends With',
                    ),
                ),
                FieldFilter(
                    type='IENDSWITH',
                    control=FieldFilterControl(
                        key=f'{property_name}__iendswith',
                        type=FieldFilterInputType.TEXT,
                        label=f'{label} Ends With (case insensitive)',
                    ),
                ),
            ]

        if property_item.type in ['number', 'date', 'datetime']:
            return [
                *default_filter,
                FieldFilter(
                    type='GT',
                    control=FieldFilterControl(
                        key=f'{property_name}__gt',
                        type=default_property_type.get(property_item.type, FieldFilterInputType.TEXT),
                        label=f'{label} Greater Than',
                    ),
                ),
                FieldFilter(
                    type='GTE',
                    control=FieldFilterControl(
                        key=f'{property_name}__gte',
                        type=default_property_type.get(property_item.type, FieldFilterInputType.TEXT),
                        label=f'{label} Greater Than or Equal',
                    ),
                ),
                FieldFilter(
                    type='LT',
                    control=FieldFilterControl(
                        key=f'{property_name}__lt',
                        type=default_property_type.get(property_item.type, FieldFilterInputType.TEXT),
                        label=f'{label} Less Than',
                    ),
                ),
                FieldFilter(
                    type='LTE',
                    control=FieldFilterControl(
                        key=f'{property_name}__lte',
                        type=default_property_type.get(property_item.type, FieldFilterInputType.TEXT),
                        label=f'{label} Less Than or Equal',
                    ),
                ),
            ]

        return default_filter

    @classmethod
    def get_class_properties(cls, schema: ObjectSchema | None) -> list[ColumnInfo]:
        properties: list[ColumnInfo] = []

        if not schema:
            return properties

        _schema = schema.model_copy(deep=True)

        model = None
        for _schema_type in [SchemaTypes.USER, SchemaTypes.CONTRIB, SchemaTypes.CORE]:
            with contextlib.suppress(AmsdalClassNotFoundError):
                model = ClassManager().import_model_class(schema.title, _schema_type)

            if model:
                break

        for _prop_name, _prop in (_schema.properties or {}).items():
            if not _prop.title:
                _prop.title = _prop_name

            prop = cls.extend_with_frontend_configs(_prop_name, _prop)

            filters = ColumnFilter(
                name=_prop_name,
                label=_prop.title or _prop_name,
                filters=cls.get_default_filters(_prop_name, _prop) or [],
            )

            if model:
                prop, _prop_name, filters = cls.extend_with_attribute_configs(model, _prop_name, prop, filters)

            column_info = ColumnInfo(**prop.model_dump())
            column_info.key = _prop_name
            column_info.filters = filters

            if _prop_name in _schema.required:
                column_info.required = True

            properties.append(column_info)

        if model:
            for custom_property in sorted(get_custom_properties(model)):
                if custom_property.endswith('_display_name'):
                    continue

                cell_template = cls._property_cell_template(getattr(model, custom_property)) or 'StringTemplate'

                column_info = ColumnInfo(
                    key=custom_property,
                    label=custom_property,
                    column_format=ColumnFormat(headerTemplate='StringTemplate', cellTemplate=cell_template),
                    read_only=True,
                    required=False,
                )
                properties.append(column_info)

        return properties

    @classmethod
    def _property_cell_template(cls, property_object: property) -> str | None:
        if 'return' not in property_object.fget.__annotations__:
            return None

        return_type = property_object.fget.__annotations__['return']

        if return_type is str:
            return 'StringTemplate'

        return 'JsonTemplate'

    @classmethod
    def extend_with_attribute_configs(
        cls,
        model: type[Model],
        property_name: str,
        property_item: PropertyData,
        filters: ColumnFilter,
    ) -> tuple[PropertyData, str, ColumnFilter]:
        attr_display_name = f'{property_name}_display_name'
        attr_cell_template = f'{property_name}_cell_template'
        attr_filters = f'{property_name}_filters'

        if hasattr(model, attr_display_name) and isinstance(getattr(model, attr_display_name), property):
            property_name = attr_display_name
            cell_template = cls._property_cell_template(getattr(model, attr_display_name))

            if cell_template:
                property_item.column_format.cellTemplate = cell_template  # type: ignore[attr-defined]

        if (
            hasattr(model, attr_cell_template)
            and not isinstance(getattr(model, attr_cell_template), property)
            and getattr(model, attr_cell_template).__self__ is model
        ):
            property_item.column_format.cellTemplate = getattr(model, attr_cell_template)()  # type: ignore[attr-defined]

        if (
            hasattr(model, attr_filters)
            and not isinstance(getattr(model, attr_filters), property)
            and getattr(model, attr_filters).__self__ is model
        ):
            filters = getattr(model, attr_filters)()

        return property_item, property_name, filters

    @classmethod
    def extend_with_frontend_configs(cls, property_name: str, property_item: PropertyData) -> PropertyData:
        frontend_config = cls.resolve_fronted_config_for_class(property_item.type)
        schema_manager = SchemaManager()

        cell_template = 'StringTemplate'
        if property_item.type == 'File':
            cell_template = 'FileTemplate'
        elif property_item.type == MetaClasses.CLASS_OBJECT or cls.get_object_object(property_item.type):
            _schema: ObjectSchema | None = schema_manager.get_schema_by_name(property_item.type)

            if not _schema or _schema.meta_class == MetaClasses.TYPE:
                cell_template = 'JsonTemplate'
            else:
                cell_template = 'ReferenceTemplate'
        elif property_item.type in ['array', 'dictionary']:
            cell_template = 'JsonTemplate'

        property_item.column_format = ColumnFormat(  # type: ignore[attr-defined]
            headerTemplate='StringTemplate',
            cellTemplate=cell_template,
        )
        property_item.label = property_item.title or property_name  # type: ignore[attr-defined]

        if not frontend_config:
            return property_item

        property_frontend_configs = frontend_config.properties_configs.get(
            property_name,
            None,
        )

        if not property_frontend_configs:
            return property_item

        if property_frontend_configs.requred:
            property_item.required = True  # type: ignore[attr-defined]

        for override_field in ['column_format', 'control', 'options']:
            override_value = getattr(property_frontend_configs, override_field, None)

            if override_value is not None:
                setattr(property_item, override_field, override_value)

        return property_item

    @classmethod
    def resolve_fronted_config_for_class(cls, class_name: str) -> Model | None:
        class_manager = ClassManager()
        schema_manager = SchemaManager()

        try:
            fronted_config_model = class_manager.import_model_class('FrontendClassObjectConfig', SchemaTypes.CONTRIB)
        except AmsdalClassNotFoundError:
            logger.debug('FrontendConfig contrib is not installed')
            return None

        if class_name in CoreTypes:
            class_name = class_name.capitalize()

        frontend_config = (
            fronted_config_model.objects.filter(class_name=class_name, _address__object_version=Versions.LATEST)
            .first()
            .execute()
        )

        if not frontend_config:
            _schema: ObjectSchema | None = schema_manager.get_schema_by_name(class_name)

            if not _schema:
                return None

            if _schema.type and _schema.type != class_name:
                return cls.resolve_fronted_config_for_class(_schema.type)
        return frontend_config
