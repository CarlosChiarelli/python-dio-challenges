from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from workoutapi.categorias.models import CategoriaModel
from workoutapi.categorias.schemas import CategoriaIn, CategoriaOut
from workoutapi.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar uma nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    # Verificar se o nome da categoria já existe
    existing_categoria = await db_session.execute(
        select(CategoriaModel).where(CategoriaModel.nome == categoria_in.nome)
    )
    existing_categoria = existing_categoria.scalar()

    if existing_categoria:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe uma categoria cadastrada com o nome: {categoria_in.nome}",
        )

    # Se o nome não existe, criar e adicionar a nova categoria
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    try:
        db_session.add(categoria_model)
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao salvar a categoria no banco de dados.",
        )

    return categoria_out


@router.get(
    path="/",
    summary="Consultar todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def get_all(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()

    return categorias


@router.get(
    path="/{id}",
    summary="Consultar uma categoria pelo id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada no id: {id}"
        )

    return categoria
