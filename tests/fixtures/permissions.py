from sqlalchemy import select

from microshop.core.models import PermissionOrm, RolePermissionsAssoc

PERMISSION = {
    'product:create': 'Добавить продукт',
    'order:read_all': 'Посмотреть все заказы',
    'user:delete': 'Удалить пользователя',
    'order:status:update': 'Обновить статус заказа',
    'order:read': 'Просмотр деталей заказа'
}


async def seed_permissions(db_session) -> dict[str, PermissionOrm]:
    codes = list(PERMISSION.keys())
    stmt = select(PermissionOrm).where(PermissionOrm.permission_code.in_(codes))
    result = await db_session.scalars(stmt)
    existing_map = {p.permission_code: p for p in result}

    to_create = list()
    perm_map = dict()
    for code, desc in PERMISSION.items():
        if code in existing_map:
            perm_map[code] = existing_map[code]
        else:
            perm = PermissionOrm(
                permission_code=code,
                permission_description=desc,
            )
            to_create.append(perm)
            perm_map[code] = perm

    db_session.add_all(to_create)
    await db_session.flush()
    await db_session.commit()

    return perm_map


async def grant_permissions_to_role(
    db_session,
    role_id: int,
    codes: list[str],
    permissions_map: dict[str, PermissionOrm],
) -> list[RolePermissionsAssoc]:
    perms_id = [permissions_map[code].permission_id for code in codes]

    stmt = select(RolePermissionsAssoc).where(
        RolePermissionsAssoc.role_id == role_id,
        RolePermissionsAssoc.permission_id.in_(perms_id),
    )
    result = await db_session.scalars(stmt)
    existing_permissions_ids = {assoc.permission_id for assoc in result}

    to_create = [
        RolePermissionsAssoc(
            role_id=role_id,
            permission_id=permissions_map[code].permission_id,
        )
        for code in codes
        if permissions_map[code].permission_id not in existing_permissions_ids
    ]

    if to_create:
        db_session.add_all(to_create)
        await db_session.flush()
        await db_session.commit()

    return to_create
