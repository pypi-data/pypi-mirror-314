#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   config.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   SDK config module
"""

# Default configurations
ASSET_UPLOAD_SESSION_BATCH_SIZE: int = 5000
ANNOTATION_IMPORT_SESSION_MAX_SIZE: int = 100000
ANNOTATION_IMPORT_SESSION_BATCH_SIZE: int = 1000
ANNOTATION_IMPORT_SESSION_BATCH_BYTES: int = 1.024e9
OPERATION_LOOPING_TIMEOUT_SECONDS: int = 36000
OPERATION_LOOPING_DELAY_SECONDS: int = 8
REQUEST_TIME_OUT_SECONDS = (60, 3600)
