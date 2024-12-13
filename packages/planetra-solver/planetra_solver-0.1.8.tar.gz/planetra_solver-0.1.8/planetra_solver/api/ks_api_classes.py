from .ks_api_main import KsAPI


def create_class(name: str) -> None:
    """
    Создает класс с переданным названием.
    :param name: название класса.
    :return: None.
    """
    if not isinstance(name, str):
        raise TypeError('ID класса должен быть строкой')
    KsAPI(to_log_in=True).request(
        '/classes/create-node',
        {'name': name, 'type': 'class'}
    )


def delete_class(class_id: str) -> None:
    """
    Удаляет класс с переданным UUID.
    :param class_id: UUID класса.
    :return: None.
    """
    if not isinstance(class_id, str):
        raise TypeError('ID класса должен быть строкой')
    KsAPI(to_log_in=True).request(
        '/classes/delete',
        {'UUID': class_id}
    )


def get_class_tree() -> None:
    """
    Возвращает дерево классов. В нем содержатся все классы и их показатели.
    :param None.
    :return: None.
    """
    request = KsAPI(to_log_in=True).request(
        '/classes/get-tree'
    )
    for obj in request['data']:
        print(obj)


def create_classes(name: list) -> None:
    """
    Создает класс с переданными названиями.
    Названия должны передаваться списком.
    :param name: список названий классов.
    :return: None.
    """
    if not isinstance(name, list):
        raise TypeError('name должен быть list')
    for names in name:
        KsAPI(to_log_in=True).request(
            '/classes/create-node',
            {'name': names, 'type': 'class'}
        )


def rename_class(class_id: str, name: str) -> None:
    """
    Переименовывает class с переданным UUID.
    :param class_id: UUID класса.
    :param name: Название класса.
    :return: None.
    """
    if not isinstance(class_id, str):
        raise TypeError('ID класса должен быть строкой')
    if not isinstance(name, str):
        raise TypeError('Название класса должно быть строкой')
    KsAPI(to_log_in=True).request(
        '/classes/update',
        {'name': name, 'UUID': class_id}
    )


def update_class_policy(class_id: str, denied_edit: bool = False, denied_read: bool = False) -> None:
    """
    Изменяет права доступа к классу.
    :param class_id: UUID класса.
    :param denied_edit: Запретить изменения(True/False)).
    :param denied_read: Запретить чтение(True/False)).
    :return: None.
    """
    if not isinstance(class_id, str):
        raise TypeError('ID класса должно быть строкой')
    if not isinstance(denied_edit, bool):
        raise TypeError('bool')
    if not isinstance(denied_read, bool):
        raise TypeError('bool')
    KsAPI(to_log_in=True).request(
        '/classes/update',
        {'UUID': class_id, 'DeniedEdit': denied_edit, 'DeniedRead': denied_read}
    )


if __name__ == '__main__':
    update_class_policy('01efb6d8-3d78-5911-bacb-00b15c0c4000', denied_edit=True, denied_read=True)
    # classes = KsAPI(to_log_in=True).request('/classes/get-tree')
    # class_id = classes['data'][0]['uuid']
    #
    # models = KsAPI(to_log_in=True).request('/models/get-list')
    # model_id = models['data'][0]['uuid']
    # delete_class('01efb797-32c5-5098-8114-00b15c0c4000')
    # create_class_indicator('01efb6cc-df07-8730-8bb8-00b15c0c4000', 'bis', '01efb797-32c8-de71-8114-00b15c0c4000')


    # name = 'test_3'
    #
    # objects_to_delete = [
    #     '01efb6f9-7430-9ade-a5d7-00b15c0c4000',
    #     '01efb6f9-74a9-3fa2-a5d7-00b15c0c4000',
    #     '01efb6f9-7518-4ccb-a5d7-00b15c0c4000',
    # ]

    # names = ['test_1', 'test_2', 'test_3']
    # update_class('01efb7a2-13ce-24f7-8114-00b15c0c4000', 'testtest')

    # object_id = '01efb6f5-7aed-173a-a5d7-00b15c0c4000'

    # delete_object(object_id)

    # create_objects(class_id, model_id)

    # delete_objects()

#     objects = KsAPI(to_log_in=True).request('/objects/get-list')
#     object_ids = []
#     for obj in objects['data']:
#         object_ids.append(obj['uuid'])

#     update_objects(object_ids)
# get_class_tree()