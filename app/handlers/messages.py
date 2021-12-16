help_message = 'Для того чтобы отправить ссылку на лабораторную работу, ' \
               'зарегестрируйтесь при помощи команды:' \
               '"/register"\n' \
               'Затем воспользуйтесь командой:' \
               '"/lab"\n' \
               'Если вы являетесь преподователем,воспользуйтесь командой:' \
               '"/work"\n' \
               'Для доступа к тестам используйте команду:\n' \
               '"/test"'

start_message = 'Приветствую вас. Это интеллектуальный ассистент по сдачам лабороторных работ.\n' \
                'Для ознакомления со списком команд введите "/help"\n' + help_message

cancel_message = 'Действие отменено'

register_start_message = 'Для регистрации введите ваше ФИО'

register_wrong_name_message = 'Пожалуйста укажите ваши полные имя,фамилию и отчество'

register_group_message = 'Пожалуйста укажите номер вашей группы'

register_subgroup_message = 'Пожалуйста укажите номер вашей подгруппы'

register_end_message = 'Спасибо за регистрацию'

link_update_start_message = 'Отправьте ссылку на вашу лабораторную работу'

link_success_update_message = 'Ссылка успешно добавлена'

link_update_invalid_message = 'Пожалуйста отправьте существующую ссылку'

link_update_error_message = 'Потеряна связть с модулем отправки,попробуйте ещё раз'

error_message = 'Похоже что-то пошло не так...\n' \
                'Попробуйте еще раз '

api_error_message = 'Связть с сервисами гугл в данный момент не установлена\n' \
                    'Пожалуйста,попробуйте еще раз позже '
MESSAGES = {
    'start': start_message,
    'help': help_message,
    'cancel': cancel_message,
    'register_start': register_start_message,
    'register_wrong_name': register_wrong_name_message,
    'register_group': register_group_message,
    'register_subgroup': register_subgroup_message,
    'register_end': register_end_message,
    'link_start': link_update_start_message,
    'link_update': link_success_update_message,
    'link_invalid': link_update_invalid_message,
    'link_update_error': link_update_error_message,
    'error': error_message,
    'api_error': api_error_message,
}
