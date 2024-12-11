# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Optional, Union
from urllib.parse import urlencode
from . import _common
from . import _transformers as t
from . import types
from ._api_client import ApiClient
from ._common import get_value_by_path as getv
from ._common import set_value_by_path as setv
from .pagers import AsyncPager, Pager


def _GetTuningJobParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(to_object, ['_url', 'name'], getv(from_object, ['name']))

  return to_object


def _GetTuningJobParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(to_object, ['_url', 'name'], getv(from_object, ['name']))

  return to_object


def _ListTuningJobsConfig_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['page_size']) is not None:
    setv(
        parent_object, ['_query', 'pageSize'], getv(from_object, ['page_size'])
    )

  if getv(from_object, ['page_token']) is not None:
    setv(
        parent_object,
        ['_query', 'pageToken'],
        getv(from_object, ['page_token']),
    )

  if getv(from_object, ['filter']) is not None:
    setv(parent_object, ['_query', 'filter'], getv(from_object, ['filter']))

  return to_object


def _ListTuningJobsConfig_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['page_size']) is not None:
    setv(
        parent_object, ['_query', 'pageSize'], getv(from_object, ['page_size'])
    )

  if getv(from_object, ['page_token']) is not None:
    setv(
        parent_object,
        ['_query', 'pageToken'],
        getv(from_object, ['page_token']),
    )

  if getv(from_object, ['filter']) is not None:
    setv(parent_object, ['_query', 'filter'], getv(from_object, ['filter']))

  return to_object


def _ListTuningJobsParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _ListTuningJobsConfig_to_mldev(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _ListTuningJobsParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _ListTuningJobsConfig_to_vertex(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _TuningExample_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['text_input']) is not None:
    setv(to_object, ['textInput'], getv(from_object, ['text_input']))

  if getv(from_object, ['output']) is not None:
    setv(to_object, ['output'], getv(from_object, ['output']))

  return to_object


def _TuningExample_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['text_input']):
    raise ValueError('text_input parameter is not supported in Vertex AI.')

  if getv(from_object, ['output']):
    raise ValueError('output parameter is not supported in Vertex AI.')

  return to_object


def _TuningDataset_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['gcs_uri']):
    raise ValueError('gcs_uri parameter is not supported in Google AI.')

  if getv(from_object, ['examples']) is not None:
    setv(
        to_object,
        ['examples', 'examples'],
        [
            _TuningExample_to_mldev(api_client, item, to_object)
            for item in getv(from_object, ['examples'])
        ],
    )

  return to_object


def _TuningDataset_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['gcs_uri']) is not None:
    setv(
        parent_object,
        ['supervisedTuningSpec', 'trainingDatasetUri'],
        getv(from_object, ['gcs_uri']),
    )

  if getv(from_object, ['examples']):
    raise ValueError('examples parameter is not supported in Vertex AI.')

  return to_object


def _TuningValidationDataset_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['gcs_uri']):
    raise ValueError('gcs_uri parameter is not supported in Google AI.')

  return to_object


def _TuningValidationDataset_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['gcs_uri']) is not None:
    setv(to_object, ['validationDatasetUri'], getv(from_object, ['gcs_uri']))

  return to_object


def _CreateTuningJobConfig_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['validation_dataset']):
    raise ValueError(
        'validation_dataset parameter is not supported in Google AI.'
    )

  if getv(from_object, ['tuned_model_display_name']) is not None:
    setv(
        parent_object,
        ['displayName'],
        getv(from_object, ['tuned_model_display_name']),
    )

  if getv(from_object, ['description']):
    raise ValueError('description parameter is not supported in Google AI.')

  if getv(from_object, ['epoch_count']) is not None:
    setv(
        parent_object,
        ['tuningTask', 'hyperparameters', 'epochCount'],
        getv(from_object, ['epoch_count']),
    )

  if getv(from_object, ['learning_rate_multiplier']) is not None:
    setv(
        to_object,
        ['tuningTask', 'hyperparameters', 'learningRateMultiplier'],
        getv(from_object, ['learning_rate_multiplier']),
    )

  if getv(from_object, ['adapter_size']):
    raise ValueError('adapter_size parameter is not supported in Google AI.')

  if getv(from_object, ['batch_size']) is not None:
    setv(
        parent_object,
        ['tuningTask', 'hyperparameters', 'batchSize'],
        getv(from_object, ['batch_size']),
    )

  if getv(from_object, ['learning_rate']) is not None:
    setv(
        parent_object,
        ['tuningTask', 'hyperparameters', 'learningRate'],
        getv(from_object, ['learning_rate']),
    )

  return to_object


