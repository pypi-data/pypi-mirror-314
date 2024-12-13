from .ks_api_main import KsAPI


def create_model(model_name: str) -> None:
    """
    Создаёт новую модель и присваивает ей полученное название.
    :param model_name: Название модели.
    :return: None.
    """
    if not isinstance(model_name, str):
        raise TypeError('"model_name" должен быть строкой.')

    KsAPI(to_log_in=True).request(
        '/models/create-node',
        {'name': model_name, 'type': 'model'},
    )


def create_models(model_names: list) -> None:
    """
    Создаёт новые модели и присваивает им полученные названия.
    :param model_names: Названия моделей.
    :return: None.
    """
    if not isinstance(model_names, list):
        raise TypeError('"model_names" должен быть списком строк.')

    for model_name in model_names:
        KsAPI(to_log_in=True).request(
            '/models/create-node',
            {'name': model_name, 'type': 'model'},
        )


def delete_model(node_id: str) -> None:
    """
    Удаляет модель с полученным ID.
    :param node_id: "node UUID" модели.
    :return: None.
    """
    if not isinstance(node_id, str):
        raise TypeError('"node_id" должен быть строкой.')

    KsAPI(to_log_in=True).request(
        '/models/delete-node',
        {'UUID': node_id},
    )


def delete_models(node_ids: list) -> None:
    """
    Удаляет модели с полученными IDs.
    :param node_ids: "node UUIDs" модели.
    :return: None.
    """
    if not isinstance(node_ids, list):
        raise TypeError('"node_ids" должен быть списком строк.')

    for node_id in node_ids:
        KsAPI(to_log_in=True).request(
            '/models/delete-node',
            {'UUID': node_id},
        )


def rename_model(node_id: str, model_name: str) -> None:
    """
    Переименовывает модель с полученным ID.
    :param node_id: "node UUID" модели.
    :param model_name: Название модели.
    :return: None.
    """
    if not isinstance(node_id, str):
        raise TypeError('"node_id" должен быть строкой.')
    if not isinstance(model_name, str):
        raise TypeError('"model_name" должен быть строкой.')

    KsAPI(to_log_in=True).request(
        '/models/update-node',
        {'NodeUUID': node_id, 'name': model_name},
    )


def rename_models(node_ids: list, model_names: list) -> None:
    """
    Переименовывает модели с полученными IDs.
    :param node_ids: "node UUID" модели.
    :param model_names: Название модели.
    :return: None.
    """
    if not isinstance(node_ids, list):
        raise TypeError('"node_ids" должен быть списком строк.')
    if not isinstance(model_names, list):
        raise TypeError('"model_names" должен быть списком строк.')

    for node_id, model_name in zip(node_ids, model_names):
        KsAPI(to_log_in=True).request(
            '/models/update-node',
            {'NodeUUID': node_id, 'name': model_name},
        )


def get_all_models() -> None:
    """
    Выводит все модели.
    :return: None.
    """
    models = KsAPI(to_log_in=True).request('/models/get-list')
    print('Модели:')
    for data_list in models.values():
        for index, model in enumerate(data_list, 1):
            print(f'{index} - "{model['name']}"')
