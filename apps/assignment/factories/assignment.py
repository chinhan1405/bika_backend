import datetime as dt

import factory

from .. import models


class AssignmentFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Assignment instance."""

    creator = factory.SubFactory("apps.users.factories.UserFactory")
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text", max_nb_chars=200)
    start = factory.Faker("date_time_this_month")

    @factory.lazy_attribute
    def deadline(self) -> dt.datetime:
        """Return a deadline that is 7 days after the start date."""
        return self.start + factory.Faker("timedelta", days=7)

    class Meta:
        model = models.Assignment
