async def notify_enabled_changed(self, enabled: bool):
    """
    Enables or disables notifications for plugin enable status changes.

    Args:
        enabled (bool): Whether to enable or disable notifications.

    Returns:
        None
    """
    data = {"Enabled": enabled}
    await self.send_request("NotifyEnabledChanged", data)


async def notify_frame_updated(self, enabled=True):
    data = {"Enabled": enabled}
    return await self.send_request("NotifyFrameUpdated", data)


async def notify_models_changed(self, enabled=None):
    """
    Enables or disables notifications when models are added or removed.

    Args:
        enabled (bool, optional): Whether to enable notifications. Defaults to None.

    Returns:
        dict: An empty dictionary on success.
    """
    data = {"Enabled": enabled}
    response = await self.send_request("NotifyModelsChanged", data)
    return response

async def notify_current_model_changed(self, enabled=None):
    """
    Enables or disables notifications for changes to the current model.

    Args:
        enabled (bool, optional): Whether to enable notifications. Defaults to None.

    Returns:
        dict: An empty dictionary on success.
    """
    data = {"Enabled": enabled}
    response = await self.send_request("NotifyCurrentModelChanged", data)
    return response


async def notify_items_changed(self, enabled=None):
    """
    Enables or disables notifications when items are added or removed.

    Args:
        enabled (bool, optional): Whether to enable notifications. Defaults to None.

    Returns:
        dict: An empty dictionary on success.
    """
    data = {"Enabled": enabled}
    response = await self.send_request("NotifyItemsChanged", data)
    return response