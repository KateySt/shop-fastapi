from typing import Annotated

from fastapi import Depends

from ..mappers import (
    CompanyMapper,
    CompanyPaginatedMapper,
    ItemMapper,
    ItemPaginatedMapper,
    OrderMapper,
    OrderPaginatedMapper,
    UserMapper,
    get_company_mapper,
    get_company_paginated_mapper,
    get_item_mapper,
    get_item_paginated_mapper,
    get_order_mapper,
    get_order_paginated_mapper,
    get_user_mapper,
)
from ..repo import (
    CompanyRepository,
    ItemRepository,
    OrderRepository,
    UserRepository,
    get_repo_company,
    get_repo_item,
    get_repo_order,
    get_repo_user,
)
from .abstract import (
    AbstractCompanyService,
    AbstractItemService,
    AbstractOrderService,
    AbstractPaymentService,
    AbstractUserService,
)
from .company_service import CompanyService
from .impl import OrderServiceImpl, PaymentServiceImpl, UserServiceImpl
from .impl.company_service_impl import CompanyServiceImpl
from .impl.item_service_impl import ItemServiceImpl
from .item_service import ItemService
from .order_service import OrderService
from .payment_service import PaymentService
from .redis_service import RedisService
from .sentry_service import init_sentry, unexpected_error
from .user_service import UserService


def get_company_service(
    repo: Annotated[CompanyRepository, Depends(get_repo_company)],
    mapper: Annotated[CompanyMapper, Depends(get_company_mapper)],
    paginated_mapper: Annotated[
        CompanyPaginatedMapper, Depends(get_company_paginated_mapper)
    ],
) -> AbstractCompanyService:
    return CompanyService(
        impl=CompanyServiceImpl(repo),
        mapper=mapper,
        paginated_mapper=paginated_mapper,
    )


def get_item_service(
    repo: Annotated[ItemRepository, Depends(get_repo_item)],
    mapper: Annotated[ItemMapper, Depends(get_item_mapper)],
    paginated_mapper: Annotated[
        ItemPaginatedMapper, Depends(get_item_paginated_mapper)
    ],
) -> AbstractItemService:
    return ItemService(
        impl=ItemServiceImpl(repo),
        mapper=mapper,
        paginated_mapper=paginated_mapper,
    )


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_repo_user)],
    mapper: Annotated[UserMapper, Depends(get_user_mapper)],
) -> AbstractUserService:
    return UserService(
        impl=UserServiceImpl(repo),
        mapper=mapper,
    )


def get_order_service(
    repo: Annotated[OrderRepository, Depends(get_repo_order)],
    item_repo: Annotated[ItemRepository, Depends(get_repo_item)],
    mapper: Annotated[OrderMapper, Depends(get_order_mapper)],
    paginated_mapper: Annotated[
        OrderPaginatedMapper, Depends(get_order_paginated_mapper)
    ],
) -> AbstractOrderService:
    return OrderService(
        impl=OrderServiceImpl(repo, item_repo),
        mapper=mapper,
        paginated_mapper=paginated_mapper,
    )


def get_payment_service(
    repo: Annotated[OrderRepository, Depends(get_repo_order)],
) -> AbstractPaymentService:
    return PaymentService(PaymentServiceImpl(repo))


PaymentServiceDep = Annotated[PaymentService, Depends(get_payment_service)]
UserServiceDep = Annotated[AbstractUserService, Depends(get_user_service)]
CompanyServiceDep = Annotated[AbstractCompanyService, Depends(get_company_service)]
ItemServiceDep = Annotated[AbstractItemService, Depends(get_item_service)]
OrderServiceDep = Annotated[AbstractOrderService, Depends(get_order_service)]

redis_service = RedisService()
