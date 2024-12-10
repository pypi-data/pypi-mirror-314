# GetCorporationsCorporationIdStarbases200Ok

200 ok object

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**starbase_id** | **int** | Unique ID for this starbase (POS) | 
**system_id** | **int** | The solar system this starbase (POS) is in, unanchored POSes have this information | 
**type_id** | **int** | Starbase (POS) type | 
**moon_id** | **int** | The moon this starbase (POS) is anchored on, unanchored POSes do not have this information | [optional] 
**onlined_since** | **datetime** | When the POS onlined, for starbases (POSes) in online state | [optional] 
**reinforced_until** | **datetime** | When the POS will be out of reinforcement, for starbases (POSes) in reinforced state | [optional] 
**state** | **str** | state string | [optional] 
**unanchor_at** | **datetime** | When the POS started unanchoring, for starbases (POSes) in unanchoring state | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