def _CreateTuningJobConfig_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['validation_dataset']) is not None:
    setv(
        parent_object,
        ['supervisedTuningSpec'],
        _TuningValidationDataset_to_vertex(
            api_client, getv(from_object, ['validation_dataset']), to_object
        ),
    )

  if getv(from_object, ['tuned_model_display_name']) is not None:
    setv(
        parent_object,
        ['tunedModelDisplayName'],
        getv(from_object, ['tuned_model_display_name']),
    )

  if getv(from_object, ['description']) is not None:
    setv(parent_object, ['description'], getv(from_object, ['description']))

  if getv(from_object, ['epoch_count']) is not None:
    setv(
        parent_object,
        ['supervisedTuningSpec', 'hyperParameters', 'epochCount'],
        getv(from_object, ['epoch_count']),
    )

  if getv(from_object, ['learning_rate_multiplier']) is not None:
    setv(
        to_object,
        ['supervisedTuningSpec', 'hyperParameters', 'learningRateMultiplier'],
        getv(from_object, ['learning_rate_multiplier']),
    )

  if getv(from_object, ['adapter_size']) is not None:
    setv(
        parent_object,
        ['supervisedTuningSpec', 'hyperParameters', 'adapterSize'],
        getv(from_object, ['adapter_size']),
    )

  if getv(from_object, ['batch_size']):
    raise ValueError('batch_size parameter is not supported in Vertex AI.')

  if getv(from_object, ['learning_rate']):
    raise ValueError('learning_rate parameter is not supported in Vertex AI.')

  return to_object


def _CreateTuningJobParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['base_model']) is not None:
    setv(to_object, ['baseModel'], getv(from_object, ['base_model']))

  if getv(from_object, ['training_dataset']) is not None:
    setv(
        to_object,
        ['tuningTask', 'trainingData'],
        _TuningDataset_to_mldev(
            api_client, getv(from_object, ['training_dataset']), to_object
        ),
    )

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _CreateTuningJobConfig_to_mldev(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _CreateTuningJobParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['base_model']) is not None:
    setv(to_object, ['baseModel'], getv(from_object, ['base_model']))

  if getv(from_object, ['training_dataset']) is not None:
    setv(
        to_object,
        ['supervisedTuningSpec', 'trainingDatasetUri'],
        _TuningDataset_to_vertex(
            api_client, getv(from_object, ['training_dataset']), to_object
        ),
    )

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _CreateTuningJobConfig_to_vertex(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _DistillationDataset_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['gcs_uri']):
    raise ValueError('gcs_uri parameter is not supported in Google AI.')

  return to_object


def _DistillationDataset_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['gcs_uri']) is not None:
    setv(
        parent_object,
        ['distillationSpec', 'trainingDatasetUri'],
        getv(from_object, ['gcs_uri']),
    )

  return to_object


def _DistillationValidationDataset_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['gcs_uri']):
    raise ValueError('gcs_uri parameter is not supported in Google AI.')

  return to_object


def _DistillationValidationDataset_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['gcs_uri']) is not None:
    setv(to_object, ['validationDatasetUri'], getv(from_object, ['gcs_uri']))

  return to_object


