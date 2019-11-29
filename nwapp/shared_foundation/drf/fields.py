import phonenumbers
from rest_framework import serializers


class E164PhoneNumberField(serializers.Field):
    """
    Class used to convert the "PhoneNumber" objects "to" and "from" strings.
    This objects is from the "python-phonenumbers" library. This class will
    convert the telephone string into a `E164` formatted telephone string.

    Format: +1xxxyyyzzzz

    Class is integrated with the `SharedOrganization` object and is required
    to be placed in the Django REST Framework `context` using the `request`
    key.
    """
    def to_representation(self, text):
        """
        Function used to convert the PhoneNumber object to text string
        representation.
        """
        try:
            if text:
                country_code = self.context.get('request').tenant.country_code
                obj = phonenumbers.parse(text, country_code)
                return phonenumbers.format_number(obj, phonenumbers.PhoneNumberFormat.E164)
        except Exception as e:
            print("shared_foundation | E164PhoneNumberField | to_representation | e:", e)
        return None

    def to_internal_value(self, text):
        """
        Function used to conver the text into the PhoneNumber object
        representation.
        """
        try:
            if text:
                country_code = self.context.get('request').tenant.country_code
                obj = phonenumbers.parse(text, country_code)
                return phonenumbers.format_number(obj, phonenumbers.PhoneNumberFormat.E164)
        except Exception as e:
            print("shared_foundation | E164PhoneNumberField | to_internal_value | e:", e)
        return None

class NationalPhoneNumberField(serializers.Field):
    """
    Class used to convert the "PhoneNumber" objects "to" and "from" strings.
    This objects is from the "python-phonenumbers" library. This class will
    convert the telephone string into a `NATIONAL` formatted telephone string.

    Format: +(xxx) xxx-xxxx

    Class is integrated with the `SharedOrganization` object and is required
    to be placed in the Django REST Framework `context` using the `request`
    key.
    """
    def to_representation(self, text):
        """
        Function used to convert the PhoneNumber object to text string
        representation.
        """
        try:
            country_code = self.context.get('request').tenant.country_code
            obj = phonenumbers.parse(text, country_code)
            return phonenumbers.format_number(obj, phonenumbers.PhoneNumberFormat.NATIONAL)
        except Exception as e:
            print("shared_foundation | NationalPhoneNumberField | to_representation | e:", e)
            return None

    def to_internal_value(self, text):
        """
        Function used to conver the text into the PhoneNumber object
        representation.
        """
        try:
            country_code = self.context.get('request').tenant.country_code
            obj = phonenumbers.parse(text, country_code)
            return phonenumbers.format_number(obj, phonenumbers.PhoneNumberFormat.NATIONAL)
        except Exception as e:
            print("shared_foundation | NationalPhoneNumberField | to_internal_value | e:", e)
            return None


# python-phonenumbers - https://github.com/daviddrysdale/python-phonenumbers
# Custom Fields - http://www.django-rest-framework.org/api-guide/fields/#custom-fields


import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class GenericFileBase64File(serializers.FileField):
    """
    A Django REST framework field for handling file-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(GenericFileBase64File, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        print(file_name)
        print(decoded_file)
        print(extension)

        return extension
