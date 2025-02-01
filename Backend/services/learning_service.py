from sqlalchemy.orm import Session
from models.interaction_model import Interaction

def store_interaction(db: Session, query: str, response: str):
    interaction = Interaction(user_query= query, ai_response= response)
    db.add(interaction)
    db.commit()
    return interaction.id

def retrieve_past_responses(db: Session, query: str):
    return db.query(Interaction).filter(Interaction.user_query.contains(query)).all()

def update_feedback(db: Session, interaction_id: int, feedback: int):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if interaction:
        interaction.feedback = feedback
        db.commit()
        return "Feedback updated!"
    return "Interaction not found!"