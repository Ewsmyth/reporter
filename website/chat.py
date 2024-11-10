from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
from .models import db, User, Messages, ChatParticipants

chat = Blueprint('chat', __name__)
socketio = SocketIO()

@socketio.on('join')
def on_join(data):
    """Handle a user joining a chat room and mark all current messages as read."""
    try:
        username = data.get('username')
        chat_id = data.get('chat_id')
        user_id = data.get('user_id')  # Ensure the user ID is passed

        if not username or not chat_id or not user_id:
            print("Missing username, chat_id, or user_id")
            return

        print(f"{username} joined chat {chat_id}")
        join_room(chat_id)

        # Fetch the latest message in the chat
        last_message = Messages.query.filter_by(chat_id=chat_id).order_by(Messages.id.desc()).first()

        if last_message:
            # Find the participant entry for the current user in the chat
            chat_participant = ChatParticipants.query.filter_by(chat_id=chat_id, user_id=user_id).first()

            if chat_participant:
                # Only update if the last_read_message_id is less than the last message
                if not chat_participant.last_read_message_id or chat_participant.last_read_message_id < last_message.id:
                    chat_participant.last_read_message_id = last_message.id
                    db.session.commit()
                    print(f"User {user_id} has read all messages up to {last_message.id} in chat {chat_id}.")
                else:
                    print(f"User {user_id} already up-to-date with messages in chat {chat_id}.")
            else:
                print(f"Chat participant not found for chat {chat_id} and user {user_id}.")
        else:
            print(f"No messages found in chat {chat_id}.")

        # Emit a status message to the room
        emit('status', {'msg': f'{username} has joined the room.'}, room=chat_id)

    except Exception as e:
        print(f"Error during on_join: {e}")

@socketio.on('message')
def handle_message(data):
    """Handle a new message in the chat and mark it as read by the sender"""
    try:
        chat_id = data.get('chat_id')
        content = data.get('message')
        sender_id = data.get('sender_id')

        if not chat_id or not sender_id:
            print("Missing chat_id or sender_id")
            return

        # Save the new message to the database
        new_message = Messages(sender_id=sender_id, chat_id=chat_id, content=content, timestamp=datetime.utcnow())
        db.session.add(new_message)
        db.session.commit()

        # Emit the message to all users in the chat room, including sender_id
        sender = User.query.get(sender_id)
        emit('message', {
            'sender_id': sender_id,
            'sender_username': sender.username,
            'content': content,
            'timestamp': new_message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'message_id': new_message.id
        }, room=chat_id)

        print(f"Message received from user {sender_id} for chat {chat_id}: {content}")

    except Exception as e:
        print(f"Error handling message: {e}")

@socketio.on('message_read')
def handle_message_read(data):
    """Mark messages as read when a user reads them."""
    try:
        chat_id = data.get('chat_id')
        user_id = data.get('user_id')
        message_id = data.get('message_id')

        # Fetch the participant entry for the user
        chat_participant = ChatParticipants.query.filter_by(chat_id=chat_id, user_id=user_id).first()

        if chat_participant:
            # Only update if the message being read is newer
            if not chat_participant.last_read_message_id or message_id > chat_participant.last_read_message_id:
                chat_participant.last_read_message_id = message_id
                db.session.commit()
                print(f"User {user_id} has read message {message_id} in chat {chat_id}.")
        else:
            print(f"Chat participant not found for chat {chat_id} and user {user_id}.")

    except Exception as e:
        print(f"Error updating last read message: {e}")

@socketio.on('update_last_read')
def update_last_read(data):
    """Update the last_read_message_id when a user reads messages in a chat"""
    try:
        chat_id = data.get('chat_id')
        user_id = data.get('user_id')
        message_id = data.get('message_id')

        if not chat_id or not user_id or not message_id:
            print("Missing chat_id, user_id, or message_id")
            return

        participant = ChatParticipants.query.filter_by(chat_id=chat_id, user_id=user_id).first()

        if participant and (participant.last_read_message_id is None or message_id > participant.last_read_message_id):
            participant.last_read_message_id = message_id
            db.session.commit()
            print(f"Updated last_read_message_id for user {user_id} in chat {chat_id} to message {message_id}.")
        else:
            print(f"Message {message_id} is not newer than last read message.")
    
    except Exception as e:
        print(f"Error updating last read message: {e}")

@socketio.on('leave')
def on_leave(data):
    """Handle a user leaving a chat room"""
    username = data['username']
    chat_id = data['chat_id']
    leave_room(chat_id)
    emit('status', {'msg': f'{username} has left the room.'}, room=chat_id)
