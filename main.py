import openfga_sdk
from openfga_sdk import (
    WriteAuthorizationModelRequest,
    TypeDefinition,
    Userset,
    Usersets,
    ObjectRelation,
    CheckRequest,
    TupleKey,
    WriteRequest,
    TupleKeys,
    ExpandRequest,
)
from openfga_sdk.api import open_fga_api
from openfga_sdk.models.create_store_request import CreateStoreRequest


configuration = openfga_sdk.Configuration(
    api_scheme="http", api_host="localhost:8080", store_id="01GG63MCVR116S0ZZAT5VDXSM3"
)


async def create_store():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)

    body = CreateStoreRequest(
        name="My New Store",
    )
    response = await api_instance.create_store(body)
    # response.id = "01FQH7V8BEG3GPQW93KTRFR8JB"
    await api_client.close()


async def get_store():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)

    response = await api_instance.get_store()
    await api_client.close()


async def write_authorization_model():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)
    type_definitions = WriteAuthorizationModelRequest(
        type_definitions=[
            TypeDefinition(
                type="document",
                relations=dict(
                    writer=Userset(
                        this=dict(),
                    ),
                    viewer=Userset(
                        union=Usersets(
                            child=[
                                Userset(this=dict()),
                                Userset(
                                    computed_userset=ObjectRelation(
                                        object="",
                                        relation="writer",
                                    )
                                ),
                            ],
                        ),
                    ),
                ),
            ),
        ],
    )

    response = await api_instance.write_authorization_model(type_definitions)

    id = response.authorization_model_id

    await api_client.close()

    return id


async def read_authorization_id():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)

    response = await api_instance.read_authorization_model("01GG65CXTDNA3YMFYXS935V0X2")
    # response.authorization_model =  AuthorizationModel(id='1uHxCSuTP0VKPYSnkq1pbb1jeZw', type_definitions=type_definitions[...])
    await api_client.close()


async def write():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)
    body = WriteRequest(
        writes=TupleKeys(
            tuple_keys=[
                TupleKey(
                    user="user:bob",
                    relation="viewer",
                    object="document:test_document",
                ),
            ],
        ),
    )

    response = await api_instance.write(body)
    await api_client.close()


async def check():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)
    body = CheckRequest(
        tuple_key=TupleKey(
            user="user:ryan",
            relation="viewer",
            object="document:test_document",
        ),
    )

    response = await api_instance.check(body)
    # response.allowed = True
    await api_client.close()


# Expand all relationships in userset tree format, and following userset rewrite rules.  Useful to reason about and debug a certain relationship
async def expand():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)
    body = ExpandRequest(
        tuple_key=TupleKey(
            relation="viewer",
            object="document:test_document",
        ),
    )

    response = await api_instance.expand(body)
    # response = ExpandResponse({"tree": UsersetTree({"root": Node({"name": "workspace:675bcac4-ad38-4fb1-a19a-94a5648c91d6#admin", "leaf": Leaf({"users": Users({"users": ["user:81684243-9356-4421-8fbf-a4f8d36aa31b", "user:f52a4f7a-054d-47ff-bb6e-3ac81269988f"]})})})})})
    await api_client.close()


async def read_changes():
    # Create an instance of the API class
    api_client = openfga_sdk.ApiClient(configuration)
    api_instance = open_fga_api.OpenFgaApi(api_client)

    type = "workspace"
    page_size = 25

    response = await api_instance.read_changes(type=type, page_size=page_size)
    # response.continuation_token = ...
    # response.changes = [TupleChange(tuple_key=TupleKey(object="...",relation="...",user="..."),operation=TupleOperation("TUPLE_OPERATION_WRITE"),timestamp=datetime.fromisoformat("..."))]
    await api_client.close()


async def api_setup():
    # Enter a context with an instance of the API client
    async with openfga_sdk.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = open_fga_api.OpenFgaApi(api_client)


async def test_setup():
    await api_setup()
    await check()


async def test_get_store():
    await get_store()


async def test_create_store():
    await create_store()


async def test_write_auth():
    await write_authorization_model()


async def test_write_tuple():
    await write()


async def test_read_auth():
    await read_authorization_id()


async def test_expand():
    await expand()


async def test_read_changes():
    await read_changes()
