import datetime as dt

import factory

from .. import models


class TaskFactory(factory.django.DjangoModelFactory):
    """Factory to generate test Task instance."""

    assignment = factory.SubFactory(
        "apps.assignment.factories.AssignmentFactory",
    )
    assignee = factory.SubFactory("apps.users.factories.UserFactory")
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text", max_nb_chars=200)
    start = factory.Faker("date_time_this_month")

    @factory.lazy_attribute
    def end(self) -> dt.datetime:
        """Return a deadline that is 7 days after the start date."""
        return self.start + factory.Faker("timedelta", days=7)

    class Meta:
        model = models.Task