def _CreateDistillationJobConfig_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['validation_dataset']):
    raise ValueError(
        'validation_dataset parameter is not supported in Google AI.'
    )

  if getv(from_object, ['tuned_model_display_name']) is not None:
    setv(
        parent_object,
        ['displayName'],
        getv(from_object, ['tuned_model_display_name']),
    )

  if getv(from_object, ['epoch_count']) is not None:
    setv(
        parent_object,
        ['tuningTask', 'hyperparameters', 'epochCount'],
        getv(from_object, ['epoch_count']),
    )

  if getv(from_object, ['learning_rate_multiplier']) is not None:
    setv(
        parent_object,
        ['tuningTask', 'hyperparameters', 'learningRateMultiplier'],
        getv(from_object, ['learning_rate_multiplier']),
    )

  if getv(from_object, ['adapter_size']):
    raise ValueError('adapter_size parameter is not supported in Google AI.')

  if getv(from_object, ['pipeline_root_directory']):
    raise ValueError(
        'pipeline_root_directory parameter is not supported in Google AI.'
    )

  return to_object


def _CreateDistillationJobConfig_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['validation_dataset']) is not None:
    setv(
        parent_object,
        ['distillationSpec'],
        _DistillationValidationDataset_to_vertex(
            api_client, getv(from_object, ['validation_dataset']), to_object
        ),
    )

  if getv(from_object, ['tuned_model_display_name']) is not None:
    setv(
        parent_object,
        ['tunedModelDisplayName'],
        getv(from_object, ['tuned_model_display_name']),
    )

  if getv(from_object, ['epoch_count']) is not None:
    setv(
        parent_object,
        ['distillationSpec', 'hyperParameters', 'epochCount'],
        getv(from_object, ['epoch_count']),
    )

  if getv(from_object, ['learning_rate_multiplier']) is not None:
    setv(
        parent_object,
        ['distillationSpec', 'hyperParameters', 'learningRateMultiplier'],
        getv(from_object, ['learning_rate_multiplier']),
    )

  if getv(from_object, ['adapter_size']) is not None:
    setv(
        parent_object,
        ['distillationSpec', 'hyperParameters', 'adapterSize'],
        getv(from_object, ['adapter_size']),
    )

  if getv(from_object, ['pipeline_root_directory']) is not None:
    setv(
        parent_object,
        ['distillationSpec', 'pipelineRootDirectory'],
        getv(from_object, ['pipeline_root_directory']),
    )

  return to_object


def _CreateDistillationJobParameters_to_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['student_model']):
    raise ValueError('student_model parameter is not supported in Google AI.')

  if getv(from_object, ['teacher_model']):
    raise ValueError('teacher_model parameter is not supported in Google AI.')

  if getv(from_object, ['training_dataset']) is not None:
    setv(
        to_object,
        ['tuningTask', 'trainingData'],
        _DistillationDataset_to_mldev(
            api_client, getv(from_object, ['training_dataset']), to_object
        ),
    )

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _CreateDistillationJobConfig_to_mldev(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _CreateDistillationJobParameters_to_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['student_model']) is not None:
    setv(
        to_object,
        ['distillationSpec', 'studentModel'],
        getv(from_object, ['student_model']),
    )

  if getv(from_object, ['teacher_model']) is not None:
    setv(
        to_object,
        ['distillationSpec', 'baseTeacherModel'],
        getv(from_object, ['teacher_model']),
    )

  if getv(from_object, ['training_dataset']) is not None:
    setv(
        to_object,
        ['distillationSpec', 'trainingDatasetUri'],
        _DistillationDataset_to_vertex(
            api_client, getv(from_object, ['training_dataset']), to_object
        ),
    )

  if getv(from_object, ['config']) is not None:
    setv(
        to_object,
        ['config'],
        _CreateDistillationJobConfig_to_vertex(
            api_client, getv(from_object, ['config']), to_object
        ),
    )

  return to_object


def _TunedModel_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(to_object, ['model'], getv(from_object, ['name']))

  if getv(from_object, ['name']) is not None:
    setv(to_object, ['endpoint'], getv(from_object, ['name']))

  return to_object


