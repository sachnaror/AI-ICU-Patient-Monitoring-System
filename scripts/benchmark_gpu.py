from app.holoscan_pipeline.resource_manager import ResourceManager


def main() -> None:
    print(ResourceManager().describe())


if __name__ == "__main__":
    main()
