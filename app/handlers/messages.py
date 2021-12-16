help_message = 'Для того чтобы отправить ссылку на лабораторную работу, ' \
               'зарегестрируйтесь при помощи команды:' \
               '"/register"\n' \
               'Затем воспользуйтесь командой:' \
               '"/lab"\n' \
               'Если вы являетесь преподователем,воспользуйтесь командой:' \
               '"/work"\n'

start_message = 'Приветствую вас. Это интеллектуальный ассистент по сдачам лабороторных работ.\n' \
                'Для ознакомления со списком команд введите "/help"\n' + help_message

cancel_message = 'Действие отменено'

link_update_start_message = 'Отправьте ссылку на вашу лабораторную работу'

link_success_update_message = 'Ссылка успешно добавлена'

link_update_invalid_message = 'Пожалуйста отправьте существующую ссылку'

link_update_error_message = 'Потеряна связть с модулем отправки,попробуйте ещё раз'

register_start_message = 'Для регистрации в системе нажмите на кнопку "Зарегистрироваться"'

register_missing_data_message = 'Произошла ошибка: ваших данных нет в системе, обратитесь к администратору за помощью'

error_message = 'Похоже что-то пошло не так...\n' \
                'Попробуйте еще раз '

api_error_message = 'Связть с сервисами гугл в данный момент не установлена\n' \
                    'Пожалуйста,попробуйте еще раз позже '
MESSAGES = {
    'start': start_message,
    'help': help_message,
    'cancel': cancel_message,
    'link_start': link_update_start_message,
    'link_update': link_success_update_message,
    'link_invalid': link_update_invalid_message,
    'link_update_error': link_update_error_message,
    'error': error_message,
    'api_error': api_error_message,
    'register.start': register_start_message,
    'register.data.error': register_missing_data_message,
}
