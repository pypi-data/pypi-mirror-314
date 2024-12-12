from datetime import datetime

from typing import List, Tuple, Union, Dict, Type, Optional

import arrow
import pymongo
from beanie import Document
from fastapi import FastAPI
from pydantic import Field, BaseModel

from .operate import Operate
from ..const import DEF_PAGE_SIZE, DEF_PAGE_NO
from ..exception.internal_exception import NoChangeException
from ..common_enum.order_type import OrderTypeEnum


class InternalBaseDocument(Document):
    create_time: datetime = Field(default_factory=datetime.utcnow)
    update_time: Optional[datetime] = None

    @classmethod
    async def get_pagination_list(cls, app: FastAPI, query: list = None, sort: List[Tuple] = None,
                                  page_size: int = DEF_PAGE_SIZE, page_no: int = DEF_PAGE_NO,
                                  ignore_cache: bool = False,
                                  fetch_links: bool = False):
        if not query:
            final_query = []
        else:
            final_query = query

        if not sort:
            final_sort = [(cls.id, pymongo.ASCENDING)]
        else:
            final_sort = []
            for temp_sort in sort:
                if temp_sort[1] == OrderTypeEnum.ASC:
                    final_sort.append((temp_sort[0], pymongo.ASCENDING))
                elif temp_sort[1] == OrderTypeEnum.DESC:
                    final_sort.append((temp_sort[0], pymongo.DESCENDING))
                else:
                    print(f"order type value error: temp_sort:{temp_sort}")
                    continue
            final_sort.append((cls.id, pymongo.ASCENDING))

        total_num = await cls.find(*final_query, ignore_cache=ignore_cache, fetch_links=fetch_links).sort(
            *final_sort).count()
        if total_num == 0:
            page_data = []
        else:
            page_data = await cls.find(*final_query, ignore_cache=ignore_cache, fetch_links=fetch_links).sort(
                *final_sort).limit(page_size).skip((page_no - 1) * page_size).to_list()

        return page_no, page_size, total_num, page_data

    async def update_wrap(self, schema: Union[Dict, Type[BaseModel]]) -> Tuple[
        Operate, 'InternalBaseDocument', 'InternalBaseDocument']:
        if not issubclass(type(schema), dict) and not issubclass(type(schema), BaseModel):
            raise TypeError("Schema must be a subclass of BaseModel or dict")

        original_model = self.model_copy(deep=True)
        delta_dict = schema
        if issubclass(type(schema), BaseModel):
            delta_dict = schema.model_dump(exclude_unset=True)

        for key, value in delta_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

        operate = await Operate.generate_operate(original_model.model_dump(), self.model_dump())
        if not operate.add and not operate.remove and not operate.change:
            raise NoChangeException()

        self.update_time = arrow.utcnow().datetime

        await self.save()
        return operate, original_model, self

    @classmethod
    async def get_list(cls, app: FastAPI, query: list = None, sort: List[Tuple] = None, ignore_cache: bool = False,
                       fetch_links: bool = False):
        if not query:
            final_query = []
        else:
            final_query = query

        if not sort:
            final_sort = [(cls.id, pymongo.ASCENDING)]
        else:
            final_sort = []
            for temp_sort in sort:
                if temp_sort[1] == OrderTypeEnum.ASC:
                    final_sort.append((temp_sort[0], pymongo.ASCENDING))
                elif temp_sort[1] == OrderTypeEnum.DESC:
                    final_sort.append((temp_sort[0], pymongo.DESCENDING))
                else:
                    print(f"order type value error: temp_sort:{temp_sort}")
                    continue
            final_sort.append((cls.id, pymongo.ASCENDING))

        data = await cls.find(*final_query, ignore_cache=ignore_cache, fetch_links=fetch_links).sort(
            *final_sort).to_list()

        return data
