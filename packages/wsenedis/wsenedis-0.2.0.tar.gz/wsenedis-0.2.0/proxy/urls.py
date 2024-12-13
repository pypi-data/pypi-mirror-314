"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from proxy import views

urlpatterns = [
    path('v2.0/recherchepoint/', views.RecherchePointV2View.as_view()),
    path('v1.0/rechercheservicessouscritsmesures/', views.RechercherServicesSouscritsMesuresV1View.as_view()),
    path('v4.0/consulterpoint/', views.ConsultationPointV4View.as_view()),
    path('v3.0/consultermesuresdetaillees/', views.ConsultationMesuresDetailleesV3View.as_view()),
    path('v1.1/consultermesures/', views.ConsultationMesuresV1View.as_view()),
    path('v1.0/consulterdonneestechniquescontractuelles/', views.ConsultationDonneesTechniquesContractuellesV1View.as_view()),
    path('v3.0/commandercollectepublicationmesures/', views.CommandeCollectePublicationMesuresV3View.as_view()),
    path('v1.0/commanderarretservicessouscritmesures/', views.CommandeArretServicesSouscritsMesuresV1View.as_view()),
    path('v1.0/commandeaccesdonneesmesures/', views.CommandeAccesDonneesMesuresV1View.as_view()),

    # M023 service
    path('v1.0/m023/CommandeHistoriqueDonneesMesuresFines/', views.CommandeHistoriqueDonneesMesuresFinesV1View.as_view()),
    path('v1.0/m023/CommandeInformationsTechniquesEtContractuelles/', views.CommandeInformationsTechniquesEtContractuellesV1View.as_view()),
    path('v1.0/m023/CommandeAccesDonneesMesures/', views.CommandeAccesDonneesMesuresV1View.as_view()),
]