def _TunedModel_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['model']) is not None:
    setv(to_object, ['model'], getv(from_object, ['model']))

  if getv(from_object, ['endpoint']) is not None:
    setv(to_object, ['endpoint'], getv(from_object, ['endpoint']))

  return to_object


def _TuningJob_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(to_object, ['name'], getv(from_object, ['name']))

  if getv(from_object, ['state']) is not None:
    setv(
        to_object,
        ['state'],
        t.t_tuning_job_status(api_client, getv(from_object, ['state'])),
    )

  if getv(from_object, ['createTime']) is not None:
    setv(to_object, ['create_time'], getv(from_object, ['createTime']))

  if getv(from_object, ['tuningTask', 'startTime']) is not None:
    setv(
        to_object,
        ['start_time'],
        getv(from_object, ['tuningTask', 'startTime']),
    )

  if getv(from_object, ['tuningTask', 'completeTime']) is not None:
    setv(
        to_object,
        ['end_time'],
        getv(from_object, ['tuningTask', 'completeTime']),
    )

  if getv(from_object, ['updateTime']) is not None:
    setv(to_object, ['update_time'], getv(from_object, ['updateTime']))

  if getv(from_object, ['description']) is not None:
    setv(to_object, ['description'], getv(from_object, ['description']))

  if getv(from_object, ['baseModel']) is not None:
    setv(to_object, ['base_model'], getv(from_object, ['baseModel']))

  if getv(from_object, ['_self']) is not None:
    setv(
        to_object,
        ['tuned_model'],
        _TunedModel_from_mldev(
            api_client, getv(from_object, ['_self']), to_object
        ),
    )

  if getv(from_object, ['experiment']) is not None:
    setv(to_object, ['experiment'], getv(from_object, ['experiment']))

  if getv(from_object, ['labels']) is not None:
    setv(to_object, ['labels'], getv(from_object, ['labels']))

  if getv(from_object, ['tunedModelDisplayName']) is not None:
    setv(
        to_object,
        ['tuned_model_display_name'],
        getv(from_object, ['tunedModelDisplayName']),
    )

  return to_object


def _TuningJob_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['name']) is not None:
    setv(to_object, ['name'], getv(from_object, ['name']))

  if getv(from_object, ['state']) is not None:
    setv(
        to_object,
        ['state'],
        t.t_tuning_job_status(api_client, getv(from_object, ['state'])),
    )

  if getv(from_object, ['createTime']) is not None:
    setv(to_object, ['create_time'], getv(from_object, ['createTime']))

  if getv(from_object, ['startTime']) is not None:
    setv(to_object, ['start_time'], getv(from_object, ['startTime']))

  if getv(from_object, ['endTime']) is not None:
    setv(to_object, ['end_time'], getv(from_object, ['endTime']))

  if getv(from_object, ['updateTime']) is not None:
    setv(to_object, ['update_time'], getv(from_object, ['updateTime']))

  if getv(from_object, ['error']) is not None:
    setv(to_object, ['error'], getv(from_object, ['error']))

  if getv(from_object, ['description']) is not None:
    setv(to_object, ['description'], getv(from_object, ['description']))

  if getv(from_object, ['baseModel']) is not None:
    setv(to_object, ['base_model'], getv(from_object, ['baseModel']))

  if getv(from_object, ['tunedModel']) is not None:
    setv(
        to_object,
        ['tuned_model'],
        _TunedModel_from_vertex(
            api_client, getv(from_object, ['tunedModel']), to_object
        ),
    )

  if getv(from_object, ['supervisedTuningSpec']) is not None:
    setv(
        to_object,
        ['supervised_tuning_spec'],
        getv(from_object, ['supervisedTuningSpec']),
    )

  if getv(from_object, ['tuningDataStats']) is not None:
    setv(
        to_object, ['tuning_data_stats'], getv(from_object, ['tuningDataStats'])
    )

  if getv(from_object, ['encryptionSpec']) is not None:
    setv(to_object, ['encryption_spec'], getv(from_object, ['encryptionSpec']))

  if getv(from_object, ['distillationSpec']) is not None:
    setv(
        to_object,
        ['distillation_spec'],
        getv(from_object, ['distillationSpec']),
    )

  if getv(from_object, ['partnerModelTuningSpec']) is not None:
    setv(
        to_object,
        ['partner_model_tuning_spec'],
        getv(from_object, ['partnerModelTuningSpec']),
    )

  if getv(from_object, ['pipelineJob']) is not None:
    setv(to_object, ['pipeline_job'], getv(from_object, ['pipelineJob']))

  if getv(from_object, ['experiment']) is not None:
    setv(to_object, ['experiment'], getv(from_object, ['experiment']))

  if getv(from_object, ['labels']) is not None:
    setv(to_object, ['labels'], getv(from_object, ['labels']))

  if getv(from_object, ['tunedModelDisplayName']) is not None:
    setv(
        to_object,
        ['tuned_model_display_name'],
        getv(from_object, ['tunedModelDisplayName']),
    )

  return to_object


