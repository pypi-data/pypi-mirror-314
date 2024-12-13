<a id="documentation-for-api-endpoints"></a>
## Documentation for API Endpoints

All URIs are relative to *https://fbn-prd.lusid.com/scheduler2*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ApplicationMetadataApi* | [**list_access_controlled_resources**](docs/ApplicationMetadataApi.md#list_access_controlled_resources) | **GET** /api/metadata/access/resources | [EXPERIMENTAL] ListAccessControlledResources: Get resources available for access control
*ImagesApi* | [**delete_image**](docs/ImagesApi.md#delete_image) | **DELETE** /api/images/{name} | [EXPERIMENTAL] DeleteImage: Delete a Docker Image
*ImagesApi* | [**download_image**](docs/ImagesApi.md#download_image) | **GET** /api/images/{name}/contents | [EXPERIMENTAL] DownloadImage: Download Docker Image
*ImagesApi* | [**get_image**](docs/ImagesApi.md#get_image) | **GET** /api/images/{name} | [EXPERIMENTAL] GetImage: Get metadata of a Docker Image
*ImagesApi* | [**list_images**](docs/ImagesApi.md#list_images) | **GET** /api/images/repository/{name} | [EXPERIMENTAL] ListImages: List all images under same image repository
*ImagesApi* | [**list_repositories**](docs/ImagesApi.md#list_repositories) | **GET** /api/images/repository | [EXPERIMENTAL] ListRepositories: List all Docker image repositories
*ImagesApi* | [**upload_image**](docs/ImagesApi.md#upload_image) | **POST** /api/images | [EXPERIMENTAL] UploadImage: Upload a Docker Image used for Scheduler jobs
*JobsApi* | [**create_job**](docs/JobsApi.md#create_job) | **POST** /api/jobs | [EXPERIMENTAL] CreateJob: Create a new job
*JobsApi* | [**delete_job**](docs/JobsApi.md#delete_job) | **DELETE** /api/jobs/{scope}/{code} | [EXPERIMENTAL] DeleteJob: Delete a job
*JobsApi* | [**get_history**](docs/JobsApi.md#get_history) | **GET** /api/jobs/history | [EXPERIMENTAL] GetHistory: Get the history of job runs
*JobsApi* | [**get_job_console_output**](docs/JobsApi.md#get_job_console_output) | **GET** /api/jobs/history/{runId}/console | [EXPERIMENTAL] GetJobConsoleOutput: Gets the console output of a specific job run
*JobsApi* | [**get_run_history**](docs/JobsApi.md#get_run_history) | **GET** /api/jobs/history/{runId} | [EXPERIMENTAL] GetRunHistory: Get the history for a single job run
*JobsApi* | [**get_schedules_for_a_job**](docs/JobsApi.md#get_schedules_for_a_job) | **GET** /api/jobs/{scope}/{code}/schedules | [EXPERIMENTAL] GetSchedulesForAJob: Get all the schedules for a single job
*JobsApi* | [**list_jobs**](docs/JobsApi.md#list_jobs) | **GET** /api/jobs | [EXPERIMENTAL] ListJobs: List the available jobs
*JobsApi* | [**run_job**](docs/JobsApi.md#run_job) | **POST** /api/jobs/{scope}/{code}/$run | RunJob: Run a job immediately
*JobsApi* | [**update_job**](docs/JobsApi.md#update_job) | **PUT** /api/jobs/{scope}/{code} | [EXPERIMENTAL] UpdateJob: Update a JobDefinition
*SchedulesApi* | [**create_schedule**](docs/SchedulesApi.md#create_schedule) | **POST** /api/schedules | [EXPERIMENTAL] CreateSchedule: Create a Schedule for a job
*SchedulesApi* | [**delete_schedule**](docs/SchedulesApi.md#delete_schedule) | **DELETE** /api/schedules/{scope}/{code} | [EXPERIMENTAL] DeleteSchedule: Delete a schedule
*SchedulesApi* | [**enabled_schedule**](docs/SchedulesApi.md#enabled_schedule) | **PUT** /api/schedules/{scope}/{code}/enabled | [EXPERIMENTAL] EnabledSchedule: Enable/disable a schedule
*SchedulesApi* | [**get_schedule**](docs/SchedulesApi.md#get_schedule) | **GET** /api/schedules/{scope}/{code} | [EXPERIMENTAL] GetSchedule: Get a single Schedule
*SchedulesApi* | [**list_schedules**](docs/SchedulesApi.md#list_schedules) | **GET** /api/schedules | [EXPERIMENTAL] ListSchedules: List the available Schedules
*SchedulesApi* | [**run_schedule**](docs/SchedulesApi.md#run_schedule) | **POST** /api/schedules/{scope}/{code}/$run | [EXPERIMENTAL] RunSchedule: Run a schedule immediately
*SchedulesApi* | [**update_schedule**](docs/SchedulesApi.md#update_schedule) | **PUT** /api/schedules/{scope}/{code} | [EXPERIMENTAL] UpdateSchedule: Update a schedule.


<a id="documentation-for-models"></a>
## Documentation for Models

 - [AccessControlledAction](docs/AccessControlledAction.md)
 - [AccessControlledResource](docs/AccessControlledResource.md)
 - [ActionId](docs/ActionId.md)
 - [ArgumentDefinition](docs/ArgumentDefinition.md)
 - [CreateJobRequest](docs/CreateJobRequest.md)
 - [CreateScheduleRequest](docs/CreateScheduleRequest.md)
 - [IdSelectorDefinition](docs/IdSelectorDefinition.md)
 - [IdentifierPartSchema](docs/IdentifierPartSchema.md)
 - [Image](docs/Image.md)
 - [ImageSummary](docs/ImageSummary.md)
 - [JobDefinition](docs/JobDefinition.md)
 - [JobHistory](docs/JobHistory.md)
 - [JobRunResult](docs/JobRunResult.md)
 - [Link](docs/Link.md)
 - [LusidProblemDetails](docs/LusidProblemDetails.md)
 - [LusidValidationProblemDetails](docs/LusidValidationProblemDetails.md)
 - [Notification](docs/Notification.md)
 - [Repository](docs/Repository.md)
 - [RequiredResources](docs/RequiredResources.md)
 - [ResourceId](docs/ResourceId.md)
 - [ResourceListOfAccessControlledResource](docs/ResourceListOfAccessControlledResource.md)
 - [ResourceListOfImageSummary](docs/ResourceListOfImageSummary.md)
 - [ResourceListOfJobDefinition](docs/ResourceListOfJobDefinition.md)
 - [ResourceListOfJobHistory](docs/ResourceListOfJobHistory.md)
 - [ResourceListOfRepository](docs/ResourceListOfRepository.md)
 - [ResourceListOfScheduleDefinition](docs/ResourceListOfScheduleDefinition.md)
 - [ScanReport](docs/ScanReport.md)
 - [ScanSummary](docs/ScanSummary.md)
 - [ScheduleDefinition](docs/ScheduleDefinition.md)
 - [StartJobRequest](docs/StartJobRequest.md)
 - [StartJobResponse](docs/StartJobResponse.md)
 - [StartScheduleResponse](docs/StartScheduleResponse.md)
 - [Tag](docs/Tag.md)
 - [TimeTrigger](docs/TimeTrigger.md)
 - [Trigger](docs/Trigger.md)
 - [UpdateJobRequest](docs/UpdateJobRequest.md)
 - [UpdateScheduleRequest](docs/UpdateScheduleRequest.md)
 - [UploadImageInstructions](docs/UploadImageInstructions.md)
 - [UploadImageRequest](docs/UploadImageRequest.md)
 - [Vulnerability](docs/Vulnerability.md)

