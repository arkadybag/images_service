from uuid import UUID

from fastapi import APIRouter, Path, Query, Request, status

from app.image_processing.formatting import ImageProcessor
from app.repository.sql_repository import SQLRepository
from app.schema.input import CustomColor
from app.schema.output import FrameSchema, FramesSchema, ImageSchema, ImagesSchema
from app.service.frame_service import Service

api_router = APIRouter()


@api_router.get("/images", status_code=status.HTTP_200_OK)
async def get_images(request: Request) -> ImagesSchema:
    repository = SQLRepository(request.app.state.session_factory)
    image_processor = ImageProcessor()
    service = Service(repository, image_processor)

    images = await service.get_images()

    return ImagesSchema(data=[ImageSchema(id=i.id) for i in images])


@api_router.get("/frames/{image_id}")
async def get_frames(
    request: Request,
    image_id: UUID = Path(),
    depth_min: float = Query(),
    depth_max: float = Query(),
    custom_color: CustomColor | None = Query(None),
) -> FramesSchema:
    repository = SQLRepository(request.app.state.session_factory)
    image_processor = ImageProcessor()
    service = Service(repository, image_processor)

    frames = await service.get_frames(
        depth_min,
        depth_max,
        image_id,
        custom_color=custom_color.value if custom_color else custom_color,
    )

    return FramesSchema(
        data=[
            FrameSchema(
                id=frame.id, image_id=frame.image_id, depth=frame.depth, points=frame.points
            )
            for frame in frames
        ]
    )
