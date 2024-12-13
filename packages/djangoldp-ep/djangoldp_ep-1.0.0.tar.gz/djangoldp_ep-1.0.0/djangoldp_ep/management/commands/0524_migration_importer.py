import pandas as pd
from django.core.management.base import BaseCommand

from djangoldp_ep.models import (Actor, CapitalDistribution, CitizenProject,
                                 CommunicationProfile, ContractType,
                                 EarnedDistinction, EnergyBuyer,
                                 EnergyProduction, EnergyType, ProductionSite,
                                 Region, Shareholder, Testimony)

ENERGY_TYPES_MAP = {
    "Bois énergie": "wood",
    "Éolien": "eolien",
    "Eolien": "eolien",
    "Géothermie": "geothermy",
    "Méthanisation": "methan",
    "Hydroélectricité": "hydroelectricity",
    "Économies d'énergie": "economy",
    "Economies d'énergie": "economy",
    "Solaire photovoltaïque au sol": "floor_photo",
    "Solaire photovoltaïque en ombrière": "ombre_photo",
    "Solaire photovoltaïque en toiture": "roof_photo",
    "Solaire photovoltaïque flottant": "floating_photo",
    "Solaire thermique": "heat_photo",
}

PROGRESS_STATUS_MAP = {
    "Émergence": "emergence",
    "Développement": "development",
    "Construction": "construction",
    "Exploitation": "exploitation",
    "Fin d'exploitation": "appeal",
    "Projet abandonné": "aborted",
}

# May 2024 - Citizen Projects & Production Sites importer


