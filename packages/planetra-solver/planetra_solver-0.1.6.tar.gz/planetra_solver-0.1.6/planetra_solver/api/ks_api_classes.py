from .ks_api_main import KsAPI


def create_class(name):

    request = KsAPI(to_log_in=True).request(
        '/classes/create-node',
        {'name': name, 'type': 'class'}
    )


def delete_class(class_id):

    request = KsAPI(to_log_in=True).request(
        '/classes/delete',
        {'UUID': class_id}
    )


def get_class_tree():

    request = KsAPI(to_log_in=True).request(
        '/classes/get-tree'
    )
    for obj in request['data']:
        print(obj)


def create_classes(name:list):
    if type(name) != list:
        print('type ERROR, на вход должен подаваться список')
    for names in name:
        request = KsAPI(to_log_in=True).request(
            '/classes/create-node',
            {'name': names, 'type': 'class'}
        )


def update_class(class_id, name):
    request = KsAPI(to_log_in=True).request(
        '/classes/update',
        {'name': name, 'UUID': class_id}
    )


def update_class_policy(class_id, denied_edit=False, denied_read=False):
    request = KsAPI(to_log_in=True).request(
        '/classes/update',
        {'UUID': class_id, 'DeniedEdit':denied_edit, 'DeniedRead':denied_read}
    )


if __name__ == '__main__':
    classes = KsAPI(to_log_in=True).request('/classes/get-tree')
    class_id = classes['data'][0]['uuid']

    models = KsAPI(to_log_in=True).request('/models/get-list')
    model_id = models['data'][0]['uuid']
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