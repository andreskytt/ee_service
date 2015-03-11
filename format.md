# SDF format specification

## Background & intro
-----
The service description file (SDF) format described in this document is meant to distribute public service information. It relies heavily on CPSV (<http://joinup.ec.europa.eu/site/core_vocabularies/Core_Vocabularies_v1.1>) and JSON-LD for the vocabulary and file format respectively. The format is specified in terms of sufficient requirements. The actual files can contain much more information but certain bits are necessary for the service aggregation machinery to work.

## The file
----
An SDF file is an array of service objects. A service object is one of the following JSON objects:

* A legal identity identified by a CPSV type **LegalEntity** that specifies the CPSV Agent type
* A service description identified by a CPSV type **PublicService**
* An URL of another SDF file identified by a **http://meta.eesti.ee/tüüp/SDF/SDFReference** type 

## The requirements
----
* Each LegalEntity and PublicService object **must** have a **@id** attribute that is unique within the service scope. A URI is preferable
* Each LegalEntity **must** have an attribute of type **CPSV:LegalName** 
* If a LegalEntity provides services, the object **must** contain an attribute of type **CPSV:Provides** the **@value** of which **must** contain an array of service identifiers
* Each PublicService object **must** have an attribute of type **CPSV:Name**
* A PublicService object **may** contain an attribute of type **CPSV:ProvidedBy**. This is an utility extension of the CPSV vocabulary that is *not* part of the core specification. It's @value attribute can contain both an @id or **CPSV:LegalIdentifier** of a service provide
* A SDF reference of type **http://meta.eesti.ee/tüüp/SDF/SDFReference** **must** have an **@value** attribute

## An example
----
```
[
    {
        "@context": {
            "CPSV": "http://joinup.ec.europa.eu/site/core_vocabularies/Core_Vocabularies_v1.1"
        },
        "@id": "http://register.fin.ee/RKOAR/70000303",
        "@type": "LegalEntity",
        "JurID": {
            "@type": "CPSV:LegalIdentifier",
            "@value": "http://register.fin.ee/RKOAR/70000303"
        },
        "JurNimi": {
            "@type": "CPSV:LegalName",
            "@value": "Konkurentsiamet"
        },
        "Tüüp": {
            "@type": "CPSV:CompanyType",
            "@value": "https://riha.eesti.ee/riha/main/kla/esa_institutsionaalsete_sektorite_s_eesti_jaoks_kohandatud_klassifikaator_2010/S.13111"
        },
        "pakub": {
            "@type": "CPSV:Provides",
            "@value": [
                "http://www.mkm.ee/teenused/Raudteeseaduse_tegevuslubade_taotlemine",
                "http://www.mkm.ee/teenused/Elektrituruseaduse_tegevuslubade_taotlemine"
            ]
        }
    },
 {
"@context": {
            "CPSV": "http://joinup.ec.europa.eu/site/core_vocabularies/Core_Vocabularies_v1.1"
        },
        "@id": "http://www.mkm.ee/teenused/Raudteeseaduse_tegevuslubade_taotlemine",
        "@type": "PublicService",
        "Keel": {
            "@type": "CPSV:Language",
            "@value": "https://riha.eesti.ee/riha/main/kla/keelte_klassifikaator_2013/est"
        },
        "Kirjeldus": {
            "@type": "CPSV:Description",
            "@value": "\"Tegevusluba on vaja taotleda, kui ettevõtja soovib tegutseda raudteevaldkonnas ning osutada järgmiseid teenuseid: avaliku raudteeinfrastruktuuri majandamine; raudtee reisijatevedu; raudtee kaubavedu.\""
        },
        "Koduleht": {
            "@type": "CPSV:Homepage",
            "@value": "https://mtr.mkm.ee/"
        },
        "Nimi": {
            "@type": "CPSV:Name",
            "@value": "Raudteeseaduse tegevuslubade taotlemine"
        },
        "Sihtrühm": "\"Ettevõtja,\"",
        "Teenuseosutaja": {
            "@type": "CPSV:ProvidedBy",
            "@value": "http://register.fin.ee/RKOAR/70000303"
        },
        "Tüüp": {
            "@type": "CPSV:Type",
            "@value": "Liitumine/Registreerimine"                                                                                                                
        },                                                                                                                                                       
        "Valdkond": "Raudteetransport"                                                                                                                           
    },
{
	"@type":"http://meta.eesti.ee/tüüp/SDF/SDFReference",
	"@value": "https://raw.githubusercontent.com/andreskytt/ee_service/master/sample_service.json"
}                         
]

```
 

