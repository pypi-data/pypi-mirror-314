"""Module to generate a template for a new dashboard."""

import filecmp
import os
import shutil
from pathlib import Path


class ProjectAlreadyExistsError(Exception):
    """Exception raised when a project already exists."""


class _TemplateGenerator:
    PLACEHOLDER_SLUG = "@dashboard_slug@"
    PLACEHOLDER_APP_SLUG = "@app_slug@"
    PLACEHOLDER_WORKSPACE_SLUG = "@workspace_slug@"
    DIRECTORY_NAME = "content"
    MAIN_FILE = "main%s.py"

    def __init__(self, dashboard_slug: str, app_slug: str, workspace_slug: str) -> None:
        self._dashboard_slug: Path = Path(dashboard_slug)
        self._app_slug: str = app_slug
        self._workspace_slug: str = workspace_slug
        self.empty: bool = True
        self.__is_new_project: bool = False

    @property
    def _template_path(self) -> Path:
        return Path(f"{Path(__file__).parent.absolute()}/template")

    @property
    def _project_path(self) -> Path:
        return Path.cwd() / self._dashboard_slug

    @property
    def is_new_project(self) -> bool:
        return self.__is_new_project

    def run(self) -> None:
        os.chdir(Path.cwd())
        self.__validate_project()
        self.__add_project()

    def __validate_project(self) -> None:
        """Validate current project."""
        if self._dashboard_slug.exists():
            raise ProjectAlreadyExistsError

    def __add_project(self) -> None:
        if not self._project_path.exists():
            self.__copy_paths()
            self.__update_dashboard_slug()

            self.__move_files()
            self.__create_dot_env()

            self.__is_new_project = True

    def __copy_paths(self) -> None:
        shutil.copytree(
            self._template_path / self.DIRECTORY_NAME,
            Path.cwd() / self.DIRECTORY_NAME,
        )

    def __update_dashboard_slug(self) -> None:
        if self.empty:
            old_file = Path(self.DIRECTORY_NAME) / (self.MAIN_FILE % "_tmp")
            new_file = Path(self.DIRECTORY_NAME) / (self.MAIN_FILE % "")

            Path.rename(new_file, old_file)

            with open(old_file, encoding="UTF-8") as read, open(
                new_file, "w", encoding="UTF-8"
            ) as write:
                data = read.readlines()
                for line in data:
                    if self.PLACEHOLDER_SLUG in line:
                        line = line.replace(
                            self.PLACEHOLDER_SLUG, str(self._dashboard_slug)
                        )
                    if self.PLACEHOLDER_APP_SLUG in line:
                        line = line.replace(self.PLACEHOLDER_APP_SLUG, self._app_slug)
                    if self.PLACEHOLDER_WORKSPACE_SLUG in line:
                        line = line.replace(
                            self.PLACEHOLDER_WORKSPACE_SLUG, self._workspace_slug
                        )
                    write.write(line)

            Path.unlink(old_file)

    def __move_files(self) -> None:
        if not self.empty:
            self._dashboard_slug.mkdir(exist_ok=True, parents=True)
            # We compare the files in the current directory with the files in the tmp
            # directory
            dir_diff = filecmp.dircmp(f"./{self.DIRECTORY_NAME}", "./tmp")
            # We move the common files to the tmp directory
            for filename in dir_diff.common:
                shutil.move(Path("./tmp") / Path(filename), self._dashboard_slug)

            # We move the files that are only in the tmp directory to the parent
            # directory
            for filename in dir_diff.right_only:
                shutil.move(Path("./tmp") / Path(filename), self._dashboard_slug)

            # We move the files that are only in the current directory to the parent
            # directory
            for filename in os.listdir(f"./{self.DIRECTORY_NAME}"):
                if filename not in dir_diff.common:
                    if (
                        filename in [".env.sample"]
                        and (self._dashboard_slug / ".env").exists()
                    ):
                        pass
                    else:
                        shutil.move(
                            Path(f"./{self.DIRECTORY_NAME}") / Path(filename),
                            self._dashboard_slug,
                        )

        else:
            Path.rename(self.DIRECTORY_NAME, self._dashboard_slug)

    def __create_dot_env(self) -> None:
        if not (self._dashboard_slug / ".env").exists():
            Path.rename(
                f"{self._dashboard_slug}/.env.sample", self._dashboard_slug / ".env"
            )


def generate_template(dashboard_slug: str, app_slug: str, workspace_slug: str) -> bool:
    """Interface to generate a template for a new dashboard.

    Args:
        dashboard_slug: Dashboard slug.
        app_slug: App slug.
        workspace_slug: Workspace slug.

    Returns:
        True if it is a new project, False otherwise.
    """
    template_generator = _TemplateGenerator(dashboard_slug, app_slug, workspace_slug)
    template_generator.run()
    return template_generator.is_new_project


def remove_temporary_files() -> None:
    """Method that removes the temporary files created by the cookiecutter."""
    if Path.is_dir(main_folder := Path.cwd() / Path("content")):
        shutil.rmtree(main_folder)

    if Path.is_dir(tmp_folder := Path.cwd() / Path("tmp")):
        shutil.rmtree(tmp_folder)
