import json
import websockets
from asyncio import Queue
import asyncio
from .utils import image_to_base64
from .errors import *


class NizimaRequest:

    def __init__(self, port=22022, ip="localhost", debug=False):
        self.websocket = None
        self.port = port
        self.uri = f"ws://{ip}:{port}/"
        self.debug = debug
        self.response_queue = Queue()
        self.event_queue = Queue()

    async def response_handler(self):
        while True:
            try:
                response = await self.websocket.recv()
                response_data = json.loads(response)

                if response_data.get("Type") in ["Response", "Error"]:
                    await self.response_queue.put(response_data)
                elif response_data.get("Type") == "Event":
                    await self.event_queue.put(response_data)
                else:
                    print(f"Unknown message type: {response_data}")
            except Exception as e:
                print(f"Error in response_handler: {e}")
                break

    async def handle_events(self):
        while True:
            event = await self.event_queue.get()
            event_name = event.get("EventName")
            print('event :', event_name)

    async def send_request(self, method, values):
        """
        Send a JSON request via WebSocket and return the response.

        :param method: The method of the request (str)
        :param data: The data to send in the request (dict)
        :return: The server's response (dict)
        """
        request = {
            "nLPlugin": "1.0.1",
            "Type": "Request",
            "Method": method,
            "Data": values
        }

        if not self.websocket:
            self.websocket = await websockets.connect(self.uri)
            asyncio.create_task(self.response_handler())

        if self.debug:
            print(f"Sending request: {request}")
        await self.websocket.send(json.dumps(request))

        response = await self.response_queue.get()
        if self.debug:
            print(f"Received response: {response}")
        data = response.get("Data")

        if response.get('Type') == 'Error':
            error_type = data.get('ErrorType')
            response = data
            ErrorManager(error_type, request, response)

        return data

    async def register_plugin(self, name, developer=None, version=None, icon=None):
        """
        Registers a new plugin in nizima LIVE.

        Args:
            name (str): name of the plugin
            developer (str): developer of the plugin
            version (str, optional): version of the plugin
            icon (str, optional): path icon plugin
        Returns:
            str: connection token
        """
        if icon:
            icon = image_to_base64(icon)
        data = {"Name": name, "Developer": developer, "Version": version, "Icon": icon}
        response = await self.send_request("RegisterPlugin", data)
        return response.get('Token')

    async def establish_connection(self, name: str, token: str, version: str = None):
        """
        Reconnects to nizima LIVE using the provided plugin name and token.

        Args:
            name (str): The registered name of the plugin.
            token (str): The token obtained during plugin registration.
            version (str, optional): The version of the plugin.

        Returns:
            bool: True if the plugin is enabled, otherwise False.
        """
        data = {"Name": name, "Token": token}
        if version:
            data["Version"] = version
        response = await self.send_request("EstablishConnection", data)
        return response.get("Enabled", False)

    async def register_plugin_path(self, plugin_path: str):
        """
        Registers the path to the plugin executable to allow launching from nizima LIVE.

        Args:
            plugin_path (str): The absolute path to the plugin executable.

        Returns: None
        """
        data = {"PluginPath": plugin_path}
        await self.send_request("RegisterPluginPath", data)

    async def delay_test(self, delay: int):
        """
        Returns a response after the specified delay (for plugin development).

        Args:
            delay (int): The delay in milliseconds.

        Returns: None
        """
        data = {"Delay": delay}
        await self.send_request("DelayTest", data)

    async def get_connection_status(self):
        """
        Retrieves the connection status with nizima LIVE.

        Returns:
            dict: A dictionary containing 'Established' and 'Enabled' status.
        """
        response = await self.send_request("GetConnectionStatus", {})
        return {
            "Established": response.get("Established", False),
            "Enabled": response.get("Enabled", False),
        }

    async def close_connection(self):
        if self.websocket and not self.websocket.closed:
            await self.websocket.close()

    async def insert_live_parameters(self, live_parameters):
        """
        Adds new Live2D parameters to the system.

        Args:
            live_parameters (list[dict]): List of parameter values with keys 'Id', 'Base', 'Min', 'Max' and optional keys 'Group' and 'Repeat'

        Returns:
            None
        """
        data = {"LiveParameters": live_parameters}
        return await self.send_request("InsertLiveParameters", data)

    async def set_live_parameter_values(self, live_parameter_values, model_id=None):
        data = {"LiveParameterValues": live_parameter_values, "ModelId": model_id}
        return await self.send_request("SetLiveParameterValues", data)

    async def get_live_parameter_values(self, model_id, live_parameter_ids=None):
        data = {"ModelId": model_id, "LiveParameterIds": live_parameter_ids}
        response = await self.send_request("GetLiveParameterValues", data)
        return response.get("LiveParameterValues")

    async def get_live_parameters(self):
        response = await self.send_request("GetLiveParameters", {})
        return response.get("LiveParameters")

    async def get_cubism_parameters(self, model_id):
        data = {"ModelId": model_id}
        response = await self.send_request("GetCubismParameters", data)
        return response.get("CubismParameters")

    async def set_cubism_parameter_values(self, model_id: str, parameter_values: list):
        """
        Sets the values of specified Cubism parameters for a model.

        Args:
            model_id (str): The ID of the model.
            parameter_values (list): A list of parameter dictionaries with 'Id' and 'Value'.

        Returns:
            None
        """
        data = {"ModelId": model_id, "CubismParameterValues": parameter_values}
        await self.send_request("SetCubismParameterValues", data)

    async def get_cubism_parameter_values(self, model_id: str, parameter_ids: list[str] = None):
        """
        Gets current Cubism parameter values for a model.

        Args:
            model_id (str): The model ID.
            parameter_ids (list[str], optional): List of parameter IDs to fetch. Fetches all if not specified.

        Returns:
            list[dict]: List of parameter values with keys 'Id' and 'Value'.
        """
        data = {"ModelId": model_id}
        if parameter_ids:
            data["CubismParameterIds"] = parameter_ids
        response = await self.send_request("GetCubismParameterValues", data)
        return response.get("CubismParameterValues", [])

    async def reset_cubism_parameter_values(self, model_id):
        data = {"ModelId": model_id}
        return await self.send_request("ResetCubismParameterValues", data)

    async def get_scenes(self):
        """
        Retrieves all scenes and the models/items within them.

        Returns:
            list: A list of scenes with models and items information.
        """
        response = await self.send_request("GetScenes", {})
        return response.get("Scenes")

    async def get_current_scene_id(self):
        """
        Gets the ID of the focused scene.

        Returns:
            str: ID Scene
        """
        response = await self.send_request("GetCurrentSceneId", {})
        return response.get("SceneId")

    async def remove_model(self, model_id):
        """
        Removes the specified model from the display.

        Args:
            model_id (str): The ID of the model to remove.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("RemoveModel", data)
        return response

    async def add_model(self, model_path, scene_id=None):
        """
        Adds a specified model to the given scene or a new window.

        Args:
            model_path (str): The path to the model.
            scene_id (str, optional): The ID of the scene. Defaults to None (new window).

        Returns:
            str: The ID of the added model.
        """
        data = {"ModelPath": model_path, "SceneId": scene_id}
        response = await self.send_request("AddModel", data)
        return response.get("ModelId")

    async def change_model(self, model_id, model_path):
        """
        Changes the specified model to a different model.

        Args:
            model_id (str): The ID of the current model.
            model_path (str): The path to the new model.

        Returns:
            str: The ID of the new model.
        """
        data = {"ModelId": model_id, "ModelPath": model_path}
        response = await self.send_request("ChangeModel", data)
        return response.get("ModelId")

    async def register_model(self, model_path, icon_path=None):
        """
        Registers a model in nizima LIVE.

        Args:
            model_path (str): The path to the model.
            icon_path (str, optional): The path to the icon. Defaults to None.

        Returns:
            str: The path of the registered model.
        """
        data = {"ModelPath": model_path, "IconPath": icon_path}
        response = await self.send_request("RegisterModel", data)
        return response.get("ModelPath")

    async def move_model(self, model_id, absolute=False, position_x=None, position_y=None,
                         scale=None, rotation=None, delay=None, interpolation_type=None):
        """
        Moves the specified model.

        Args:
            model_id (str): The ID of the model to move.
            absolute (bool, optional): Use absolute positioning. Defaults to False.
            position_x (float, optional): The X position. Defaults to None.
            position_y (float, optional): The Y position. Defaults to None.
            scale (float, optional): The scale factor. Defaults to None.
            rotation (float, optional): The rotation angle in degrees. Defaults to None.
            delay (float, optional): The delay in seconds. Defaults to None.
            interpolation_type (str, optional): The interpolation type. Defaults to None.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {
            "ModelId": model_id,
            "Absolute": absolute,
            "PositionX": position_x,
            "PositionY": position_y,
            "Scale": scale,
            "Rotation": rotation,
            "Delay": delay,
            "InterpolationType": interpolation_type,
        }
        response = await self.send_request("MoveModel", data)
        return response

    async def reset_pose(self, model_id):
        """
        Resets the pose of the specified model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("ResetPose", data)
        return response

    async def get_models(self):
        """
        Retrieves the list of currently displayed models.

        Returns:
            list: A list of displayed models with their properties.
        """
        data = {}
        response = await self.send_request("GetModels", data)
        return response.get("Models")

    async def get_registered_model_icons(self, model_paths):
        """
        Retrieves the icon data for the specified models.

        Args:
            model_paths (list[str]): A list of model paths.

        Returns:
            list: A list of dictionaries containing model paths and base64-encoded icons.
        """
        data = {"ModelPaths": model_paths}
        response = await self.send_request("GetRegisteredModelIcons", data)
        return response.get("RegisteredModelIcons")

    async def get_registered_models(self):
        """
        Retrieves the list of models registered in nizima LIVE.

        Returns:
            list: A list of registered models with their properties.
        """
        data = {}
        response = await self.send_request("GetRegisteredModels", data)
        return response.get("RegisteredModels")

    async def set_drawables_color(self, model_id, drawable_ids, multiply_color=None, screen_color=None):
        """
        Changes the color of the specified model's drawables.

        Args:
            model_id (str): The ID of the model.
            drawable_ids (list[str]): The IDs of the drawables to modify.
            multiply_color (dict, optional): Multiply color data. Defaults to None.
            screen_color (dict, optional): Screen color data. Defaults to None.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {
            "ModelId": model_id,
            "DrawableIds": drawable_ids,
            "MultiplyColor": multiply_color,
            "ScreenColor": screen_color,
        }
        response = await self.send_request("SetDrawablesColor", data)
        return response

    async def set_parts_color(self, model_id, part_ids, multiply_color=None, screen_color=None):
        """
        Changes the color of the specified model's parts.

        Args:
            model_id (str): The ID of the model.
            part_ids (list[str]): The IDs of the parts to modify.
            multiply_color (dict, optional): Multiply color data. Defaults to None.
            screen_color (dict, optional): Screen color data. Defaults to None.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {
            "ModelId": model_id,
            "PartIds": part_ids,
            "MultiplyColor": multiply_color,
            "ScreenColor": screen_color,
        }
        response = await self.send_request("SetPartsColor", data)
        return response

    async def set_model_color(self, model_id, multiply_color=None, screen_color=None):
        """
        Changes the color of the specified model.

        Args:
            model_id (str): The ID of the model.
            multiply_color (dict, optional): Multiply color data. Defaults to None.
            screen_color (dict, optional): Screen color data. Defaults to None.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {
            "ModelId": model_id,
            "MultiplyColor": multiply_color,
            "ScreenColor": screen_color,
        }
        response = await self.send_request("SetModelColor", data)
        return response

    async def get_drawables(self, model_id):
        """
        Retrieves the list of drawables for the specified model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            list: A list of drawable IDs.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("GetDrawables", data)
        ids = [item['Id'] for item in response.get("Drawables")]
        return ids

    async def get_parts(self, model_id):
        """
        Retrieves the list of parts for the specified model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            list: A list of parts with their properties.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("GetParts", data)
        return response.get("Parts")

    async def get_parts_tree(self, model_id):
        """
        Retrieves the parts and drawables of the specified model as a tree structure.

        Args:
            model_id (str): The ID of the model.

        Returns:
            dict: The root node of the parts tree.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("GetPartsTree", data)
        return response.get("Children")

    async def get_current_model_id(self):
        """
        Retrieves the ID of the last selected model.

        Returns:
            str: model ID.
        """
        data = {}
        response = await self.send_request("GetCurrentModelId", data)
        return response.get("ModelId")

    async def add_item(self, scene_id, item_path):
        """
        Adds a specified item to the given scene.

        Args:
            scene_id (str): The ID of the scene.
            item_path (str): The path of the item to add.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"SceneId": scene_id, "ItemPath": item_path}
        response = await self.send_request("AddItem", data)
        return response.get('ItemId')

    async def remove_item(self, item_id):
        """
        Removes the specified item from the display.

        Args:
            item_id (str): The ID of the item to remove.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"ItemId": item_id}
        response = await self.send_request("RemoveItem", data)
        return response

    async def move_item(self, item_id, absolute=False, position_x=None, position_y=None,
                        scale=None, rotation=None, delay=None, interpolation_type=None):
        """
        Moves the specified item.

        Args:
            item_id (str): The ID of the item to move.
            absolute (bool, optional): If true, use absolute positioning. Defaults to False.
            position_x (float, optional): The X position. Defaults to None.
            position_y (float, optional): The Y position. Defaults to None.
            scale (float, optional): The scale factor. Defaults to None.
            rotation (float, optional): The rotation angle in degrees. Defaults to None.
            delay (float, optional): The delay in seconds. Defaults to None.
            interpolation_type (str, optional): The interpolation type. Defaults to None.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {
            "ItemId": item_id,
            "Absolute": absolute,
            "PositionX": position_x,
            "PositionY": position_y,
            "Scale": scale,
            "Rotation": rotation,
            "Delay": delay,
            "InterpolationType": interpolation_type,
        }
        response = await self.send_request("MoveItem", data)
        return response

    async def get_registered_items(self):
        """
        Retrieves the list of items registered in nizima LIVE.

        Returns:
            list: A list of registered items with their properties.
        """
        data = {}
        response = await self.send_request("GetRegisteredItems", data)
        return response.get("RegisteredItems")

    async def get_items(self):
        """
        Retrieves the list of currently displayed items.

        Returns:
            list: A list of displayed items with their properties.
        """
        data = {}
        response = await self.send_request("GetItems", data)
        return response.get("Items")

    async def start_motion(self, model_id, motion_path):
        """
        Starts the motion of the specified model.

        Args:
            model_id (str): The ID of the model.
            motion_path (str): The path of the motion.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"ModelId": model_id, "MotionPath": motion_path}
        response = await self.send_request("StartMotion", data)
        return response

    async def stop_motion(self, model_id):
        """
        Stops the motion of the specified model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("StopMotion", data)
        return response

    async def get_motions(self, model_id):
        """
        Retrieves the list of motions for the specified model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            list: A list of motions with their properties.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("GetMotions", data)
        return response.get("Motions")

    async def start_expression(self, model_id, expression_path):
        """
        Starts a specific expression for the specified model.

        Args:
            model_id (str): The ID of the model.
            expression_path (str): The path of the expression.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"ModelId": model_id, "ExpressionPath": expression_path}
        response = await self.send_request("StartExpression", data)
        return response

    async def stop_expression(self, model_id, expression_path):
        """
        Stops a specific expression of the specified model.

        Args:
            model_id (str): The ID of the model.
            expression_path (str): The path of the expression.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"ModelId": model_id, "ExpressionPath": expression_path}
        response = await self.send_request("StopExpression", data)
        return response

    async def stop_all_expressions(self, model_id):
        """
        Stops all expressions of the specified model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            dict: An empty dictionary on success.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("StopAllExpressions", data)
        return response

    async def get_expressions(self, model_id):
        """
        Retrieves the list of expressions for the specified model.

        Args:
            model_id (str): The ID of the model.

        Returns:
            list: A list of expressions with their properties.
        """
        data = {"ModelId": model_id}
        response = await self.send_request("GetExpressions", data)
        return response.get("Expressions")

