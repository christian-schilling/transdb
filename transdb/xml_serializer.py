from django.core.serializers import base, xml_serializer
from django.db import models
from django.utils.encoding import smart_unicode

from fields import TransField

class Serializer(xml_serializer.Serializer):
    def get_string_value(self, obj, field):
        if isinstance(field, TransField):
            return smart_unicode(getattr(obj, field.name).raw_data)
        else:
            return super(Serializer, self).get_string_value(obj, field)


class Deserializer(xml_serializer.Deserializer):
    def _handle_object(self, node):
        """
        Convert an <object> node to a DeserializedObject.
        """
        # Look up the model using the model loading mechanism. If this fails,
        # bail.
        Model = self._get_model_from_node(node, "model")

        # Start building a data dictionary from the object.  If the node is
        # missing the pk attribute, bail.
        pk = node.getAttribute("pk")
        if not pk:
            raise base.DeserializationError("<object> node is missing the 'pk' attribute")

        data = {Model._meta.pk.attname : Model._meta.pk.to_python(pk)}

        # Also start building a dict of m2m data (this is saved as
        # {m2m_accessor_attribute : [list_of_related_objects]})
        m2m_data = {}

        # Deseralize each field.
        for field_node in node.getElementsByTagName("field"):
            # If the field is missing the name attribute, bail (are you
            # sensing a pattern here?)
            field_name = field_node.getAttribute("name")
            if not field_name:
                raise base.DeserializationError("<field> node is missing the 'name' attribute")

            # Get the field from the Model. This will raise a
            # FieldDoesNotExist if, well, the field doesn't exist, which will
            # be propagated correctly.
            field = Model._meta.get_field(field_name)

            # As is usually the case, relation fields get the special treatment.
            if field.rel and isinstance(field.rel, models.ManyToManyRel):
                m2m_data[field.name] = self._handle_m2m_field_node(field_node, field)
            elif field.rel and isinstance(field.rel, models.ManyToOneRel):
                data[field.attname] = self._handle_fk_field_node(field_node, field)
            else:
                if field_node.getElementsByTagName('None'):
                    value = None
                elif isinstance(field, TransField):
                    value = field.to_python(xml_serializer.getInnerText(field_node).strip()).raw_data
                else:
                    value = field.to_python(xml_serializer.getInnerText(field_node).strip())
                data[field.name] = value

        # Return a DeserializedObject so that the m2m data has a place to live.
        return base.DeserializedObject(Model(**data), m2m_data)