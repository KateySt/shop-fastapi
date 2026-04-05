import uuid

from fastapi import APIRouter, Depends, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from app.dependencies import Pagination, Sorting
from app.dependencies.auth import get_current_user
from app.schemas import (
    CompanyCreate,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
)
from app.services import CompanyServiceDep

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(company_data: CompanyCreate, service: CompanyServiceDep):
    return await service.create_company(company_data)


@router.get("/{company_id}", response_model=CompanyResponse)
@cache(expire=300, namespace="companies")
async def get_company(company_id: uuid.UUID, company_service: CompanyServiceDep):
    return await company_service.get_company(company_id)


@router.get("/", response_model=CompanyListResponse)
async def list_companies(
    service: CompanyServiceDep,
    pagination: Pagination,
    sort: Sorting,
):
    return await service.list_companies(pagination, sort)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: uuid.UUID,
    company: CompanyUpdate,
    service: CompanyServiceDep,
):
    result = await service.update_company(company_id, company)
    await FastAPICache.clear(namespace="companies")
    return result


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: uuid.UUID,
    service: CompanyServiceDep,
):
    await service.delete_company(company_id)
    await FastAPICache.clear(namespace="companies")
