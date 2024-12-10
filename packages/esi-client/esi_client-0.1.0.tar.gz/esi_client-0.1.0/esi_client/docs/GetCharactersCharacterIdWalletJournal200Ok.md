# GetCharactersCharacterIdWalletJournal200Ok

200 ok object

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date** | **datetime** | Date and time of transaction | 
**description** | **str** | The reason for the transaction, mirrors what is seen in the client | 
**id** | **int** | Unique journal reference ID | 
**ref_type** | **str** | \&quot;The transaction type for the given. transaction. Different transaction types will populate different attributes.\&quot; | 
**amount** | **float** | The amount of ISK given or taken from the wallet as a result of the given transaction. Positive when ISK is deposited into the wallet and negative when ISK is withdrawn | [optional] 
**balance** | **float** | Wallet balance after transaction occurred | [optional] 
**context_id** | **int** | An ID that gives extra context to the particular transaction. Because of legacy reasons the context is completely different per ref_type and means different things. It is also possible to not have a context_id | [optional] 
**context_id_type** | **str** | The type of the given context_id if present | [optional] 
**first_party_id** | **int** | The id of the first party involved in the transaction. This attribute has no consistency and is different or non existant for particular ref_types. The description attribute will help make sense of what this attribute means. For more info about the given ID it can be dropped into the /universe/names/ ESI route to determine its type and name | [optional] 
**reason** | **str** | The user stated reason for the transaction. Only applies to some ref_types | [optional] 
**second_party_id** | **int** | The id of the second party involved in the transaction. This attribute has no consistency and is different or non existant for particular ref_types. The description attribute will help make sense of what this attribute means. For more info about the given ID it can be dropped into the /universe/names/ ESI route to determine its type and name | [optional] 
**tax** | **float** | Tax amount received. Only applies to tax related transactions | [optional] 
**tax_receiver_id** | **int** | The corporation ID receiving any tax paid. Only applies to tax related transactions | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


