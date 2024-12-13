import os
from langchain_core.documents import Document
from abc import ABC, abstractmethod
from unstructured_ingest.interfaces import PartitionConfig,  ProcessorConfig, ReadConfig, RetryStrategyConfig
from typing import Union

class IntegrationStrategy(ABC):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    self.knowledgebase_path = knowledgebase_path
    self.data = data
    self.working_directory = os.path.join(self.knowledgebase_path,self.working_subdirectory())
    os.makedirs(self.working_directory, exist_ok=True)
  @property
  @abstractmethod
  def working_subdirectory(self) -> str:
    pass
  @abstractmethod
  #@timer
  def load(self) -> list[Document]:
    pass

class UnstructuredIngest():
  def __init__(self, working_directory: str):
    self.working_directory = working_directory
  def processor_config(self) -> ProcessorConfig:
    return ProcessorConfig(
      reprocess=False,
      verbose=False,
      #work_dir=os.path.join(self.working_directory,'.__work_dir'),
      #output_dir=self.working_directory,
      num_processes=1,
      raise_on_error=False
    )
  def read_config(self) -> ReadConfig:
    return ReadConfig(
      download_dir=self.working_directory,
      re_download=True,
      preserve_downloads=False,
      download_only=True
    )
  def partition_config(self) -> PartitionConfig:
    return None
  def retry_strategy_config(self) -> RetryStrategyConfig:
    return None
