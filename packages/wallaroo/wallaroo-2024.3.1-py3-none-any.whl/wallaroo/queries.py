from importlib import resources

# from . import graphql


def named(name: str) -> str:
    split_name = name.split("/")
    filename = split_name[0]
    prefix = ""
    if len(split_name) == 2:
        filename = split_name[1]
        prefix = f".{split_name[0]}"

    return resources.read_text(f"wallaroo.graphql{prefix}", f"{filename}.graphql")


## This is only compatible with Python >=3.9
## The benefit of this is that graphql subdirectories don't need to by Python modules.
# def named(name: str) -> str:
#     """Returns text from resources in the package."""
#     return (
#         resources.files(graphql)
#         .joinpath(f"{name}.graphql")
#         .open("r", encoding="utf8")
#         .read()
#     )
