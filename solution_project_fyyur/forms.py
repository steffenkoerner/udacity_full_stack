from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, ValidationError, Length
import re


def validate_phone(form, field):
    if not re.search(r"^[0-9]*$", field.data):
        raise ValidationError("The phone number should only contain digits.")


states = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]

genres = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]


class BaseForm(Form):
    name = StringField('name', validators=[DataRequired(), Length(
        max=100, message="The input of name is too long")])

    city = StringField(
        'city', validators=[DataRequired(), Length(max=120, message="The input of city is too long")]
    )

    state = SelectField(
        'state', validators=[DataRequired()],
        choices=states
    )

    phone = StringField('phone', validators=[DataRequired(), Length(
        max=20, message="The input of phone is too long"), validate_phone])

    facebook_link = StringField(
        'facebook_link', validators=[URL(message="Please provid a correct facebook url"), Length(max=500, message="The input of facebook link is too long")]
    )

    image_link = StringField(
        'image_link', validators=[URL("Please provid a correct image link url"), Length(max=500, message="The input of image link is too long")]
    )

    website = StringField(
        'website', validators=[URL("Please provid a correct website link url"), Length(max=500, message="The input of website is too long")]
    )

    seeking_description = StringField(
        'seeking_description', validators=[Length(max=500,  message="The input of seeking description is too long")]
    )

    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=genres
    )


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )

    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(BaseForm):

    address = StringField(
        'address', validators=[DataRequired()]
    )

    seeking_talent = BooleanField(
        'seeking_talent'
    )


class ArtistForm(BaseForm):

    seeking_venue = BooleanField(
        'seeking_venue'
    )


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
