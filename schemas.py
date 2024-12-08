from marshmallow import Schema, fields, validate, ValidationError as MarshmallowValidationError

from errors import ValidationError


class BookSchema(Schema):
    isbn = fields.String(required=True, validate=validate.Length(equal=13, error="ISBN Must include 13 digits"))
    title = fields.String(required=True, validate=validate.Length(min=1, error="Title cannot be empty"))
    author_name = fields.String(required=True, validate=validate.Length(min=1, error="Author name cannot be empty"))
    publisher_name = fields.String(required=True, validate=validate.Length(min=1, error="Publisher name cannot be empty"))
    publication_date = fields.String(required=True)

    def validate_book(self, data):
        try:
            return self.load(data)
        except MarshmallowValidationError as err:
            raise ValidationError("Invalid input data", details=err.messages)

