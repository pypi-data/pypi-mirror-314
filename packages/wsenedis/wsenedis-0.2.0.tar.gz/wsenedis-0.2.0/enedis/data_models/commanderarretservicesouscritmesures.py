from enedis.utils.regex import verification_prm


class ArretServiceSouscrit(dict):
    def __init__(self, service_souscrit_id: str):
        _kwargs = {'serviceSouscritId': service_souscrit_id}
        dict.__init__(self, **_kwargs)


class DonneesGeneralesArretService(dict):
    def __init__(self, point_id: str, ref_frn=None):
        verification_prm(point_id)
        _kwargs = {'pointId': point_id, 'initiateurLogin': '', 'objetCode': 'ASS', 'contratId': ''}
        if ref_frn is not None:
            _kwargs['refFrn'] = ref_frn
        dict.__init__(self, **_kwargs)


class DemandeArretServiceSouscritMesures(dict):

    def __init__(self, donnees_generales: DonneesGeneralesArretService, arret_service_souscrit: ArretServiceSouscrit):
        dict.__init__(self, donneesGenerales=donnees_generales, arretServiceSouscrit=arret_service_souscrit)

# <xs:complexType name="CommanderArretServiceSouscritMesuresType">
#       <xs:sequence>
#          <xs:element name="demande" type="sc:DemandeType"/>
#       </xs:sequence>
#    </xs:complexType>

#    <xs:complexType name="DemandeType">
#       <xs:sequence>
#          <xs:element name="donneesGenerales" type="sc:DonneesGeneralesType"/>
#          <xs:element name="arretServiceSouscrit" type="sc:ArretServiceSouscritType"/>
#       </xs:sequence>
#    </xs:complexType>

#   <xs:complexType name="DonneesGeneralesType">
#       <xs:sequence>
#          <xs:element name="refFrn" type="ds:Chaine255Type" minOccurs="0"/>
#          <xs:element name="objetCode" type="ds:DemandeObjetCodeType"/>
#          <xs:element name="pointId" type="ds:PointIdType"/>
#          <xs:element name="initiateurLogin" type="ds:UtilisateurLoginType"/>
#          <xs:element name="contratId" type="ds:ContratIdType"/>
#       </xs:sequence>
#    </xs:complexType>

#    <xs:complexType name="ArretServiceSouscritType">
#       <xs:sequence>
#          <xs:element name="serviceSouscritId" type="ds:Chaine15Type"/>
#       </xs:sequence>
#    </xs:complexType>