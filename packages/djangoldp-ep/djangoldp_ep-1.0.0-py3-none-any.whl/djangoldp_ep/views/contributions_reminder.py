from djangoldp_ep.models.contribution import CONTRIBUTION_CHOICES
from djangoldp_ep.views.contributions import ContributionsView


class ContributionsReminderView(ContributionsView):
    def post(self, request):
        specificdata = {
            "status_before": [CONTRIBUTION_CHOICES[1][0], CONTRIBUTION_CHOICES[2][0]],
            "status_after": CONTRIBUTION_CHOICES[2][0],
            "status_after_given": CONTRIBUTION_CHOICES[4][0],
            "email_text": "emails/txt/subscription_reminder.txt",
            "email_html": "emails/html/subscription_reminder.html",
            "email_title": "Énergie Partagée - Relance d'appel à cotisation",
        }
        return self.contributionMail(request, specificdata)
