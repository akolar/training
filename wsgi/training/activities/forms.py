from datetime import timedelta

from django import forms
from django.utils.translation import ugettext as _

from activities.models import Activity, Equipment
from activities.parser import Parser, TrackSerializer
from utils.helpers import point_distance


class UploadForm(forms.ModelForm):
    """Form for automatic activity upload"""

    fit_file = forms.FileField(required=True, help_text=_('File containing the activity track.'))

    def save(self, user, fit_file):
        """Converts the FIT file and saves the activity into the database.
        Arguments:
            user: user who uploaded the activity
            fit_file: path to the fit file
        """

        data = self.cleaned_data

        parser = Parser(fit_file)
        track = parser.convert()
        activity = TrackSerializer.serialize(track, user=user, **data)

        if self.__similar_exists(activity):
            return None

        activity.save()
        return activity.id

    def __similar_exists(self, activity):
        d_range = [activity.date - timedelta(minutes=5), activity.date + timedelta(minutes=5)]

        similar = Activity.objects.filter(user=activity.user, date__range=d_range)

        if not similar.count():
            return False

        for s in similar:
            dist = point_distance(s.track[0], activity.track[0])
            if dist < 1000:
                return True

        return False

    class Meta:
        model = Activity
        fields = ['sport', 'equipment', 'description', 'comments', 'primary_objective', 'rating']


class ManualUploadForm(forms.ModelForm):
    """Form for manual activity entries"""

    def save(self, user):
        """Calculates average values and saves the data into the database.
        Arguments:
            user: user who uploaded the file
        """

        data = self.cleaned_data

        data['speed_avg'] = data['total_distance'] / data['elapsed'] * 360

        activity = Activity(user=user, **data)
        activity.save()

        return activity.id

    class Meta:
        model = Activity
        fields = ['date', 'sport', 'equipment', 'description', 'comments', 'primary_objective', 'rating', 'elapsed',
                  'total_distance', 'elevation_gain']


class EditForm(forms.ModelForm):
    """Form for editing an existing activity.
        Unlike the upload form does not provide the ability to set distance/time/file.
    """

    class Meta:
        model = Activity
        fields = ['sport', 'equipment', 'description', 'comments', 'primary_objective', 'rating']


class EquipmentForm(forms.ModelForm):
    """Form for adding or editing of an equipment."""

    def save(self, user, id_=None):
        """Saves the updated activity into the database.
        Arguments:
            user: user who created the equipment
            id_: id of existing object; only for editing
        """

        data = self.cleaned_data

        if id_:
            eq = Equipment.objects.get(pk=id_)
        else:
            eq = Equipment()
            eq.user = user

        eq.name = data['name']
        eq.comment = data['comment']

        eq.save()

        return eq.id

    class Meta:
        model = Equipment
        fields = ['name', 'comment']
