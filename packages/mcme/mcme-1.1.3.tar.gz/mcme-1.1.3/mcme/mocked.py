from openapi_client import PostgresqlAssetState, SchemasBetasAvatarRequest, SchemasMeasurementAvatarRequest, DocschemasDocAFIInputs, DocschemasDocExportInputs, DocschemasDocAFVInputs
from keycloak import exceptions
import uuid

class SchemasURLResponse:
    def __init__(self):
        self.path = "example_url.com"

class AvatarAttributes:
    def __init__(self, state: PostgresqlAssetState, url: SchemasURLResponse):
        self.state = state
        self.url = url

class AssetResponse:
    def __init__(self, avatar_attributes: AvatarAttributes, id: str):
        self.attributes = avatar_attributes
        self.id = id

class ApiResponse:
    def __init__(self, state: PostgresqlAssetState):
        state = state
        url = SchemasURLResponse()
        attributes = AvatarAttributes(state=state, url=url)
        id = uuid.uuid1()
        self.data = AssetResponse(avatar_attributes=attributes, id=str(id))  


class CreateAvatarsFromBetasApi:
    def create_avatar_from_betas(self, request: SchemasBetasAvatarRequest):
        api_response = ApiResponse(PostgresqlAssetState("READY"))
        return api_response


class CreateAvatarFromMeasurementsApi:
    def avatar_from_measurements(self, request: SchemasMeasurementAvatarRequest):
        api_response = ApiResponse(PostgresqlAssetState("AWAITING_PROCESSING"))
        return api_response
    
class AvatarsApi:
    def __init__(self):
        self.succeed_on_try = 1
        self.counter = 0

    def describe_avatar(self, asset_id: str):
        self.counter += 1
        if self.counter >= self.succeed_on_try: 
            api_response = ApiResponse(PostgresqlAssetState("READY"))
        else:
            api_response = ApiResponse(PostgresqlAssetState("PROCESSING"))
        return api_response
    
    def export_avatar(self, asset_id: uuid.UUID, input: DocschemasDocExportInputs):  
        self.counter += 1
        if self.counter >= self.succeed_on_try: 
            api_response = ApiResponse(PostgresqlAssetState("READY"))
        else:
            api_response = ApiResponse(PostgresqlAssetState("PROCESSING"))
        return api_response
    
    def set_number_of_tries(self, succeed_on: int):
        self.succeed_on_try = succeed_on

class CreateAvatarFromImagesApi:
    def create_avatar_from_images(self):
        api_response = ApiResponse(PostgresqlAssetState("AWAITING_AFI_INPUT"))
        return api_response

    def upload_image_to_avatar(self, asset_id: uuid.UUID):
        api_response = ApiResponse(PostgresqlAssetState("AWAITING_UPLOAD"))
        return api_response
    
    def avatar_fit_to_images(self, asset_id: uuid.UUID, afi_inputs: DocschemasDocAFIInputs):
        api_response = ApiResponse(PostgresqlAssetState("AWAITING_PROCESSING"))
        return api_response 
    
class CreateAvatarFromScansApi:
    def create_avatar_from_scans(self):
        api_response = ApiResponse(PostgresqlAssetState("AWAITING_AFS_INPUT"))
        return api_response

    def upload_mesh_to_avatar(self, asset_id: uuid.UUID):
        api_response = ApiResponse(PostgresqlAssetState("AWAITING_UPLOAD"))
        return api_response
    
    def avatar_fit_to_scans(self, asset_id: uuid.UUID, afi_inputs: DocschemasDocAFIInputs):
        api_response = ApiResponse(PostgresqlAssetState("AWAITING_PROCESSING"))
        return api_response 


class MockUploader:
    def upload(self, file_to_upload: str, upload_url: str):
        pass

class KeycloakOpenID:
    def __init__(self):
        self.valid = True

    def userinfo(self, token: str):
        if self.valid and token == "valid_token":
            return
        raise exceptions.KeycloakAuthenticationError()

    def set_valid(self, valid: bool):
        self.valid = valid

    def refresh_token(self, refresh_token: str):
        if self.valid and refresh_token == "valid_token":
            return {"access_token": "valid_token"}
        raise exceptions.KeycloakPostError

    def token(self, username: str, password: str) -> dict[str,str]:
        if self.valid:
            return {"access_token": "valid_token"}
        return {}

class MockState:
    def __init__(self) -> None:
        """Initialize mocked state with valid tokens and user"""
        self.state_file: str = ""
        self.active_user: str = "test_user"
        self.auth_tokens: dict[str, dict[str, str]] = {"test_user": {"access_token": "valid_token", "refresh_token": "valid_token"}}
    
    def invalidate_token(self, user: str, key: str):
        self.auth_tokens[user][key] = "invalid_token"
    
    def get_user_and_tokens(self, username: str) -> tuple[str, dict[str,str]]:
        """Load state from a local file"""
        return username, self.auth_tokens[username]

    def update(self, keycloak_tokens: dict[str, str], username: str) -> None:
        pass
