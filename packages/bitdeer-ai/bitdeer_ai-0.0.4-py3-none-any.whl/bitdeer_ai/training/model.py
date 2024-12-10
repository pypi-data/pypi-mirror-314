from pydantic import BaseModel
from typing import List, Optional
from enum import IntEnum
from .training_pb2 import (
    CreateTrainingJobResponse,
    GetTrainingJobResponse,
    ListTrainingJobsResponse,
    GetTrainingJobWorkersResponse,
    GetTrainingJobLogsResponse,
    WorkerInfo
)


class JobType(IntEnum):
    TORCH_JOB = 1
    TF_JOB = 2
    MPI_JOB = 3

class JobStatus(IntEnum):
    PENDING = 1
    SCHEDULING = 2
    RUNNING = 3
    COMPLETED = 4
    FAILED = 5
    SUSPENDED = 6
    RESTARTING = 7
    SUSPENDING = 8

class Worker(BaseModel):
    name: str
    status: Optional[str] = None

    @staticmethod
    def from_pb(pb: WorkerInfo) -> "Worker":
        return Worker(
            name=pb.name,
            status=pb.status,
        )
    
class CreateTrainingJob(BaseModel):
    training_job_id: str

    @staticmethod
    def from_pb(pb: CreateTrainingJobResponse) -> "CreateTrainingJobResponse":
        return CreateTrainingJobResponse(
            training_job_id=pb.training_job_id,
        )


class GetTrainingJob(BaseModel):
    project_id: str
    region_id: str
    zone_id: str
    project_name: str
    training_job_id: str
    job_name: str
    job_type: str
    job_status: str
    worker_spec: str
    num_workers: int
    worker_image: Optional[str] = None
    volume_name: Optional[str] = None
    volume_size_gb: Optional[int] = None
    volume_mount_path: Optional[str] = None
    workers: Optional[List[Worker]] = None
    created_at: str

    @staticmethod
    def from_pb(pb: GetTrainingJobResponse) -> "GetTrainingJob":
        workers = None
        if hasattr(pb, 'workers'):
            workers = [Worker.from_pb(worker) for worker in pb.workers]

        return GetTrainingJob(
            project_id=pb.project_id,
            region_id=pb.region_id,
            zone_id=pb.zone_id,
            project_name=pb.project_name,
            training_job_id=pb.training_job_id,
            job_name=pb.job_name,
            job_type=JobType(pb.job_type).name,
            job_status=JobStatus(pb.job_status).name,
            worker_spec=pb.worker_spec.spec_key,
            num_workers=pb.num_workers,
            worker_image=pb.worker_image if hasattr(pb, "worker_image") else None,
            volume_name=pb.volume_name if hasattr(pb, 'volume_name') else None,
            volume_size_gb=pb.volume_size_gb if hasattr(pb, 'volume_size_gb') else None,
            volume_mount_path=pb.volume_mount_path if hasattr(pb, 'volume_mount_path') else None,
            workers=workers,
            created_at=pb.created_at.ToJsonString(),
        )

class ListTrainingJobs(BaseModel):
    training_jobs: List[GetTrainingJob]
    count: int

    @staticmethod
    def from_pb(pb: ListTrainingJobsResponse) -> "ListTrainingJobs":
        training_jobs = []
        for training_job in pb.training_jobs:
            training_jobs.append(GetTrainingJob.from_pb(training_job))

        return ListTrainingJobs(
            training_jobs=training_jobs,
            count=pb.count,
        )
    
class GetTrainingJobLogs(BaseModel):
    logs: str

    @staticmethod
    def from_pb(pb: GetTrainingJobLogsResponse) -> "GetTrainingJobLogs":
        return GetTrainingJobLogs(
            logs=pb.logs,
        )



class GetTrainingJobWorkers(BaseModel):
    workers: List[Worker]

    @staticmethod
    def from_pb(pb: GetTrainingJobWorkersResponse) -> "GetTrainingJobWorkers":
        workers = [Worker.from_pb(worker) for worker in pb.workers]
        return GetTrainingJobWorkers(
            workers=workers,
        )