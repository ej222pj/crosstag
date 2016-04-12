from crosstag_init import db
from db_models.detailedtagevent import DetailedTagevent


def get_last_tag_event():
    """
    Helper script to get the last tag event from the local database.

    :return: if tagevent exist return tagevent aither None.
    """
    top_index = db.session.query(db.func.max(DetailedTagevent.index)).scalar()
    tagevent = DetailedTagevent.query.filter_by(index=top_index).first()
    print(tagevent.tag_id)
    if tagevent is None:
        return None
    else:
        return tagevent
