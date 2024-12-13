from djangoldp_ep.views.contributions import ContributionsView


class ContributionsActorUpdateView(ContributionsView):
    def post(self, request):
        specificdata = {
            "status_before": "all",
            "email_text": "emails/txt/actor_update.txt",
            "email_html": "emails/html/actor_update.html",
            "email_title": "[Votre adhésion] [action requise] Mettez à jour les données de votre fiche acteur",
        }
        return self.contributionMail(request, specificdata)
