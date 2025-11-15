from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Processes"])
from services.db_service import db_service
from sqlmodel import select
from models.db_models import Process, ProcessCreate, Candidate, ProcessCandidateLink

@router.get("/processes")
async def get_processes():
    async with db_service.get_session() as session:
        statement = select(Process)
        result = await session.exec(statement)
        processes = result.all()

        return [
            {"id": p.id, "name": p.name_process}
            for p in processes
        ]


@router.post("/processes", response_model=Process)
async def create_process(process_data: ProcessCreate):
    async with db_service.get_session() as session:
        # Create the process entry first
        process = Process(
            name_process=process_data.name_process,
            job_description=process_data.job_description
        )
        session.add(process)
        await session.commit()
        await session.refresh(process)

        # If candidate_ids are provided, add them in the link table
        if process_data.candidate_ids:
            for cid in process_data.candidate_ids:
                candidate = await session.get(Candidate, cid)
                if not candidate:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Candidate id {cid} not found"
                    )

                link = ProcessCandidateLink(
                    process_id=process.id,
                    candidate_id=cid
                )
                session.add(link)

            await session.commit()

        await session.refresh(process)
        return process
