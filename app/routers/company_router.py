import uuid

from fastapi import APIRouter, Depends, status, Query

from app.schemas import CompanyCreate, CompanyBase, CompanyListResponse
from app.services import CompanyService, get_company_service

router = APIRouter()


@router.post("/", response_model=CompanyBase, status_code=status.HTTP_201_CREATED)
async def create_company(
        company_data: CompanyCreate,
        service: CompanyService = Depends(get_company_service)
):
    return await service.create_company(company_data)


@router.get("/{company_id}", response_model=CompanyBase)
async def get_company(
        company_id: uuid.UUID,
        company_service: CompanyService = Depends(get_company_service)
):
    company = await company_service.get_company(company_id)
    return CompanyBase.model_validate(company)


@router.get("/", response_model=CompanyListResponse)
async def list_companies(
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        company_service: CompanyService = Depends(get_company_service)
):
    return await company_service.list_companies(skip=skip, limit=limit)


@router.put("/", response_model=CompanyBase)
async def update_company(
        company: CompanyBase,
        service: CompanyService = Depends(get_company_service),
):
    return await service.update_company(company)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
        company_id: uuid.UUID,
        service: CompanyService = Depends(get_company_service),
):
    await service.delete_company(company_id)
