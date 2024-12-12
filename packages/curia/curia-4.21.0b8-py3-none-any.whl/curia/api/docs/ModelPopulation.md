# ModelPopulation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**query_count_status** | **str** |  | [optional] 
**query_count_error** | **str** |  | [optional] 
**query_list_status** | **str** |  | [optional] 
**query_list_error** | **str** |  | [optional] 
**query_all_status** | **str** |  | [optional] 
**query_all_error** | **str** |  | [optional] 
**query_count_started_at** | **datetime** |  | [optional] 
**query_count_ended_at** | **datetime** |  | [optional] 
**query_list_started_at** | **datetime** |  | [optional] 
**query_list_ended_at** | **datetime** |  | [optional] 
**query_all_started_at** | **datetime** |  | [optional] 
**query_all_ended_at** | **datetime** |  | [optional] 
**organization_id** | **str** |  | [optional] 
**organization** | [**Organization**](Organization.md) |  | [optional] 
**population_id** | **str** |  | [optional] 
**population** | [**Population**](Population.md) |  | [optional] 
**cohorts** | [**list[CohortDefinition]**](CohortDefinition.md) |  | [optional] 
**outcome** | [**OutcomeDefinition**](OutcomeDefinition.md) |  | [optional] 
**intervention** | [**InterventionDefinition**](InterventionDefinition.md) |  | [optional] 
**features** | [**list[Feature]**](Feature.md) |  | [optional] 
**tecton_features** | [**list[TectonFeature]**](TectonFeature.md) |  | [optional] 
**cohort_results** | [**list[CohortResults]**](CohortResults.md) |  | [optional] 
**data_query_id** | **str** |  | [optional] 
**data_query** | [**DataQuery**](DataQuery.md) |  | [optional] 
**outcome_distribution_histogram_query_id** | **str** |  | [optional] 
**outcome_distribution_histogram_query** | [**DataQuery**](DataQuery.md) |  | [optional] 
**model_jobs** | [**list[ModelJob]**](ModelJob.md) |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**created_by** | **str** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**archived_at** | **datetime** |  | [optional] 
**last_updated_by** | **str** |  | [optional] 
**version** | **float** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

