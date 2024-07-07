from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, Query, status
from fastapi_pagination import LimitOffsetPage, paginate
from pydantic import UUID4
from sqlalchemy import select

from workoutapi.atleta.models import AtletaModel
from workoutapi.atleta.schema import AtletaIn, AtletaOut, AtletaOutGetAll, AtletaUpdate
from workoutapi.categorias.models import CategoriaModel
from workoutapi.centro_treinamento.models import CentroTreinamentoModel
from workoutapi.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)) -> AtletaOut:
    # Verificar se o CPF do atleta já existe
    existing_atleta = await db_session.execute(select(AtletaModel).where(AtletaModel.cpf == atleta_in.cpf))
    existing_atleta = existing_atleta.scalar()

    if existing_atleta:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o CPF: {atleta_in.cpf}",
        )

    # Verificar se a categoria do atleta existe
    categoria_nome = atleta_in.categoria.nome
    categoria = (
        (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
    )
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"A categoria {categoria_nome} não foi encontrada"
        )

    # Verificar se o centro de treinamento do atleta existe
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    centro_treinamento = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)))
        .scalars()
        .first()
    )
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {centro_treinamento_nome} não foi encontrado",
        )

    try:
        # Criar e adicionar o novo atleta
        atleta_out = AtletaOut(id=uuid4(), create_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={"categoria", "centro_treinamento"}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao salvar o atleta no banco de dados.",
        )

    return atleta_out


@router.get(
    path="/",
    summary="Consultar todas os atletas com paginação",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaOutGetAll],
)
async def get_all(
    db_session: DatabaseDependency,
    nome: Optional[str] = Query(None, description="Filtrar por nome do atleta"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF do atleta"),
) -> LimitOffsetPage[AtletaOutGetAll]:
    query = select(AtletaModel)

    if nome:
        query = query.where(AtletaModel.nome == nome)

    if cpf:
        query = query.where(AtletaModel.cpf == cpf)

    atletas_query = await db_session.execute(query)
    atletas = atletas_query.scalars().all()

    return paginate(atletas)


@router.get(
    path="/{id}",
    summary="Consultar um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrada no id: {id}"
        )

    return atleta


@router.patch(
    path="/{id}",
    summary="Editar um atleta pelo id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def update_by_id(
    id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrada no id: {id}"
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    path="/{id}",
    summary="Deletar um atleta pelo id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_by_id(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrada no id: {id}"
        )

    await db_session.delete(atleta)
    await db_session.commit()
