from lost.db import state


# def add_user(data_man, user):
#     '''add user to user meta

#     Args:
#         db_man (obj): Project database manager.
#         user (obj): User object
#     '''
#     user = model.User(idx=user.id, user_name=user.username,
#                        first_name=user.first_name, last_name=user.last_name,
#                        email=user.email)
#     data_man.save_obj(user)

# def add_superuser(data_man, user):
#     '''add superuser to user meta

#     Args:
#         db_man (obj): Project database manager.
#         user (obj): User object
#     '''
#     user = model.User(idx=user.id)
#     data_man.save_obj(user)

# def update_user(data_man, user):
#     '''update existing user in user meta

#     Args:
#         db_man (obj): Project database manager.
#         user (obj): User object
#     '''
#     usermeta = data_man.get_user_meta(user_id=user.id)
#     usermeta.first_name = user.first_name
#     usermeta.last_name = user.last_name
#     usermeta.user_name = user.username
#     usermeta.email = user.email

#     data_man.save_obj(usermeta)

def release_user_annos(dbm, user_id):
    '''Release locked annos for a specific user.

    Args:
        dbm (object): DBMan object.
        user_id (int): ID of the user to release locked annos.
    '''
    print('Was Here! User id is: {}'.format(user_id))
    for anno_task in dbm.get_anno_task(state=state.AnnoTask.IN_PROGRESS):
        locked_annos = dbm.get_locked_img_annos(anno_task.idx)
        print('locked annos')
        print(locked_annos)
        for anno in locked_annos:
            print('UserID: {}, AnnoID: {}'.format(anno.user_id, anno.idx))
        locked_user_annos = [anno for anno in locked_annos if anno.user_id == user_id]
        print(locked_user_annos)
        for anno in locked_user_annos:
            anno.state = state.Anno.UNLOCKED
            anno.timestamp_lock = None
            anno.user_id = None
            dbm.add(anno)
                
        locked_annos = dbm.get_locked_two_d_annos(anno_task.idx)
        print('locked 2d annos')
        print(locked_annos)
        for anno in locked_annos:
            print('UserID: {} AnnoID: {}'.format(anno.user_id, anno.idx))
        locked_user_annos = [anno for anno in locked_annos if anno.user_id == user_id]
        print(locked_user_annos)
        for anno in locked_user_annos:
            anno.state = state.Anno.UNLOCKED
            anno.timestamp_lock = None
            anno.user_id = None
            dbm.add(anno)
        dbm.commit()