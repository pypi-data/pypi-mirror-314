from utils.regex import verification_prm


class DonneesConsulterPoint(dict):
    def __init__(self, point_id, autorisation_client=True, donnees_generales=True, modifications=True, interventions=True,
                 historique=True, elements_prochaines_mesures=True, derniers_index=True):

        verification_prm(point_id)

        donnees_demandees = {
            'donneesGeneralesPoint': donnees_generales,
            'modificationsContractuellesEnCours': modifications,
            'interventionsEnCours': interventions,
            'historiqueAffaires': historique,
            'elementsProchainesMesures': elements_prochaines_mesures,
            'derniersIndex': derniers_index
        }
        _kwargs = {'pointId': point_id,
                   'loginUtilisateur': '',
                   'donneesDemandees': donnees_demandees,
                   'autorisationClient': autorisation_client}

        dict.__init__(self, **_kwargs)


#   <xs:complexType name="ConsulterDonneesPointType">
#     <xs:sequence>
#       <xs:element name="pointId" type="ds:PointIdType"/>
#       <xs:element name="loginUtilisateur" type="ds:UtilisateurLoginType"/>
#       <xs:element name="donneesDemandees" type="sc:DonneesDemandeesType"/>
#       <xs:choice minOccurs="0">
#         <xs:element name="contratConcluNouveauClientSurSite" type="ds:BooleenType"/>
#         <xs:element name="autorisationClient" type="ds:BooleenType"/>
#       </xs:choice>
#     </xs:sequence>
#   </xs:complexType>

#   <xs:complexType name="DonneesDemandeesType">
#     <xs:sequence>
#       <xs:element name="donneesGeneralesPoint" type="ds:BooleenType"/>
#       <xs:element name="modificationsContractuellesEnCours" type="ds:BooleenType"/>
#       <xs:element name="interventionsEnCours" type="ds:BooleenType"/>
#       <xs:element name="historiqueAffaires" type="ds:BooleenType"/>
#       <xs:element name="elementsProchainesMesures" type="ds:BooleenType"/>
#       <xs:element name="derniersIndex" type="ds:BooleenType"/>
#     </xs:sequence>
#   </xs:complexType>