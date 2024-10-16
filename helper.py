import uuid


def assert_response_ok(response, message):
    if not response.ok:
        raise Exception(
            message + "\nStatus received={}\n{}".format(response.status_code, response.text))

def create_unique_coodinates_instance(text):
    myuuid = uuid.uuid4()
    final_text = text + str(myuuid)
    return final_text