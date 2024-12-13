from .ks_api_main import KsAPI


def create_dataset(model_id: str, dataset_name: str) -> None:
    """
    Создаёт новый набор данных, привязывает его к модели по переданному ID и присваивает ей полученное название.
    :param model_id: UUID модели.
    :param dataset_name: Название набора данных.
    :return: None.
    """
    if not isinstance(model_id, str):
        raise TypeError('"model_id" должен быть строкой.')
    if not isinstance(dataset_name, str):
        raise TypeError('"dataset_name" должен быть строкой.')

    KsAPI(to_log_in=True).request(
        '/datasets/create',
        {'modelUuid': model_id, 'name': dataset_name},
    )


def create_datasets(model_id: str, dataset_names: list) -> None:
    """
    Создаёт новые наборы данных, привязывает их к модели по переданному ID и присваивает им полученные названия.
    :param model_id: UUID модели.
    :param dataset_names: Названия наборов данных.
    :return: None.
    """
    if not isinstance(model_id, str):
        raise TypeError('"model_id" должен быть строкой.')
    if not isinstance(dataset_names, list):
        raise TypeError('"dataset_names" должен быть списком строк.')

    for dataset_name in dataset_names:
        KsAPI(to_log_in=True).request(
            '/datasets/create',
            {'modelUuid': model_id, 'name': dataset_name},
        )


def delete_dataset(dataset_id: str) -> None:
    """
    Удаляет набор данных с полученным ID.
    :param dataset_id: UUID набора данных.
    :return: None.
    """
    if not isinstance(dataset_id, str):
        raise TypeError('"dataset_id" должен быть строкой.')

    KsAPI(to_log_in=True).request(
        '/datasets/delete',
        {'UUID': dataset_id}
    )


def delete_datasets(dataset_ids: list) -> None:
    """
    Удаляет наборы данных с полученными IDs.
    :param dataset_ids: UUIDs наборов данных.
    :return: None.
    """
    if not isinstance(dataset_ids, list):
        raise TypeError('"dataset_ids" должен быть списком строк.')

    for dataset_id in dataset_ids:
        KsAPI(to_log_in=True).request(
            '/datasets/delete',
            {'UUID': dataset_id}
        )


def get_all_datasets() -> None:
    """
    Выводит наборы данных.
    :return: None.
    """
    datasets = KsAPI(to_log_in=True).request('/datasets/get-list')
    print('Наборы данных:')
    for data_list in datasets.values():
        for index, dataset in enumerate(data_list, 1):
            print(f'{index} - "{dataset['name']}"')
