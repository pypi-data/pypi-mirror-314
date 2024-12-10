# GetCorporationsCorporationIdStarbasesStarbaseIdOk

200 ok object

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allow_alliance_members** | **bool** | allow_alliance_members boolean | 
**allow_corporation_members** | **bool** | allow_corporation_members boolean | 
**anchor** | **str** | Who can anchor starbase (POS) and its structures | 
**attack_if_at_war** | **bool** | attack_if_at_war boolean | 
**attack_if_other_security_status_dropping** | **bool** | attack_if_other_security_status_dropping boolean | 
**fuel_bay_take** | **str** | Who can take fuel blocks out of the starbase (POS)&#39;s fuel bay | 
**fuel_bay_view** | **str** | Who can view the starbase (POS)&#39;s fule bay. Characters either need to have required role or belong to the starbase (POS) owner&#39;s corporation or alliance, as described by the enum, all other access settings follows the same scheme | 
**offline** | **str** | Who can offline starbase (POS) and its structures | 
**online** | **str** | Who can online starbase (POS) and its structures | 
**unanchor** | **str** | Who can unanchor starbase (POS) and its structures | 
**use_alliance_standings** | **bool** | True if the starbase (POS) is using alliance standings, otherwise using corporation&#39;s | 
**attack_security_status_threshold** | **float** | Starbase (POS) will attack if target&#39;s security standing is lower than this value | [optional] 
**attack_standing_threshold** | **float** | Starbase (POS) will attack if target&#39;s standing is lower than this value | [optional] 
**fuels** | [**[GetCorporationsCorporationIdStarbasesStarbaseIdFuel]**](GetCorporationsCorporationIdStarbasesStarbaseIdFuel.md) | Fuel blocks and other things that will be consumed when operating a starbase (POS) | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


