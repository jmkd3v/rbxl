from rbxl.dom import RobloxDOM
from rbxl.dom.instance import Instance


def main():
    with open("./Baseplate.rbxl", "rb") as file:
        dom = RobloxDOM.from_file(file)

    def iterate_through_instance(instance: Instance, prefix=""):
        for child_referent in instance.children_referents:
            child_instance = dom.get_instance_from_referent(child_referent)
            print(f"{prefix}{child_instance}")

            iterate_through_instance(
                instance=child_instance,
                prefix=prefix + "\t"
            )

    iterate_through_instance(dom.root_instance)


if __name__ == '__main__':
    main()