class Command(BaseCommand):
    help = 'Import -f="filename.csv" to the database, require pandas openpyxl'

    def add_arguments(self, parser):
        parser.add_argument(
            "-f",
            nargs="?",
            type=str,
            help="filename.csv",
        )
        parser.add_argument(
            "-i",
            action="store_true",
            help="Ignore created, force insert and publish everything",
        )

    def handle(self, *args, **options):
        data_frames = pd.read_excel(
            io=options["f"],
            sheet_name="5-Migration",
            header=1,
            usecols="A:CS",
            engine="openpyxl",
            skiprows=0,
            false_values=[
                "A créer",
            ],
        )
        data_frames.replace("Oui", True, inplace=True)
        data_frames.replace("Non", False, inplace=True)
        data_frames.replace("oui", True, inplace=True)
        data_frames.replace("non", False, inplace=True)
        data_frames.replace("A créer", False, inplace=True)
        data_frames.fillna("", inplace=True)

        energie_partagee_actor, created = Actor.objects.get_or_create(
            longname="Énergie Partagée Investissement"
        )

        def clean_lines(line):
            print(
                "Importing WP Project",
                line["ID"],
                "-",
                line["Title"],
                "-",
                line["Nom du site de production"] or line["Nom du projet"],
            )
            # Import only based on longname, as Thomas gave all three,
            # it would allow a proper import on staging without
            # re-importing production
            actor, created = Actor.objects.get_or_create(
                # id=line["ID acteur"],
                # urlid=line["Lien vers l'acteur moncompte"],
                longname=line["Nom acteur moncompte"]
                or line["Title"],
            )

            # if options["i"]:
            #     actor.visible = True
            #     actor.save()

            if line["Distinctions"] == "Centrales Villageoises":
                actor.villageoise = True
                actor.save()

            capital_distribution, created = CapitalDistribution.objects.get_or_create(
                actor=actor
            )
            if line["Participation des personnes physiques_nombre_actionnaires"]:
                capital_distribution.individuals_count = line[
                    "Participation des personnes physiques_nombre_actionnaires"
                ]
            if line["Participation des personnes physiques_montant_capital"]:
                capital_distribution.individuals_capital = line[
                    "Participation des personnes physiques_montant_capital"
                ]
            if line["Participation des personnes physiques_autre_fond_propres"]:
                capital_distribution.other_funds_capital = line[
                    "Participation des personnes physiques_autre_fond_propres"
                ]
            if line[
                "Dont résidents (département et département voisins)_nombre_actionnaires"
            ]:
                capital_distribution.individuals_count_resident = line[
                    "Dont résidents (département et département voisins)_nombre_actionnaires"
                ]
            if line["Participation des autres organisations de lESS_montant_capital"]:
                capital_distribution.other_ess_orgs_capital = line[
                    "Participation des autres organisations de lESS_montant_capital"
                ]
            if line[
                "Participation des autres organisations de lESS_autre_fond_propres"
            ]:
                capital_distribution.other_ess_orgs_other_funds = line[
                    "Participation des autres organisations de lESS_autre_fond_propres"
                ]
            if line[
                "Participation des collectivités (en direct ou via une SEM)_nombre_actionnaires"
            ]:
                capital_distribution.communities_count = line[
                    "Participation des collectivités (en direct ou via une SEM)_nombre_actionnaires"
                ]
            if line[
                "Participation des collectivités (en direct ou via une SEM)_montant_capital"
            ]:
                capital_distribution.communities_capital = line[
                    "Participation des collectivités (en direct ou via une SEM)_montant_capital"
                ]
            if line[
                "Participation des collectivités (en direct ou via une SEM)_autre_fond_propres"
            ]:
                capital_distribution.communities_other_funds = line[
                    "Participation des collectivités (en direct ou via une SEM)_autre_fond_propres"
                ]
            if line[
                "Dont communes, département et départements voisins_nombre_actionnaires"
            ]:
                capital_distribution.neighboring_communities_count = line[
                    "Dont communes, département et départements voisins_nombre_actionnaires"
                ]
            if line["Autres acteurs privés_montant_capital"]:
                capital_distribution.other_private_orgs_capital = line[
                    "Autres acteurs privés_montant_capital"
                ]
            if line["Autres acteurs privés_autre_fond_propres"]:
                capital_distribution.other_private_orgs_other_funds = line[
                    "Autres acteurs privés_autre_fond_propres"
                ]
            capital_distribution.save()

            if (
                line[
                    "Est-ce quÉnergie Partagée est engagé financièrement dans votre projet ?"
                ]
                == 1
            ):
                shareholder_ep, created = Shareholder.objects.get_or_create(
                    actor=energie_partagee_actor,
                    capital_distribution=capital_distribution,
                )
                if line["Participation dÉnergie Partagée_montant_capital"]:
                    shareholder_ep.capital_amount = line[
                        "Participation dÉnergie Partagée_montant_capital"
                    ]
                if line["Participation dÉnergie Partagée_autre_fond_propres"]:
                    shareholder_ep.other_funds_amount = line[
                        "Participation dÉnergie Partagée_autre_fond_propres"
                    ]
                shareholder_ep.save()

            if line["Nom du projet"]:
                citizen_project, created = CitizenProject.objects.get_or_create(
                    founder=actor,
                    name=line["Nom du projet"],
                )
                if created or options["i"]:
                    if line["Code postal (CP)"]:
                        citizen_project.postcode = line["Code postal (CP)"]
                    if line["Commune du projet"]:
                        citizen_project.city = line["Commune du projet"]
                    if line[
                        "Adresse exacte du projet (ou de la société de projet)_address"
                    ]:
                        citizen_project.address = line[
                            "Adresse exacte du projet (ou de la société de projet)_address"
                        ]
                    if line[
                        "Adresse exacte du projet (ou de la société de projet)_lat"
                    ]:
                        citizen_project.lat = line[
                            "Adresse exacte du projet (ou de la société de projet)_lat"
                        ]
                    if line[
                        "Adresse exacte du projet (ou de la société de projet)_lng"
                    ]:
                        citizen_project.lng = line[
                            "Adresse exacte du projet (ou de la société de projet)_lng"
                        ]
                    if line["Région (CP)"]:
                        citizen_project.region = Region.objects.get_or_create(
                            name=line["Région (CP)"]
                        )[0]
                    if line["Département (CP)"]:
                        citizen_project.department = line["Département (CP)"]
                    if line["Descriptif de linstallation envisagée"]:
                        citizen_project.short_description = line[
                            "Descriptif de linstallation envisagée"
                        ]
                    citizen_project.status = "draft"
                    if line["Status"]:
                        if line["Status"] == "private":
                            citizen_project.status = "retired"
                        elif line["Status"] == "publish":
                            citizen_project.status = "published"
                        else:
                            citizen_project.status = line["Status"]
                    citizen_project.visible = (
                        citizen_project.status == "published" and actor.visible
                    )
                    if line["Photo du projet"]:
                        citizen_project.picture = line["Photo du projet"]
                    if line["Vidéo du projet"]:
                        citizen_project.video = line["Vidéo du projet"]
                    if line["Site internet"]:
                        citizen_project.website = line["Site internet"]
                    if line["Page Facebook"]:
                        citizen_project.facebook_link = line["Page Facebook"]
                    if line["Page LinkedIn"]:
                        citizen_project.linkedin_link = line["Page LinkedIn"]
                    if line["Compte Twitter"]:
                        citizen_project.twitter_link = line["Compte Twitter"]
                    if line["Compte Instagram"]:
                        citizen_project.instagram_link = line["Compte Instagram"]
                    if line["Permalink"]:
                        citizen_project.wp_project_url = line["Permalink"]
                    if line["Nom contact"]:
                        citizen_project.contact_name = line["Nom contact"]
                    if line["Prénom contact"]:
                        citizen_project.contact_first_name = line["Prénom contact"]
                    if line["Téléphone de la personne contact"]:
                        citizen_project.contact_phone = line[
                            "Téléphone de la personne contact"
                        ]
                    if line["Email de la personne contact"]:
                        citizen_project.contact_email = line[
                            "Email de la personne contact"
                        ]
                    if line[
                        "Souhaitez-vous rendre votre email visible sur la page projet ?"
                    ]:
                        citizen_project.contact_visibility = (
                            line[
                                "Souhaitez-vous rendre votre email visible sur la page projet ?"
                            ]
                            == 1
                        )
                    citizen_project.save()

                communication_profile, created = (
                    CommunicationProfile.objects.get_or_create(
                        citizen_project=citizen_project
                    )
                )

                if created or options["i"]:
                    if line["Description du projet"]:
                        communication_profile.long_description = line[
                            "Description du projet"
                        ]
                    communication_profile.save()

                if line["Distinctions"]:
                    if (
                        line["Distinctions"] != "Non"
                        and line["Distinctions"] != "Centrales Villageoises"
                    ):
                        distinction, created = EarnedDistinction.objects.get_or_create(
                            name=line["Distinctions"]
                        )
                        if citizen_project not in distinction.citizen_projects.all():
                            distinction.citizen_projects.add(citizen_project)

                if line["Labellisé Énergie Partagée"]:
                    distinction, created = EarnedDistinction.objects.get_or_create(
                        name="Labellisé Énergie Partagée"
                    )
                    if citizen_project not in distinction.citizen_projects.all():
                        distinction.citizen_projects.add(citizen_project)

                if line["Témoignage"]:
                    testimony, created = Testimony.objects.get_or_create(
                        citizen_project=citizen_project
                    )
                    if created or options["i"]:
                        if line["Portrait du ou des porteurs de projet"]:
                            testimony.author_picture = line[
                                "Portrait du ou des porteurs de projet"
                            ]
                        if line["Témoignage"]:
                            testimony.content = line["Témoignage"]
                        if line["Auteur du témoignage"]:
                            testimony.author_name = line["Auteur du témoignage"]
                        testimony.save()

                if line["Nom du site de production"]:
                    production_site, created = ProductionSite.objects.get_or_create(
                        citizen_project=citizen_project,
                        name=line["Nom du site de production"],
                    )
                    if created or options["i"]:
                        if line["Adresse exacte"]:
                            production_site.address = line["Adresse exacte"]
                        if line["Code postal"]:
                            production_site.postcode = line["Code postal"]
                        if line["Commune"]:
                            production_site.city = line["Commune"]
                        if line["Département"]:
                            production_site.department = line["Département"]
                        if line["Région"]:
                            production_site.region = Region.objects.get_or_create(
                                name=line["Région"]
                            )[0]
                        if line["Latitude (deg)"]:
                            production_site.lat = line["Latitude (deg)"]
                        if line["Longitude (deg)"]:
                            production_site.lng = line["Longitude (deg)"]
                        if line["État d'avancement du projet  Site de Production"]:
                            production_site.progress_status = PROGRESS_STATUS_MAP[
                                line["État d'avancement du projet  Site de Production"]
                            ]
                        if line["Année de mise en service prévue"]:
                            production_site.expected_commissionning_year = int(
                                line["Année de mise en service prévue"]
                            )
                        if line["Année de mise en service effective"]:
                            production_site.effective_commissionning_year = int(
                                line["Année de mise en service effective"]
                            )
                        if line["Description du site de production"]:
                            production_site.description = line[
                                "Description du site de production"
                            ]
                        if line[
                            "Montant des subventions reçues pour le projet Site de production (en €)"
                        ]:
                            production_site.grants_earned_amount = line[
                                "Montant des subventions reçues pour le projet Site de production (en €)"
                            ]
                        if line["Budget total d'investissement (en €)"]:
                            production_site.total_investment_budget = line[
                                "Budget total d'investissement (en €)"
                            ]
                        if line["Budget total développement (en €)"]:
                            production_site.total_development_budget = line[
                                "Budget total développement (en €)"
                            ]
                        if line["Le projet peut-il être rendu public ?"]:
                            production_site.visible = (
                                line["Le projet peut-il être rendu public ?"]
                                and citizen_project.visible
                            )
                        production_site.save()

                        energy_production, created = (
                            EnergyProduction.objects.get_or_create(
                                production_site=production_site
                            )
                        )

                        if created or options["i"]:
                            if line["Acheteur de l'énergie produite"]:
                                energy_production.energy_buyer = (
                                    EnergyBuyer.objects.get_or_create(
                                        name=line["Acheteur de l'énergie produite"]
                                    )[0]
                                )
                            if line["Contrat d'achat de l'énergie produite"]:
                                energy_production.contract_type = (
                                    ContractType.objects.get_or_create(
                                        name=line[
                                            "Contrat d'achat de l'énergie produite"
                                        ]
                                    )[0]
                                )
                            if line["Types d'énergies produites"]:
                                energy_production.energy_type = (
                                    EnergyType.objects.get_or_create(
                                        name=line["Types d'énergies produites"].replace(
                                            "Electricité", "Électricité"
                                        )
                                    )[0]
                                )
                            if line["Puissance installée (électrique) (en kW)"]:
                                energy_production.installed_capacity = line[
                                    "Puissance installée (électrique) (en kW)"
                                ]
                            if line["Puissance installée (thermique) (en kW)"]:
                                energy_production.installed_capacity = line[
                                    "Puissance installée (thermique) (en kW)"
                                ]
                            if line[
                                "Productible Production annuelle estimée (en MWh électriques)"
                            ]:
                                energy_production.estimated_yearly_production = line[
                                    "Productible Production annuelle estimée (en MWh électriques)"
                                ]
                            if line[
                                "Productible Production annuelle estimée (en MWh thermique)"
                            ]:
                                energy_production.estimated_yearly_production = line[
                                    "Productible Production annuelle estimée (en MWh thermique)"
                                ]
                            if line["Technologie (filière) (SP)"]:
                                energy_production.technology_used = ENERGY_TYPES_MAP[
                                    line["Technologie (filière) (SP)"]
                                ]
                            if line["Capacité estimée d'injection en gaz en Nm3/h"]:
                                energy_production.estimated_injection_capacity = line[
                                    "Capacité estimée d'injection en gaz en Nm3/h"
                                ]
                            energy_production.save()

            return line

        data_frames.apply(clean_lines, axis=1)

        print("Imported " + str(data_frames.shape[0]) + " entries")
