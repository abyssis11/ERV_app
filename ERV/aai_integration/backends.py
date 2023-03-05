import logging

from django.conf import settings
from django.core import exceptions

import djangosaml2.backends

logger = logging.getLogger(__name__)


class AAISAML2Backend(djangosaml2.backends.Saml2Backend):
    def _update_user(self, user, attributes, attribute_mapping, force_save=False):
        user = super()._update_user(user, attributes, attribute_mapping, force_save)
        self._update_aai_data(user, attributes, attribute_mapping)
        return user

    def _update_aai_data(self, user, attributes, attribute_mapping):
        # TODO: Add support for multi-valued attributes, currently only first value is read.
        aai_attributes = 0
        validated_privileged_attrs = 0
        for saml_attribute, user_attributes in attribute_mapping.items():
            if len(user_attributes) == 0:
                raise exceptions.ImproperlyConfigured('Attribute %s not mapped to anything.', saml_attribute)

            if saml_attribute in attributes:
                attribute_value = attributes[saml_attribute][0]
                for user_attribute in user_attributes:
                    if user_attribute.startswith(settings.AAI_DATA_RELATED_NAME):
                        # Discard related name qualifier.
                        user_attribute = user_attribute[len(settings.AAI_DATA_RELATED_NAME) + 1:]
                        aai_data = getattr(user, settings.AAI_DATA_RELATED_NAME)
                        if hasattr(aai_data, user_attribute):
                            aai_attributes += 1
                            existing_value = getattr(aai_data, user_attribute)
                            if existing_value != attribute_value:
                                setattr(aai_data, user_attribute, attribute_value)
                            else:
                                logger.debug('Attribute %s has not changed.', saml_attribute)
                        else:
                            logger.warning('Attribute %s not present in AAI data model.', user_attribute)

                if (saml_attribute in settings.AAI_PRIVILEGED_ATTRIBUTES
                        and attribute_value in settings.AAI_PRIVILEGED_ATTRIBUTES[saml_attribute]):
                    validated_privileged_attrs += 1
            else:
                logger.warning('%s not present in SAML attributes.', saml_attribute)

        if validated_privileged_attrs == len(settings.AAI_PRIVILEGED_ATTRIBUTES):
            user.is_staff = True

        logging.info('Updated AAI data with %d attributes.', aai_attributes)
        user.aai_data.save()
        user.save()
