# TaskExecutionResponseDto

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**last_updated_by** | **str** |  | [optional] 
**created_by** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**archived_at** | **datetime** |  | [optional] 
**version** | **float** |  | [optional] 
**workflow_execution** | [**TaskExecutionJoinedWorkflowExecutionResponseDto**](TaskExecutionJoinedWorkflowExecutionResponseDto.md) |  | [optional] 
**task** | [**TaskExecutionJoinedTaskResponseDto**](TaskExecutionJoinedTaskResponseDto.md) |  | [optional] 
**task_id** | **str** |  | 
**workflow_execution_id** | **str** |  | 
**node_name** | **str** |  | [optional] 
**run_id** | **str** |  | [optional] 
**status** | **object** |  | [optional] 
**inputs** | [**TaskInputs**](TaskInputs.md) |  | [optional] 
**outputs** | [**TaskOutputs**](TaskOutputs.md) |  | [optional] 
**queued_at** | **datetime** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**ended_at** | **datetime** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

