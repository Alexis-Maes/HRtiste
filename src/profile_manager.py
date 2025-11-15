from models.db_models import CandidateFromCV, CandidateProfile
from services.db_service import db_service


def convert_cv_to_profile(cv_profile: CandidateFromCV) -> CandidateProfile:
    return CandidateProfile(
        name=cv_profile.name,
        email=cv_profile.email,
        phone=cv_profile.phone,
    )


async def add_profile_to_db(profile: CandidateProfile):
    async with db_service.get_session() as session:
        session.add(profile)
        await session.commit()


if __name__ == "__main__":
    cv_profile = CandidateFromCV(
        name="John Doe",
        email="john.doe@example.com",
        phone="1234567890",
    )
    profile = convert_cv_to_profile(cv_profile)
    print(profile)
