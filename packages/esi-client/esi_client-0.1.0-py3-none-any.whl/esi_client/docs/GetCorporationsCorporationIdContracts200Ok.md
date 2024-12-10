# GetCorporationsCorporationIdContracts200Ok

200 ok object

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**acceptor_id** | **int** | Who will accept the contract | 
**assignee_id** | **int** | ID to whom the contract is assigned, can be corporation or character ID | 
**availability** | **str** | To whom the contract is available | 
**contract_id** | **int** | contract_id integer | 
**date_expired** | **datetime** | Expiration date of the contract | 
**date_issued** | **datetime** | Сreation date of the contract | 
**for_corporation** | **bool** | true if the contract was issued on behalf of the issuer&#39;s corporation | 
**issuer_corporation_id** | **int** | Character&#39;s corporation ID for the issuer | 
**issuer_id** | **int** | Character ID for the issuer | 
**status** | **str** | Status of the the contract | 
**type** | **str** | Type of the contract | 
**buyout** | **float** | Buyout price (for Auctions only) | [optional] 
**collateral** | **float** | Collateral price (for Couriers only) | [optional] 
**date_accepted** | **datetime** | Date of confirmation of contract | [optional] 
**date_completed** | **datetime** | Date of completed of contract | [optional] 
**days_to_complete** | **int** | Number of days to perform the contract | [optional] 
**end_location_id** | **int** | End location ID (for Couriers contract) | [optional] 
**price** | **float** | Price of contract (for ItemsExchange and Auctions) | [optional] 
**reward** | **float** | Remuneration for contract (for Couriers only) | [optional] 
**start_location_id** | **int** | Start location ID (for Couriers contract) | [optional] 
**title** | **str** | Title of the contract | [optional] 
**volume** | **float** | Volume of items in the contract | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


