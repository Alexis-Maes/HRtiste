from fastapi import APIRouter

router = APIRouter(tags=["Interviews"])


# @router.post("/interviews", response_model=Interview)
# def add_interview(interview_data: Interview):
#     with Session(engine) as session:

#         # Validate recruiter exists
#         recruiter = session.get(Recruiter, interview_data.recruiter_id)
#         if not recruiter:
#             raise HTTPException(status_code=404, detail="Recruiter not found")

#         # Validate candidate exists
#         candidate = session.get(Candidate, interview_data.candidate_id)
#         if not candidate:
#             raise HTTPException(status_code=404, detail="Candidate not found")

#         # Create interview
#         interview = Interview(
#             recruiter_id=interview_data.recruiter_id,
#             candidate_id=interview_data.candidate_id,
#             feedback=interview_data.feedback
#         )

#         session.add(interview)
#         session.commit()
#         session.refresh(interview)

#         return interview


# @router.get("/interviews", response_model=list[Interview])
# def get_all_interviews():
#     with Session(engine) as session:
#         interviews = session.exec(
#             select(Interview)
#         ).all()
#         return interviews
