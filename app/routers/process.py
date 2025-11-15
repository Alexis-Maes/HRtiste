from fastapi import APIRouter

router = APIRouter(tags=["Processes"])

# @router.get("/processes")
# def get_processes():
#     with Session(engine) as session:
#         statement = select(Process)
#         processes = session.exec(statement).all()

#         return [
#             {"id": p.id, "name": p.name_process}
#             for p in processes
#         ]


# @router.post("/processes", response_model=Process)
# def create_process(process_data: ProcessCreate):
#     with Session(engine) as session:
#         # Create the process entry first
#         process = Process(
#             name_process=process_data.name_process,
#             job_description=process_data.job_description
#         )
#         session.add(process)
#         session.commit()
#         session.refresh(process)

#         # If candidate_ids are provided, add them in the link table
#         if process_data.candidate_ids:
#             for cid in process_data.candidate_ids:
#                 candidate = session.get(Candidate, cid)
#                 if not candidate:
#                     raise HTTPException(
#                         status_code=404,
#                         detail=f"Candidate id {cid} not found"
#                     )

#                 link = ProcessCandidateLink(
#                     process_id=process.id,
#                     candidate_id=cid
#                 )
#                 session.add(link)

#             session.commit()

#         session.refresh(process)
#         return process
