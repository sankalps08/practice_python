from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schema, database, models, Oauth2


router = APIRouter(
    prefix="/votes",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(Oauth2.get_current_user)):

    post = db.query(models.Posts).filter(models.Posts.id == vote.Post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.Post_id} does not exist")

    vote_query = db.query(models.Votes).filter(
        models.Votes.Post_id == vote.Post_id, models.Votes.User_id == current_user.id) # type: ignore

    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has alredy voted on post {vote.Post_id}") # type: ignore
        new_vote = models.Votes(Post_id=vote.Post_id, User_id=current_user.id) # type: ignore
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}