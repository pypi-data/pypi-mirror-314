# GetWarsWarIdOk

200 ok object

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggressor** | [**GetWarsWarIdAggressor**](GetWarsWarIdAggressor.md) |  | 
**declared** | **datetime** | Time that the war was declared | 
**defender** | [**GetWarsWarIdDefender**](GetWarsWarIdDefender.md) |  | 
**id** | **int** | ID of the specified war | 
**mutual** | **bool** | Was the war declared mutual by both parties | 
**open_for_allies** | **bool** | Is the war currently open for allies or not | 
**allies** | [**[GetWarsWarIdAlly]**](GetWarsWarIdAlly.md) | allied corporations or alliances, each object contains either corporation_id or alliance_id | [optional] 
**finished** | **datetime** | Time the war ended and shooting was no longer allowed | [optional] 
**retracted** | **datetime** | Time the war was retracted but both sides could still shoot each other | [optional] 
**started** | **datetime** | Time when the war started and both sides could shoot each other | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


