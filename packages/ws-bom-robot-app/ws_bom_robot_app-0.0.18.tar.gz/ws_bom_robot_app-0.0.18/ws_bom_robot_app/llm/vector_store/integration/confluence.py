import asyncio
import os
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy, UnstructuredIngest
from unstructured_ingest.connector.confluence import SimpleConfluenceConfig, ConfluenceAccessConfig
from unstructured_ingest.runner import ConfluenceRunner
from langchain_core.documents import Document
from ws_bom_robot_app.llm.vector_store.loader.base import Loader
from typing import Optional, Union
from pydantic import BaseModel, Field, AliasChoices

class ConfluenceParams(BaseModel):
  url: str
  access_token: str = Field(validation_alias=AliasChoices("accessToken","access_token"))
  user_email: str = Field(validation_alias=AliasChoices("userEmail","user_email"))
  spaces: list[str] = []
class Confluence(IntegrationStrategy):
  def __init__(self, knowledgebase_path: str, data: dict[str, Union[str,int,list]]):
    super().__init__(knowledgebase_path, data)
    self.__data = ConfluenceParams.model_validate(self.data)
    self.__loader = Loader(self.working_directory)
    self.__unstructured_ingest = UnstructuredIngest(self.working_directory)
  def working_subdirectory(self) -> str:
    return 'confluence'
  def run(self) -> None:
    access_config = ConfluenceAccessConfig(
      api_token=self.__data.access_token
    )
    config = SimpleConfluenceConfig(
      user_email=self.__data.user_email,
      url = self.__data.url,
      access_config=access_config,
      #max_num_of_spaces=self.data.get('max_num_of_spaces',500),
      #max_num_of_docs_from_each_space=self.data.get('max_num_of_docs_from_each_space',100),
      spaces=self.__data.spaces
    )
    runner = ConfluenceRunner(
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
