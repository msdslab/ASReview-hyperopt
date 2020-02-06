# Copyright 2020 The ASReview Authors. All Rights Reserved.
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

import logging
import os
from os.path import join, splitext


def empty_shared():
    return {
        "query_src": {},
        "current_queries": {}
    }


def quality(result_list, alpha=1):
    q = 0
    for _, rank in result_list:
        q += rank**alpha

    return (q/len(result_list))**(1/alpha)


def get_trial_fp(datasets, model_name=None, query_name=None, balance_name=None,
                 feature_name=None, hyper_type="passive"):

    name_list = [
        name for name in [model_name, query_name, balance_name, feature_name]
        if name is not None
    ]

    trials_dir = join("output", hyper_type, "_".join(name_list),
                      "_".join(datasets))
    os.makedirs(trials_dir, exist_ok=True)
    trials_fp = os.path.join(trials_dir, f"trials.pkl")

    return trials_dir, trials_fp


def get_data_names(datasets, data_dir="data"):
    data_dir = "data"
    file_list = os.listdir(data_dir)
    file_list = [file_name for file_name in file_list
                 if file_name.endswith((".csv", ".xlsx", ".ris"))]
    if "all" not in datasets:
        file_list = [file_name for file_name in file_list
                     if splitext(file_name)[0] in datasets]
    return [splitext(file_name)[0] for file_name in file_list]


def _get_prefix_param(raw_param, prefix):
    return {key[4:]: value for key, value in raw_param.items()
            if key[:4] == prefix}


def get_split_param(raw_param):
    split_param = {
        "model_param": _get_prefix_param(raw_param, "mdl_"),
        "query_param": _get_prefix_param(raw_param, "qry_"),
        "balance_param": _get_prefix_param(raw_param, "bal_"),
        "feature_param": _get_prefix_param(raw_param, "fex_"),
    }
    merge_param = {}
    for param in split_param.values():
        merge_param.update(param)

    for param in raw_param:
        if param[4:] not in merge_param:
            logging.warning(f"Warning: parameter {param} is being ignored.")
            print(merge_param)
    return split_param


def data_fp_from_name(data_dir, data_name):
    file_list = os.listdir(data_dir)
    file_list = [file_name for file_name in file_list
                 if file_name.endswith((".csv", ".xlsx", ".ris")) and
                 os.path.splitext(file_name)[0] == data_name]
    return join(data_dir, file_list[0])


def get_out_dir(trials_dir, data_name):
    out_dir = join(trials_dir, "current", data_name)
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def get_out_fp(trials_dir, data_name, i_run):
    return join(get_out_dir(trials_dir, data_name),
                f"results_{i_run}.json")


def get_label_fp(trials_dir, data_name):
    return join(get_out_dir(trials_dir, data_name), "labels.json")
