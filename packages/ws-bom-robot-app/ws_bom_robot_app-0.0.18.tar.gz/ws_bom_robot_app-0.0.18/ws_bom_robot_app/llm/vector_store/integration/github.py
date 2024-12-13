import asyncio
import os
from typing import Optional, Union
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.connector.git import GitAccessConfig
from unstructured_ingest.connector.github import SimpleGitHubConfig
from unstructured_ingest.runner import GithubRunner
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from pydantic import BaseModel, Field, AliasChoices

class GithubParams(BaseModel):
  repo: str
  access_token: Optional[str] | None = Field(None,validation_alias=AliasChoices("accessToken","access_token"))
  branch: Optional[str] = 'main'
  file_ext: Optional[list[str]] = Field(default_factory=list, validation_alias=AliasChoices("fileExt","file_ext"))
class Github(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = GithubParams.model_validate(self.data)
    self.__loader = Loader(self.working_directory)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'github'
  def run(self) -> None:
    access_config = GitAccessConfig(
      access_token=self.__data.access_token
    )
    file_ext = self.__data.file_ext or None
    file_glob = [f"**/*{ext}" for ext in file_ext] if file_ext else None
    config = SimpleGitHubConfig(
      url = self.__data.repo,
      access_config=access_config,
      branch=self.__data.branch,
      file_glob=file_glob
    )
    runner = GithubRunner(
      connector_config=config,
      processor_config=self.__unstructured_ingest.processor_config(),
      read_config=self.__unstructured_ingest.read_config(),
      partition_config=self.__unstructured_ingest.partition_config(),
      retry_strategy_config=self.__unstructured_ingest.retry_strategy_config()
      )
    runner.run()
  async def load(self) -> list[Document]:
      self.run()
      await asyncio.sleep(1)
      return await self.__loader.load()
