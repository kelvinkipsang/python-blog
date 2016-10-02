from flask import jsonify
from . import api
from .errors import forbidden, bad_request
from ..models import Comment

@api.route('/comments/<int:id>', methods=['PUT'])
def approve_comment(id):
    comment = Comment.query.get_or_404(id)
    if comment.talk.author != g.current_user and \
            not g.current_user.is_admin:
        return forbidden('You cannot modify this comment.')
    if comment.approved:
        return bad_request('Comment is already approved.')
    comment.approved = True
    db.session.add(comment)
    db.session.commit()
    send_comment_notification(comment)
    return jsonify({'status': 'ok'})


@api.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if comment.talk.author != g.current_user and \
            not g.current_user.is_admin:
        return forbidden('You cannot modify this comment.')
    if comment.approved:
        return bad_request('Comment is already approved.')
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'status': 'ok'})