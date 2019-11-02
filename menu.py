class Const:
    main=[
        {'text': u'Order', 'switch_inline_query_current_chat': '{kID} order'},
        {'text': u'Tasks', 'callback_data': 'tasks'},
        {'text': u'Edit', 'callback_data': 'edit'},
        ]
    editTop=[
        {'text': u'Name', 'switch_inline_query_current_chat': '{kID} name'},
        {'text': u'kID', 'switch_inline_query_current_chat': '{kID} kID'}
    ]
    edit = [
        {'text': u'🧠', 'callback_data': 'done'},
        {'text': u'Reject', 'callback_data': 'reject'},
        {'text': u'Reassign', 'callback_data': 'reassign_{dep}_{tid}'}  
        ]
        
    task_levelInKeyBoard=[
        {'text': u'Urgent', 'callback_data': 'urgent_{dep}_{tid}'},
        {'text': u'ASAP', 'callback_data': 'asap_{dep}_{tid}'}, 
        ]   

    menu_keyboard = [['set Task'], ['view tasks']]