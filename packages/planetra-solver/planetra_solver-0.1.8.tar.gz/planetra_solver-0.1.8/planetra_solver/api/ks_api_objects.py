from .ks_api_main import KsAPI


def create_object(class_id: str, model_id: str, object_name: str) -> None:
    """
    Создаёт новый объект и привязывает его к переданным классу и модели.
    :param class_id: UUID класса.
    :param model_id: UUID модели.
    :param object_name: Название объекта.
    :return: None.
    """
    if not isinstance(class_id, str):
        raise TypeError('"class_id" должен быть строкой.')
    if not isinstance(model_id, str):
        raise TypeError('"model_id" должен быть строкой.')
    if not isinstance(object_name, str):
        raise TypeError('"object_name" должен быть строкой.')

    KsAPI(to_log_in=True).request(
        '/objects/create',
        {'classUuid': class_id, 'modelUuids': [model_id], 'name': object_name}
    )


def create_objects(class_id: str, model_id: str, object_names: list) -> None:
    """
    Создаёт новые объекты и привязывает их к переданным классу и модели.
    :param class_id: UUID класса.
    :param model_id: UUID модели.
    :param object_names: Названия объектов.
    :return: None.
    """
    if not isinstance(class_id, str):
        raise TypeError('"class_id" должен быть строкой.')
    if not isinstance(model_id, str):
        raise TypeError('"model_id" должен быть строкой.')
    if not isinstance(object_names, list):
        raise TypeError('"object_names" должен быть списком строк.')

    new_objects: list[dict] = [dict(classUuid=class_id, modelUuids=[model_id], name=name) for name in object_names]
    KsAPI(to_log_in=True).request(
        '/objects/create-batch',
        {'Objects': new_objects},
    )


def delete_object(object_id: str) -> None:
    """
    Удаляет объект с переданным UUID.
    :param object_id: UUID объекта.
    :return: None.
    """
    if not isinstance(object_id, str):
        raise TypeError('"object_id" должен быть строкой.')

    KsAPI(to_log_in=True).request(
        '/objects/delete',
        {'UUID': object_id}
    )


def delete_objects(object_ids: list) -> None:
    """
    Удаляет объекты с переданными UUIDs.
    :param object_ids: UUIDs объектов.
    :return: None.
    """
    if not isinstance(object_ids, list):
        raise TypeError('"object_ids" должен быть списком строк.')

    KsAPI(to_log_in=True).request(
        '/objects/delete-batch',
        {'UUIDs': object_ids},
    )


def rename_object(object_id: str, object_name: str) -> None:
    """
    Переименовывает объект с переданным UUID.
    :param object_id: UUID объекта.
    :param object_name: Название объекта.
    :return: None.
    """
    if not isinstance(object_id, str):
        raise TypeError('"object_id" должен быть строкой.')
    if not isinstance(object_name, str):
        raise TypeError('"object_name" должен быть строкой.')

    KsAPI(to_log_in=True).request(
        '/objects/update',
        {'UUID': object_id, 'name': object_name},
    )


def rename_objects(object_ids: list, object_names: list) -> None:
    """
    Переименовывает объекты с переданными UUIDs.
    :param object_ids: UUIDs объектов.
    :param object_names: Названия объектов.
    :return: None.
    """
    if not isinstance(object_ids, list):
        raise TypeError('"object_ids" должен быть списком строк.')
    if not isinstance(object_names, list):
        raise TypeError('"object_names" должен быть списком строк.')

    new_objects: list[dict] = [dict(UUID=object_id, name=object_name)
                               for object_id, object_name in zip(object_ids, object_names)]
    KsAPI(to_log_in=True).request(
        '/objects/update-batch',
        {'Objects': new_objects},
    )


def get_all_objects() -> None:
    """
    Выводит все объекты.
    Опционально ID модели.
    :return: None.
    """
    objects = KsAPI(to_log_in=True).request('/objects/get-list')
    print('Объекты:')
    for index, data in enumerate(objects['data'], 1):
        print(f'{index} - "{data['name']}"')
