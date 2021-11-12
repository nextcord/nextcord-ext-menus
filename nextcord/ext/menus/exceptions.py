class MenuError(Exception):
    """Base exception for menu errors"""

    pass


class CannotEmbedLinks(MenuError):
    """Exception for when the bot is unable to embed links"""

    def __init__(self):
        super().__init__("Bot does not have embed links permission in this channel.")


class CannotSendMessages(MenuError):
    """Exception for when the bot is unable to send messages"""

    def __init__(self):
        super().__init__("Bot cannot send messages in this channel.")


class CannotAddReactions(MenuError):
    """Exception for when the bot is unable to add reactions"""

    def __init__(self):
        super().__init__("Bot cannot add reactions in this channel.")


class CannotReadMessageHistory(MenuError):
    """Exception for when the bot is unable to read message history"""

    def __init__(self):
        super().__init__(
            "Bot does not have Read Message History permissions in this channel."
        )
