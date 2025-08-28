import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

def make_question(text, days):
    """
    Create a question with `pub_date` offset by `days` from now.
    days < 0: past, days > 0: future
    """
    pub = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=pub)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        future_q = make_question("future", days=30)
        self.assertIs(future_q.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        old_q = make_question("old", days=-2)  # > 1 day old
        self.assertIs(old_q.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        recent_q = Question(
            question_text="recent",
            pub_date=timezone.now() - datetime.timedelta(hours=23, minutes=59)
        )
        self.assertIs(recent_q.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question_shows(self):
        q = make_question("past", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [q])

    def test_future_question_hidden(self):
        make_question("future", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_and_future_only_shows_past(self):
        past = make_question("past", days=-30)
        make_question("future", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [past])

    def test_future_question_returns_404(self):
        future = make_question("future", days=5)
        url = reverse("polls:detail", args=(future.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_displays_text(self):
        past = make_question("past", days=-5)
        url = reverse("polls:detail", args=(past.id,))
        response = self.client.get(url)
        self.assertContains(response, past.question_text)