class Notification:
    def to_json(self):
        raise NotImplementedError()


class Email(Notification):
    def __init__(self, to):
        self.args = {"to": to}

    def to_json(self):
        return self.args

    @classmethod
    def from_json(cls, json):
        return Email(json["to"])


def to_json(notifications):
    emails = [n for n in notifications if isinstance(n, Email)]
    return {"email": [n.to_json() for n in emails]}


def from_json(json):
    return [Email.from_json(e) for e in json["email"]]


class AlertConfiguration:
    def __init__(self, name, expression, notifications):
        self.name = name
        self.expression = expression
        self.notifications = notifications

    @classmethod
    def from_json(Cls, json):
        return Cls(
            json["name"],
            json["expression"],
            from_json(json["notifications"]),
        )

    def to_json(self):
        return {
            "name": self.name,
            "expression": self.expression,
            "notifications": to_json(self.notifications),
        }