def _ListTuningJobsResponse_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['nextPageToken']) is not None:
    setv(to_object, ['next_page_token'], getv(from_object, ['nextPageToken']))

  if getv(from_object, ['tunedModels']) is not None:
    setv(
        to_object,
        ['tuning_jobs'],
        [
            _TuningJob_from_mldev(api_client, item, to_object)
            for item in getv(from_object, ['tunedModels'])
        ],
    )

  return to_object


def _ListTuningJobsResponse_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['nextPageToken']) is not None:
    setv(to_object, ['next_page_token'], getv(from_object, ['nextPageToken']))

  if getv(from_object, ['tuningJobs']) is not None:
    setv(
        to_object,
        ['tuning_jobs'],
        [
            _TuningJob_from_vertex(api_client, item, to_object)
            for item in getv(from_object, ['tuningJobs'])
        ],
    )

  return to_object


def _TuningJobOrOperation_from_mldev(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['_self']) is not None:
    setv(
        to_object,
        ['tuning_job'],
        _TuningJob_from_mldev(
            api_client,
            t.t_resolve_operation(api_client, getv(from_object, ['_self'])),
            to_object,
        ),
    )

  return to_object


def _TuningJobOrOperation_from_vertex(
    api_client: ApiClient,
    from_object: Union[dict, object],
    parent_object: dict = None,
) -> dict:
  to_object = {}
  if getv(from_object, ['_self']) is not None:
    setv(
        to_object,
        ['tuning_job'],
        _TuningJob_from_vertex(
            api_client,
            t.t_resolve_operation(api_client, getv(from_object, ['_self'])),
            to_object,
        ),
    )

  return to_object


