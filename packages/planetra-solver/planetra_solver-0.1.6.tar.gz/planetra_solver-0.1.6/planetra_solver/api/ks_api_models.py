from .ks_api_main import KsAPI


def create_model(model_name: str) -> None:
    """
    Создаёт новую модель и присваивает ей полученное название.
    :param model_name: Название модели.
    :return: None.
    """
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
    KsAPI(to_log_in=True).request(
        '/models/delete-node',
        {'UUID': node_id}
    )


def rename_model(node_id, model_name):
    """
    Переименовывает модель с полученным ID.
    :param node_id: "node UUID" модели.
    :param model_name: Название модели.
    :return: None.
    """
    KsAPI(to_log_in=True).request(
        '/models/update-node',
        {'NodeUUID': node_id, 'name': model_name},
    )
