from __future__ import annotations

from enum import Enum


class ClusterSelMethod(Enum):
    none = "none"
    static = "static"


class AppManagerAppStatus(Enum):
    running = "running"
    stopped = "stopped"
    updating = "updating"
    requires_attention = "requires_attention"


class DataType(Enum):
    boolean = "boolean"
    number = "number"
    object = "object"
    string = "string"


class AppType(Enum):
    kelvin = "kelvin"
    docker = "docker"
    bridge = "bridge"


class AssetState(Enum):
    online = "online"
    offline = "offline"
    unknown = "unknown"


class PropertyType(Enum):
    boolean = "boolean"
    number = "number"
    string = "string"
    timestamp = "timestamp"


class ControlChangeState(Enum):
    pending = "pending"
    ready = "ready"
    sent = "sent"
    processed = "processed"
    applied = "applied"
    failed = "failed"
    rejected = "rejected"


class ParameterType(Enum):
    raw_boolean = "raw.boolean"
    raw_float32 = "raw.float32"
    raw_float64 = "raw.float64"
    raw_int32 = "raw.int32"
    raw_uint32 = "raw.uint32"
    raw_text = "raw.text"
    number = "number"
    string = "string"
    boolean = "boolean"


class RecommendationState(Enum):
    pending = "pending"
    accepted = "accepted"
    auto_accepted = "auto_accepted"
    rejected = "rejected"
    expired = "expired"
    error = "error"


class WorkloadStatus(Enum):
    pending_deploy = "pending_deploy"
    pending_update = "pending_update"
    pending_start = "pending_start"
    pending_stop = "pending_stop"
    pending_apply = "pending_apply"
    deploying = "deploying"
    running = "running"
    stopping = "stopping"
    stopped = "stopped"
    failed = "failed"
    starting = "starting"
    received = "received"
    downloading = "downloading"
    ready = "ready"
    unreachable = "unreachable"
    staged = "staged"


class ControlChangeSource(Enum):
    bridge = "bridge"
    ccm = "ccm"


class GuardrailRelativeType(Enum):
    VALUE = "value"
    PERCENTAGE = "percentage"


class ClusterType(Enum):
    k3s = "k3s"
    kubernetes = "kubernetes"


class OrchestrationClusterStatus(Enum):
    pending_provision = "pending_provision"
    pending = "pending"
    online = "online"
    unreachable = "unreachable"
    requires_attention = "requires_attention"


class OrchestrationNodeStatus(Enum):
    online = "online"
    unreachable = "unreachable"
    not_ready = "not_ready"


class ParameterScheduleState(Enum):
    scheduled = "scheduled"
    scheduled_revert = "scheduled-revert"
    completed = "completed"
    error = "error"


class ResourceType(Enum):
    asset = "asset"
    datastream = "datastream"
    app = "app"
    parameter = "parameter"


class RolePolicyAction(Enum):
    field_ = "*"
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class WorkloadDownloadStatus(Enum):
    pending = "pending"
    scheduled = "scheduled"
    processing = "processing"
    downloading = "downloading"
    ready = "ready"
    failed = "failed"