class Tunings(_common.BaseModule):

  def get(self, *, name: str) -> types.TuningJob:
    """Gets a TuningJob.

    Args:
      name: The resource name of the tuning job.

    Returns:
      A TuningJob object.
    """

    parameter_model = types._GetTuningJobParameters(
        name=name,
    )

    if self.api_client.vertexai:
      request_dict = _GetTuningJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = '{name}'.format_map(request_dict.get('_url'))
    else:
      request_dict = _GetTuningJobParameters_to_mldev(
          self.api_client, parameter_model
      )
      path = '{name}'.format_map(request_dict.get('_url'))
    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'get', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _TuningJob_from_vertex(self.api_client, response_dict)
    else:
      response_dict = _TuningJob_from_mldev(self.api_client, response_dict)

    return_value = types.TuningJob._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  def _list(
      self, *, config: Optional[types.ListTuningJobsConfigOrDict] = None
  ) -> types.ListTuningJobsResponse:
    """Lists tuning jobs.

    Args:
      config: The configuration for the list request.

    Returns:
      A list of tuning jobs.
    """

    parameter_model = types._ListTuningJobsParameters(
        config=config,
    )

    if self.api_client.vertexai:
      request_dict = _ListTuningJobsParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'tuningJobs'.format_map(request_dict.get('_url'))
    else:
      request_dict = _ListTuningJobsParameters_to_mldev(
          self.api_client, parameter_model
      )
      path = 'tunedModels'.format_map(request_dict.get('_url'))
    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'get', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _ListTuningJobsResponse_from_vertex(
          self.api_client, response_dict
      )
    else:
      response_dict = _ListTuningJobsResponse_from_mldev(
          self.api_client, response_dict
      )

    return_value = types.ListTuningJobsResponse._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  def tune(
      self,
      *,
      base_model: str,
      training_dataset: types.TuningDatasetOrDict,
      config: Optional[types.CreateTuningJobConfigOrDict] = None,
  ) -> types.TuningJobOrOperation:
    """Creates a supervised fine-tuning job.

    Args:
      base_model: The name of the model to tune.
      training_dataset: The training dataset to use.
      config: The configuration to use for the tuning job.

    Returns:
      A TuningJob object.
    """

    parameter_model = types._CreateTuningJobParameters(
        base_model=base_model,
        training_dataset=training_dataset,
        config=config,
    )

    if self.api_client.vertexai:
      request_dict = _CreateTuningJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'tuningJobs'.format_map(request_dict.get('_url'))
    else:
      request_dict = _CreateTuningJobParameters_to_mldev(
          self.api_client, parameter_model
      )
      path = 'tunedModels'.format_map(request_dict.get('_url'))
    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'post', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _TuningJobOrOperation_from_vertex(
          self.api_client, response_dict
      )
    else:
      response_dict = _TuningJobOrOperation_from_mldev(
          self.api_client, response_dict
      )

    return_value = types.TuningJobOrOperation._from_response(
        response_dict, parameter_model
    ).tuning_job
    self.api_client._verify_response(return_value)
    return return_value

  def distill(
      self,
      *,
      student_model: str,
      teacher_model: str,
      training_dataset: types.DistillationDatasetOrDict,
      config: Optional[types.CreateDistillationJobConfigOrDict] = None,
  ) -> types.TuningJob:
    """Creates a distillation job.

    Args:
      student_model: The name of the model to tune.
      teacher_model: The name of the model to distill from.
      training_dataset: The training dataset to use.
      config: The configuration to use for the distillation job.

    Returns:
      A TuningJob object.
    """

    parameter_model = types._CreateDistillationJobParameters(
        student_model=student_model,
        teacher_model=teacher_model,
        training_dataset=training_dataset,
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _CreateDistillationJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'tuningJobs'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = self.api_client.request(
        'post', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _TuningJob_from_vertex(self.api_client, response_dict)
    else:
      response_dict = _TuningJob_from_mldev(self.api_client, response_dict)

    return_value = types.TuningJob._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  def list(
      self, *, config: Optional[types.ListTuningJobsConfigOrDict] = None
  ) -> Pager[types.TuningJob]:
    return Pager(
        'tuning_jobs',
        self._list,
        self._list(config=config),
        config,
    )


class AsyncTunings(_common.BaseModule):

  async def get(self, *, name: str) -> types.TuningJob:
    """Gets a TuningJob.

    Args:
      name: The resource name of the tuning job.

    Returns:
      A TuningJob object.
    """

    parameter_model = types._GetTuningJobParameters(
        name=name,
    )

    if self.api_client.vertexai:
      request_dict = _GetTuningJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = '{name}'.format_map(request_dict.get('_url'))
    else:
      request_dict = _GetTuningJobParameters_to_mldev(
          self.api_client, parameter_model
      )
      path = '{name}'.format_map(request_dict.get('_url'))
    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'get', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _TuningJob_from_vertex(self.api_client, response_dict)
    else:
      response_dict = _TuningJob_from_mldev(self.api_client, response_dict)

    return_value = types.TuningJob._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  async def _list(
      self, *, config: Optional[types.ListTuningJobsConfigOrDict] = None
  ) -> types.ListTuningJobsResponse:
    """Lists tuning jobs.

    Args:
      config: The configuration for the list request.

    Returns:
      A list of tuning jobs.
    """

    parameter_model = types._ListTuningJobsParameters(
        config=config,
    )

    if self.api_client.vertexai:
      request_dict = _ListTuningJobsParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'tuningJobs'.format_map(request_dict.get('_url'))
    else:
      request_dict = _ListTuningJobsParameters_to_mldev(
          self.api_client, parameter_model
      )
      path = 'tunedModels'.format_map(request_dict.get('_url'))
    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'get', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _ListTuningJobsResponse_from_vertex(
          self.api_client, response_dict
      )
    else:
      response_dict = _ListTuningJobsResponse_from_mldev(
          self.api_client, response_dict
      )

    return_value = types.ListTuningJobsResponse._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  async def tune(
      self,
      *,
      base_model: str,
      training_dataset: types.TuningDatasetOrDict,
      config: Optional[types.CreateTuningJobConfigOrDict] = None,
  ) -> types.TuningJobOrOperation:
    """Creates a supervised fine-tuning job.

    Args:
      base_model: The name of the model to tune.
      training_dataset: The training dataset to use.
      config: The configuration to use for the tuning job.

    Returns:
      A TuningJob object.
    """

    parameter_model = types._CreateTuningJobParameters(
        base_model=base_model,
        training_dataset=training_dataset,
        config=config,
    )

    if self.api_client.vertexai:
      request_dict = _CreateTuningJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'tuningJobs'.format_map(request_dict.get('_url'))
    else:
      request_dict = _CreateTuningJobParameters_to_mldev(
          self.api_client, parameter_model
      )
      path = 'tunedModels'.format_map(request_dict.get('_url'))
    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'post', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _TuningJobOrOperation_from_vertex(
          self.api_client, response_dict
      )
    else:
      response_dict = _TuningJobOrOperation_from_mldev(
          self.api_client, response_dict
      )

    return_value = types.TuningJobOrOperation._from_response(
        response_dict, parameter_model
    ).tuning_job
    self.api_client._verify_response(return_value)
    return return_value

  async def distill(
      self,
      *,
      student_model: str,
      teacher_model: str,
      training_dataset: types.DistillationDatasetOrDict,
      config: Optional[types.CreateDistillationJobConfigOrDict] = None,
  ) -> types.TuningJob:
    """Creates a distillation job.

    Args:
      student_model: The name of the model to tune.
      teacher_model: The name of the model to distill from.
      training_dataset: The training dataset to use.
      config: The configuration to use for the distillation job.

    Returns:
      A TuningJob object.
    """

    parameter_model = types._CreateDistillationJobParameters(
        student_model=student_model,
        teacher_model=teacher_model,
        training_dataset=training_dataset,
        config=config,
    )

    if not self.api_client.vertexai:
      raise ValueError('This method is only supported in the Vertex AI client.')
    else:
      request_dict = _CreateDistillationJobParameters_to_vertex(
          self.api_client, parameter_model
      )
      path = 'tuningJobs'.format_map(request_dict.get('_url'))

    query_params = request_dict.get('_query')
    if query_params:
      path = f'{path}?{urlencode(query_params)}'
    # TODO: remove the hack that pops config.
    config = request_dict.pop('config', None)
    http_options = config.pop('httpOptions', None) if config else None
    request_dict = _common.convert_to_dict(request_dict)
    request_dict = _common.apply_base64_encoding(request_dict)

    response_dict = await self.api_client.async_request(
        'post', path, request_dict, http_options
    )

    if self.api_client.vertexai:
      response_dict = _TuningJob_from_vertex(self.api_client, response_dict)
    else:
      response_dict = _TuningJob_from_mldev(self.api_client, response_dict)

    return_value = types.TuningJob._from_response(
        response_dict, parameter_model
    )
    self.api_client._verify_response(return_value)
    return return_value

  async def list(
      self, *, config: Optional[types.ListTuningJobsConfigOrDict] = None
  ) -> AsyncPager[types.TuningJob]:
    return AsyncPager(
        'tuning_jobs',
        self._list,
        await self._list(config=config),
        config,
    )
