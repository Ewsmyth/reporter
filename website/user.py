import json  # Add this import to use json.loads

from flask import Flask, render_template, Blueprint, request, redirect, url_for, flash, jsonify
from .utils import userReq
from flask_login import login_required, current_user
from datetime import datetime
from .models import db, Reports, User, Contacts, Chats, ChatParticipants, Messages, GroupChatDetails
from sqlalchemy import and_, asc
from sqlalchemy.orm import joinedload

user = Blueprint('user', __name__)

@user.route('/<username>/user-home/user-account')
@login_required
@userReq
def userAccount(username):
    return render_template('user-account.html', username=username)

@user.route('/api/messages', methods=['POST'])
def receive_messages():
    """Receive messages from backup API and store them in the reporter's database"""
    data = request.json
    new_message = Messages(
        chat_id=data['chat_id'],
        sender_id=data['sender_id'],
        content=data['content'],
        timestamp=data['timestamp']
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message stored successfully'}), 201

@user.route('/<username>/user-home')
@login_required
@userReq
def userHome(username):
    return render_template('user-home.html', username=username)

@user.route('/<username>/user-home/SPOTREP', methods=['GET', 'POST'])
@login_required
@userReq
def userSpotrep(username):
    if request.method == 'POST':
        size = request.form.get('size-fr-usr')
        activity = request.form.get('activity-fr-usr')
        location = request.form.get('location-fr-usr')
        unit = request.form.get('unit-fr-usr')
        date = request.form.get('date-fr-usr')
        time = request.form.get('time-fr-usr')
        equipment = request.form.get('equip-fr-usr')

        try:
            joinDateTimeSpot = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            print(f"{joinDateTimeSpot}")
        except ValueError as e:
            print(f"Error pasrsing date/time: {e}")
            return redirect(url_for('user.userSpotrep', username=username))

        submitSpotrep = Reports(
            author_id=current_user.id, 
            report_type="SPOTREP", 
            report_time=joinDateTimeSpot,
            location=location,
            size=size,
            activity=activity,
            unit=unit,
            equipment=equipment
            )

        db.session.add(submitSpotrep)
        db.session.commit()
        print(f"A new SPOTREP was submitted by: {current_user.username}.")

        return redirect(url_for('user.userHome', username=username))
    
    return render_template('user-spotrep.html', username=username)

@user.route('/<username>/user-home/POSREP', methods=['GET', 'POST'])
@login_required
@userReq
def userPosrep(username):
    if request.method == 'POST':
        team = request.form.get('team-fr-usr')
        location = request.form.get('location-fr-usr')
        date = request.form.get('date-fr-usr')
        time = request.form.get('time-fr-usr')

        try:
            joinDateTimePos = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            print(f"{joinDateTimePos}")
        except ValueError as e:
            print(f"Invalid submission: {e}")
            return redirect(url_for('user.userPosrep', username=username))

        submitPosrep = Reports(
            author_id=current_user.id,
            report_type="POSREP",
            report_time=joinDateTimePos,
            location=location,
            team=team
        )

        db.session.add(submitPosrep)
        db.session.commit()
        print(f"A new POSREP was submitted by: {current_user.username}.")

        return redirect(url_for('user.userHome', username=username))

    return render_template('user-posrep.html', username=username)

@user.route('/<username>/user-home/SITREP')
@login_required
@userReq
def userSitrep(username):
    return render_template('user-sitrep.html', username=username)

@user.route('/<username>/user-home/MISREP', methods=['GET', 'POST'])
@login_required
@userReq
def userMisrep(username):

    if request.method == 'POST':
        misName = request.form.get('mis-name-fr-usr')
        result = request.form.get('result-fr-usr')
        misDetail = request.form.get('mis-detail-fr-usr')

        submitMisrep = Reports(
            author_id=current_user.id,
            report_type="MISREP",
            mission_name=misName,
            result=result,
            mission_details=misDetail
        )

        db.session.add(submitMisrep)
        db.session.commit()
        print(f"A new MISREP was submitted by: {current_user.username}.")

        return redirect(url_for('user.userHome', username=username))

    return render_template('user-misrep.html', username=username)

@user.route('/<username>/user-home/DFREP', methods=['GET', 'POST'])
@login_required
@userReq
def userDfrep(username):
    if request.method == 'POST':
        date = request.form.get('date-fr-usr')
        time = request.form.get('time-fr-usr')
        location = request.form.get('location-fr-usr')
        azimuth = request.form.get('azimuth-fr-usr')
        freq = request.form.get('freq-fr-usr')
        rssi = request.form.get('rssi-fr-usr')
        modulation = request.form.get('mod-fr-usr')
        tech = request.form.get('tech-fr-usr')
        protocol = request.form.get('proto-fr-usr')

        print(f"RSSI from form: {rssi}")

        try:
            # Combine date and time into a datetime object
            joinDateTimeDf = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            print(f"Joined DateTime: {joinDateTimeDf}")
            
            # Convert azimuth, frequency, and rssi to the correct types
            azimuth_value = float(azimuth) if azimuth else None
            freq_value = float(freq) if freq else None
            rssi_value = int(rssi) if rssi else None  # Handle negative RSSI values as well

        except ValueError as e:
            print(f"Invalid submission: {e}")
            flash('Invalid input detected. Please check your values.', 'error')
            return redirect(url_for('user.userDfrep', username=username))

        print(f"RSSI after conversion: {rssi_value}")

        submitDfrep = Reports(
            author_id=current_user.id,
            report_type="DFREP",
            report_time=joinDateTimeDf,
            location=location,
            azimuth=azimuth,
            frequency=freq,
            rssi=rssi,
            modulation=modulation,
            technology=tech,
            protocol=protocol
        )

        db.session.add(submitDfrep)
        db.session.commit()
        print(f"A new DFREP was submitted by: {current_user.username}.")

        return redirect(url_for('user.userHome', username=username))

    return render_template('user-dfrep.html', username=username)

@user.route('/<username>/user-home/chatter')
@login_required
@userReq
def userChatter(username):
    # Fetch chats that the user participates in
    chats = (Chats.query
             .options(
                 joinedload(Chats.participants).joinedload(ChatParticipants.participant),
                 joinedload(Chats.group_details)
             )
             .join(ChatParticipants)
             .filter(ChatParticipants.user_id == current_user.id)
             .all())
    
    chat_list = []
    
    for chat in chats:
        if chat.is_group:
            chat_type = {
                'id': chat.id,
                'group_name': chat.group_details.group_name,
                'is_group': True
            }
        else:
            # Exclude the current user from the list of participants
            participants = [p.participant.username for p in chat.participants if p.participant.username != current_user.username]
            chat_type = {
                'id': chat.id,
                'participants': participants,
                'is_group': False
            }
        
        # Get the most recent message for this chat
        latest_message = (Messages.query
                          .filter_by(chat_id=chat.id)
                          .order_by(Messages.timestamp.desc())
                          .options(joinedload(Messages.sender))
                          .first())
        
        # Include the latest message's content or a default message if none exists
        if latest_message:
            chat_type['latest_message'] = {
                'content': latest_message.content,
                'sender_username': latest_message.sender.username  # This assumes `Messages` has a relationship to `User` named `sender`
            }
        else:
            chat_type['latest_message'] = {
                'content': "No messages yet",
                'sender_username': ""
            }

        # Get last read message for the current user
        chat_participant = ChatParticipants.query.filter_by(chat_id=chat.id, user_id=current_user.id).first()
        last_read_message_id = chat_participant.last_read_message_id if chat_participant else None
        
        # Calculate unread messages based on last_read_message_id
        if last_read_message_id:
            unread_count = Messages.query.filter(Messages.chat_id == chat.id, Messages.id > last_read_message_id).count()
        else:
            unread_count = Messages.query.filter_by(chat_id=chat.id).count()  # All messages are unread if no last read message

        chat_type['unread_count'] = unread_count
        chat_list.append(chat_type)

    return render_template('user-chatter.html', username=username, chats=chat_list)

@user.route('/<username>/user-home/chatter/start-group-chat', methods=['GET'])
@login_required
@userReq
def startGroupChat(username):
    return render_template('start-group-chat.html', username=username)

@user.route('/<username>/user-home/chatter/start-group-chat/create', methods=['POST'])
@login_required
@userReq
def createGroupChat(username):
    group_name = request.form.get('group_name')
    selected_users = request.form.get('selected_users')  # This will be a JSON string

    if not group_name or not selected_users:
        flash("Group name and users are required.", "error")
        return redirect(url_for('user.startGroupChat', username=username))

    selected_users = json.loads(selected_users)

    # Create a new group chat
    new_chat = Chats(is_group=True)
    db.session.add(new_chat)
    db.session.commit()

    # Add participants (current user and selected users)
    participant_1 = ChatParticipants(chat_id=new_chat.id, user_id=current_user.id)
    db.session.add(participant_1)

    for user in selected_users:
        participant = ChatParticipants(chat_id=new_chat.id, user_id=user['id'])
        db.session.add(participant)

    # Add group chat details
    group_details = GroupChatDetails(chat_id=new_chat.id, group_name=group_name, created_by=current_user.id)
    db.session.add(group_details)

    db.session.commit()

    # Return a JSON response with the URL of the new group chat
    return jsonify({"message": "Group chat created successfully", "chat_url": url_for('user.viewChat', username=username, chat_id=new_chat.id)})

@user.route('/<username>/user-home/chatter/start-chat/contact', methods=['POST'])
@login_required
@userReq
def createChatWithContact(username):
    contact_id = request.form.get('contact_id')

    # Check if a direct message chat already exists between the current user and the contact
    existing_chat = (Chats.query
                     .join(ChatParticipants)
                     .filter(
                         Chats.is_group == False,  # Ensure it's a direct message (not a group chat)
                         ChatParticipants.chat_id == Chats.id,
                         ChatParticipants.user_id.in_([current_user.id, contact_id])  # Both users should be participants
                     )
                     .group_by(Chats.id)  # Group by chat id to prevent duplicates
                     .having(db.func.count(ChatParticipants.user_id) == 2)  # Both users are in the chat
                     .first())

    if existing_chat:
        # If a direct chat exists, redirect to that chat
        return redirect(url_for('user.viewChat', username=username, chat_id=existing_chat.id))

    # If no direct chat exists, create a new direct message chat
    new_chat = Chats(is_group=False)
    db.session.add(new_chat)
    db.session.commit()

    # Add participants (current user and contact)
    participant_1 = ChatParticipants(chat_id=new_chat.id, user_id=current_user.id)
    participant_2 = ChatParticipants(chat_id=new_chat.id, user_id=contact_id)
    db.session.add_all([participant_1, participant_2])
    db.session.commit()

    return redirect(url_for('user.viewChat', username=username, chat_id=new_chat.id))

@user.route('/api/search', methods=['POST'])
@login_required
@userReq
def searchForUser():
    search_query = request.form.get('search_query')

    # Perform case-insensitive search for users by username
    search_results = User.query.filter(User.username.ilike(f"%{search_query}%")).all()

    # Return the results as JSON for easier front-end handling
    users = [{'id': user.id, 'username': user.username} for user in search_results]
    return jsonify(users)

@user.route('/<username>/user-home/chatter/chat/<int:chat_id>', methods=['GET'])
@login_required
@userReq
def viewChat(username, chat_id):
    # Fetch the chat by ID
    chat = Chats.query.get_or_404(chat_id)

    # Ensure the current user is a participant in this chat
    is_participant = ChatParticipants.query.filter_by(chat_id=chat.id, user_id=current_user.id).first()
    if not is_participant:
        flash("You are not authorized to view this chat.", "error")
        return redirect(url_for('user.userChatter', username=username))

    # Query only the reporter database for messages, ordered by timestamp
    reporter_messages = Messages.query.filter_by(chat_id=chat.id).order_by(asc(Messages.timestamp)).all()

    # For group chats, show the group name. For direct messages, list the other participants (excluding the current user).
    chat_info = {
        'id': chat.id,  # Pass the actual chat ID
        'is_group': chat.is_group,
        'group_name': chat.group_details.group_name if chat.is_group else None,
        'participants': [p.user for p in chat.participants if p.user.id != current_user.id] if not chat.is_group else None
    }

    return render_template('user-chat.html', username=username, chat=chat_info, messages=reporter_messages)

@user.route('/<username>/user-home/chatter/contacts')
@login_required
@userReq
def userContacts(username):
    # Get current user's contacts sorted alphabetically by username
    contacts = (db.session.query(User)
                .join(Contacts, Contacts.contact_id == User.id)
                .filter(Contacts.user_id == current_user.id)
                .order_by(User.username.asc())
                .all())

    return render_template('user-contacts.html', username=username, contacts=contacts)

@user.route('/<username>/user-home/chatter/contacts/search', methods=['POST'])
@login_required
@userReq
def searchContacts(username):
    search_query = request.form.get('search_query')

    if not search_query:
        flash("Please enter a username to search.", "warning")
        return redirect(url_for('user.userContacts', username=username))
    
    # Search users by username
    search_results = User.query.filter(User.username.ilike(f'%{search_query}%')).all()

    # If no results are found, redirect back to the userContacts page with a message
    if not search_results:
        flash("No users found matching your search.", "info")
        return redirect(url_for('user.userContacts', username=username))
    
    # If results are found, render the template with the results
    return render_template('user-contacts.html', username=username, search_results=search_results, search_performed=True)

# Add route for viewing user profile and checking contact status
@user.route('/<username>/user-home/chatter/contacts/<int:user_id>/profile')
@login_required
@userReq
def viewProfile(username, user_id):
    user_profile = User.query.get_or_404(user_id)

    # Check if user_profile is already in the current user's contacts list
    in_contacts = Contacts.query.filter_by(user_id=current_user.id, contact_id=user_id).first() is not None
    
    return render_template('user-profile.html', username=username, user_profile=user_profile, in_contacts=in_contacts)

# Route to add or remove a user from contacts
@user.route('/<username>/user-home/chatter/contacts/<int:user_id>/add_remove', methods=['POST'])
@login_required
@userReq
def addRemoveContact(username, user_id):
    user_to_modify = User.query.get_or_404(user_id)
    
    # Check if user is in contacts
    contact_entry = Contacts.query.filter_by(user_id=current_user.id, contact_id=user_id).first()

    if contact_entry:
        # If user is already in contacts, remove them
        db.session.delete(contact_entry)
        db.session.commit()
        flash(f"{user_to_modify.username} has been removed from your contacts.", "info")
    else:
        # If user is not in contacts, add them
        new_contact = Contacts(user_id=current_user.id, contact_id=user_to_modify.id)
        db.session.add(new_contact)
        db.session.commit()
        flash(f"{user_to_modify.username} has been added to your contacts.", "info")
    
    return redirect(url_for('user.viewProfile', username=username, user_id=user_id))

@user.route('/<username>/user-home/files')
@login_required
@userReq
def userFiles(username):
    return render_template('user-files.html', username=username)