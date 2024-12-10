# GetCorporationsCorporationIdStructures200Ok

200 ok object

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**corporation_id** | **int** | ID of the corporation that owns the structure | 
**profile_id** | **int** | The id of the ACL profile for this citadel | 
**state** | **str** | state string | 
**structure_id** | **int** | The Item ID of the structure | 
**system_id** | **int** | The solar system the structure is in | 
**type_id** | **int** | The type id of the structure | 
**fuel_expires** | **datetime** | Date on which the structure will run out of fuel | [optional] 
**name** | **str** | The structure name | [optional] 
**next_reinforce_apply** | **datetime** | The date and time when the structure&#39;s newly requested reinforcement times (e.g. next_reinforce_hour and next_reinforce_day) will take effect | [optional] 
**next_reinforce_hour** | **int** | The requested change to reinforce_hour that will take effect at the time shown by next_reinforce_apply | [optional] 
**reinforce_hour** | **int** | The hour of day that determines the four hour window when the structure will randomly exit its reinforcement periods and become vulnerable to attack against its armor and/or hull. The structure will become vulnerable at a random time that is +/- 2 hours centered on the value of this property | [optional] 
**services** | [**[GetCorporationsCorporationIdStructuresService]**](GetCorporationsCorporationIdStructuresService.md) | Contains a list of service upgrades, and their state | [optional] 
**state_timer_end** | **datetime** | Date at which the structure will move to it&#39;s next state | [optional] 
**state_timer_start** | **datetime** | Date at which the structure entered it&#39;s current state | [optional] 
**unanchors_at** | **datetime** | Date at which the structure will unanchor | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


