from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from schemas.content import ContentCreate, ContentResponse, ContentListResponse
from models.user import User
from models.content import Content
from utils.dependencies import get_current_user
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/contents", tags = ["Contents"])


def process_content_with_ai():
    """Method for AI processing of Content"""
    #todo

@router.post("", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate, 
    background_tasks: BackgroundTasks, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ) -> str:
    """Create new content and trigger AI analysis."""
    new_content = Content(
        user_id = current_user.user_id,
        text_body = content_data.text_body
    )

    db.add(new_content)
    db.commit()
    db.refresh(new_content)

    background_tasks.add_task(
        process_content_with_ai,
        new_content.id,
        content_data.text_body,
        db
    )
    
    return new_content


@router.get("", response_model= ContentListResponse)
async def get_all_contents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all content submitted by the authenticated user."""
    contents = db.query(Content).filter(Content.user_id == current_user.user_id).all()
    return {"totla": len(contents), "contents": contents}

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content_by_id(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve a specific piece of content."""
    content = db.query(Content).filter(Content.id == content_id, Content.user_id == current_user.user_id).first()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    return {"summary": content.summary, "sentiment": content.sentiment}

@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific piece of content."""
    content = db.query(Content).filter(
        Content.id == content_id,
        Content.user_id == current_user.user_id
    ).first()
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    db.delete(content)
    db.commit()
    return None
